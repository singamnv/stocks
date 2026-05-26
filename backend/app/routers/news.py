from typing import Optional

from fastapi import APIRouter, Query

from .. import ecosystems
from ..config import settings
from ..schemas import NewsItem, NewsResponse
from ..services.finnhub_service import get_news

router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("", response_model=NewsResponse)
def list_news(
    ecosystem: str = Query(ecosystems.DEFAULT_KEY),
    ticker: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = Query(100, ge=1, le=500),
) -> NewsResponse:
    if not settings.FINNHUB_API_KEY:
        return NewsResponse(items=[], warning="FINNHUB_API_KEY not configured")

    eco = ecosystems.get(ecosystem)
    items = get_news(eco.KEY)
    if ticker:
        items = [n for n in items if n["ticker"] == ticker.upper()]
    if category:
        items = [n for n in items if n["category"] == category]
    items = items[:limit]
    return NewsResponse(items=[NewsItem(**n) for n in items])
