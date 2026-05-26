# NVIDIA Ecosystem Tracker

A single-page dashboard for monitoring NVIDIA's key suppliers, partners, and direct investments — prices, fundamentals, news, and earnings — in one place.

## Quick start

```sh
npm run install:all                 # installs root, frontend, and backend deps
cp .env.example backend/.env        # then paste your Finnhub key into backend/.env
npm run dev                         # starts backend (:8000) + frontend (:5173)
```

Open http://localhost:5173.

## Stack

- **Backend:** FastAPI + yfinance + Finnhub (httpx) + cachetools in-memory TTL.
- **Frontend:** Vite + React + TypeScript + Tailwind + Recharts + TanStack Query.
- No database. All caching in memory.

## Configuration

`backend/.env`:

```
FINNHUB_API_KEY=your_key_here   # https://finnhub.io free tier
CORS_ORIGIN=http://localhost:5173
```

Without a Finnhub key the app still loads — prices, fundamentals, and charts work fine, but the News and Earnings tabs show a "key not configured" warning.

## Adding a ticker

Edit `backend/app/ecosystem.py`:

1. Add the symbol to the appropriate list in `ECOSYSTEM`.
2. Add a 1–2 sentence role blurb in `ROLES`.

That's the only change needed. The frontend grid, news filter, earnings list, and KPI bar all derive from this file.

## Endpoints

| Route | Purpose |
|---|---|
| `GET /api/kpis` | Header bar: NVDA price, ecosystem mcap, earnings-this-week, avg %chg |
| `GET /api/tickers` | Grid: quotes for every tracked ticker, grouped by category |
| `GET /api/tickers/{symbol}` | Detail: fundamentals + supply-chain role |
| `GET /api/tickers/{symbol}/history?range=1D\|1W\|1M\|1Y\|5Y` | Price history |
| `GET /api/news?ticker=&category=` | Aggregated Finnhub news |
| `GET /api/earnings` | Upcoming earnings for tracked tickers |
| `GET /health` | Health check |

FastAPI docs: http://localhost:8000/docs
