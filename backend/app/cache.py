import hashlib
import json
from functools import wraps
from typing import Callable

from cachetools import TTLCache

CACHES: dict[str, TTLCache] = {}


def cached(name: str, ttl: int, maxsize: int = 256) -> Callable:
    """Decorator: cache return values in a named TTLCache keyed by (args, kwargs)."""
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
            cache[key] = result
            return result

        wrapper.cache = cache  # type: ignore[attr-defined]
        return wrapper

    return decorator
