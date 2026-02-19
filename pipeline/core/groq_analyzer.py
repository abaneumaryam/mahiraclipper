"""
MahiraClipper — Groq Analyzer
Analisis momen viral dari transkrip menggunakan Groq (LLaMA 3.3 70B).

Kenapa Groq:
  - 14.400 request/hari GRATIS tanpa kartu kredit
  - OpenAI-compatible API → mudah dipakai
  - LLaMA 3.3 70B sangat pintar, jauh lebih baik dari GPT-3.5
  - Tidak perlu upload video/audio → hanya kirim teks transkrip
  - 300+ token/detik → respons super cepat

Daftar API key gratis: https://console.groq.com (pakai akun Google)
"""

import json
import re
import time
import uuid
from pathlib import Path
from typing import Callable, Optional

from config.settings import ClipConfig, log
from config.prompts import DAKWAH_ANALYSIS_PROMPT, DEFAULT_HASHTAGS

# Model Groq terbaik untuk analisis teks
GROQ_MODEL        = "llama-3.3-70b-versatile"
GROQ_MODEL_FAST   = "llama-3.1-8b-instant"   # fallback kalau 70B kena limit
GROQ_API_URL      = "https://api.groq.com/openai/v1/chat/completions"
MAX_TRANSCRIPT_CHARS = 12000   # batasi panjang transkrip yang dikirim per request


# ─── Main Entry ──────────────────────────────────────────────────────────────

def analyze(
    transcript: dict,
    clip_config: Optional[ClipConfig] = None,
    groq_api_key: str = "",
    progress_callback: Optional[Callable[[str, float], None]] = None,
) -> dict:
    """
    Analisis transkrip ceramah → temukan segmen viral terbaik.

    Args:
        transcript: hasil dari whisper_transcriber.transcribe()
        clip_config: berisi num_clips, min_duration, max_duration
        groq_api_key: key dari console.groq.com (gratis)

    Returns:
        {
          "segments": [...],         # list segmen klip yang direkomendasikan
          "video_summary": "...",
          "dominant_theme": "...",
          "speaker_style": "..."
        }
    """
    _progress(progress_callback, 0.05)

    if not groq_api_key:
        raise ValueError(
            "Groq API key belum diisi!\n"
            "Daftar gratis di: https://console.groq.com\n"
            "Lalu masuk Settings dan isi Groq API Key."
        )

    ccfg      = clip_config or ClipConfig()
    segments  = transcript.get("segments", [])
    full_text = transcript.get("full_text", "")
    duration  = transcript.get("duration", 0)

    if not segments:
        raise ValueError("Transkrip kosong — tidak ada yang bisa dianalisis.")

    log.info("Mulai analisis Groq: %d segmen, durasi=%.0fs", len(segments), duration)

    # ── Bagi transkrip kalau terlalu panjang ─────────────────────────────
    transcript_text = _format_transcript_for_llm(segments, max_chars=MAX_TRANSCRIPT_CHARS)
    _progress(progress_callback, 0.15)

    # ── Kirim ke Groq ─────────────────────────────────────────────────────
    prompt = _build_prompt(transcript_text, ccfg, duration)
    raw_response = _call_groq(prompt, groq_api_key, progress_callback)

    _progress(progress_callback, 0.80)

    # ── Parse respons JSON dari LLM ────────────────────────────────────────
    result = _parse_response(raw_response, segments, ccfg)

    _progress(progress_callback, 1.0)
    log.info("Groq analisis selesai: %d segmen ditemukan, tema=%s",
             len(result["segments"]), result.get("dominant_theme", "?"))

    return result


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _format_transcript_for_llm(segments: list, max_chars: int = 12000) -> str:
    """Format transkrip ke teks dengan timestamp — mudah dibaca LLM."""
    lines = []
    total = 0
    for seg in segments:
        start = seg.get("start", 0)
        end   = seg.get("end", 0)
        text  = seg.get("text", "").strip()
        if not text:
            continue
        line = f"[{_fmt_time(start)} → {_fmt_time(end)}] {text}"
        total += len(line)
        if total > max_chars:
            lines.append(f"... (transkrip dipotong, total lebih dari {max_chars} karakter)")
            break
        lines.append(line)
    return "\n".join(lines)


