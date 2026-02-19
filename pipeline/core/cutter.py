"""
MahiraClipper — Cutter
Potong video berdasarkan timestamp dari Gemini, embed word-level subtitle JSON.
"""

import json
import subprocess
from pathlib import Path
from typing import Optional, Callable

from config.settings import log


def cut_clips(
    video_path: Path,
    segments: list,
    output_folder: Path,
    transcript_data: Optional[dict] = None,
    skip_existing: bool = True,
    progress_callback: Optional[Callable[[str, float], None]] = None,
) -> list:
    output_folder.mkdir(parents=True, exist_ok=True)
    subs_folder   = output_folder.parent / "subs"
    thumbs_folder = output_folder.parent / "thumbnails"
    subs_folder.mkdir(exist_ok=True)
    thumbs_folder.mkdir(exist_ok=True)

    transcript_segs = transcript_data.get("segments", []) if transcript_data else []
    approved = [s for s in segments if s.get("is_approved", True)]
    total    = len(approved)

    if total == 0:
        log.warning("Tidak ada segmen yang approved.")
        return segments

    log.info("Memotong %d klip...", total)
    results   = list(segments)
    done      = 0

    for i, seg in enumerate(results):
        if not seg.get("is_approved", True):
            continue

        safe     = _safe_name(seg.get("title", f"clip_{i}"))
        filename = f"{i:03d}_{safe}"
        out_mp4  = output_folder / f"{filename}.mp4"

        if skip_existing and out_mp4.exists() and out_mp4.stat().st_size > 10000:
            log.info("Skip (sudah ada): %s", out_mp4.name)
            results[i]["raw_cut_path"]       = str(out_mp4)
            results[i]["is_cut"]             = True
            results[i]["subtitle_json_path"] = str(subs_folder / f"{filename}.json")
            done += 1
            if progress_callback:
                progress_callback("cutting", done / total)
            continue

        start    = float(seg.get("start_time", 0))
        end      = float(seg.get("end_time", start + 60))
        duration = end - start

        if duration <= 1:
            log.warning("Skip segmen durasi terlalu pendek (%.1fs): %s", duration, seg.get("title"))
            continue

        # Cut video
        success = _ffmpeg_cut(video_path, out_mp4, start, duration)
        if not success:
            log.error("Gagal potong klip: %s", filename)
            results[i]["is_cut"] = False
            continue

        results[i]["raw_cut_path"] = str(out_mp4)
        results[i]["is_cut"]       = True

        # Thumbnail
        thumb = thumbs_folder / f"{filename}.jpg"
        _generate_thumbnail(out_mp4, thumb)
        results[i]["thumbnail_path"] = str(thumb) if thumb.exists() else None

        # Subtitle JSON — extract dari transkrip Gemini
        sub_json = subs_folder / f"{filename}.json"
        _build_subtitle_json(seg, sub_json, transcript_segs)
        results[i]["subtitle_json_path"] = str(sub_json)

        done += 1
        log.info("[%d/%d] Cut: %s (%.1fs)", done, total, filename, duration)
        if progress_callback:
            progress_callback("cutting", done / total)

    return results


def _build_subtitle_json(seg: dict, output_path: Path, transcript_segs: list):
    """
    Buat subtitle JSON dari transkrip Gemini untuk klip ini.
    Timestamps dikonversi ke relatif terhadap awal klip.
    """
    clip_start = float(seg.get("start_time", 0))
    clip_end   = float(seg.get("end_time", clip_start + 60))

    # Filter transkrip yang masuk ke range klip
    clip_transcript = []
    for ts in transcript_segs:
        ts_start = float(ts.get("start", 0))
        ts_end   = float(ts.get("end", 0))
        if ts_start < clip_end + 1.0 and ts_end > clip_start - 1.0:
            # Konversi ke waktu relatif
            rel_start = max(0.0, ts_start - clip_start)
            rel_end   = max(0.0, ts_end   - clip_start)
            clip_transcript.append({
                "start": round(rel_start, 3),
                "end":   round(rel_end,   3),
                "text":  ts.get("text", "").strip(),
            })

    data = {
        "clip_id":    seg.get("id"),
        "title":      seg.get("title"),
        "category":   seg.get("category"),
        "duration":   round(clip_end - clip_start, 2),
        "language":   "auto",
        "segments":   clip_transcript,
        "hook":       seg.get("hook", ""),
        "viral_score":seg.get("viral_score", 0),
    }

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except IOError as e:
        log.warning("Gagal simpan subtitle JSON: %s", e)


def _ffmpeg_cut(video_path: Path, output_path: Path, start: float, duration: float) -> bool:
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start),
        "-i", str(video_path),
        "-t", str(duration),
        "-c:v", "libx264", "-crf", "18", "-preset", "fast",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        "-avoid_negative_ts", "make_zero",
        str(output_path),
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if result.returncode != 0:
            log.error("FFmpeg cut error:\n%s", result.stderr[-300:])
            return False
        return True
    except FileNotFoundError:
        raise RuntimeError("FFmpeg tidak ditemukan. Install FFmpeg dan tambahkan ke PATH.")
    except Exception as e:
        log.error("FFmpeg exception: %s", e)
        return False


def _generate_thumbnail(video_path: Path, output_path: Path, offset: float = 2.0):
    cmd = ["ffmpeg", "-y", "-ss", str(offset), "-i", str(video_path),
           "-frames:v", "1", "-q:v", "2", str(output_path)]
    try:
        subprocess.run(cmd, capture_output=True, check=False)
    except Exception:
        pass


def _safe_name(title: str, max_len: int = 50) -> str:
    clean = "".join(c for c in title if c.isalnum() or c in " _-").strip()
    result = clean.replace(" ", "_")[:max_len]
    return result if result else "clip"
