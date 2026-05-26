"""Batched Yahoo Finance client — direct HTTP, no yfinance dependency.

Why this exists: yfinance's `.fast_info` / `.info` does one HTTP call per
ticker, which causes Yahoo's anti-bot to IP-block the machine when warming
many tickers. Yahoo's actual `/v7/finance/quote` endpoint accepts a comma-
separated list of up to ~250 symbols and returns everything in one call.

Two endpoints used here:
- `/v7/finance/quote` — price, change, mcap, P/E, 52w range, name (1 call / 50 symbols)
- `/v7/finance/spark`  — range-bounded close prices for deriving YTD% and 1Y% (1 call / batch)

A crumb + cookie session is required (Yahoo's anti-bot dance). We cache the
session for an hour and rebuild on failure.
"""
import logging
import math
import threading
import time
from typing import Optional

from curl_cffi import requests as cffi

log = logging.getLogger(__name__)

QUOTE_URL = "https://query1.finance.yahoo.com/v7/finance/quote"
SPARK_URL = "https://query1.finance.yahoo.com/v7/finance/spark"
CRUMB_URL = "https://query1.finance.yahoo.com/v1/test/getcrumb"
COOKIE_URL = "https://fc.yahoo.com"

# Per-endpoint symbol caps (observed):
#   /v7/finance/quote — 50+ symbols accepted comfortably
#   /v7/finance/spark — Yahoo returns 400 above 20 symbols
QUOTE_CHUNK = 50
SPARK_CHUNK = 20

# Crumbs are valid for ~1 day in practice; rebuild hourly to be safe.
SESSION_TTL_SEC = 3600

_lock = threading.Lock()
_session: Optional[cffi.Session] = None
_crumb: Optional[str] = None
_session_expires: float = 0.0


def _get_session_and_crumb() -> tuple[cffi.Session, str]:
    """Return (session, crumb), rebuilding if expired or missing."""
    global _session, _crumb, _session_expires
    with _lock:
        if _session is not None and _crumb and time.monotonic() < _session_expires:
            return _session, _crumb

        s = cffi.Session(impersonate="chrome")
        # Warm cookies — 404 is fine, we just need the Set-Cookie headers.
        try:
            s.get(COOKIE_URL, timeout=10)
        except Exception:
            pass
        # Get a crumb tied to those cookies.
        r = s.get(CRUMB_URL, timeout=10)
        r.raise_for_status()
        crumb = r.text.strip()
        if not crumb or len(crumb) < 6:
            raise RuntimeError(f"Yahoo returned bogus crumb: {crumb!r}")

        _session = s
        _crumb = crumb
        _session_expires = time.monotonic() + SESSION_TTL_SEC
        log.info("yf_batch: refreshed Yahoo session + crumb")
        return _session, _crumb


def _invalidate_session() -> None:
    global _session, _crumb, _session_expires
    with _lock:
        _session = None
        _crumb = None
        _session_expires = 0.0


def _safe_float(x) -> Optional[float]:
    try:
        if x is None:
            return None
        f = float(x)
        if math.isnan(f) or math.isinf(f):
            return None
        return f
    except (ValueError, TypeError):
        return None


def fetch_quotes(symbols: list[str]) -> dict[str, dict]:
    """Fetch live quote data for many tickers in batched calls.

    Returns `{symbol: quote_dict}` with keys:
        name, price, change_pct, market_cap, pe_ratio,
        fifty_two_week_high, fifty_two_week_low, prev_close,
        sector, industry, website
    Missing tickers are simply absent from the result (the caller should treat
    them as failures and serve None values).
    """
    if not symbols:
        return {}
    out: dict[str, dict] = {}

    for i in range(0, len(symbols), QUOTE_CHUNK):
        chunk = symbols[i : i + QUOTE_CHUNK]
        try:
            session, crumb = _get_session_and_crumb()
            r = session.get(
                QUOTE_URL,
                params={"symbols": ",".join(chunk), "crumb": crumb},
                timeout=15,
            )
            if r.status_code == 401 or r.status_code == 403:
                _invalidate_session()
                session, crumb = _get_session_and_crumb()
                r = session.get(
                    QUOTE_URL,
                    params={"symbols": ",".join(chunk), "crumb": crumb},
                    timeout=15,
                )
            r.raise_for_status()
            data = r.json() or {}
        except Exception as e:
            log.warning("fetch_quotes chunk failed (%d symbols): %s: %s",
                        len(chunk), type(e).__name__, e)
            continue

        for q in (data.get("quoteResponse") or {}).get("result") or []:
            sym = q.get("symbol")
            if not sym:
                continue
            price = _safe_float(q.get("regularMarketPrice"))
            prev = _safe_float(q.get("regularMarketPreviousClose"))
            change_pct = _safe_float(q.get("regularMarketChangePercent"))
            if change_pct is None and price is not None and prev:
                change_pct = (price - prev) / prev * 100
            out[sym] = {
                "name": q.get("shortName") or q.get("longName") or sym,
                "price": price,
                "prev_close": prev,
                "change_pct": change_pct,
                "market_cap": _safe_float(q.get("marketCap")),
                "pe_ratio": _safe_float(q.get("trailingPE")) or _safe_float(q.get("forwardPE")),
                "fifty_two_week_high": _safe_float(q.get("fiftyTwoWeekHigh")),
                "fifty_two_week_low": _safe_float(q.get("fiftyTwoWeekLow")),
                # These come from the quoteSummary endpoint, not /v7/quote; fill
                # in via a separate call only when needed (e.g. detail view).
                "sector": None,
                "industry": None,
                "website": None,
            }
    return out


def fetch_range_pct(symbols: list[str], range_: str) -> dict[str, Optional[float]]:
    """Return `{symbol: pct_change}` over the given range (e.g. 'ytd', '1y').

    Uses Yahoo's /v7/spark endpoint, which returns a `meta.chartPreviousClose`
    (the close just before the range starts) and `meta.regularMarketPrice` —
    perfect for computing range-pct without parsing the full bar array.
    """
    if not symbols:
        return {}
    out: dict[str, Optional[float]] = {}

    for i in range(0, len(symbols), SPARK_CHUNK):
        chunk = symbols[i : i + SPARK_CHUNK]
        try:
            session, crumb = _get_session_and_crumb()
            r = session.get(
                SPARK_URL,
                params={
                    "symbols": ",".join(chunk),
                    "range": range_,
                    "interval": "1d",
                    "crumb": crumb,
                },
                timeout=15,
            )
            r.raise_for_status()
            data = r.json() or {}
        except Exception as e:
            log.warning("fetch_range_pct(%s) chunk failed: %s: %s",
                        range_, type(e).__name__, e)
            continue

        for item in (data.get("spark") or {}).get("result") or []:
            sym = item.get("symbol")
            if not sym:
                continue
            for resp in item.get("response") or []:
                meta = resp.get("meta") or {}
                start = _safe_float(meta.get("chartPreviousClose"))
                last = _safe_float(meta.get("regularMarketPrice"))
                if start and last is not None:
                    out[sym] = (last - start) / start * 100
                else:
                    out[sym] = None
    return out
