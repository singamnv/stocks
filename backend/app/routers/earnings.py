from fastapi import APIRouter, Query

from .. import ecosystems
from ..config import settings
from ..schemas import EarningsItem, EarningsResponse
from ..services.finnhub_service import get_earnings
from ..services.yf_service import get_grid

router = APIRouter(prefix="/api/earnings", tags=["earnings"])


@router.get("", response_model=EarningsResponse)
def list_earnings(ecosystem: str = Query(ecosystems.DEFAULT_KEY)) -> EarningsResponse:
    if not settings.FINNHUB_API_KEY:
        return EarningsResponse(items=[], warning="FINNHUB_API_KEY not configured")

    eco = ecosystems.get(ecosystem)
    items = get_earnings(eco.KEY)
    grid = {q["symbol"]: q.get("name") for q in get_grid(eco.KEY)}
    out: list[EarningsItem] = []
    for it in items:
        out.append(EarningsItem(
            date=it["date"],
            ticker=it["ticker"],
            name=grid.get(it["ticker"]) or it["ticker"],
            category=it["category"],
            hour=it.get("hour"),
            eps_estimate=it.get("eps_estimate"),
            revenue_estimate=it.get("revenue_estimate"),
        ))
    return EarningsResponse(items=out)
