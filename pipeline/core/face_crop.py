"""
MahiraClipper — Face Crop
Reframe video horizontal ke 9:16 vertikal dengan face tracking.
Pakai MediaPipe (ringan, tanpa GPU) atau fallback center crop.

Mode:
  auto    = deteksi jumlah wajah, pilih mode otomatis
  center  = crop tengah saja (no face detection, paling ringan)
  face    = tracking satu wajah
"""

import json
import subprocess
from pathlib import Path
from typing import Optional, Callable

from config.settings import FaceConfig, log


# ─── Main Entry ──────────────────────────────────────────────────────────────

def crop_to_vertical(
    video_path: Path,
    output_path: Path,
    config: Optional[FaceConfig] = None,
    progress_callback: Optional[Callable[[str, float], None]] = None,
    target_w: int = 1080,
    target_h: int = 1920,
) -> bool:
    """
    Crop video ke format target (default 9:16 = 1080x1920).
    target_w/target_h bisa diset dari UI untuk format lain (1:1, 16:9, 4:5).

    Returns:
        True jika berhasil, False jika gagal
    """
    cfg = config or FaceConfig()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Skip kalau sudah ada
    if output_path.exists() and output_path.stat().st_size > 10000:
        log.info("Skip crop (sudah ada): %s", output_path.name)
        return True

    # Cek dimensi video
    info = _get_video_info(video_path)
    if not info:
        log.warning("Tidak bisa baca info video: %s", video_path.name)
        return False

    w, h = info["width"], info["height"]
    log.info("Video input: %dx%d | Target: %dx%d", w, h, target_w, target_h)

    _progress(progress_callback, 0.1)

    # Jika video sudah sesuai target ratio, skip crop
    target_ratio_val = target_w / target_h
    src_ratio = w / h
    if abs(src_ratio - target_ratio_val) < 0.05:
        log.info("Video sudah sesuai rasio target, skip crop.")
        import shutil
        shutil.copy2(video_path, output_path)
        return True

    # Pilih metode crop
    if cfg.mode == "center" or not _check_mediapipe():
        log.info("Pakai center crop (mediapipe tidak tersedia).")
        success = _center_crop(video_path, output_path, w, h, cfg, target_w, target_h)
    else:
        log.info("Pakai face tracking dengan MediaPipe.")
        success = _face_tracking_crop(video_path, output_path, w, h, cfg, progress_callback, target_w, target_h)

    _progress(progress_callback, 1.0)
    return success


# ─── Batch Crop ───────────────────────────────────────────────────────────────

def crop_all_clips(
    clips: list,
    cuts_folder: Path,
    cropped_folder: Path,
    config: Optional[FaceConfig] = None,
    progress_callback: Optional[Callable[[str, float], None]] = None,
    target_w: int = 1080,
    target_h: int = 1920,
) -> list:
    """Crop semua klip yang sudah di-cut ke format target (default 9:16)."""
    cropped_folder.mkdir(parents=True, exist_ok=True)
    cfg = config or FaceConfig()

    approved = [c for c in clips if c.get("is_approved", True) and c.get("is_cut", False)]
    total    = len(approved)
    done     = 0

    if total == 0:
        log.warning("Tidak ada klip untuk di-crop.")
        return clips

    log.info("Cropping %d klip ke format 9:16...", total)
    results = list(clips)

    for i, clip in enumerate(results):
        if not clip.get("is_approved", True) or not clip.get("is_cut", False):
            continue

        raw_cut = clip.get("raw_cut_path")
        if not raw_cut or not Path(raw_cut).exists():
            continue

        safe     = _safe_name(clip.get("title", f"clip_{i}"))
        filename = f"{i:03d}_{safe}_cropped.mp4"
        out_path = cropped_folder / filename

        def cb(step, pct):
            overall = (done + pct) / total
            if progress_callback:
                progress_callback("cropping", overall)

        success = crop_to_vertical(
            video_path=Path(raw_cut),
            output_path=out_path,
            config=cfg,
            progress_callback=cb,
            target_w=target_w,
            target_h=target_h,
        )

        if success:
            results[i]["cropped_path"] = str(out_path)
            results[i]["is_cropped"]   = True
        else:
            # Fallback: pakai raw cut tanpa crop
            results[i]["cropped_path"] = raw_cut
            results[i]["is_cropped"]   = False
            log.warning("Crop gagal untuk: %s, pakai original.", clip.get("title",""))

        done += 1
        log.info("[%d/%d] Crop selesai: %s", done, total, filename)

    return results


