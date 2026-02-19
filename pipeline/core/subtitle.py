"""
MahiraClipper — Subtitle Engine
Buat file ASS dari transkrip Gemini lalu burn ke video pakai FFmpeg.
Support semua 22 style dari subtitle_styles.py.

Alur:
  1. Ambil transkrip segments dari Gemini (sudah ada timestamps)
  2. Build file .ass dengan style yang dipilih
  3. Burn subtitle ke video dengan FFmpeg (hardcoded, jalan di semua device)
"""

import re
import subprocess
from pathlib import Path
from typing import Optional, Callable

from config.settings import log
from core.subtitle_styles import get_style, recommend_styles, STYLES


# ─── Main: Generate + Burn ────────────────────────────────────────────────────

def process_subtitles(
    clip: dict,
    transcript_segments: list,
    video_path: Path,
    output_path: Path,
    style_key: Optional[str] = None,
    font_size_override: Optional[int] = None,
    v_position: Optional[str] = None,  # "bottom" | "middle" | "top"
    progress_callback: Optional[Callable[[str, float], None]] = None,
) -> dict:
    """
    Pipeline lengkap: transkrip → ASS → burn ke video.

    Args:
        clip: dict klip dari project (berisi category, title, start_time, end_time)
        transcript_segments: list segment dari Gemini [{start, end, text}]
        video_path: path video yang sudah di-cut (dari cutter.py)
        output_path: path output video final dengan subtitle
        style_key: key dari STYLES dict, None = auto-recommend berdasar category

    Returns:
        dict update untuk clip: {final_path, is_subtitled, style_used}
    """
    # Pilih style
    if not style_key:
        style_key = _auto_select_style(clip.get("category", "knowledge"))
    
    try:
        style = get_style(style_key)
    except ValueError:
        log.warning("Style '%s' tidak ditemukan, pakai default.", style_key)
        style_key = "hormozi_hijau"
        style = get_style(style_key)

    style = dict(style)  # copy agar tidak mutate original

    # Deteksi resolusi video aktual untuk sizing yang tepat
    video_info = _get_video_dimensions(video_path)
    vid_w = video_info.get("width",  1080)
    vid_h = video_info.get("height", 1920)

    # Base font size ideal = 6.5% dari tinggi video
    # 9:16 (1920px) → 70px  |  1:1 (1080px) → 55px  |  16:9 (1080px tall) → 55px
    ideal_base = max(40, round(vid_h * 0.065 / 2) * 2)
    ideal_hl   = round(ideal_base * 1.2 / 2) * 2

    if font_size_override and font_size_override > 0:
        # User manual override
        style["base_size"]      = font_size_override
        style["highlight_size"] = round(font_size_override * 1.2 / 2) * 2
    else:
        # Auto berdasar resolusi
        style["base_size"]      = ideal_base
        style["highlight_size"] = ideal_hl

    # Posisi vertikal berdasar pilihan user
    # Dalam ASS: MarginV = jarak dari tepi (bottom kalau alignment=2)
    # 9:16 (1920px): bottom=120, middle=960, top=1700
    if v_position == "top":
        style["vertical_position"] = round(vid_h * 0.85)
        style["alignment"] = 2   # tetap alignment bawah tapi margin besar = naiknya ke atas
    elif v_position == "middle":
        style["vertical_position"] = round(vid_h * 0.45)
    else:
        # bottom (default) — 6% dari bawah
        style["vertical_position"] = round(vid_h * 0.06)

    # Update PlayRes sesuai resolusi aktual
    style["play_res_x"] = vid_w
    style["play_res_y"] = vid_h

    log.info("Subtitle: style=%s size=%s pos=%s res=%dx%d",
             style_key, style["base_size"], v_position or "bottom", vid_w, vid_h)

    _progress(progress_callback, 0.1)

    # Filter transkrip hanya untuk durasi klip ini
    clip_start = clip.get("start_time", 0)
    clip_end   = clip.get("end_time", clip_start + clip.get("duration", 60))
    clip_segs  = _filter_segments(transcript_segments, clip_start, clip_end)

    if not clip_segs:
        log.warning("Tidak ada transkrip untuk klip '%s', skip subtitle.", clip.get("title",""))
        return {"final_path": str(video_path), "is_subtitled": False, "style_used": None}

    _progress(progress_callback, 0.2)

    # Build ASS file
    ass_path = output_path.parent / f"{output_path.stem}.ass"
    _build_ass_file(clip_segs, style, ass_path, time_offset=clip_start)

    _progress(progress_callback, 0.5)

    # Burn ke video
    success = _burn_subtitles(video_path, ass_path, output_path)

    _progress(progress_callback, 1.0)

    if success:
        log.info("Subtitle di-burn ke: %s", output_path.name)
        return {
            "final_path": str(output_path),
            "is_subtitled": True,
            "style_used": style_key,
        }
    else:
        # Fallback: copy video tanpa subtitle
        import shutil
        shutil.copy2(video_path, output_path)
        return {
            "final_path": str(output_path),
            "is_subtitled": False,
            "style_used": None,
        }


