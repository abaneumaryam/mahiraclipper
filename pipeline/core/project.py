"""
MahiraClipper — Project Manager
Handles semua urusan project: buat, load, simpan history, checkpoint system.
"""

import json
import uuid
import shutil
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional
from enum import Enum

from config.settings import PROJECTS_DIR, log


# ─── Enums ────────────────────────────────────────────────────────────────────

class ProjectStatus(str, Enum):
    CREATED     = "created"
    DOWNLOADING = "downloading"
    TRANSCRIBING= "transcribing"
    ANALYZING   = "analyzing"
    CUTTING     = "cutting"
    CROPPING    = "cropping"
    SUBTITLING  = "subtitling"
    DONE        = "done"
    FAILED      = "failed"

class StepStatus(str, Enum):
    PENDING  = "pending"
    RUNNING  = "running"
    DONE     = "done"
    SKIPPED  = "skipped"
    FAILED   = "failed"


# ─── Dataclasses ──────────────────────────────────────────────────────────────

@dataclass
class ClipInfo:
    """Info satu klip hasil analisis AI."""
    id: str
    title: str
    start_time: float          # detik
    end_time: float
    duration: float
    category: str
    viral_score: float
    hook: str
    caption_suggestion: str
    hashtags: list
    reason: str
    start_time_ref: str        # referensi teks dari transkrip
    end_time_ref: str

    # Status processing
    is_cut: bool = False
    is_cropped: bool = False
    is_subtitled: bool = False
    is_approved: bool = True   # bisa di-reject dari preview UI
    is_uploaded: bool = False

    # File paths
    raw_cut_path: Optional[str] = None
    cropped_path: Optional[str] = None
    final_path: Optional[str] = None
    thumbnail_path: Optional[str] = None

    # Caption yang sudah diedit user
    final_title: Optional[str] = None
    final_caption: Optional[str] = None

    def display_title(self) -> str:
        return self.final_title or self.title

    def safe_filename(self) -> str:
        clean = "".join(c for c in self.display_title() if c.isalnum() or c in " _-").strip()
        return clean.replace(" ", "_")[:60]


@dataclass
class PipelineStep:
    name: str
    status: StepStatus = StepStatus.PENDING
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    error: Optional[str] = None

    def start(self):
        self.status = StepStatus.RUNNING
        self.started_at = datetime.now().isoformat()

    def complete(self):
        self.status = StepStatus.DONE
        self.finished_at = datetime.now().isoformat()

    def skip(self):
        self.status = StepStatus.SKIPPED
        self.finished_at = datetime.now().isoformat()

    def fail(self, error: str):
        self.status = StepStatus.FAILED
        self.error = error
        self.finished_at = datetime.now().isoformat()


@dataclass
class Project:
    """Satu project = satu video ceramah."""
    id: str
    name: str
    created_at: str
    updated_at: str
    status: ProjectStatus

    # Source
    source_url: Optional[str] = None
    source_file: Optional[str] = None
    source_platform: str = "unknown"

    # Paths
    folder: Optional[str] = None
    input_video: Optional[str] = None
    transcript_path: Optional[str] = None

    # AI Analysis results
    clips: list = field(default_factory=list)
    video_summary: str = ""
    dominant_theme: str = ""
    speaker_style: str = ""

    # Pipeline steps tracking
    steps: dict = field(default_factory=lambda: {
        "download":   asdict(PipelineStep("download")),
        "transcribe": asdict(PipelineStep("transcribe")),
        "analyze":    asdict(PipelineStep("analyze")),
        "cut":        asdict(PipelineStep("cut")),
        "crop":       asdict(PipelineStep("crop")),
        "subtitle":   asdict(PipelineStep("subtitle")),
    })

    # Config snapshot (untuk reproducibility)
    config_snapshot: dict = field(default_factory=dict)

    def get_folder(self) -> Path:
        return Path(self.folder).resolve() if self.folder else (PROJECTS_DIR / self.id).resolve()

    def get_cuts_folder(self) -> Path:
        return self.get_folder() / "cuts"

    def get_final_folder(self) -> Path:
        return self.get_folder() / "final"

    def get_subs_folder(self) -> Path:
        return self.get_folder() / "subs"

    def get_thumbnails_folder(self) -> Path:
        return self.get_folder() / "thumbnails"

    def approved_clips(self) -> list:
        return [c for c in self.clips if c.get("is_approved", True)]

    def step_is_done(self, step_name: str) -> bool:
        return self.steps.get(step_name, {}).get("status") == StepStatus.DONE

    def to_dict(self) -> dict:
        return asdict(self) if hasattr(self, '__dataclass_fields__') else self.__dict__

    def touch(self):
        self.updated_at = datetime.now().isoformat()


# ─── Project Manager ──────────────────────────────────────────────────────────