# ─── Center Crop (no face detection) ─────────────────────────────────────────

def _center_crop(
    video_path: Path,
    output_path: Path,
    src_w: int,
    src_h: int,
    cfg: FaceConfig,
    target_w: int = 1080,
    target_h: int = 1920,
) -> bool:
    """
    Crop tengah video ke target ratio.
    Kalau video lebih lebar: crop sisi kiri-kanan.
    Kalau video lebih tinggi: letterbox dengan padding hitam.
    """

    if cfg.no_face_mode == "zoom":
        # Zoom + crop tengah
        scale_h = target_h / src_h
        scaled_w = int(src_w * scale_h)
        if scaled_w < target_w:
            scale_w = target_w / src_w
            scaled_h = int(src_h * scale_w)
            vf = f"scale={target_w}:{scaled_h},crop={target_w}:{target_h}:(iw-{target_w})/2:(ih-{target_h})/2"
        else:
            vf = f"scale={scaled_w}:{target_h},crop={target_w}:{target_h}:(iw-{target_w})/2:0"
    else:
        # Padding hitam (letterbox)
        vf = f"scale={target_w}:{target_h}:force_original_aspect_ratio=decrease,pad={target_w}:{target_h}:(ow-iw)/2:(oh-ih)/2:black"

    return _run_ffmpeg_vf(video_path, output_path, vf)


# ─── Face Tracking Crop ───────────────────────────────────────────────────────

