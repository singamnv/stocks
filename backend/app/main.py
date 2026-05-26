import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers import ai_brief, brief, earnings, ecosystems, kpis, news, tickers
from .services.warmup import warm_default_ecosystem

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Kick off cache warmup in the background — server is ready to serve immediately.
    task = asyncio.create_task(warm_default_ecosystem())
    try:
        yield
    finally:
        task.cancel()


app = FastAPI(title="NVIDIA Ecosystem Tracker", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CORS_ORIGIN],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(kpis.router)
app.include_router(tickers.router)
app.include_router(news.router)
app.include_router(earnings.router)
app.include_router(brief.router)
app.include_router(ai_brief.router)
app.include_router(ecosystems.router)


@app.get("/health")
def health() -> dict:
    from .services.yf_service import rate_limit_status
    return {
        "status": "ok",
        "finnhub_configured": bool(settings.FINNHUB_API_KEY),
        "yfinance": rate_limit_status(),
    }