# ─── Batch Process Semua Klip ─────────────────────────────────────────────────

def process_all_clips(
    clips: list,
    transcript_data: dict,
    cuts_folder: Path,
    final_folder: Path,
    style_key: Optional[str] = None,
    font_size_override: Optional[int] = None,
    v_position: Optional[str] = None,
    progress_callback: Optional[Callable[[str, float], None]] = None,
) -> list:
    """
    Proses subtitle untuk semua klip yang sudah di-cut.

    Args:
        clips: list clip dicts dari project
        transcript_data: dict dari gemini_processor {language, segments, full_text}
        cuts_folder: folder berisi raw cuts
        final_folder: folder output video final dengan subtitle
        style_key: style untuk semua klip, None = auto per klip
    """
    final_folder.mkdir(parents=True, exist_ok=True)
    transcript_segments = transcript_data.get("segments", [])

    approved = [c for c in clips if c.get("is_approved", True) and c.get("is_cut", False)]
    total = len(approved)

    if total == 0:
        log.warning("Tidak ada klip yang siap untuk diproses subtitle-nya.")
        return clips

    log.info("Memproses subtitle untuk %d klip...", total)
    results = list(clips)
    done = 0

    for i, clip in enumerate(results):
        if not clip.get("is_approved", True) or not clip.get("is_cut", False):
            continue

        raw_cut = clip.get("raw_cut_path")
        if not raw_cut or not Path(raw_cut).exists():
            log.warning("File cut tidak ditemukan untuk: %s", clip.get("title",""))
            continue

        safe = _safe_name(clip.get("title", f"clip_{i}"))
        filename   = f"{i:03d}_{safe}"
        output_mp4 = final_folder / f"{filename}_final.mp4"

        # Skip kalau sudah ada
        if output_mp4.exists() and output_mp4.stat().st_size > 10000:
            log.info("Skip subtitle (sudah ada): %s", output_mp4.name)
            results[i]["final_path"]    = str(output_mp4)
            results[i]["is_subtitled"]  = True
            done += 1
            continue

        # Pilih style — per klip atau global
        clip_style = style_key or _auto_select_style(clip.get("category", "knowledge"))

        def cb(step, pct):
            overall = (done + pct) / total
            if progress_callback:
                progress_callback("subtitling", overall)

        update = process_subtitles(
            clip=clip,
            transcript_segments=transcript_segments,
            video_path=Path(raw_cut),
            output_path=output_mp4,
            style_key=clip_style,
            progress_callback=cb,
        )

        results[i].update(update)
        done += 1
        log.info("[%d/%d] Subtitle selesai: %s (style: %s)",
                 done, total, filename, clip_style)

    return results


# ─── ASS File Builder ─────────────────────────────────────────────────────────

def _build_ass_file(
    segments: list,
    style: dict,
    output_path: Path,
    time_offset: float = 0.0,
) -> Path:
    """
    Build file ASS subtitle dari segments dengan style yang diberikan.
    """
    mode = style.get("mode", "highlight")

    if mode == "word_by_word":
        events = _build_word_by_word_events(segments, style, time_offset)
    elif mode == "no_highlight":
        events = _build_no_highlight_events(segments, style, time_offset)
    else:
        events = _build_highlight_events(segments, style, time_offset)

    ass_content = _build_ass_header(style) + "\n".join(events)

    with open(output_path, "w", encoding="utf-8-sig") as f:
        f.write(ass_content)

    return output_path


