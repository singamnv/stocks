---
name: run
description: Launch the NVIDIA Ecosystem Tracker dev servers (FastAPI on :8000, Vite on :5173) via the root `npm run dev` script. Use when the user asks to run, start, launch, or open the dashboard.
---

# Run the dashboard

This project has a one-command dev setup. From the project root run:

```
npm run dev
```

That uses `concurrently` to start both:
- **backend** — `uvicorn app.main:app --reload --port 8000 --app-dir backend`
- **frontend** — `vite` on port 5173 (proxies `/api` → `:8000`)

Run it with `run_in_background: true`. Watch the output until you see both:
- `Uvicorn running on http://127.0.0.1:8000`
- `Local:   http://localhost:5173/`

Then report `http://localhost:5173` to the user.

## Preflight (only if `npm run dev` errors)

- `concurrently: command not found` or any "module not found" → run `npm run install:all` first (installs root devDeps, frontend deps, and Python deps in one go).
- `FINNHUB_API_KEY not configured` warnings in the UI → app still works; News + Earnings tabs are degraded until the key is added to `backend/.env`.
- Port 8000 or 5173 already in use → find the offender (`netstat -ano | findstr :8000` on Windows) and ask the user before killing anything.

## Stop

The background process keeps both servers alive. Stop with the harness shutdown — do not `taskkill` without asking.
