"""Cache warmup — pre-fetch every ecosystem's data so first page-load is instant.

`warm_all_caches()` is the startup hook. It runs the cheap concurrent yfinance
work first, then the slow throttled Finnhub work. Server is ready to serve
requests immediately; warmup happens in the background.

`warm_ecosystem_sync()` is for the on-demand refresh button — same shape but
scoped to one ecosystem.
"""
import asyncio
import logging
import time

from .. import ecosystems
from . import finnhub_service, yf_service

log = logging.getLogger(__name__)

# yfinance concurrency — keep modest; the library is finicky under heavy parallelism.
YF_CONCURRENCY = 8


def _unique_symbols() -> set[str]:
    out: set[str] = set()
    for m in ecosystems.all_modules():
        out.add(m.ANCHOR_TICKER)
        out.update(ecosystems.all_tickers(m))
    return out


def _ecosystem_symbols(eco_key: str) -> set[str]:
    eco = ecosystems.get(eco_key)
    return {eco.ANCHOR_TICKER, *ecosystems.all_tickers(eco)}


async def warm_all_caches() -> None:
    """Warm the cache for every ecosystem. Safe to run in background at startup."""
    start = time.monotonic()
    symbols = _unique_symbols()
    n_ecos = len(ecosystems.all_keys())
    log.info(
        "warmup: starting; %d unique tickers across %d ecosystems",
        len(symbols), n_ecos,
    )

    # 1. yfinance per-ticker quotes (concurrent, no rate limit).
    sem = asyncio.Semaphore(YF_CONCURRENCY)

    async def warm_quote(sym: str) -> None:
        async with sem:
            try:
                await asyncio.to_thread(yf_service.get_quote, sym)
            except Exception as e:
                log.warning("warmup: get_quote(%s) failed: %s", sym, e)

    await asyncio.gather(*(warm_quote(s) for s in symbols))
    log.info("warmup: yfinance quotes done in %.1fs", time.monotonic() - start)

    # 2. per-ecosystem grids (uses cached quotes — fast).
    for m in ecosystems.all_modules():
        try:
            await asyncio.to_thread(yf_service.get_grid, m.KEY)
        except Exception as e:
            log.warning("warmup: get_grid(%s) failed: %s", m.KEY, e)

    if not finnhub_service.has_key():
        log.info("warmup: skipping Finnhub (no API key); complete in %.1fs",
                 time.monotonic() - start)
        return

    # 3. earnings — one Finnhub call shared by every ecosystem's aggregate.
    try:
        await asyncio.to_thread(finnhub_service._fetch_earnings_calendar, 60)
    except Exception as e:
        log.warning("warmup: earnings calendar failed: %s", e)
    for m in ecosystems.all_modules():
        try:
            await asyncio.to_thread(finnhub_service.get_earnings, m.KEY)
        except Exception:
            pass

    # 4. per-ticker news (one Finnhub call per ticker; throttled inside finnhub_service).
    log.info("warmup: starting Finnhub news (%d tickers, ~%.0fs at 1.2s each)",
             len(symbols), len(symbols) * 1.2)
    for sym in symbols:
        try:
            await asyncio.to_thread(finnhub_service._news_for_ticker, sym)
        except Exception:
            pass

    # 5. per-ecosystem news aggregates (uses cached per-ticker — fast).
    for m in ecosystems.all_modules():
        try:
            await asyncio.to_thread(finnhub_service.get_news, m.KEY)
        except Exception:
            pass

    log.info("warmup: complete in %.1fs", time.monotonic() - start)


def warm_ecosystem_sync(eco_key: str) -> None:
    """Warm one ecosystem's caches synchronously. Used by the refresh endpoint
    via BackgroundTasks so the response returns immediately."""
    start = time.monotonic()
    symbols = list(_ecosystem_symbols(eco_key))

    # yfinance — sequential is fine, ~15-20 tickers takes ~5s
    for s in symbols:
        try:
            yf_service.get_quote(s)
        except Exception as e:
            log.warning("refresh(%s): get_quote(%s) failed: %s", eco_key, s, e)
    try:
        yf_service.get_grid(eco_key)
    except Exception:
        pass

    if not finnhub_service.has_key():
        log.info("refresh(%s): yfinance-only complete in %.1fs",
                 eco_key, time.monotonic() - start)
        return

    # Finnhub — throttled at the service layer (~1.2s per call).
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