def _build_ass_header(style: dict) -> str:
    """Buat header ASS dengan style parameters."""
    font       = style.get("font", "Montserrat-Regular")
    base_size  = style.get("base_size", 70)
    base_color = style.get("base_color", "&H00FFFFFF&")
    outline_c  = style.get("outline_color", "&HFF000000&")
    shadow_c   = style.get("shadow_color",  "&H00000000&")
    bold       = style.get("bold", 1)
    italic     = style.get("italic", 0)
    underline  = style.get("underline", 0)
    border     = style.get("border_style", 1)
    outline_t  = style.get("outline_thickness", 2.0)
    shadow_s   = style.get("shadow_size", 2)
    v_pos      = style.get("vertical_position", 120)
    alignment  = style.get("alignment", 2)

    play_x = style.get("play_res_x", 1080)
    play_y = style.get("play_res_y", 1920)

    return f"""[Script Info]
ScriptType: v4.00+
PlayResX: {play_x}
PlayResY: {play_y}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font},{base_size},{base_color},&H000000FF&,{outline_c},{shadow_c},{bold},{italic},{underline},0,100,100,0,0,{border},{outline_t},{shadow_s},{alignment},10,10,{v_pos},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def _build_highlight_events(segments: list, style: dict, time_offset: float) -> list:
    """
    Mode highlight: tampilkan N kata per block, highlight kata aktif.
    """
    words_per_block = style.get("words_per_block", 3)
    hl_color        = style.get("highlight_color", "&H0000FF00&")
    hl_size         = style.get("highlight_size", 84)
    base_size       = style.get("base_size", 28)
    gap_limit       = style.get("gap_limit", 0.5)
    rm_punct        = style.get("remove_punctuation", True)

    # Flatten semua kata dengan timestamps
    all_words = _segments_to_words(segments, time_offset, rm_punct)
    if not all_words:
        return []

    events = []
    blocks = [all_words[i:i+words_per_block]
              for i in range(0, len(all_words), words_per_block)]

    for block in blocks:
        if not block:
            continue

        block_start = block[0]["start"]
        block_end   = block[-1]["end"]

        # Satu event per kata (kata aktif = highlight)
        for wi, word_data in enumerate(block):
            w_start = word_data["start"]
            w_end   = word_data["end"]

            # Build teks: kata sebelum dan sesudah = default, kata ini = highlight
            parts = []
            for j, wd in enumerate(block):
                txt = wd["word"]
                if j == wi:
                    parts.append(
                        f"{{\\c{_ass_color(hl_color)}\\fs{hl_size}}}{txt}"
                        f"{{\\c{_ass_color(style.get('base_color','&H00FFFFFF&'))}\\fs{base_size}}}"
                    )
                else:
                    parts.append(txt)

            line = " ".join(parts)
            events.append(
                f"Dialogue: 0,{_ts(w_start)},{_ts(w_end)},Default,,0,0,0,,{line}"
            )

    return events


def _build_word_by_word_events(segments: list, style: dict, time_offset: float) -> list:
    """
    Mode word_by_word: satu kata muncul satu-satu, ukuran besar.
    """
    hl_color  = style.get("highlight_color", "&H0000FF00&")
    hl_size   = style.get("highlight_size", 84)
    rm_punct  = style.get("remove_punctuation", True)

    all_words = _segments_to_words(segments, time_offset, rm_punct)
    events    = []

    for wd in all_words:
        line = f"{{\\c{_ass_color(hl_color)}\\fs{hl_size}}}{wd['word']}"
        events.append(
            f"Dialogue: 0,{_ts(wd['start'])},{_ts(wd['end'])},Default,,0,0,0,,{line}"
        )

    return events


def _build_no_highlight_events(segments: list, style: dict, time_offset: float) -> list:
    """
    Mode no_highlight: tampilkan teks per block, semua warna sama.
    """
    words_per_block = style.get("words_per_block", 5)
    rm_punct        = style.get("remove_punctuation", False)

    all_words = _segments_to_words(segments, time_offset, rm_punct)
    events    = []
    blocks    = [all_words[i:i+words_per_block]
                 for i in range(0, len(all_words), words_per_block)]

    for block in blocks:
        if not block:
            continue
        text  = " ".join(w["word"] for w in block)
        start = block[0]["start"]
        end   = block[-1]["end"]
        events.append(
            f"Dialogue: 0,{_ts(start)},{_ts(end)},Default,,0,0,0,,{text}"
        )

    return events


# ─── FFmpeg Burn ──────────────────────────────────────────────────────────────

def _burn_subtitles(video_path: Path, ass_path: Path, output_path: Path) -> bool:
    """Burn ASS subtitle ke video menggunakan FFmpeg."""
    # BUG FIX: Windows path escaping untuk FFmpeg ASS filter
    # Benar: C:/path → C\:/path  (hanya colon drive letter yang di-escape)
    # Salah: replace semua : termasuk drive letter → double escape
    import re as _re
    p = str(ass_path).replace("\\", "/")
    ass_str = _re.sub(r'^([A-Za-z]):', lambda m: m.group(1) + '\\:', p)

    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vf", f"ass='{ass_str}'",
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
            log.error("FFmpeg burn subtitle error:\n%s", result.stderr[-400:])
            return False
        return True
    except FileNotFoundError:
        raise RuntimeError("FFmpeg tidak ditemukan.")
    except Exception as e:
        log.error("FFmpeg exception: %s", e)
        return False


# ─── Segment Helpers ──────────────────────────────────────────────────────────

def _filter_segments(
    all_segments: list,
    clip_start: float,
    clip_end: float,
    tolerance: float = 1.0,
) -> list:
    """Filter segments yang masuk ke dalam range waktu klip."""
    result = []
    for seg in all_segments:
        s = seg.get("start", 0)
        e = seg.get("end", 0)
        # Segment overlap dengan window klip
        if s < clip_end + tolerance and e > clip_start - tolerance:
            result.append(seg)
    return result


def _segments_to_words(
    segments: list,
    time_offset: float,
    remove_punctuation: bool,
) -> list:
    """
    Ubah list segments ke list kata dengan timestamps individual.
    Kalau Gemini tidak kasih word-level timestamps, distribusi merata per segment.
    """
    all_words = []

    for seg in segments:
        seg_start = max(0, seg.get("start", 0) - time_offset)
        seg_end   = max(0, seg.get("end",   0) - time_offset)
        text      = seg.get("text", "").strip()

        if not text:
            continue

        if remove_punctuation:
            text = re.sub(r'[،,\.؟?!،؛;:\'"()\[\]]', '', text)

        words = text.split()
        if not words:
            continue

        # Kalau ada word-level timing dari Whisper
        # Format Whisper: [{"word": "Allah", "start": 1.2, "end": 1.5, ...}]
        word_timestamps = seg.get("words", [])
        if word_timestamps:
            for wt in word_timestamps:
                w = wt.get("word", "").strip()
                if not w:
                    continue
                if remove_punctuation:
                    w = re.sub(r'[،,\.؟?!،؛;:\'"()\[\]]', '', w)
                if not w:
                    continue
                all_words.append({
                    "word":  w,
                    "start": max(0, wt.get("start", seg_start) - time_offset),
                    "end":   max(0, wt.get("end",   seg_end)   - time_offset),
                })
        else:
            # Fallback: distribusi merata per kata (kalau word timestamps tidak ada)
            dur   = max(0.01, seg_end - seg_start)
            w_dur = dur / max(len(words), 1)
            for wi, word in enumerate(words):
                all_words.append({
                    "word":  word,
                    "start": seg_start + wi * w_dur,
                    "end":   seg_start + (wi + 1) * w_dur,
                })

    return all_words


# ─── Auto Style Selection ─────────────────────────────────────────────────────

def _auto_select_style(category: str) -> str:
    """Pilih style terbaik secara otomatis berdasarkan kategori klip."""
    DEFAULTS = {
        "knowledge":    "hormozi_hijau",
        "viral_quote":  "hormozi_kuning",
        "emotional":    "soft_dakwah",
        "quran_hadith": "arabic_style",
        "beginner":     "minimalis_putih",
    }
    return DEFAULTS.get(category, "hormozi_hijau")


# ─── ASS Format Helpers ───────────────────────────────────────────────────────

def _ts(seconds: float) -> str:
    """Convert detik ke format timestamp ASS: H:MM:SS.cc"""
    seconds = max(0, seconds)
    h  = int(seconds // 3600)
    m  = int((seconds % 3600) // 60)
    s  = int(seconds % 60)
    cs = int((seconds % 1) * 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def _ass_color(color_str: str) -> str:
    """Ekstrak kode warna dari format ASS &HAABBGGRR& → &HBBGGRR&"""
    clean = color_str.strip("&H").strip("&")
    if len(clean) == 8:
        return f"&H{clean[2:]}&"
    return f"&H{clean}&"


def _safe_name(title: str, max_len: int = 50) -> str:
    clean = "".join(c for c in title if c.isalnum() or c in " _-").strip()
    return clean.replace(" ", "_")[:max_len]


def _progress(cb, val: float):
    if cb:
        cb("subtitling", val)
