# NVIDIA Ecosystem Tracker

Single-page dashboard for monitoring NVIDIA's suppliers, partners, and direct investments. Localhost-only, no database, in-memory caching.

## Stack

- **Backend:** FastAPI (Python 3.11+), yfinance, Finnhub (via httpx), cachetools.
- **Frontend:** Vite + React 18 + TypeScript + Tailwind, Recharts for charts, TanStack Query for fetching/caching.
- **Run:** `npm run dev` at repo root (uses `concurrently` to start both servers).

## Layout

```
backend/app/
  ecosystems/        # one module per ecosystem; KEY/NAME/DESCRIPTION/ANCHOR_TICKER/ECOSYSTEM/ROLES/CATEGORY_DESC
    __init__.py      #   registry: ECOSYSTEMS dict, get(key), all_tickers(eco), ticker_to_category(eco)
    nvidia.py        #   NVIDIA + supply chain (33 tickers, 10 categories)
    amd.py           #   AMD Instinct stack
    hyperscaler.py   #   Custom silicon at META/GOOG/AMZN/MSFT + their fabless partners
    automotive.py    #   Self-driving + EV compute + sensors + lidar
    power.py         #   Data center power + IPPs + nuclear
  schemas.py         # Pydantic response models — MIRROR in frontend/src/types/api.ts
  cache.py           # @cached(name, ttl) decorator using cachetools.TTLCache
  config.py          # pydantic-settings, reads backend/.env
  services/yf_service.py        # yfinance wrappers (per-ticker shared across ecosystems; get_grid takes eco_key)
  services/finnhub_service.py   # Finnhub REST wrappers (per-ticker shared; get_news/get_earnings take eco_key)
  routers/{kpis,tickers,news,earnings,ecosystems}.py  # all accept ?ecosystem=<key>
  main.py            # FastAPI app + CORS + router mounting

frontend/src/
  pages/Dashboard.tsx
  components/{KpiBar,EcosystemGrid,EcosystemCards,EcosystemTable,EcosystemTabs,TickerCard,DetailDrawer,PriceChart,RangeToggle,NewsFeed,NewsItem,EarningsCalendar,Tabs}.tsx
  types/api.ts       # MIRROR of backend/app/schemas.py
  lib/{api,queryClient,format,ecosystem}.tsx
```

## Conventions

- **Ticker universe:** add/remove tickers only in `backend/app/ecosystems/<key>.py`. Adding a new ecosystem = new module + one import line in `ecosystems/__init__.py`. Use the **ecosystem-data** subagent.
- **Active ecosystem:** every collection endpoint takes `?ecosystem=<key>` (default `nvidia`). Frontend state lives in `lib/ecosystem.tsx` (`useEcosystem()`, `useActiveEcosystem()`); persisted in localStorage as `ecosystem:active`.
- **Schema sync:** when changing `schemas.py` or any router response, also update `frontend/src/types/api.ts`. Use the **api-contract** subagent.
- **Cache TTLs:** quotes/grid/detail = 5 min (300s); history/news/earnings = 15 min (900s). Set via `@cached("name", ttl=seconds)` in `cache.py`. Aggregate-fetch caches partition automatically by `eco_key`; per-ticker caches are shared across ecosystems.
- **Per-ticker failure:** wrap yfinance calls so one bad symbol doesn't fail the whole grid — return that row with `error: "..."` instead.
- **Finnhub optional:** if `FINNHUB_API_KEY` is missing, news + earnings endpoints return `{items: [], warning: "..."}` rather than 500. UI shows a soft banner.
- **CORS:** allow only `http://localhost:5173`. This is a localhost-only tool.
- **No premature abstractions.** Routers are thin; logic lives in `services/`.

## .claude/ helpers

- `.claude/skills/run/SKILL.md` — `/run` to launch both dev servers.
- `.claude/agents/ecosystem-data.md` — subagent for ticker map + role blurbs.
- `.claude/agents/api-contract.md` — subagent that keeps FE/BE types in sync.

## Out of scope (v1)

No auth, no users, no DB, no deploy config, no tests, no alerts, no options data.
