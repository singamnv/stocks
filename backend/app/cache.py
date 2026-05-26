import hashlib
import json
from functools import wraps
from typing import Any, Callable, Optional

from cachetools import TTLCache

CACHES: dict[str, TTLCache] = {}


def cached(
    name: str,
    ttl: int,
    maxsize: int = 256,
    should_cache: Optional[Callable[[Any], bool]] = None,
) -> Callable:
    """Decorator: cache return values in a named TTLCache keyed by (args, kwargs).

    `should_cache(result) -> bool` lets the caller veto caching specific results
    (e.g., don't cache yfinance responses where price is None — they're failures,
    not real values, and we don't want to serve them for the full TTL).
    """
    if name not in CACHES:
        CACHES[name] = TTLCache(maxsize=maxsize, ttl=ttl)
    cache = CACHES[name]

    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            payload = json.dumps([args, kwargs], default=str, sort_keys=True)
            key = hashlib.md5(payload.encode()).hexdigest()
            if key in cache:
                return cache[key]
            result = fn(*args, **kwargs)
            if should_cache is None or should_cache(result):
                cache[key] = result
            return result

        wrapper.cache = cache  # type: ignore[attr-defined]
        return wrapper

    return decorator
