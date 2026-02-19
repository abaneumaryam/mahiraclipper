"""
MahiraClipper — Downloader (fixed)
Bug fix:
- _find_downloaded_file: scan semua file di folder, tidak bergantung nama "input"
- download: pakai --print SETELAH download, bukan bareng, supaya tidak conflict
- use_local_file: strip tanda kutip dari path (bug jalankan.bat Windows)
"""

import json
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Callable

from config.settings import log

QUALITY_MAP = {
    "best":  "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
    "1080p": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]",
    "720p":  "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]",
    "480p":  "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]",
}

VIDEO_EXTS = {".mp4", ".mkv", ".webm", ".avi", ".mov", ".m4v", ".flv"}


def download(
    url: str,
    output_folder: Path,
    quality: str = "best",
    download_subtitles: bool = False,
    progress_callback: Optional[Callable[[str, float], None]] = None,
) -> dict:
    if not shutil.which("yt-dlp"):
        raise RuntimeError(
            "yt-dlp tidak ditemukan!\n"
            "Install dengan: pip install yt-dlp\n"
            "Atau: pip install -U yt-dlp"
        )

    output_folder.mkdir(parents=True, exist_ok=True)

    # Nama output pakai %(id)s supaya unik dan mudah dicari
    output_template = str(output_folder / "%(id)s.%(ext)s")
    format_str      = QUALITY_MAP.get(quality, QUALITY_MAP["best"])

    log.info("Mendownload: %s", url)
    if progress_callback:
        progress_callback("downloading", 0.05)

    # ── Snapshot file sebelum download ────────────────────────────────
    files_before = set(output_folder.iterdir())

    # ── Command download ──────────────────────────────────────────────
    cmd = [
        "yt-dlp",
        "--format", format_str,
        "--output", output_template,
        "--merge-output-format", "mp4",
        "--no-playlist",
        "--retries", "5",
        "--fragment-retries", "5",
        "--no-warnings",
        url,
    ]

    result = subprocess.run(
        cmd, capture_output=True, text=True,
        encoding="utf-8", errors="replace"
    )

    if result.returncode != 0:
        # Fallback: format paling simple
        log.warning("Format pertama gagal, coba fallback...")
        cmd_fb = [
            "yt-dlp",
            "--format", "best",
            "--output", output_template,
            "--merge-output-format", "mp4",
            "--no-playlist",
            "--retries", "5",
            "--no-warnings",
            url,
        ]
        result = subprocess.run(
            cmd_fb, capture_output=True, text=True,
            encoding="utf-8", errors="replace"
        )
        if result.returncode != 0:
            err = result.stderr[:600] or result.stdout[:600]
            raise RuntimeError(f"yt-dlp gagal download:\n{err}")

    if progress_callback:
        progress_callback("downloading", 0.85)

    # ── Cari file baru yang muncul setelah download ───────────────────
    files_after = set(output_folder.iterdir())
    new_files   = [f for f in (files_after - files_before)
                   if f.suffix.lower() in VIDEO_EXTS]

    if not new_files:
        # Fallback: ambil file video terbesar di folder
        all_vids = [f for f in output_folder.iterdir()
                    if f.suffix.lower() in VIDEO_EXTS]
        if all_vids:
            new_files = [max(all_vids, key=lambda f: f.stat().st_size)]

    if not new_files:
        raise RuntimeError(
            "File video tidak ditemukan setelah download.\n"
            "Kemungkinan penyebab:\n"
            "  - yt-dlp belum update (jalankan: pip install -U yt-dlp)\n"
            "  - Video memerlukan login\n"
            "  - FFmpeg tidak ada (diperlukan untuk merge video+audio)"
        )

    video_path = new_files[0]

    # ── Ambil metadata video secara terpisah ──────────────────────────
    title, duration = _get_metadata(url)

    log.info("Download selesai: '%s' → %s", title or video_path.stem, video_path.name)
    if progress_callback:
        progress_callback("downloading", 1.0)

    return {
        "video_path":    str(video_path),
        "title":         title or video_path.stem,
        "duration":      duration,
        "platform":      _detect_platform(url),
        "subtitle_path": None,
        "source_url":    url,
    }


def use_local_file(source_path_raw, output_folder: Path) -> dict:
    """
    Pakai file lokal. Auto-strip tanda kutip dari path (bug Windows bat file).
    """
    # Fix: strip tanda kutip yang mungkin masuk dari bat file
    path_str = str(source_path_raw).strip().strip('"').strip("'").strip()
    source_path = Path(path_str)

    if not source_path.exists():
        # Coba cari file dengan nama yang sama di beberapa lokasi umum
        raise FileNotFoundError(
            f"File tidak ditemukan: {source_path}\n"
            f"Tips:\n"
            f"  - Jangan pakai tanda kutip saat input path\n"
            f"  - Contoh benar: C:\\Users\\Umar\\Downloads\\aqso.mp4\n"
            f"  - Contoh salah: \"C:\\Users\\Umar\\Downloads\\aqso.mp4\""
        )

    output_folder.mkdir(parents=True, exist_ok=True)
    dest = output_folder / f"input{source_path.suffix}"

    if source_path.resolve() != dest.resolve():
        log.info("Menyalin file lokal ke project folder...")
        shutil.copy2(source_path, dest)
    else:
        log.info("File sudah ada di project folder.")

    duration = _get_duration_ffprobe(dest)
    log.info("File lokal siap: %s (%.0f detik)", dest.name, duration)

    return {
        "video_path":    str(dest),
        "title":         source_path.stem,
        "duration":      duration,
        "platform":      "local",
        "subtitle_path": None,
        "source_url":    None,
    }


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _get_metadata(url: str) -> tuple:
    """Ambil title & duration via yt-dlp --dump-json (tidak download ulang)."""
    try:
        result = subprocess.run(
            ["yt-dlp", "--dump-json", "--no-playlist", "--no-warnings", url],
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout.strip().splitlines()[0])
            return data.get("title", ""), float(data.get("duration", 0))
    except Exception:
        pass
    return "", 0.0


def _get_duration_ffprobe(video_path: Path) -> float:
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json",
             "-show_format", str(video_path)],
            capture_output=True, text=True, timeout=15
        )
        data = json.loads(result.stdout)
        return float(data.get("format", {}).get("duration", 0))
    except Exception:
        return 0.0


def _detect_platform(url: str) -> str:
    url = url.lower()
    if "youtube.com" in url or "youtu.be" in url: return "youtube"
    if "instagram.com" in url:  return "instagram"
    if "facebook.com" in url or "fb.watch" in url: return "facebook"
    if "tiktok.com" in url: return "tiktok"
    return "other"
