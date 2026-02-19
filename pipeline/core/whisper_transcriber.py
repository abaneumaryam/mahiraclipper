"""
MahiraClipper — Whisper Transcriber (Lokal, Offline, Unlimited)
Transkripsi video pakai faster-whisper di CPU. Tidak butuh internet, tidak ada rate limit.

Model yang dipakai:
  - "small"  : 244M param, ~1-2GB RAM, cepat, cukup akurat untuk ceramah
  - "medium" : 769M param, ~2-4GB RAM, lebih akurat untuk aksen & istilah Arab
  - "large-v3": paling akurat, butuh 4-6GB RAM, lebih lambat

Untuk ceramah Indonesia dengan istilah Arab → medium direkomendasikan.
"""

import json
import subprocess
from pathlib import Path
from typing import Callable, Optional

from config.settings import log

SUPPORTED_EXTS = {".mp4", ".mkv", ".webm", ".avi", ".mov", ".mp3", ".wav", ".m4a"}


# ─── Main Entry ──────────────────────────────────────────────────────────────

def transcribe(
    video_path: Path,
    project_folder: Path,
    model_size: str = "small",
    language: str = "id",
    progress_callback: Optional[Callable[[str, float], None]] = None,
) -> dict:
    """
    Transkripsi video/audio menggunakan faster-whisper lokal.

    Returns:
        {
          "segments": [...],       # [{start, end, text, words:[{start,end,word}]}]
          "full_text": "...",
          "language": "id",
          "transcript_path": "/path/to/transcript.json"
        }
    """
    _progress(progress_callback, 0.05)

    # ── Cek faster-whisper tersedia ───────────────────────────────────────
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        raise RuntimeError(
            "faster-whisper belum terinstall!\n"
            "Jalankan: pip install faster-whisper"
        )

    # ── Ekstrak audio dulu (lebih ringan dari video untuk Whisper) ────────
    audio_path = project_folder / "audio.wav"
    _extract_audio(video_path, audio_path, progress_callback)
    _progress(progress_callback, 0.15)

    # ── Load model (download otomatis pertama kali ~500MB untuk small) ────
    log.info("Loading Whisper model: %s", model_size)
    _progress(progress_callback, 0.20)

    # Cache model di folder permanen agar tidak download ulang setiap kali
    import os
    cache_dir = Path(os.environ.get(
        "MAHIRA_WHISPER_CACHE",
        Path.home() / ".cache" / "mahiraclipper" / "whisper"
    ))
    cache_dir.mkdir(parents=True, exist_ok=True)
    log.info("Whisper cache dir: %s", cache_dir)

    try:
        model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8",      # int8 = 2x lebih cepat di CPU
            download_root=str(cache_dir),  # simpan model di sini, tidak download ulang!
        )
    except Exception as e:
        raise RuntimeError(f"Gagal load Whisper model '{model_size}': {e}")

    log.info("Mulai transkripsi dengan Whisper %s...", model_size)
    _progress(progress_callback, 0.25)

    # ── Transkripsi ───────────────────────────────────────────────────────
    try:
        segments_gen, info = model.transcribe(
            str(audio_path),
            language=language if language != "auto" else None,
            beam_size=5,
            word_timestamps=True,      # word-level timestamps untuk subtitle
            vad_filter=True,           # skip silence → lebih bersih
            vad_parameters={
                "min_silence_duration_ms": 500,
                "speech_pad_ms": 200,
            },
            condition_on_previous_text=True,
        )

        # Consume generator (sambil update progress)
        segments_list = []
        total_duration = info.duration or 1
        last_pct = 0.25

        for seg in segments_gen:
            segments_list.append(seg)
            pct = 0.25 + (seg.end / total_duration) * 0.65
            if pct - last_pct > 0.02:
                _progress(progress_callback, min(pct, 0.90))
                last_pct = pct

    except Exception as e:
        raise RuntimeError(f"Whisper transkripsi gagal: {e}")

    _progress(progress_callback, 0.90)

    # ── Format hasil ──────────────────────────────────────────────────────
    formatted_segs = []
    full_text_parts = []

    for seg in segments_list:
        words = []
        if seg.words:
            for w in seg.words:
                words.append({
                    "start": round(w.start, 3),
                    "end":   round(w.end, 3),
                    "word":  w.word.strip(),
                    "probability": round(getattr(w, "probability", 1.0), 3),
                })

        formatted_segs.append({
            "start":       round(seg.start, 3),
            "end":         round(seg.end, 3),
            "text":        seg.text.strip(),
            "words":       words,
            "avg_logprob": round(getattr(seg, "avg_logprob", 0), 4),
            "no_speech_prob": round(getattr(seg, "no_speech_prob", 0), 4),
        })
        full_text_parts.append(seg.text.strip())

    full_text      = " ".join(full_text_parts)
    detected_lang  = getattr(info, "language", language) or language

    log.info("Transkripsi selesai: %d segmen, bahasa=%s, durasi=%.0fs",
             len(formatted_segs), detected_lang, total_duration)

    # ── Simpan ke file ────────────────────────────────────────────────────
    transcript_path = project_folder / "transcript.json"
    transcript_data = {
        "language":  detected_lang,
        "duration":  round(total_duration, 2),
        "model":     model_size,
        "segments":  formatted_segs,
        "full_text": full_text,
    }
    with open(transcript_path, "w", encoding="utf-8") as f:
        json.dump(transcript_data, f, ensure_ascii=True, indent=2)

    # Cleanup audio temp
    if audio_path.exists():
        audio_path.unlink()

    _progress(progress_callback, 1.0)

    return {
        "segments":        formatted_segs,
        "full_text":       full_text,
        "language":        detected_lang,
        "duration":        round(total_duration, 2),
        "transcript_path": str(transcript_path),
    }


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _extract_audio(video_path: Path, audio_path: Path, progress_callback):
    """Ekstrak audio dari video ke WAV 16kHz mono (format optimal untuk Whisper)."""
    log.info("Ekstrak audio dari: %s", video_path.name)
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-ar", "16000",     # 16kHz — yang Whisper minta
        "-ac", "1",         # mono
        "-c:a", "pcm_s16le", # PCM uncompressed — paling cepat diproses
        str(audio_path),
    ]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True,
            encoding="utf-8", errors="replace"
        )
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg extract audio gagal:\n{result.stderr[-300:]}")
        log.info("Audio diekstrak: %s (%.1f MB)",
                 audio_path.name,
                 audio_path.stat().st_size / 1024 / 1024)
    except FileNotFoundError:
        raise RuntimeError("FFmpeg tidak ditemukan. Install FFmpeg terlebih dahulu.")


