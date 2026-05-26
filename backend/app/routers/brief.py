from fastapi import APIRouter

from ..schemas import BriefResponse
from ..services.macro_service import get_brief

router = APIRouter(prefix="/api/brief", tags=["brief"])


@router.get("", response_model=BriefResponse)
def brief() -> BriefResponse:
    return BriefResponse(**get_brief())
