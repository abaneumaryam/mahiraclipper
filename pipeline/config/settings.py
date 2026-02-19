"""
MahiraClipper — Global Configuration
Full Gemini edition — tanpa WhisperX, tanpa GPU.
"""

import os
import json
import logging
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR     = Path(__file__).parent.parent.resolve()
PROJECTS_DIR = BASE_DIR / "projects"
MODELS_DIR   = BASE_DIR / "models"
CONFIG_FILE  = BASE_DIR / "api_config.json"
LOG_FILE     = BASE_DIR / "mahiraclipper.log"

PROJECTS_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

# ─── Logging ──────────────────────────────────────────────────────────────────
def setup_logging(verbose: bool = False):
    level = logging.DEBUG if verbose else logging.INFO
    # BUG FIX: JANGAN pakai StreamHandler — akan korup JSON stream ke Electron!
    # Hanya tulis ke file log saja.
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            # logging.StreamHandler(),  ← DIHAPUS! korupsi stdout JSON
        ],
    )

log = logging.getLogger("mahira")

# ─── Dataclasses ──────────────────────────────────────────────────────────────

@dataclass
class GeminiConfig:
    api_key: str             = ""
    model: str               = "gemini-1.5-flash"
    temperature: float       = 0.4
    max_output_tokens: int   = 8192

@dataclass
class GroqConfig:
    api_key: str             = ""
    model: str               = "llama-3.3-70b-versatile"

@dataclass
class WhisperConfig:
    model_size: str          = "small"   # tiny/base/small/medium/large-v3/turbo
    language: str            = "id"      # id=Indonesia, auto=detect otomatis
    device: str              = "cpu"     # cpu (GPU tidak diperlukan)
    compute_type: str        = "int8"    # int8 = lebih cepat di CPU

@dataclass
class ClipConfig:
    min_duration: int        = 30
    max_duration: int        = 90
    num_clips: int           = 5
    overlap_tolerance: float = 2.0

@dataclass
class FaceConfig:
    model: str                   = "mediapipe"
    mode: str                    = "auto"
    no_face_mode: str            = "zoom"
    detect_interval_1face: float = 0.17
    detect_interval_2face: float = 1.0
    filter_threshold: float      = 0.35
    two_face_threshold: float    = 0.60
    confidence_threshold: float  = 0.30
    dead_zone: float             = 40.0

@dataclass
class SubtitleConfig:
    style_key: str           = "hormozi_hijau"
    auto_select: bool        = True
    font: str                = "Montserrat-Regular"
    base_size: int           = 70
    highlight_size: int      = 84
    base_color: str          = "&H00FFFFFF&"
    highlight_color: str     = "&H0033CC00&"
    words_per_block: int     = 3
    gap_limit: float         = 0.5
    mode: str                = "highlight"
    vertical_position: int   = 120
    alignment: int           = 2
    bold: int                = 1
    italic: int              = 0
    border_style: int        = 1
    outline_thickness: float = 2.5
    outline_color: str       = "&HFF000000&"
    shadow_size: int         = 2
    shadow_color: str        = "&H00000000&"
    remove_punctuation: bool = True

@dataclass
class UploadConfig:
    tiktok_enabled: bool             = False
    youtube_enabled: bool            = False
    instagram_enabled: bool          = False
    tiktok_session_id: str           = ""
    youtube_client_secret_path: str  = ""

@dataclass
class AppConfig:
    gemini:   GeminiConfig   = field(default_factory=GeminiConfig)
    groq:     GroqConfig     = field(default_factory=GroqConfig)
    whisper:  WhisperConfig  = field(default_factory=WhisperConfig)
    clip:     ClipConfig     = field(default_factory=ClipConfig)
    face:     FaceConfig     = field(default_factory=FaceConfig)
    subtitle: SubtitleConfig = field(default_factory=SubtitleConfig)
    upload:   UploadConfig   = field(default_factory=UploadConfig)
    video_quality: str       = "best"
    translate_target: Optional[str] = None
    verbose: bool            = False

    def to_dict(self) -> dict:
        return asdict(self)


# ─── Loader ───────────────────────────────────────────────────────────────────

def load_config(config_path: Optional[Path] = None) -> AppConfig:
    cfg  = AppConfig()
    path = config_path or CONFIG_FILE

    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            _apply_json(cfg, data)
        except (json.JSONDecodeError, IOError) as e:
            log.warning("Gagal baca config: %s — pakai default.", e)

    _apply_env(cfg)
    return cfg


def save_config(cfg: AppConfig, path: Optional[Path] = None):
    target = path or CONFIG_FILE
    try:
        with open(target, "w", encoding="utf-8") as f:
            # BUG FIX: ensure_ascii=True agar aman di semua OS
            json.dump(cfg.to_dict(), f, indent=4, ensure_ascii=True)
    except IOError as e:
        log.error("Gagal simpan config: %s", e)


def _apply_json(cfg: AppConfig, data: dict):
    g = data.get("gemini", {})
    if g.get("api_key"):    cfg.gemini.api_key = g["api_key"]
    if g.get("model"):      cfg.gemini.model   = g["model"]

    c = data.get("clip", {})
    if c.get("min_duration"): cfg.clip.min_duration = int(c["min_duration"])
    if c.get("max_duration"): cfg.clip.max_duration = int(c["max_duration"])
    if c.get("num_clips"):    cfg.clip.num_clips    = int(c["num_clips"])

    f = data.get("face", {})
    if f.get("model"):        cfg.face.model        = f["model"]
    if f.get("mode"):         cfg.face.mode         = f["mode"]
    if f.get("no_face_mode"): cfg.face.no_face_mode = f["no_face_mode"]

    s = data.get("subtitle", {})
    if s.get("style_key"):    cfg.subtitle.style_key   = s["style_key"]
    if "auto_select" in s:    cfg.subtitle.auto_select = bool(s["auto_select"])

    gr = data.get("groq", {})
    if gr.get("api_key"):  cfg.groq.api_key = gr["api_key"]
    if gr.get("model"):    cfg.groq.model   = gr["model"]

    wh = data.get("whisper", {})
    if wh.get("model_size"):  cfg.whisper.model_size  = wh["model_size"]
    if wh.get("language"):    cfg.whisper.language    = wh["language"]

    u = data.get("upload", {})
    if u.get("tiktok_session_id"):
        cfg.upload.tiktok_session_id = u["tiktok_session_id"]

    if data.get("video_quality"):    cfg.video_quality    = data["video_quality"]
    if data.get("translate_target"): cfg.translate_target = data["translate_target"]


def _apply_env(cfg: AppConfig):
    if os.getenv("MAHIRA_GEMINI_KEY"):   cfg.gemini.api_key = os.environ["MAHIRA_GEMINI_KEY"]
    if os.getenv("MAHIRA_GEMINI_MODEL"): cfg.gemini.model   = os.environ["MAHIRA_GEMINI_MODEL"]
    if os.getenv("MAHIRA_SUBTITLE_STYLE"):
        cfg.subtitle.style_key   = os.environ["MAHIRA_SUBTITLE_STYLE"]
        cfg.subtitle.auto_select = False
    if os.getenv("MAHIRA_GROQ_KEY"):    cfg.groq.api_key       = os.environ["MAHIRA_GROQ_KEY"]
    if os.getenv("MAHIRA_WHISPER_MODEL"): cfg.whisper.model_size = os.environ["MAHIRA_WHISPER_MODEL"]
    if os.getenv("MAHIRA_VERBOSE", "").lower() in ("1","true","yes"):
        cfg.verbose = True
