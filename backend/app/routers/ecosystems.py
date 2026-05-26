import time

from fastapi import APIRouter, BackgroundTasks, HTTPException

from .. import ecosystems
from ..schemas import EcosystemMeta, EcosystemsResponse
from ..services import cache_admin, warmup

router = APIRouter(prefix="/api/ecosystems", tags=["ecosystems"])

# Per-ecosystem cooldown so the refresh button can't be hammered.
# 30s is plenty given Finnhub throttle of 1.2s/call * ~20 tickers ≈ 24s/refresh.
MIN_REFRESH_INTERVAL_SEC = 30.0
_last_refresh: dict[str, float] = {}


@router.get("", response_model=EcosystemsResponse)
def list_ecosystems() -> EcosystemsResponse:
    items = [
        EcosystemMeta(
            key=m.KEY,
            name=m.NAME,
            group=getattr(m, "GROUP", "Other"),
            description=m.DESCRIPTION,
            anchor_ticker=m.ANCHOR_TICKER,
            categories=dict(m.CATEGORY_DESC),
        )
        for m in ecosystems.all_modules()
    ]
    return EcosystemsResponse(ecosystems=items, default_key=ecosystems.DEFAULT_KEY)


@router.post("/{key}/refresh")
def refresh_ecosystem(key: str, background_tasks: BackgroundTasks) -> dict:
    eco = ecosystems.get(key)
    if eco.KEY != key:
        raise HTTPException(status_code=404, detail=f"Unknown ecosystem: {key}")

    now = time.monotonic()
    last = _last_refresh.get(key, 0.0)
    elapsed = now - last
    if elapsed < MIN_REFRESH_INTERVAL_SEC:
        wait = int(MIN_REFRESH_INTERVAL_SEC - elapsed) + 1
        raise HTTPException(
            status_code=429,
            detail=f"Wait {wait}s before refreshing {eco.NAME} again",
        )
    _last_refresh[key] = now

    cleared = cache_admin.clear_ecosystem_caches(key)
    # Re-warm in the background so subsequent GETs are fast.
    background_tasks.add_task(warmup.warm_ecosystem_sync, key)
    return {"status": "ok", "key": key, "cleared": cleared}
