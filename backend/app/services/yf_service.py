"""yfinance wrappers. All return-shapes are plain dicts that match schemas.py.

Per-ticker functions (get_quote, get_detail, get_history) are ecosystem-agnostic
and their caches are shared across ecosystems. Aggregate functions (get_grid)
take an `eco_key` so their caches partition cleanly per ecosystem.

When Yahoo rate-limits us (YFRateLimitError), we short-circuit all subsequent
yfinance calls for RATE_LIMIT_BACKOFF_SEC instead of hammering Yahoo and making
the block longer. The first call after the backoff window expires will try
again and either succeed or restart the backoff.
"""
import logging
import math
import threading
import time
from datetime import datetime
from typing import Any, Optional

import yfinance as yf

from .. import ecosystems
from ..cache import cached

log = logging.getLogger(__name__)

# When Yahoo rate-limits us, back off for this long before trying again.
RATE_LIMIT_BACKOFF_SEC = 15 * 60  # 15 minutes — Yahoo blocks typically clear in 15-60 min

_rate_limit_lock = threading.Lock()
_rate_limited_until: float = 0.0


def _is_rate_limited() -> bool:
    return time.monotonic() < _rate_limited_until


def _mark_rate_limited() -> None:
    global _rate_limited_until
    with _rate_limit_lock:
        _rate_limited_until = time.monotonic() + RATE_LIMIT_BACKOFF_SEC
    log.warning(
        "yfinance: Yahoo rate-limited; backing off all yf calls for %ds",
        RATE_LIMIT_BACKOFF_SEC,
    )


def rate_limit_status() -> dict:
    """For diagnostics — exposed via the API so the user knows what's happening."""
    remaining = max(0, _rate_limited_until - time.monotonic())
    return {"rate_limited": remaining > 0, "seconds_until_retry": int(remaining)}

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


def _ytd_pct(ticker: yf.Ticker) -> Optional[float]:
    try:
        start = datetime(datetime.now().year, 1, 1).strftime("%Y-%m-%d")
        hist = ticker.history(start=start, interval="1d", auto_adjust=False)
        if hist.empty or len(hist) < 2:
            return None
        first = float(hist["Close"].iloc[0])
        last = float(hist["Close"].iloc[-1])
        return (last - first) / first * 100
    except Exception:
        return None


def _period_pct(ticker: yf.Ticker, period: str) -> Optional[float]:
    try:
        hist = ticker.history(period=period, interval="1d", auto_adjust=False)
        if hist.empty or len(hist) < 2:
            return None
        first = float(hist["Close"].iloc[0])
        last = float(hist["Close"].iloc[-1])
        return (last - first) / first * 100
    except Exception:
        return None


def _is_valid_quote(q: dict) -> bool:
    # Don't cache failures — yfinance hiccups under concurrent load and we'd
    # rather retry on next request than serve None-price stubs for 5 minutes.
    return q.get("price") is not None


def _empty_quote(symbol: str) -> dict:
    return {
        "symbol": symbol, "name": symbol,
        "price": None, "change_pct": None, "market_cap": None,
        "pe_ratio": None, "ytd_pct": None, "one_year_pct": None,
    }


@cached("quote", ttl=300, should_cache=_is_valid_quote)
def get_quote(symbol: str) -> dict:
    if _is_rate_limited():
        return _empty_quote(symbol)
    t = yf.Ticker(symbol)
    try:
        fast = dict(t.fast_info) if t.fast_info else {}
    except Exception as e:
        if "RateLimit" in type(e).__name__:
            _mark_rate_limited()
        else:
            log.warning("get_quote(%s) fast_info failed: %s: %s", symbol, type(e).__name__, e)
        fast = {}
    try:
        info = t.info or {}
    except Exception as e:
        if "RateLimit" in type(e).__name__:
            _mark_rate_limited()
        else:
            log.warning("get_quote(%s) info failed: %s: %s", symbol, type(e).__name__, e)
        info = {}

    price = (
        _safe_float(fast.get("last_price"))
        or _safe_float(info.get("currentPrice"))
        or _safe_float(info.get("regularMarketPrice"))
    )
    prev_close = (
        _safe_float(fast.get("previous_close"))
        or _safe_float(info.get("regularMarketPreviousClose"))
        or _safe_float(info.get("previousClose"))
    )
    change_pct: Optional[float] = None
    if price is not None and prev_close:
        change_pct = (price - prev_close) / prev_close * 100

    return {
        "symbol": symbol,
        "name": info.get("shortName") or info.get("longName") or symbol,
        "price": price,
        "change_pct": change_pct,
        "market_cap": _safe_float(fast.get("market_cap")) or _safe_float(info.get("marketCap")),
        "pe_ratio": _safe_float(info.get("trailingPE")) or _safe_float(info.get("forwardPE")),
        "ytd_pct": _ytd_pct(t),
        "one_year_pct": _period_pct(t, "1y"),
    }


@cached("grid", ttl=300)
def get_grid(eco_key: str) -> list[dict]:
    """Return quote dicts for every ticker in `eco_key`; per-ticker failures are isolated."""
    eco = ecosystems.get(eco_key)
    tic_to_cat = ecosystems.ticker_to_category(eco)
    out: list[dict] = []
    for symbol in ecosystems.all_tickers(eco):
        try:
            q = get_quote(symbol)
            q["category"] = tic_to_cat[symbol]
            out.append(q)
        except Exception as e:
            out.append({
                "symbol": symbol,
                "name": symbol,
                "category": tic_to_cat[symbol],
                "error": str(e),
            })
    return out


@cached("detail", ttl=300)
def get_detail(symbol: str) -> dict:
    t = yf.Ticker(symbol)
    try:
        info = t.info or {}
    except Exception:
        info = {}
    base = get_quote(symbol)
    return {
        **base,
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
    period, interval = PERIOD_MAP.get(range_, PERIOD_MAP["1M"])
    t = yf.Ticker(symbol)
    hist = t.history(period=period, interval=interval, auto_adjust=False)
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
