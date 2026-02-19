"""
MahiraClipper — Gemini Processor
Satu modul untuk segalanya: upload audio → transkripsi → analisis dakwah.
Tidak butuh WhisperX, tidak butuh GPU. Cukup Gemini API (gratis).

Alur kerja:
  1. Ekstrak audio dari video (FFmpeg, ringan)
  2. Upload audio ke Gemini File API
  3. Satu prompt → dapat transkripsi + segmen dakwah sekaligus
  4. Simpan hasil ke project folder
"""

import json
import os
import re
import subprocess
import time
import uuid
from pathlib import Path
from typing import Callable, Optional

from config.settings import GeminiConfig, ClipConfig, log
from config.prompts import (
    DAKWAH_ANALYSIS_PROMPT,
    CAPTION_PROMPT,
    DEFAULT_HASHTAGS,
)


# ─── Konstanta ────────────────────────────────────────────────────────────────

MAX_AUDIO_MB   = 100          # Batas aman untuk Gemini File API (free tier)
CHUNK_MINUTES  = 25           # Potong audio per 25 menit kalau terlalu panjang
AUDIO_BITRATE  = "32k"        # Bitrate rendah = file kecil, transkripsi tetap oke
SUPPORTED_EXTS = {".mp4", ".mkv", ".webm", ".avi", ".mov", ".mp3", ".wav", ".m4a"}


# ─── Main Entry Point ─────────────────────────────────────────────────────────

def process(
    video_path: Path,
    project_folder: Path,
    gemini_config: Optional[GeminiConfig] = None,
    clip_config: Optional[ClipConfig] = None,
    progress_callback: Optional[Callable[[str, float], None]] = None,
) -> dict:
    """
    Pipeline utama: video → transkripsi + segmen dakwah via Gemini.

    Returns dict:
    {
      "transcript": {language, segments, full_text, transcript_path},
      "analysis":   {segments, video_summary, dominant_theme, speaker_style}
    }
    """
    gcfg = gemini_config or GeminiConfig()
    ccfg = clip_config   or ClipConfig()

    _validate_config(gcfg)

    # ── Cache check ───────────────────────────────────────────────────────
    cache_path = project_folder / "gemini_result.json"
    if cache_path.exists():
        log.info("Hasil Gemini sudah ada, skip proses ulang.")
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)

    _progress(progress_callback, 0.05)

    # ── Step 1: Ekstrak audio ─────────────────────────────────────────────
    log.info("Mengekstrak audio dari video...")
    audio_path = _extract_audio(video_path, project_folder)
    _progress(progress_callback, 0.15)

    # ── Step 2: Upload ke Gemini File API ─────────────────────────────────
    audio_size_mb = audio_path.stat().st_size / (1024 * 1024)
    log.info("Ukuran audio: %.1f MB", audio_size_mb)

    if audio_size_mb > MAX_AUDIO_MB:
        log.info("Audio terlalu besar, proses per chunk...")
        result = _process_chunked(audio_path, project_folder, gcfg, ccfg, progress_callback)
    else:
        result = _process_single(audio_path, project_folder, gcfg, ccfg, progress_callback)

    # ── Step 3: Simpan cache ──────────────────────────────────────────────
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    # Simpan juga transcript terpisah untuk kompatibilitas
    transcript_path = project_folder / "transcript.json"
    with open(transcript_path, "w", encoding="utf-8") as f:
        json.dump(result["transcript"], f, indent=2, ensure_ascii=False)

    log.info("✓ Proses Gemini selesai:")
    log.info("  Bahasa    : %s", result["transcript"].get("language", "?"))
    log.info("  Kata      : %d", len(result["transcript"].get("full_text", "").split()))
    log.info("  Segmen AI : %d", len(result["analysis"].get("segments", [])))
    log.info("  Tema      : %s", result["analysis"].get("dominant_theme", "?"))

    _progress(progress_callback, 1.0)
    return result


# ─── Single File Processing ───────────────────────────────────────────────────

