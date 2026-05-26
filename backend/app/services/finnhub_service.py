"""Finnhub REST wrappers (news + earnings calendar). Returns empty lists if no key.

Per-ticker fetch (_news_for_ticker) is symbol-keyed and shared across ecosystems.
Aggregate functions (get_news, get_earnings) take an `eco_key` so their caches
partition per ecosystem.

Finnhub free tier is 60 calls/min. A module-level throttle blocks every HTTP
call to enforce a min gap of FINNHUB_MIN_INTERVAL seconds — applied to cache
misses only (cache hits don't go through it).
"""
import threading
import time
from datetime import datetime, timedelta, timezone

import httpx

from .. import ecosystems
from ..cache import cached
from ..config import settings

BASE = "https://finnhub.io/api/v1"
TIMEOUT = 10.0

# ~50 calls/min — safely under the 60/min free-tier ceiling.
FINNHUB_MIN_INTERVAL = 1.2

_throttle_lock = threading.Lock()
_last_call_ts: float = 0.0


def _throttle() -> None:
    """Block until at least FINNHUB_MIN_INTERVAL seconds have passed since the last call."""
    global _last_call_ts
    with _throttle_lock:
        gap = time.monotonic() - _last_call_ts
        if gap < FINNHUB_MIN_INTERVAL:
            time.sleep(FINNHUB_MIN_INTERVAL - gap)
        _last_call_ts = time.monotonic()


def has_key() -> bool:
    return bool(settings.FINNHUB_API_KEY)


def _eco_symbols(eco_key: str) -> tuple[list[str], dict[str, str]]:
    """Return (symbols, ticker->category) for the ecosystem; includes the anchor even if not in the map."""
    eco = ecosystems.get(eco_key)
    tic_to_cat = ecosystems.ticker_to_category(eco)
    symbols: list[str] = []
    seen: set[str] = set()
    for s in [eco.ANCHOR_TICKER, *ecosystems.all_tickers(eco)]:
        if s in seen:
            continue
        seen.add(s)
        symbols.append(s)
    return symbols, tic_to_cat


@cached("news_per_ticker", ttl=900)
def _news_for_ticker(symbol: str, days: int = 14) -> list[dict]:
    if not has_key():
        return []
    _throttle()
    today = datetime.now(timezone.utc).date()
    from_date = today - timedelta(days=days)
    params = {
        "symbol": symbol,
        "from": from_date.isoformat(),
        "to": today.isoformat(),
        "token": settings.FINNHUB_API_KEY,
    }
    try:
        r = httpx.get(f"{BASE}/company-news", params=params, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json() or []
    except Exception:
        return []


@cached("news_all", ttl=900)
def get_news(eco_key: str) -> list[dict]:
    symbols, tic_to_cat = _eco_symbols(eco_key)
    eco_name = ecosystems.get(eco_key).NAME
    out: list[dict] = []
    for sym in symbols:
        for item in _news_for_ticker(sym):
            out.append({
                "id": str(item.get("id") or f"{sym}-{item.get('datetime')}-{item.get('headline','')[:24]}"),
                "title": item.get("headline") or "",
                "source": item.get("source") or "",
                "url": item.get("url") or "",
                "timestamp": int(item.get("datetime") or 0),
                "ticker": sym,
                "category": tic_to_cat.get(sym, eco_name),
                "image": item.get("image") or None,
                "summary": item.get("summary") or None,
            })
    seen: set[str] = set()
    deduped: list[dict] = []
    for n in sorted(out, key=lambda x: x["timestamp"], reverse=True):
        key = n["url"] or n["id"]
        if key in seen:
            continue
        seen.add(key)
        deduped.append(n)
    return deduped


@cached("earnings_raw", ttl=900)
def _fetch_earnings_calendar(days_ahead: int = 60) -> list[dict]:
    """One Finnhub call shared across every ecosystem's get_earnings()."""
    if not has_key():
        return []
    _throttle()
    today = datetime.now(timezone.utc).date()
    to_date = today + timedelta(days=days_ahead)
    params = {
        "from": today.isoformat(),
        "to": to_date.isoformat(),
        "token": settings.FINNHUB_API_KEY,
    }
    try:
        r = httpx.get(f"{BASE}/calendar/earnings", params=params, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json() or {}
    except Exception:
        return []
    return data.get("earningsCalendar", []) or []


@cached("earnings", ttl=900)
def get_earnings(eco_key: str, days_ahead: int = 60) -> list[dict]:
    if not has_key():
        return []
    items = _fetch_earnings_calendar(days_ahead)
    symbols, tic_to_cat = _eco_symbols(eco_key)
    eco_name = ecosystems.get(eco_key).NAME
    tracked = set(symbols)
    out: list[dict] = []
    for it in items:
        sym = it.get("symbol")
        if sym not in tracked:
            continue
        out.append({
            "date": it.get("date"),
            "ticker": sym,
            "category": tic_to_cat.get(sym, eco_name),
            "hour": it.get("hour"),
            "eps_estimate": it.get("epsEstimate"),
            "revenue_estimate": it.get("revenueEstimate"),
        })
    out.sort(key=lambda x: x["date"] or "")
    return out