def _face_tracking_crop(
    video_path: Path,
    output_path: Path,
    src_w: int,
    src_h: int,
    cfg: FaceConfig,
    progress_callback,
    target_w: int = 1080,
    target_h: int = 1920,
) -> bool:
    """
    Deteksi wajah per-frame, buat crop coordinates, apply dengan FFmpeg.
    """
    try:
        import mediapipe as mp
        import cv2
        import numpy as np
    except ImportError:
        log.warning("mediapipe/cv2 tidak tersedia. Fallback ke center crop.")
        return _center_crop(video_path, output_path, src_w, src_h, cfg, target_w, target_h)

    _progress(progress_callback, 0.2)

    # Target (dari parameter)
    target_ratio = target_w / target_h

    # Hitung crop window di source
    crop_h = src_h
    crop_w = int(crop_h * target_ratio)
    if crop_w > src_w:
        crop_w = src_w
        crop_h = int(crop_w / target_ratio)

    # Detect wajah tiap N frame
    cap = cv2.VideoCapture(str(video_path))
    fps_src = cap.get(cv2.CAP_PROP_FPS) or 30
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    detect_every = max(1, int(fps_src * cfg.detect_interval_1face))

    face_detection = mp.solutions.face_detection.FaceDetection(
        model_selection=1,
        min_detection_confidence=cfg.confidence_threshold,
    )

    # Kumpulkan crop X per frame
    crop_x_per_frame = {}
    center_x = (src_w - crop_w) // 2  # default center
    last_cx  = center_x

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % detect_every == 0:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_detection.process(rgb)

            if results.detections:
                # Ambil wajah terbesar
                best = max(
                    results.detections,
                    key=lambda d: d.location_data.relative_bounding_box.width
                              * d.location_data.relative_bounding_box.height
                )
                bb  = best.location_data.relative_bounding_box
                fx  = int((bb.xmin + bb.width / 2) * src_w)
                # Hitung crop x berdasar posisi wajah
                ideal_x = max(0, min(src_w - crop_w, fx - crop_w // 2))
                # Smooth movement (dead zone)
                if abs(ideal_x - last_cx) > cfg.dead_zone:
                    last_cx = int(last_cx * 0.7 + ideal_x * 0.3)
                crop_x_per_frame[frame_idx] = last_cx
            else:
                crop_x_per_frame[frame_idx] = last_cx
        else:
            crop_x_per_frame[frame_idx] = last_cx

        frame_idx += 1

    cap.release()
    face_detection.close()

    _progress(progress_callback, 0.6)

    # Simpan crop data ke JSON (untuk FFmpeg sendcmd)
    crop_data = {
        "src_w": src_w, "src_h": src_h,
        "crop_w": crop_w, "crop_h": crop_h,
        "fps": fps_src,
        "frames": crop_x_per_frame,
    }
    crop_json = output_path.parent / f"{output_path.stem}_crop.json"
    with open(crop_json, "w") as f:
        json.dump(crop_data, f)

    _progress(progress_callback, 0.7)

    # Buat crop filter yang smooth
    # Karena FFmpeg tidak bisa baca JSON per-frame langsung,
    # kita gunakan pendekatan: temukan crop X yang paling sering muncul
    # lalu buat weighted crop
    if crop_x_per_frame:
        # Pakai median sebagai crop_x tetap (cukup untuk video ceramah statis)
        import statistics
        cx_vals = list(crop_x_per_frame.values())
        median_x = int(statistics.median(cx_vals))
    else:
        median_x = center_x

    crop_y = max(0, (src_h - crop_h) // 2)
    vf = (f"crop={crop_w}:{crop_h}:{median_x}:{crop_y},"
          f"scale={target_w}:{target_h}")

    success = _run_ffmpeg_vf(video_path, output_path, vf)

    # Cleanup
    if crop_json.exists():
        crop_json.unlink()

    return success


# ─── FFmpeg Helper ────────────────────────────────────────────────────────────

def _run_ffmpeg_vf(video_path: Path, output_path: Path, vf: str) -> bool:
    """Jalankan FFmpeg dengan video filter."""
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vf", vf,
        "-c:v", "libx264",
        "-crf", "18",
        "-preset", "fast",
        "-c:a", "copy",
        "-movflags", "+faststart",
        str(output_path),
    ]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True,
            encoding="utf-8", errors="replace"
        )
        if result.returncode != 0:
            log.error("FFmpeg crop error:\n%s", result.stderr[-300:])
            return False
        return True
    except FileNotFoundError:
        raise RuntimeError("FFmpeg tidak ditemukan.")
    except Exception as e:
        log.error("FFmpeg exception: %s", e)
        return False


# ─── Utility ─────────────────────────────────────────────────────────────────

def _get_video_info(video_path: Path) -> Optional[dict]:
    """Ambil info dimensi & FPS video dengan ffprobe."""
    try:
        import json as _json
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json",
             "-show_streams", str(video_path)],
            capture_output=True, text=True
        )
        data = _json.loads(result.stdout)
        for stream in data.get("streams", []):
            if stream.get("codec_type") == "video":
                return {
                    "width":  int(stream.get("width", 0)),
                    "height": int(stream.get("height", 0)),
                    "fps":    eval(stream.get("r_frame_rate", "30/1")),
                }
    except Exception as e:
        log.debug("ffprobe error: %s", e)
    return None


def _is_vertical(w: int, h: int) -> bool:
    """Cek apakah video sudah vertikal (rasio ~9:16)."""
    if h == 0:
        return False
    ratio = w / h
    return ratio < 0.7  # 9/16 = 0.5625


def _check_mediapipe() -> bool:
    try:
        import mediapipe
        import cv2
        return True
    except ImportError:
        return False


def _safe_name(title: str, max_len: int = 50) -> str:
    clean = "".join(c for c in title if c.isalnum() or c in " _-").strip()
    return clean.replace(" ", "_")[:max_len]


def _progress(cb, val: float):
    if cb:
        cb("cropping", val)
