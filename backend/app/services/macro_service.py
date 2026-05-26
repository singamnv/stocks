"""Macro data for the Morning Brief: futures, FX/commodities, rates, VIX, global indices, sectors."""
from typing import Optional

import yfinance as yf

from ..cache import cached
from .yf_service import _safe_float

FUTURES = [
    ("ES=F", "S&P 500"),
    ("NQ=F", "Nasdaq 100"),
    ("YM=F", "Dow"),
    ("RTY=F", "Russell 2000"),
]

FX_COMMODITIES = [
    ("DX-Y.NYB", "DXY"),
    ("GC=F", "Gold"),
    ("CL=F", "Crude Oil"),
]

RATES_TICKER = "^TNX"  # 10Y treasury yield (already in %)

VIX_SPOT = "^VIX"
VIX_3M = "^VIX3M"

ASIA = [("^N225", "Nikkei 225"), ("^HSI", "Hang Seng"), ("000001.SS", "Shanghai Composite")]
EUROPE = [("^FTSE", "FTSE 100"), ("^GDAXI", "DAX"), ("^FCHI", "CAC 40"), ("^STOXX50E", "Euro Stoxx 50")]
US = [("^GSPC", "S&P 500"), ("^DJI", "Dow Jones"), ("^IXIC", "Nasdaq Composite"), ("^RUT", "Russell 2000")]

SECTORS = [
    ("XLK", "Technology"),
    ("XLF", "Financials"),
    ("XLV", "Health Care"),
    ("XLE", "Energy"),
    ("XLY", "Consumer Discretionary"),
    ("XLP", "Consumer Staples"),
    ("XLI", "Industrials"),
    ("XLB", "Materials"),
    ("XLU", "Utilities"),
    ("XLRE", "Real Estate"),
    ("XLC", "Communication Services"),
]

ALL_SYMBOLS: list[str] = list({
    *[s for s, _ in FUTURES],
    *[s for s, _ in FX_COMMODITIES],
    RATES_TICKER,
    VIX_SPOT,
    VIX_3M,
    *[s for s, _ in ASIA],
    *[s for s, _ in EUROPE],
    *[s for s, _ in US],
    *[s for s, _ in SECTORS],
})


@cached("macro", ttl=300)
def _fetch_all() -> dict[str, dict]:
    """Batch-fetch every macro symbol via yf.Tickers; returns symbol -> {price, prev}."""
    tickers = yf.Tickers(" ".join(ALL_SYMBOLS))
    out: dict[str, dict] = {}
    for sym in ALL_SYMBOLS:
        try:
            t = tickers.tickers.get(sym)
            if t is None:
                out[sym] = {"price": None, "prev": None}
                continue
            try:
                fast = dict(t.fast_info) if t.fast_info else {}
            except Exception:
                fast = {}
            out[sym] = {
                "price": _safe_float(fast.get("lastPrice") or fast.get("last_price")),
                "prev": _safe_float(fast.get("previousClose") or fast.get("previous_close")),
            }
        except Exception:
            out[sym] = {"price": None, "prev": None}
    return out


def _change_pct(price: Optional[float], prev: Optional[float]) -> Optional[float]:
    if price is None or not prev:
        return None
    return (price - prev) / prev * 100


def _row(symbol: str, name: str, data: dict[str, dict]) -> dict:
    d = data.get(symbol, {})
    p = d.get("price")
    return {
        "symbol": symbol,
        "name": name,
        "price": p,
        "change_pct": _change_pct(p, d.get("prev")),
    }


def get_brief() -> dict:
    data = _fetch_all()

    ten_y_data = data.get(RATES_TICKER, {})
    ten_y = ten_y_data.get("price")
    prev_y = ten_y_data.get("prev")
    # ^TNX is the yield in percent (e.g. 4.21). 1 percentage point = 100 bps.
    bps_change = ((ten_y - prev_y) * 100) if (ten_y is not None and prev_y is not None) else None

    vix_spot = data.get(VIX_SPOT, {}).get("price")
    vix_3m = data.get(VIX_3M, {}).get("price")
    term_ratio = (vix_spot / vix_3m) if (vix_spot and vix_3m) else None

    return {
        "vitals": {
            "futures": [_row(s, n, data) for s, n in FUTURES],
            "fx_commodities": [_row(s, n, data) for s, n in FX_COMMODITIES],
            "rates": [{"label": "10Y Treasury", "yield_pct": ten_y, "bps_change": bps_change}],
            "vix": {"spot": vix_spot, "three_month": vix_3m, "term_ratio": term_ratio},
        },
        "tape": {
            "asia": [_row(s, n, data) for s, n in ASIA],
            "europe": [_row(s, n, data) for s, n in EUROPE],
            "us": [_row(s, n, data) for s, n in US],
        },
        "sectors": [_row(s, n, data) for s, n in SECTORS],
    }
