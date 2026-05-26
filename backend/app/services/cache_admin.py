"""Bust cached entries for a specific ecosystem (refresh button).

The cache decorator (cache.py) keys entries by md5 of `(args, kwargs)`. The
aggregate caches have call-shape variance (e.g. earnings called with
`days_ahead=7`, `=14`, or default `=60` from different callers), so we just
clear the whole named cache for aggregates — they rebuild fast from cached
per-ticker results. Per-ticker caches we clear selectively for this
ecosystem's symbols only.
"""
import hashlib
import json

from .. import ecosystems
from ..cache import CACHES

# Aggregate caches partition cleanly by call signature, but we have multiple
# call shapes in the codebase. Clear them entirely on refresh — cheap to rebuild.
_AGGREGATE_CACHES = ("grid", "news_all", "earnings", "earnings_raw")

# Per-ticker caches: clear only this ecosystem's symbols. Call shapes here are
# stable: get_quote(sym), get_detail(sym), _news_for_ticker(sym).
_PER_TICKER_CACHES = ("quote", "detail", "news_per_ticker")


def _key(*args, **kwargs) -> str:
    payload = json.dumps([args, kwargs], default=str, sort_keys=True)
    return hashlib.md5(payload.encode()).hexdigest()


def clear_ecosystem_caches(eco_key: str) -> int:
    """Remove all cache entries that the given ecosystem reads from.

    Returns the count of entries cleared (for observability).
    """
    eco = ecosystems.get(eco_key)
    symbols = {eco.ANCHOR_TICKER, *ecosystems.all_tickers(eco)}

    cleared = 0
    for name in _AGGREGATE_CACHES:
        c = CACHES.get(name)
        if c:
            cleared += len(c)
            c.clear()

    for name in _PER_TICKER_CACHES:
        c = CACHES.get(name)
        if not c:
            continue
        for sym in symbols:
            k = _key(sym)
            if k in c:
                del c[k]
                cleared += 1

    return cleared