def _fmt_time(secs: float) -> str:
    m, s = divmod(int(secs), 60)
    return f"{m:02d}:{s:02d}"


def _build_prompt(transcript_text: str, ccfg: ClipConfig, total_duration: float) -> str:
    """Buat prompt analisis dakwah untuk LLM."""
    return f"""{DAKWAH_ANALYSIS_PROMPT}

---

## DATA VIDEO:
- Durasi total: {int(total_duration // 60)} menit {int(total_duration % 60)} detik
- Jumlah klip diminta: {ccfg.num_clips}
- Durasi klip: {ccfg.min_duration}–{ccfg.max_duration} detik

## TRANSKRIP (dengan timestamp):
{transcript_text}

---

## INSTRUKSI OUTPUT:
Berikan HANYA JSON valid (tanpa penjelasan, tanpa markdown code block), format persis seperti ini:

{{
  "video_summary": "ringkasan 2-3 kalimat isi ceramah",
  "dominant_theme": "tema utama dalam 3-5 kata",
  "speaker_style": "gaya penceramah (tegas/lembut/humoris/dll)",
  "segments": [
    {{
      "id": "clip_001",
      "title": "judul klip menarik max 60 karakter",
      "start_time": 45.5,
      "end_time": 105.0,
      "duration": 59.5,
      "category": "knowledge",
      "viral_score": 8.7,
      "hook": "kalimat pembuka yang bikin penonton tidak skip",
      "caption_suggestion": "caption instagram/tiktok max 150 karakter",
      "hashtags": ["#dakwah", "#islam"],
      "reason": "alasan singkat kenapa klip ini dipilih",
      "start_time_ref": "kutipan awal kalimat dari transkrip",
      "end_time_ref": "kutipan akhir kalimat dari transkrip"
    }}
  ]
}}

Kategori yang valid: knowledge, viral_quote, emotional, quran_hadith, beginner
Viral score: 1.0–10.0 (10 = paling viral)
Pastikan start_time dan end_time tepat sesuai timestamp transkrip di atas.
Jangan tambahkan teks apapun selain JSON."""