def _process_single(
    audio_path: Path,
    project_folder: Path,
    gcfg: GeminiConfig,
    ccfg: ClipConfig,
    progress_callback,
) -> dict:
    """Proses audio dalam satu request Gemini."""
    import google.generativeai as genai
    genai.configure(api_key=gcfg.api_key)

    # Upload audio
    log.info("Mengupload audio ke Gemini...")
    audio_file = _upload_audio(audio_path, gcfg)
    _progress(progress_callback, 0.40)

    # Build prompt gabungan: transkripsi + analisis sekaligus
    prompt = _build_combined_prompt(ccfg)

    # Call Gemini
    log.info("Meminta Gemini untuk transkripsi + analisis dakwah...")
    model = genai.GenerativeModel(
        model_name=gcfg.model,
        generation_config={
            "temperature": gcfg.temperature,
            "max_output_tokens": gcfg.max_output_tokens,
        },
    )

    _progress(progress_callback, 0.50)

    raw = _call_with_retry(model, [audio_file, prompt], gcfg)
    _progress(progress_callback, 0.80)

    # Cleanup file di Gemini
    _delete_uploaded_file(audio_file)

    # Parse hasil
    result = _parse_combined_response(raw, ccfg)
    return result


# ─── Chunked Processing (video panjang) ──────────────────────────────────────

def _process_chunked(
    audio_path: Path,
    project_folder: Path,
    gcfg: GeminiConfig,
    ccfg: ClipConfig,
    progress_callback,
) -> dict:
    """Potong audio jadi chunk, proses tiap chunk, gabungkan hasilnya."""
    import google.generativeai as genai
    genai.configure(api_key=gcfg.api_key)

    chunks_folder = project_folder / "audio_chunks"
    chunks_folder.mkdir(exist_ok=True)

    chunks = _split_audio(audio_path, chunks_folder, minutes=CHUNK_MINUTES)
    log.info("Audio dibagi menjadi %d chunk.", len(chunks))

    all_transcript_segments = []
    all_analysis_segments   = []
    summaries               = []
    themes                  = []
    language                = "id"
    speaker_style           = ""
    time_offset             = 0.0

    model = genai.GenerativeModel(
        model_name=gcfg.model,
        generation_config={
            "temperature": gcfg.temperature,
            "max_output_tokens": gcfg.max_output_tokens,
        },
    )

    for i, chunk_path in enumerate(chunks):
        log.info("Memproses chunk %d/%d...", i + 1, len(chunks))
        pct_start = 0.3 + (i / len(chunks)) * 0.5

        # Upload chunk
        audio_file = _upload_audio(chunk_path, gcfg)

        # Prompt dengan context offset waktu
        prompt = _build_combined_prompt(ccfg, time_offset_minutes=time_offset / 60)

        raw = _call_with_retry(model, [audio_file, prompt], gcfg)
        _delete_uploaded_file(audio_file)

        # Parse chunk result
        chunk_result = _parse_combined_response(raw, ccfg)

        # Adjust timestamps
        chunk_transcripts = chunk_result["transcript"].get("segments", [])
        for seg in chunk_transcripts:
            seg["start"] = seg.get("start", 0) + time_offset
            seg["end"]   = seg.get("end",   0) + time_offset

        chunk_analysis = chunk_result["analysis"].get("segments", [])
        for seg in chunk_analysis:
            seg["start_time"] = seg.get("start_time", 0) + time_offset
            seg["end_time"]   = seg.get("end_time",   0) + time_offset
            seg["duration"]   = seg["end_time"] - seg["start_time"]

        all_transcript_segments.extend(chunk_transcripts)
        all_analysis_segments.extend(chunk_analysis)

        if chunk_result["transcript"].get("language"):
            language = chunk_result["transcript"]["language"]
        if chunk_result["analysis"].get("video_summary"):
            summaries.append(chunk_result["analysis"]["video_summary"])
        if chunk_result["analysis"].get("dominant_theme"):
            themes.append(chunk_result["analysis"]["dominant_theme"])
        if not speaker_style and chunk_result["analysis"].get("speaker_style"):
            speaker_style = chunk_result["analysis"]["speaker_style"]

        # Estimasi durasi chunk untuk offset berikutnya
        time_offset += CHUNK_MINUTES * 60

        _progress(progress_callback, pct_start + (1 / len(chunks)) * 0.5)

    # Gabungkan dan ambil best segments
    merged_analysis = _merge_and_rank_segments(all_analysis_segments, ccfg)

    full_text = " ".join(
        s.get("text", "") for s in all_transcript_segments
    )

    return {
        "transcript": {
            "language": language,
            "segments": all_transcript_segments,
            "full_text": full_text,
        },
        "analysis": {
            "segments":       merged_analysis,
            "video_summary":  " ".join(summaries[:2]),
            "dominant_theme": themes[0] if themes else "",
            "speaker_style":  speaker_style,
        },
    }


# ─── Prompt Builder ───────────────────────────────────────────────────────────

