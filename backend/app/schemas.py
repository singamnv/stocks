from typing import Optional

from pydantic import BaseModel


class TickerQuote(BaseModel):
    symbol: str
    name: str
    category: str
    price: Optional[float] = None
    change_pct: Optional[float] = None
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    ytd_pct: Optional[float] = None
    one_year_pct: Optional[float] = None
    error: Optional[str] = None


class TickerGroup(BaseModel):
    category: str
    tickers: list[TickerQuote]


class GridResponse(BaseModel):
    groups: list[TickerGroup]


class KpiResponse(BaseModel):
    nvda_price: Optional[float] = None
    nvda_change_pct: Optional[float] = None
    total_market_cap: Optional[float] = None
    earnings_this_week: int = 0
    avg_change_pct: Optional[float] = None


class TickerDetail(BaseModel):
    symbol: str
    name: str
    category: str
    role: str
    price: Optional[float] = None
    change_pct: Optional[float] = None
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    revenue: Optional[float] = None
    gross_margins: Optional[float] = None
    free_cashflow: Optional[float] = None
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low: Optional[float] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None


class PricePoint(BaseModel):
    t: int  # unix ms
    c: float  # close price


class HistoryResponse(BaseModel):
    symbol: str
    range: str
    points: list[PricePoint]


class NewsItem(BaseModel):
    id: str
    title: str
    source: str
    url: str
    timestamp: int  # unix seconds
    ticker: str
    category: str
    image: Optional[str] = None
    summary: Optional[str] = None


class NewsResponse(BaseModel):
    items: list[NewsItem]
    warning: Optional[str] = None


class EarningsItem(BaseModel):
    date: str  # YYYY-MM-DD
    ticker: str
    name: str
    category: str
    hour: Optional[str] = None  # 'bmo' | 'amc' | 'dmh'
    eps_estimate: Optional[float] = None
    revenue_estimate: Optional[float] = None


class EarningsResponse(BaseModel):
    items: list[EarningsItem]
    warning: Optional[str] = None


class MarketRow(BaseModel):
    symbol: str
    name: str
    price: Optional[float] = None
    change_pct: Optional[float] = None


class RatesRow(BaseModel):
    label: str
    yield_pct: Optional[float] = None
    bps_change: Optional[float] = None


class VixData(BaseModel):
    spot: Optional[float] = None
    three_month: Optional[float] = None
    term_ratio: Optional[float] = None


class BriefVitals(BaseModel):
    futures: list[MarketRow]
    fx_commodities: list[MarketRow]
    rates: list[RatesRow]
    vix: VixData


class BriefTape(BaseModel):
    asia: list[MarketRow]
    europe: list[MarketRow]
    us: list[MarketRow]


class BriefResponse(BaseModel):
    vitals: BriefVitals
    tape: BriefTape
    sectors: list[MarketRow]


class AiBriefBullet(BaseModel):
    title: str
    body: str
    tickers: list[str]


class AiBriefWatchItem(BaseModel):
    label: str
    when: Optional[str] = None


class AiBriefResponse(BaseModel):
    date: str  # YYYY-MM-DD (ET)
    headline: str
    bullets: list[AiBriefBullet]
    watch_today: list[AiBriefWatchItem]
    model: str
    generated_at: int  # unix seconds


class EcosystemMeta(BaseModel):
    key: str
    name: str
    group: str
    description: str
    anchor_ticker: str
    categories: dict[str, str]  # category name -> description


class EcosystemsResponse(BaseModel):
    ecosystems: list[EcosystemMeta]
    default_key: str