def _call_groq(
    prompt: str,
    api_key: str,
    progress_callback,
    model: str = GROQ_MODEL,
    retry: int = 0,
) -> str:
    """Panggil Groq API dengan retry otomatis kalau kena rate limit."""
    import urllib.request
    import urllib.error

    _progress(progress_callback, 0.20 + retry * 0.1)

    payload = json.dumps({
        "model":       model,
        "messages":    [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens":  4096,
        "response_format": {"type": "json_object"},   # paksa JSON output
    }).encode("utf-8")

    req = urllib.request.Request(
        GROQ_API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type":  "application/json",
            "User-Agent":    "MahiraClipper/2.0 (Python)",  # FIX: Cloudflare blokir tanpa User-Agent
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            content = body["choices"][0]["message"]["content"]
            usage   = body.get("usage", {})
            log.info("Groq response: %d tokens, model=%s", usage.get("total_tokens", 0), model)
            return content

    except urllib.error.HTTPError as e:
        body_raw = e.read().decode("utf-8", errors="replace")
        if e.code == 429:
            # Rate limit — tunggu dan retry
            wait = 15 * (retry + 1)
            log.warning("Groq rate limit! Tunggu %d detik...", wait)
            if progress_callback:
                progress_callback("analyze", 0.3)
            time.sleep(wait)
            if retry < 3:
                return _call_groq(prompt, api_key, progress_callback, model, retry + 1)
            # Fallback ke model lebih kecil
            if model != GROQ_MODEL_FAST:
                log.warning("Fallback ke model lebih kecil: %s", GROQ_MODEL_FAST)
                return _call_groq(prompt, api_key, progress_callback, GROQ_MODEL_FAST, 0)
            raise RuntimeError("Groq rate limit habis. Coba lagi besok atau ganti API key.")
        elif e.code == 401:
            raise ValueError(
                "Groq API key tidak valid!\n"
                "Pastikan API key benar di Settings.\n"
                "Daftar baru di: https://console.groq.com"
            )
        else:
            raise RuntimeError(f"Groq API error {e.code}: {body_raw[:300]}")

    except Exception as e:
        raise RuntimeError(f"Koneksi ke Groq gagal: {e}")


def _parse_response(raw: str, segments: list, ccfg: ClipConfig) -> dict:
    """Parse JSON dari LLM, validasi, dan normalize."""
    # Strip markdown fence kalau ada
    raw = re.sub(r"```(?:json)?", "", raw).strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        log.error("Gagal parse JSON dari Groq: %s\nRaw: %s", e, raw[:500])
        # Coba ekstrak JSON dengan regex
        m = re.search(r'\{[\s\S]*\}', raw)
        if m:
            try:
                data = json.loads(m.group())
            except Exception:
                raise RuntimeError(f"Groq mengembalikan JSON tidak valid: {raw[:200]}")
        else:
            raise RuntimeError(f"Groq tidak mengembalikan JSON. Response: {raw[:200]}")

    raw_segs = data.get("segments", [])

    # Validasi dan bersihkan setiap segmen
    valid_cats = {"knowledge", "viral_quote", "emotional", "quran_hadith", "beginner"}
    cleaned    = []

    for i, seg in enumerate(raw_segs):
        start = float(seg.get("start_time", 0))
        end   = float(seg.get("end_time", start + 60))
        dur   = end - start

        # Skip kalau durasi tidak masuk range
        if dur < ccfg.min_duration * 0.7 or dur > ccfg.max_duration * 1.3:
            log.debug("Skip segmen durasi tidak valid: %.1f detik", dur)
            continue

        cat = seg.get("category", "knowledge")
        if cat not in valid_cats:
            cat = "knowledge"

        score = float(seg.get("viral_score", 7.0))
        score = max(1.0, min(10.0, score))

        cleaned.append({
            "id":               seg.get("id") or f"clip_{i+1:03d}",
            "title":            str(seg.get("title", f"Klip {i+1}"))[:80],
            "start_time":       round(start, 2),
            "end_time":         round(end, 2),
            "duration":         round(dur, 2),
            "category":         cat,
            "viral_score":      round(score, 1),
            "hook":             str(seg.get("hook", ""))[:200],
            "caption_suggestion": str(seg.get("caption_suggestion", ""))[:200],
            "hashtags":         seg.get("hashtags", DEFAULT_HASHTAGS)[:10],
            "reason":           str(seg.get("reason", ""))[:200],
            "start_time_ref":   str(seg.get("start_time_ref", ""))[:100],
            "end_time_ref":     str(seg.get("end_time_ref", ""))[:100],
            # Status processing
            "is_cut":       False,
            "is_cropped":   False,
            "is_subtitled": False,
            "is_approved":  True,
            "is_uploaded":  False,
            "raw_cut_path":   None,
            "cropped_path":   None,
            "final_path":     None,
            "thumbnail_path": None,
            "final_title":    None,
            "final_caption":  None,
        })

    # Sort by viral score, ambil top N
    cleaned.sort(key=lambda s: s["viral_score"], reverse=True)
    top = cleaned[:ccfg.num_clips]

    # Sort ulang by start_time untuk urutan kronologis
    top.sort(key=lambda s: s["start_time"])

    return {
        "segments":       top,
        "video_summary":  str(data.get("video_summary", ""))[:500],
        "dominant_theme": str(data.get("dominant_theme", ""))[:100],
        "speaker_style":  str(data.get("speaker_style", ""))[:100],
    }


def _progress(cb, val: float):
    if cb:
        cb("analyze", val)


def check_groq_key(api_key: str) -> tuple[bool, str]:
    """Cek apakah Groq API key valid."""
    import urllib.request, urllib.error
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/models",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return True, "OK"
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return False, "API key tidak valid"
        return False, f"Error {e.code}"
    except Exception as e:
        return False, f"Koneksi gagal: {e}"