def _progress(cb, val: float):
    if cb:
        cb("transcribe", val)


def check_whisper_installed() -> bool:
    """Cek apakah faster-whisper sudah terinstall."""
    try:
        import faster_whisper
        return True
    except ImportError:
        return False


def get_model_info(model_size: str) -> dict:
    """Info ukuran model untuk ditampilkan di UI."""
    models = {
        "tiny":     {"size_mb": 75,   "ram_gb": 1,   "speed": "sangat cepat", "akurasi": "rendah"},
        "base":     {"size_mb": 145,  "ram_gb": 1,   "speed": "cepat",        "akurasi": "cukup"},
        "small":    {"size_mb": 490,  "ram_gb": 2,   "speed": "cepat",        "akurasi": "baik"},
        "medium":   {"size_mb": 1500, "ram_gb": 4,   "speed": "sedang",       "akurasi": "sangat baik"},
        "large-v3": {"size_mb": 3100, "ram_gb": 6,   "speed": "lambat",       "akurasi": "terbaik"},
        "turbo":    {"size_mb": 1600, "ram_gb": 3,   "speed": "cepat",        "akurasi": "sangat baik"},
    }
    return models.get(model_size, {"size_mb": 0, "ram_gb": 0, "speed": "?", "akurasi": "?"})
