"""Cache warmup — pre-fetch ONLY the default ecosystem's data at startup.

Earlier versions warmed all 13 ecosystems (~173 unique tickers) at startup, but
Yahoo's anti-bot tripped on that volume and IP-blocked the machine for 15-60min.
Now we warm only the default ecosystem so first page-load is instant for the
most common case; other ecosystems lazy-load on first visit.

`warm_ecosystem_sync()` is used by the refresh button and is rate-limit aware
(the throttle is in yf_service / finnhub_service themselves).
"""
import asyncio
import logging
import time

from .. import ecosystems
from . import finnhub_service, yf_service

log = logging.getLogger(__name__)

# Sequential with a small delay so we never blast Yahoo. ~30s for ~30 tickers.
YF_CALL_DELAY_SEC = 0.4


def _ecosystem_symbols(eco_key: str) -> list[str]:
    eco = ecosystems.get(eco_key)
    seen: set[str] = set()
    out: list[str] = []
    for s in [eco.ANCHOR_TICKER, *ecosystems.all_tickers(eco)]:
        if s in seen:
            continue
        seen.add(s)
        out.append(s)
    return out


async def warm_default_ecosystem() -> None:
    """At startup, warm only the default ecosystem. Other ecosystems lazy-load.

    Why not warm everything: 173 unique tickers blasted at startup trips Yahoo's
    anti-bot heuristics and IP-blocks the machine. One ecosystem's worth (~30
    tickers) at 0.4s/call is gentle enough to be safe.
    """
    start = time.monotonic()
    eco_key = ecosystems.DEFAULT_KEY
    symbols = _ecosystem_symbols(eco_key)
    log.info("warmup: starting; %d tickers in default ecosystem (%s)", len(symbols), eco_key)

    for sym in symbols:
        try:
            await asyncio.to_thread(yf_service.get_quote, sym)
        except Exception as e:
            log.warning("warmup: get_quote(%s) failed: %s", sym, e)
        await asyncio.sleep(YF_CALL_DELAY_SEC)

    try:
        await asyncio.to_thread(yf_service.get_grid, eco_key)
    except Exception:
        pass

    if finnhub_service.has_key():
        try:
            await asyncio.to_thread(finnhub_service._fetch_earnings_calendar, 60)
        except Exception:
            pass
        try:
            await asyncio.to_thread(finnhub_service.get_earnings, eco_key)
        except Exception:
            pass
        # News: throttle is in finnhub_service, but skip individual ticker news
        # at startup to keep warmup quick. /api/news lazy-fills on first visit.

    log.info("warmup: %s complete in %.1fs", eco_key, time.monotonic() - start)


def warm_ecosystem_sync(eco_key: str) -> None:
    """Warm one ecosystem's caches synchronously. Used by the refresh endpoint
    via BackgroundTasks so the response returns immediately."""
    start = time.monotonic()
    symbols = _ecosystem_symbols(eco_key)

    for s in symbols:
        try:
            yf_service.get_quote(s)
        except Exception as e:
            log.warning("refresh(%s): get_quote(%s) failed: %s", eco_key, s, e)
        time.sleep(YF_CALL_DELAY_SEC)
    try:
        yf_service.get_grid(eco_key)
    except Exception:
        pass

    if not finnhub_service.has_key():
        log.info("refresh(%s): yfinance-only complete in %.1fs",
                 eco_key, time.monotonic() - start)
        return

    try:
        finnhub_service._fetch_earnings_calendar(60)
    except Exception:
        pass
    for s in symbols:
        try:
            finnhub_service._news_for_ticker(s)
        except Exception:
            pass
    try:
        finnhub_service.get_news(eco_key)
    except Exception:
        pass
    try:
        finnhub_service.get_earnings(eco_key)
    except Exception:
        pass

    log.info("refresh(%s): complete in %.1fs", eco_key, time.monotonic() - start)