class ProjectManager:

    def __init__(self, projects_dir: Path = PROJECTS_DIR):
        self.dir = projects_dir
        self.dir.mkdir(exist_ok=True)

    # ── Create ──────────────────────────────────────────────────────────────

    def create(
        self,
        name: str,
        source_url: Optional[str] = None,
        source_file: Optional[str] = None,
        config_snapshot: Optional[dict] = None,
    ) -> Project:
        """Buat project baru."""
        project_id = uuid.uuid4().hex[:10]
        folder = self.dir / project_id
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "cuts").mkdir(exist_ok=True)
        (folder / "final").mkdir(exist_ok=True)
        (folder / "subs").mkdir(exist_ok=True)
        (folder / "thumbnails").mkdir(exist_ok=True)

        now = datetime.now().isoformat()
        platform = _detect_platform(source_url)

        project = Project(
            id=project_id,
            name=name,
            created_at=now,
            updated_at=now,
            status=ProjectStatus.CREATED,
            source_url=source_url,
            source_file=source_file,
            source_platform=platform,
            folder=str(folder),
            config_snapshot=config_snapshot or {},
        )

        self.save(project)
        log.info("Project dibuat: %s (%s)", name, project_id)
        return project

    # ── Save / Load ─────────────────────────────────────────────────────────

    def save(self, project: Project):
        """Simpan project ke project.json di foldernya."""
        project.touch()
        path = Path(project.folder) / "project.json"
        try:
            data = self._project_to_dict(project)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=True)
        except IOError as e:
            log.error("Gagal simpan project %s: %s", project.id, e)

    def load(self, project_id: str) -> Optional[Project]:
        """Load project dari folder."""
        path = self.dir / project_id / "project.json"
        if not path.exists():
            log.warning("Project tidak ditemukan: %s", project_id)
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return self._dict_to_project(data)
        except (json.JSONDecodeError, IOError) as e:
            log.error("Gagal load project %s: %s", project_id, e)
            return None

    def load_all(self) -> list:
        """Load semua project, diurutkan terbaru dulu."""
        projects = []
        for folder in self.dir.iterdir():
            if folder.is_dir():
                p = self.load(folder.name)
                if p:
                    projects.append(p)
        projects.sort(key=lambda p: p.updated_at, reverse=True)
        return projects

    def delete(self, project_id: str) -> bool:
        """Hapus project beserta semua filenya."""
        folder = self.dir / project_id
        if folder.exists():
            shutil.rmtree(folder)
            log.info("Project dihapus: %s", project_id)
            return True
        return False

    # ── Step Tracking ────────────────────────────────────────────────────────

    def start_step(self, project: Project, step: str):
        if step in project.steps:
            project.steps[step]["status"] = StepStatus.DONE  # mark running
            project.steps[step]["started_at"] = datetime.now().isoformat()
            project.status = ProjectStatus(step + "ing") if (step + "ing") in ProjectStatus._value2member_map_ else project.status
            self.save(project)

    def complete_step(self, project: Project, step: str):
        if step in project.steps:
            project.steps[step]["status"] = StepStatus.DONE
            project.steps[step]["finished_at"] = datetime.now().isoformat()
            self.save(project)
        log.info("[%s] Step '%s' selesai ✓", project.id, step)

    def fail_step(self, project: Project, step: str, error: str):
        if step in project.steps:
            project.steps[step]["status"] = StepStatus.FAILED
            project.steps[step]["error"] = error
            project.steps[step]["finished_at"] = datetime.now().isoformat()
        project.status = ProjectStatus.FAILED
        self.save(project)
        log.error("[%s] Step '%s' GAGAL: %s", project.id, step, error)

    def skip_step(self, project: Project, step: str):
        if step in project.steps:
            project.steps[step]["status"] = StepStatus.SKIPPED
            project.steps[step]["finished_at"] = datetime.now().isoformat()
            self.save(project)
        log.info("[%s] Step '%s' di-skip (sudah ada).", project.id, step)

    # ── Clip Management ──────────────────────────────────────────────────────

    def update_clip(self, project: Project, clip_id: str, updates: dict):
        """Update satu klip (misal: approve/reject, edit caption)."""
        for i, clip in enumerate(project.clips):
            if clip.get("id") == clip_id:
                project.clips[i].update(updates)
                self.save(project)
                return True
        return False

    def get_clip(self, project: Project, clip_id: str) -> Optional[dict]:
        for clip in project.clips:
            if clip.get("id") == clip_id:
                return clip
        return None

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _project_to_dict(self, project: Project) -> dict:
        """Convert project ke dict yang bisa di-JSON-kan."""
        d = {}
        for k, v in project.__dict__.items():
            if isinstance(v, (ProjectStatus, StepStatus)):
                d[k] = v.value
            else:
                d[k] = v
        return d

    def _dict_to_project(self, data: dict) -> Project:
        """Rebuild Project dari dict."""
        data["status"] = ProjectStatus(data.get("status", "created"))
        return Project(**{k: v for k, v in data.items() if k in Project.__dataclass_fields__})

    def summary(self) -> dict:
        """Statistik singkat semua project."""
        all_p = self.load_all()
        return {
            "total": len(all_p),
            "done": sum(1 for p in all_p if p.status == ProjectStatus.DONE),
            "failed": sum(1 for p in all_p if p.status == ProjectStatus.FAILED),
            "total_clips": sum(len(p.clips) for p in all_p),
        }


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _detect_platform(url: Optional[str]) -> str:
    if not url:
        return "local"
    url = url.lower()
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    if "instagram.com" in url:
        return "instagram"
    if "facebook.com" in url or "fb.watch" in url:
        return "facebook"
    if "tiktok.com" in url:
        return "tiktok"
    return "other"
