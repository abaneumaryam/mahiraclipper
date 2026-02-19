#!/usr/bin/env python3
"""
MahiraClipper — Pipeline Runner v2
Arsitektur baru: Whisper (lokal) + Groq (gratis 14k/hari) — tanpa Gemini!

Alur:
  1. Download / pakai file lokal
  2. Faster-Whisper → transkripsi lokal (offline, unlimited)
  3. Groq LLaMA 3.3 70B → analisis momen viral (14.400 req/hari gratis)
  4. FFmpeg → potong klip
  5. MediaPipe → face tracking crop (opsional)
  6. FFmpeg → burn subtitle
"""

import json
import sys
import os
from pathlib import Path

# ── WAJIB: Paksa UTF-8 di Windows ──────────────────────────────────────────
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering=True)
sys.stdin  = io.TextIOWrapper(sys.stdin.buffer,  encoding='utf-8')

BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))

def emit(event: str, data: dict):
    payload = json.dumps({"event": event, **data}, ensure_ascii=True)
    print(payload, flush=True)

def emit_log(msg: str, level: str = "info"):
    emit("log", {"msg": msg, "level": level})

def emit_progress(step: str, pct: float):
    emit("progress", {"step": step, "pct": round(pct * 100)})

def emit_clips(clips: list):
    emit("clips", {"clips": clips})

def emit_done(project_id: str, final_folder: str, clips: list):
    emit("done", {"project_id": project_id, "final_folder": final_folder, "clips": clips})

def emit_error(msg: str):
    emit("error", {"msg": msg})


