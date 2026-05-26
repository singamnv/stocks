"""yfinance wrappers — now backed by yf_batch (direct Yahoo HTTP) for the
high-volume paths, with the yfinance library kept only for price history
(detail-drawer chart), which is per-click and low volume.

Why this design: the yfinance library hits one HTTP call per ticker for
`.fast_info`, which makes 173-ticker warmups look like a bot to Yahoo and
gets the IP blocked. The direct `/v7/quote` endpoint accepts up to ~50
symbols per call and returns the same data, so one ecosystem's worth of
quotes is one HTTP call instead of 30.
"""
import logging
import math
from datetime import datetime
from typing import Any, Optional

import yfinance as yf

from .. import ecosystems
from ..cache import cached
from . import yf_batch

log = logging.getLogger(__name__)


# Period -> (yfinance period, interval) for the price-chart history endpoint.
PERIOD_MAP: dict[str, tuple[str, str]] = {
    "1D": ("1d",  "5m"),
    "1W": ("5d",  "30m"),
    "1M": ("1mo", "1d"),
    "1Y": ("1y",  "1d"),
    "5Y": ("5y",  "1wk"),
}


def _safe_float(x: Any) -> Optional[float]:
    try:
        if x is None:
            return None
        f = float(x)
        if math.isnan(f) or math.isinf(f):
            return None
        return f
    except (ValueError, TypeError):
        return None


def _is_valid_quote(q: dict) -> bool:
    """Skip caching None-price stubs — better to retry than serve garbage for 5 min."""
    return q.get("price") is not None


def _empty_quote(symbol: str) -> dict:
    return {
        "symbol": symbol, "name": symbol,
        "price": None, "change_pct": None, "market_cap": None,
        "pe_ratio": None, "ytd_pct": None, "one_year_pct": None,
    }


@cached("quote", ttl=300, should_cache=_is_valid_quote)
def get_quote(symbol: str) -> dict:
    """Single-ticker quote. Delegates to the batched fetch (still one HTTP call,
    just over a single-symbol query). Used by detail endpoints and anywhere
    grid isn't appropriate."""
    quotes = yf_batch.fetch_quotes([symbol])
    q = quotes.get(symbol)
    if not q:
        return _empty_quote(symbol)
    return {
        "symbol": symbol,
        "name": q["name"],
        "price": q["price"],
        "change_pct": q["change_pct"],
        "market_cap": q["market_cap"],
        "pe_ratio": q["pe_ratio"],
        "ytd_pct": None,         # filled at the grid level via spark
        "one_year_pct": None,    # filled at the grid level via spark
    }


@cached("grid", ttl=300)
def get_grid(eco_key: str) -> list[dict]:
    """Return quote dicts for every ticker in `eco_key` — three batched HTTP
    calls total: one /v7/quote + two /v7/spark (ytd + 1y)."""
    eco = ecosystems.get(eco_key)
    tic_to_cat = ecosystems.ticker_to_category(eco)
    symbols = list(tic_to_cat.keys())

    quotes = yf_batch.fetch_quotes(symbols)
    ytd_map = yf_batch.fetch_range_pct(symbols, "ytd")
    y1_map = yf_batch.fetch_range_pct(symbols, "1y")

    out: list[dict] = []
    for symbol in symbols:
        q = quotes.get(symbol)
        if q is None:
            out.append({
                "symbol": symbol,
                "name": symbol,
                "category": tic_to_cat[symbol],
                "error": "Yahoo returned no data for this symbol",
            })
            continue
        out.append({
            "symbol": symbol,
            "name": q["name"],
            "category": tic_to_cat[symbol],
            "price": q["price"],
            "change_pct": q["change_pct"],
            "market_cap": q["market_cap"],
            "pe_ratio": q["pe_ratio"],
            "ytd_pct": ytd_map.get(symbol),
            "one_year_pct": y1_map.get(symbol),
        })
    return out


@cached("detail", ttl=300)
def get_detail(symbol: str) -> dict:
    """Detail view: batched quote + spark for ytd/1y, plus a `.info` call for
    the verbose-only fields (sector/industry/website/revenue/margins/FCF) that
    /v7/quote doesn't carry. The .info call is per-click, low volume, and
    caches per symbol so it rarely re-hits Yahoo."""
    base = get_quote(symbol)
    ytd = yf_batch.fetch_range_pct([symbol], "ytd").get(symbol)
    y1 = yf_batch.fetch_range_pct([symbol], "1y").get(symbol)

    # The verbose .info fields. If Yahoo blocks this, we fail gracefully.
    info: dict = {}
    try:
        info = yf.Ticker(symbol).info or {}
    except Exception as e:
        log.warning("get_detail(%s) .info failed: %s", symbol, e)

    return {
        **base,
        "ytd_pct": ytd,
        "one_year_pct": y1,
        "revenue": _safe_float(info.get("totalRevenue")),
        "gross_margins": _safe_float(info.get("grossMargins")),
        "free_cashflow": _safe_float(info.get("freeCashflow")),
        "fifty_two_week_high": _safe_float(info.get("fiftyTwoWeekHigh")),
        "fifty_two_week_low": _safe_float(info.get("fiftyTwoWeekLow")),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "website": info.get("website"),
    }


@cached("history", ttl=900)
def get_history(symbol: str, range_: str) -> list[dict]:
    """Price-chart history for the detail drawer. Single-ticker, per-click,
    low volume — yfinance's history() works fine here as long as we're not
    blasting it."""
    period, interval = PERIOD_MAP.get(range_, PERIOD_MAP["1M"])
    t = yf.Ticker(symbol)
    try:
        hist = t.history(period=period, interval=interval, auto_adjust=False)
    except Exception as e:
        log.warning("get_history(%s, %s) failed: %s", symbol, range_, e)
        return []
    points: list[dict] = []
    for ts, row in hist.iterrows():
        c = _safe_float(row.get("Close"))
        if c is None:
            continue
        try:
            ts_ms = int(ts.timestamp() * 1000)
        except Exception:
            continue
        points.append({"t": ts_ms, "c": c})
    return points
