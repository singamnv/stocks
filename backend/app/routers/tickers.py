from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from .. import ecosystems
from ..schemas import (
    GridResponse,
    HistoryResponse,
    PricePoint,
    TickerDetail,
    TickerGroup,
    TickerQuote,
)
from ..services.yf_service import PERIOD_MAP, get_detail, get_grid, get_history

router = APIRouter(prefix="/api/tickers", tags=["tickers"])


@router.get("", response_model=GridResponse)
def list_tickers(ecosystem: str = Query(ecosystems.DEFAULT_KEY)) -> GridResponse:
    eco = ecosystems.get(ecosystem)
    quotes = get_grid(eco.KEY)
    by_cat: dict[str, list[TickerQuote]] = {cat: [] for cat in eco.ECOSYSTEM}
    for q in quotes:
        cat = q.get("category")
        if cat in by_cat:
            by_cat[cat].append(TickerQuote(**q))
    groups = [TickerGroup(category=cat, tickers=by_cat[cat]) for cat in eco.ECOSYSTEM]
    return GridResponse(groups=groups)


@router.get("/{symbol}", response_model=TickerDetail)
def ticker_detail(
    symbol: str,
    ecosystem: Optional[str] = Query(None),
) -> TickerDetail:
    symbol = symbol.upper()

    # Resolve which ecosystem to use for category/role lookup.
    # Try the requested ecosystem first; if it doesn't contain the symbol, fall
    # back to the first ecosystem that does (NVDA appears in NVIDIA + Automotive,
    # TSM in NVIDIA + AMD + Hyperscaler, etc.).
    eco = ecosystems.get(ecosystem) if ecosystem else None
    if eco is None or (symbol not in ecosystems.all_tickers(eco) and symbol != eco.ANCHOR_TICKER):
        fallback = ecosystems.find_first_containing(symbol)
        if fallback is None:
            raise HTTPException(status_code=404, detail="Ticker not tracked in any ecosystem")
        eco = fallback

    cat_map = ecosystems.ticker_to_category(eco)
    d = get_detail(symbol)
    return TickerDetail(
        symbol=symbol,
        name=d.get("name") or symbol,
        category=cat_map.get(symbol, eco.NAME),
        role=eco.ROLES.get(symbol, ""),
        price=d.get("price"),
        change_pct=d.get("change_pct"),
        market_cap=d.get("market_cap"),
        pe_ratio=d.get("pe_ratio"),
        revenue=d.get("revenue"),
        gross_margins=d.get("gross_margins"),
        free_cashflow=d.get("free_cashflow"),
        fifty_two_week_high=d.get("fifty_two_week_high"),
        fifty_two_week_low=d.get("fifty_two_week_low"),
        sector=d.get("sector"),
        industry=d.get("industry"),
        website=d.get("website"),
    )


@router.get("/{symbol}/history", response_model=HistoryResponse)
def ticker_history(symbol: str, range: str = Query("1M")) -> HistoryResponse:
    symbol = symbol.upper()
    if range not in PERIOD_MAP:
        raise HTTPException(
            status_code=400,
            detail=f"range must be one of {list(PERIOD_MAP)}",
        )
    pts = get_history(symbol, range)
    return HistoryResponse(
        symbol=symbol,
        range=range,
        points=[PricePoint(**p) for p in pts],
    )
