from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Query

from .. import ecosystems
from ..schemas import KpiResponse
from ..services.finnhub_service import get_earnings
from ..services.yf_service import get_grid, get_quote

router = APIRouter(prefix="/api/kpis", tags=["kpis"])


@router.get("", response_model=KpiResponse)
def kpis(ecosystem: str = Query(ecosystems.DEFAULT_KEY)) -> KpiResponse:
    eco = ecosystems.get(ecosystem)
    eco_key = eco.KEY  # canonicalize (silently falls back to default on unknown)

    anchor = get_quote(eco.ANCHOR_TICKER)
    grid = get_grid(eco_key)

    mcap = sum((q.get("market_cap") or 0) for q in grid)
    # Include the anchor in mcap aggregate when it's not already in the grid.
    if eco.ANCHOR_TICKER not in {q.get("symbol") for q in grid} and anchor.get("market_cap"):
        mcap += anchor["market_cap"]

    pcts = [q.get("change_pct") for q in grid if q.get("change_pct") is not None]
    avg_pct = (sum(pcts) / len(pcts)) if pcts else None

    today = datetime.now(timezone.utc).date()
    week_end = today + timedelta(days=7)
    upcoming = get_earnings(eco_key, days_ahead=14)
    this_week = 0
    for e in upcoming:
        d = e.get("date")
        if not d:
            continue
        try:
            date = datetime.fromisoformat(d).date()
        except ValueError:
            continue
        if today <= date <= week_end:
            this_week += 1

    return KpiResponse(
        nvda_price=anchor.get("price"),
        nvda_change_pct=anchor.get("change_pct"),
        total_market_cap=mcap if mcap else None,
        earnings_this_week=this_week,
        avg_change_pct=avg_pct,
    )