def _build_combined_prompt(
    ccfg: ClipConfig,
    time_offset_minutes: float = 0,
) -> str:
    """
    Satu prompt yang minta Gemini untuk:
    1. Transkripsi audio dengan timestamp
    2. Analisis dan pilih segmen dakwah terbaik
    """
    offset_note = ""
    if time_offset_minutes > 0:
        offset_note = (
            f"\nCATATAN: Audio ini dimulai dari menit ke-{time_offset_minutes:.0f} "
            f"dari video asli. Tambahkan {time_offset_minutes * 60:.0f} detik ke semua timestamp.\n"
        )

    return f"""
Kamu adalah asisten transkripsi dan kurator konten dakwah Islam yang ahli.
Dengarkan audio ceramah/kajian Islam ini dan lakukan DUA tugas sekaligus.
{offset_note}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TUGAS 1: TRANSKRIPSI LENGKAP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Transkripsi SELURUH isi audio dengan akurat.
- Deteksi bahasa secara otomatis (Indonesia, Arab, Inggris, atau campuran)
- Beri timestamp dalam detik untuk setiap kalimat/segmen
- Untuk bacaan Arab: tulis Arab aslinya, bukan transliterasi
- Jangan lewatkan bagian manapun

Format tiap segmen transkrip:
{{"start": 12.5, "end": 18.3, "text": "isi kalimat disini"}}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TUGAS 2: PILIH SEGMEN DAKWAH TERBAIK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Dari seluruh konten, pilih {ccfg.num_clips} segmen terbaik untuk dijadikan
klip viral TikTok/Reels/Shorts. Durasi tiap klip: {ccfg.min_duration}–{ccfg.max_duration} detik.

Prioritaskan segmen yang:
1. 📚 ILMU PADAT — pelajaran Islam yang jelas, bisa langsung diamalkan
2. 💡 KUTIPAN VIRAL — kalimat powerful, analogi modern, nasihat menohok
3. 💚 EMOSIONAL — momen haru, peringatan keras, kisah menyentuh
4. 📖 QURAN/HADITS + PENJELASAN — bukan bacaan saja, harus ada tafsirnya
5. 🌱 RAMAH PEMULA — penjelasan Islam yang mudah untuk pemula/non-Muslim

HINDARI: doa tanpa penjelasan, pembukaan/penutupan ceramah, pengumuman acara,
potongan cerita tanpa konteks, dan kontroversi politik.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FORMAT OUTPUT — HANYA JSON, TIDAK ADA TEKS LAIN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{{
  "transcript": {{
    "language": "id",
    "segments": [
      {{"start": 0.0, "end": 5.2, "text": "kalimat pertama"}},
      {{"start": 5.2, "end": 11.0, "text": "kalimat kedua"}}
    ],
    "full_text": "seluruh teks tanpa timestamp"
  }},
  "analysis": {{
    "segments": [
      {{
        "id": "",
        "title": "Judul klip menarik maks 8 kata",
        "start_time": 45.0,
        "end_time": 105.0,
        "duration": 60.0,
        "category": "knowledge",
        "viral_score": 8.5,
        "hook": "Kalimat pembuka klip — kenapa penonton tidak skip?",
        "caption_suggestion": "Saran caption TikTok/IG dengan emoji",
        "hashtags": ["#dakwah", "#ceramah", "#islam"],
        "reason": "Satu kalimat kenapa segmen ini layak dijadikan klip"
      }}
    ],
    "video_summary": "Ringkasan ceramah dalam 2-3 kalimat",
    "dominant_theme": "tema utama ceramah",
    "speaker_style": "deskripsi singkat gaya penceramah"
  }}
}}
"""


# ─── Audio Helpers ────────────────────────────────────────────────────────────

