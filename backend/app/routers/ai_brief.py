from fastapi import APIRouter, Header, HTTPException
from typing import Optional

from ..config import settings
from ..schemas import AiBriefResponse
from ..services.brief_cache import load_today, save_today
from ..services.brief_generator import generate_brief

router = APIRouter(prefix="/api/ai-brief", tags=["ai-brief"])


@router.get("", response_model=AiBriefResponse)
def get_brief() -> AiBriefResponse:
    cached = load_today()
    if cached is not None:
        return cached
    if not settings.ANTHROPIC_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="ANTHROPIC_API_KEY not configured. Add it to backend/.env to enable the AI Brief.",
        )
    try:
        brief = generate_brief()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Brief generation failed: {e}")
    save_today(brief)
    return brief


@router.post("/regenerate", response_model=AiBriefResponse)
def regenerate(x_admin_token: Optional[str] = Header(None)) -> AiBriefResponse:
    if not settings.ADMIN_TOKEN or x_admin_token != settings.ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Bad or missing X-Admin-Token")
    try:
        brief = generate_brief()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Brief generation failed: {e}")
    save_today(brief)
    return brief