def run(cfg: dict):
    from config.settings import load_config, ClipConfig, FaceConfig
    from core.project import ProjectManager
    from core.downloader import download, use_local_file
    from core.whisper_transcriber import transcribe as whisper_transcribe
    from core.groq_analyzer import analyze as groq_analyze
    from core.cutter import cut_clips
    from core.face_crop import crop_all_clips
    from core.subtitle import process_all_clips as subtitle_all_clips

    app_cfg = load_config((BASE / "../api_config.json").resolve())

    # ── API Keys ─────────────────────────────────────────────────────────
    groq_key = cfg.get("groq_api_key") or app_cfg.groq.api_key
    if not groq_key:
        emit_error(
            "Groq API key belum diisi!\n"
            "Buka Settings → isi Groq API Key.\n"
            "Daftar GRATIS di: https://console.groq.com"
        )
        return

    app_cfg.groq.api_key    = groq_key
    app_cfg.groq.model      = cfg.get("groq_model", app_cfg.groq.model)
    app_cfg.whisper.model_size = cfg.get("whisper_model", app_cfg.whisper.model_size)
    app_cfg.whisper.language   = cfg.get("whisper_lang", app_cfg.whisper.language)

    app_cfg.clip = ClipConfig(
        min_duration = int(cfg.get("min_dur", 30)),
        max_duration = int(cfg.get("max_dur", 90)),
        num_clips    = int(cfg.get("num_clips", 5)),
    )

    url        = (cfg.get("url") or "").strip()
    file_path  = (cfg.get("file") or "").strip().strip('"').strip("'")
    style_key  = cfg.get("style_key") or None
    font_size  = int(cfg.get("font_size", 0))  # 0 = auto by resolution
    v_position = cfg.get("v_position", "bottom")  # bottom | middle | top
    do_crop    = bool(cfg.get("do_crop", True))
    crop_mode  = cfg.get("crop_mode", "auto")
    output_w   = int(cfg.get("output_w", 1080))
    output_h   = int(cfg.get("output_h", 1920))
    if output_w > output_h:
        do_crop = False   # 16:9 tidak perlu crop ke vertikal

    pm = ProjectManager(projects_dir=(BASE / "../projects").resolve())

    # Nama project: dari user input > nama file > nama dari URL
    custom_name = (cfg.get("project_name") or "").strip()
    if custom_name:
        name = custom_name[:60]
    elif file_path:
        name = Path(file_path).stem[:40]
    else:
        slug = url.split("?")[0].rstrip("/").split("/")[-1]
        name = (slug or "ceramah")[:40]

    project = pm.create(name=name, source_url=url or None,
                        source_file=file_path or None, config_snapshot={})
    pid    = project.id
    folder = project.get_folder()

    emit("project_created", {"project_id": pid, "name": project.name})
    emit_log("Format output: " + str(output_w) + "x" + str(output_h))
    emit_log("Transkripsi: Whisper " + app_cfg.whisper.model_size + " (lokal)")
    emit_log("Analisis: Groq " + app_cfg.groq.model)

    # ── STEP 1: Download ──────────────────────────────────────────────────
    emit_log("Mengambil video...")
    emit_progress("download", 0.05)
    pm.start_step(project, "download")

    try:
        if file_path:
            info = use_local_file(Path(file_path), folder)
        else:
            info = download(
                url=url, output_folder=folder, quality="best",
                download_subtitles=False,
                progress_callback=lambda s, p: emit_progress("download", p * 0.9),
            )
        project.input_video = info["video_path"]
        project.name = project.name or info.get("title", project.name)
        pm.complete_step(project, "download")
        pm.save(project)
        emit_log("Video siap: " + Path(project.input_video).name)
        emit_progress("download", 1.0)
    except Exception as e:
        pm.fail_step(project, "download", str(e))
        emit_error("Download gagal: " + str(e))
        return

    # ── STEP 2: Transkripsi Whisper (lokal) ───────────────────────────────
    emit_log("Transkripsi lokal dengan Whisper " + app_cfg.whisper.model_size + "...")
    emit_log("(Pertama kali: download model ~500MB, tunggu sebentar)")
    emit_progress("gemini", 0.05)
    pm.start_step(project, "transcribe")

    try:
        def whisper_cb(step, pct):
            emit_progress("gemini", pct * 0.5)   # Whisper = 50% dari step gemini

        transcript = whisper_transcribe(
            video_path=Path(project.input_video),
            project_folder=folder,
            model_size=app_cfg.whisper.model_size,
            language=app_cfg.whisper.language,
            progress_callback=whisper_cb,
        )
        project.transcript_path = transcript["transcript_path"]
        pm.complete_step(project, "transcribe")
        pm.save(project)

        seg_count = len(transcript.get("segments", []))
        emit_log("Transkripsi selesai: " + str(seg_count) + " segmen, bahasa=" + transcript.get("language", "?"))
        emit_progress("gemini", 0.50)

    except Exception as e:
        pm.fail_step(project, "transcribe", str(e))
        emit_error("Transkripsi Whisper gagal: " + str(e))
        return

    # ── STEP 2b: Analisis Groq (deteksi momen) ────────────────────────────
    emit_log("Groq AI - Analisis momen viral...")
    pm.start_step(project, "analyze")

    try:
        def groq_cb(step, pct):
            emit_progress("gemini", 0.50 + pct * 0.50)   # Groq = 50% sisanya

        analysis = groq_analyze(
            transcript=transcript,
            clip_config=app_cfg.clip,
            groq_api_key=groq_key,
            progress_callback=groq_cb,
        )
        project.clips          = analysis["segments"]
        project.video_summary  = analysis.get("video_summary", "")
        project.dominant_theme = analysis.get("dominant_theme", "")
        project.speaker_style  = analysis.get("speaker_style", "")
        pm.complete_step(project, "analyze")
        pm.save(project)

        clip_count = len(project.clips)
        emit_log(str(clip_count) + " momen ditemukan | Tema: " + project.dominant_theme)
        emit_clips(project.clips)
        emit_progress("gemini", 1.0)

    except Exception as e:
        pm.fail_step(project, "analyze", str(e))
        emit_error("Analisis Groq gagal: " + str(e))
        return

    # ── STEP 3: Cut ───────────────────────────────────────────────────────
    emit_log("Memotong klip...")
    emit_progress("cut", 0.05)
    pm.start_step(project, "cut")

    try:
        td = {}
        tp = project.transcript_path
        if tp and Path(tp).exists():
            with open(tp, encoding="utf-8") as f:
                td = json.load(f)

        updated = cut_clips(
            video_path=Path(project.input_video),
            segments=project.clips,
            output_folder=project.get_cuts_folder(),
            transcript_data=td,
            skip_existing=True,
            progress_callback=lambda s, p: emit_progress("cut", p),
        )
        project.clips = updated
        cut_n = sum(1 for c in updated if c.get("is_cut"))
        pm.complete_step(project, "cut")
        pm.save(project)
        emit_log(str(cut_n) + " klip berhasil dipotong")
        emit_clips(project.clips)
        emit_progress("cut", 1.0)
    except Exception as e:
        pm.fail_step(project, "cut", str(e))
        emit_error("Cut gagal: " + str(e))
        return

    # ── STEP 4: Crop ──────────────────────────────────────────────────────
    if do_crop:
        emit_log("Crop ke " + str(output_w) + "x" + str(output_h) + " (" + crop_mode + ")...")
        emit_progress("crop", 0.05)
        pm.start_step(project, "crop")
        try:
            face_cfg = FaceConfig(mode=crop_mode)
            updated  = crop_all_clips(
                clips=project.clips,
                cuts_folder=project.get_cuts_folder(),
                cropped_folder=(folder / "cropped").resolve(),
                config=face_cfg,
                progress_callback=lambda s, p: emit_progress("crop", p),
                target_w=output_w,
                target_h=output_h,
            )
            project.clips = updated
            pm.complete_step(project, "crop")
            pm.save(project)
            emit_log("Crop selesai")
            emit_progress("crop", 1.0)
        except Exception as e:
            emit_log("Crop gagal (" + str(e) + "), lanjut tanpa crop", "warn")
            for i, c in enumerate(project.clips):
                if not c.get("cropped_path"):
                    project.clips[i]["cropped_path"] = c.get("raw_cut_path")
    else:
        for i, c in enumerate(project.clips):
            if not c.get("cropped_path"):
                project.clips[i]["cropped_path"] = c.get("raw_cut_path")
        emit_log("Crop di-skip")

    # ── STEP 5: Subtitle ──────────────────────────────────────────────────
    emit_log("Burn subtitle...")
    emit_progress("subtitle", 0.05)
    pm.start_step(project, "subtitle")

    try:
        td = {}
        tp = project.transcript_path
        if tp and Path(tp).exists():
            with open(tp, encoding="utf-8") as f:
                td = json.load(f)

        clips_src = []
        for c in project.clips:
            c2  = dict(c)
            src = c.get("cropped_path") or c.get("raw_cut_path")
            if src:
                c2["raw_cut_path"] = src
                c2["is_cut"]       = True
            clips_src.append(c2)

        updated = subtitle_all_clips(
            clips=clips_src,
            transcript_data=td,
            cuts_folder=project.get_cuts_folder(),
            final_folder=project.get_final_folder(),
            style_key=style_key,
            font_size_override=font_size if font_size > 0 else None,
            v_position=v_position,
            progress_callback=lambda s, p: emit_progress("subtitle", p),
        )
        project.clips = updated
        sub_n = sum(1 for c in updated if c.get("is_subtitled"))
        pm.complete_step(project, "subtitle")
        pm.save(project)
        emit_log(str(sub_n) + " klip final dengan subtitle")
        emit_progress("subtitle", 1.0)
    except Exception as e:
        pm.fail_step(project, "subtitle", str(e))
        emit_log("Subtitle gagal: " + str(e), "warn")

    emit_done(pid, str(project.get_final_folder()), project.clips)


if __name__ == "__main__":
    try:
        raw = sys.stdin.readline()
        cfg = json.loads(raw)
        run(cfg)
    except json.JSONDecodeError as e:
        emit_error("Config JSON invalid: " + str(e))
    except Exception as e:
        emit_error("Pipeline crash: " + str(e))