def _extract_audio(video_path: Path, output_folder: Path) -> Path:
    """Ekstrak audio dari video ke MP3 kualitas rendah (hemat kuota)."""
    audio_path = output_folder / "audio.mp3"

    if audio_path.exists() and audio_path.stat().st_size > 1000:
        log.info("Audio sudah ada, skip ekstraksi.")
        return audio_path

    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vn",                        # no video
        "-ac", "1",                   # mono (lebih kecil)
        "-ar", "16000",               # 16kHz cukup untuk speech
        "-b:a", AUDIO_BITRATE,        # bitrate rendah
        "-f", "mp3",
        str(audio_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg gagal ekstrak audio:\n{result.stderr[-300:]}")

    size_mb = audio_path.stat().st_size / (1024 * 1024)
    log.info("Audio diekstrak: %.1f MB", size_mb)
    return audio_path


def _split_audio(audio_path: Path, output_folder: Path, minutes: int = 25) -> list:
    """Potong audio jadi beberapa bagian untuk video panjang."""
    seconds = minutes * 60
    chunk_template = str(output_folder / "chunk_%03d.mp3")

    cmd = [
        "ffmpeg", "-y",
        "-i", str(audio_path),
        "-f", "segment",
        "-segment_time", str(seconds),
        "-c", "copy",
        chunk_template,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        log.warning("Split audio gagal, pakai file asli.")
        return [audio_path]

    chunks = sorted(output_folder.glob("chunk_*.mp3"))
    return chunks if chunks else [audio_path]


def _upload_audio(audio_path: Path, gcfg: GeminiConfig):
    """Upload file audio ke Gemini File API."""
    import google.generativeai as genai

    log.info("Mengupload: %s (%.1f MB)...",
             audio_path.name, audio_path.stat().st_size / (1024 * 1024))

    audio_file = genai.upload_file(
        path=str(audio_path),
        mime_type="audio/mp3",
    )

    # Tunggu sampai file siap diproses
    max_wait = 120
    waited   = 0
    while audio_file.state.name == "PROCESSING":
        if waited >= max_wait:
            raise RuntimeError("Timeout: Gemini File API tidak merespons.")
        time.sleep(3)
        waited += 3
        audio_file = genai.get_file(audio_file.name)

    if audio_file.state.name == "FAILED":
        raise RuntimeError(f"Upload ke Gemini gagal: {audio_file.state}")

    log.info("Upload selesai: %s", audio_file.name)
    return audio_file


def _delete_uploaded_file(audio_file):
    """Hapus file dari Gemini setelah selesai dipakai."""
    try:
        import google.generativeai as genai
        genai.delete_file(audio_file.name)
        log.debug("File Gemini dihapus: %s", audio_file.name)
    except Exception as e:
        log.debug("Gagal hapus file Gemini: %s", e)


# ─── Gemini Call ──────────────────────────────────────────────────────────────

def _call_with_retry(model, contents: list, gcfg: GeminiConfig, retries: int = 3) -> str:
    """Panggil Gemini dengan retry otomatis kalau rate limit."""
    for attempt in range(retries):
        try:
            response = model.generate_content(contents)
            return response.text
        except Exception as e:
            err = str(e).lower()
            if "quota" in err or "rate" in err or "429" in err:
                wait = (attempt + 1) * 15
                log.warning("Rate limit Gemini. Tunggu %d detik...", wait)
                time.sleep(wait)
            elif "500" in err or "503" in err:
                wait = (attempt + 1) * 5
                log.warning("Gemini server error. Retry dalam %d detik...", wait)
                time.sleep(wait)
            elif attempt < retries - 1:
                log.warning("Gemini error (attempt %d): %s. Retry...", attempt + 1, e)
                time.sleep(5)
            else:
                raise RuntimeError(f"Gemini gagal setelah {retries} percobaan: {e}")

    raise RuntimeError("Gemini API tidak merespons.")


# ─── Response Parser ──────────────────────────────────────────────────────────

def _parse_combined_response(raw: str, ccfg: ClipConfig) -> dict:
    """Parse JSON response dari Gemini, handle noise dan format tidak rapi."""
    data = _extract_json(raw)

    if not data:
        log.error("Gagal parse response Gemini. Raw:\n%s", raw[:500])
        return _empty_result()

    transcript = data.get("transcript", {})
    analysis   = data.get("analysis",   {})
    segments   = analysis.get("segments", [])

    # Pastikan tiap segmen punya ID dan field wajib
    for seg in segments:
        if not seg.get("id"):
            seg["id"] = uuid.uuid4().hex[:8]

        # Hitung duration kalau belum ada
        if not seg.get("duration"):
            seg["duration"] = seg.get("end_time", 0) - seg.get("start_time", 0)

        # Default hashtags berdasar kategori
        if not seg.get("hashtags"):
            cat = seg.get("category", "knowledge")
            seg["hashtags"] = DEFAULT_HASHTAGS.get(cat, DEFAULT_HASHTAGS["knowledge"])

        # Tracking fields
        seg.setdefault("is_approved",  True)
        seg.setdefault("is_cut",       False)
        seg.setdefault("is_cropped",   False)
        seg.setdefault("is_subtitled", False)
        seg.setdefault("is_uploaded",  False)
        seg.setdefault("raw_cut_path", None)
        seg.setdefault("cropped_path", None)
        seg.setdefault("final_path",   None)
        seg.setdefault("thumbnail_path", None)
        seg.setdefault("final_title",    None)
        seg.setdefault("final_caption",  None)

    # Validasi dan filter segmen
    segments = _validate_segments(segments, ccfg)
    analysis["segments"] = segments

    return {"transcript": transcript, "analysis": analysis}


def _validate_segments(segments: list, ccfg: ClipConfig) -> list:
    """Filter overlap, durasi invalid, urutkan by viral_score."""
    valid = []
    for seg in segments:
        dur = seg.get("duration", 0)

        # Skip kalau durasi tidak masuk akal
        if dur < 5:
            log.debug("Skip segmen terlalu pendek (%.1fs): %s", dur, seg.get("title", ""))
            continue

        # Trim kalau terlalu panjang
        if dur > ccfg.max_duration * 1.3:
            trim = dur - ccfg.max_duration
            seg["end_time"] = seg["end_time"] - trim * 0.5
            seg["duration"] = seg["end_time"] - seg["start_time"]

        valid.append(seg)

    # Sort by start time, hapus overlap
    valid.sort(key=lambda s: s.get("start_time", 0))
    result    = []
    last_end  = -999

    for seg in valid:
        if seg.get("start_time", 0) >= last_end - 2.0:
            result.append(seg)
            last_end = seg.get("end_time", 0)
        else:
            log.debug("Skip segmen overlap: %s", seg.get("title", ""))

    # Final sort by viral_score
    result.sort(key=lambda s: s.get("viral_score", 0), reverse=True)

    # Ambil top N
    return result[:ccfg.num_clips + 2]


def _merge_and_rank_segments(all_segments: list, ccfg: ClipConfig) -> list:
    """Gabungkan segmen dari multiple chunks dan ambil yang terbaik."""
    if not all_segments:
        return []

    # Sort by viral_score, ambil top N, lalu sort ulang by start_time
    ranked = sorted(all_segments, key=lambda s: s.get("viral_score", 0), reverse=True)
    top    = ranked[:ccfg.num_clips]
    top.sort(key=lambda s: s.get("start_time", 0))
    return top


# ─── Caption Generator ────────────────────────────────────────────────────────

def generate_caption(
    clip: dict,
    dominant_theme: str,
    gemini_config: Optional[GeminiConfig] = None,
) -> dict:
    """
    Generate 3 versi caption (pendek/sedang/panjang) untuk satu klip.
    Dipanggil dari Web UI saat user klik "Generate Caption".
    """
    import google.generativeai as genai

    gcfg = gemini_config or GeminiConfig()
    _validate_config(gcfg)
    genai.configure(api_key=gcfg.api_key)

    prompt = CAPTION_PROMPT.format(
        title=clip.get("title", ""),
        category=clip.get("category", "knowledge"),
        hook=clip.get("hook", ""),
        theme=dominant_theme,
    )

    model = genai.GenerativeModel(
        model_name=gcfg.model,
        generation_config={"temperature": 0.7, "max_output_tokens": 1000},
    )

    try:
        raw    = model.generate_content(prompt).text
        result = _extract_json(raw)
        return result or {
            "short": clip.get("caption_suggestion", ""),
            "medium": "",
            "long": "",
            "hashtags_suggested": clip.get("hashtags", []),
        }
    except Exception as e:
        log.warning("Generate caption gagal: %s", e)
        return {
            "short": clip.get("caption_suggestion", ""),
            "medium": "",
            "long": "",
            "hashtags_suggested": clip.get("hashtags", []),
        }


# ─── Utilities ────────────────────────────────────────────────────────────────

def _extract_json(raw: str) -> Optional[dict]:
    """Ekstrak JSON dari response yang mungkin berisi noise/markdown."""
    if not raw:
        return None

    # Bersihkan markdown
    cleaned = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()

    # Coba parse langsung
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Cari objek JSON pertama yang valid
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    return None


def _empty_result() -> dict:
    return {
        "transcript": {"language": "id", "segments": [], "full_text": ""},
        "analysis":   {"segments": [], "video_summary": "", "dominant_theme": "", "speaker_style": ""},
    }


def _validate_config(gcfg: GeminiConfig):
    if not gcfg.api_key:
        raise ValueError(
            "Gemini API key belum diisi!\n"
            "Isi di api_config.json → gemini.api_key\n"
            "Atau set env var: MAHIRA_GEMINI_KEY=...\n"
            "Dapatkan key gratis: https://aistudio.google.com/app/apikey"
        )


def _progress(callback, value: float):
    if callback:
        callback("processing", value)
