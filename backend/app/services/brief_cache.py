"""File-backed JSON cache for the daily AI Brief.

One file per ET day: backend/data/briefs/YYYY-MM-DD.json. Gitignored.
Generate-on-first-read is fine for v1 — no cron needed yet.
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo

from ..schemas import AiBriefResponse

ET = ZoneInfo("America/New_York")
BRIEF_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "briefs"


def today_et() -> str:
    return datetime.now(ET).date().isoformat()


def _path_for(date: str) -> Path:
    return BRIEF_DIR / f"{date}.json"


def load_today() -> Optional[AiBriefResponse]:
    p = _path_for(today_et())
    if not p.exists():
        return None
    try:
        return AiBriefResponse.model_validate_json(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def save_today(brief: AiBriefResponse) -> None:
    BRIEF_DIR.mkdir(parents=True, exist_ok=True)
    _path_for(today_et()).write_text(
        brief.model_dump_json(indent=2), encoding="utf-8"
    )
