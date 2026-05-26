"""Generates the daily AI Brief by calling Claude Haiku 4.5 with structured output.

Inputs are assembled from existing services (news, macro, ecosystem, earnings).
Retries once on Pydantic validation failure. Caches the system prompt for the
benefit of dev-loop iterations (multiple regens within the 5-min TTL).
"""
import json
import time
from datetime import datetime
from typing import Any

import anthropic
from pydantic import ValidationError

from ..config import settings
from ..ecosystems import nvidia as nvidia_eco
from ..schemas import AiBriefBullet, AiBriefResponse, AiBriefWatchItem
from .brief_cache import today_et
from .finnhub_service import get_earnings, get_news, has_key as finnhub_has_key
from .macro_service import get_brief as get_macro
from .yf_service import get_grid

NVDA_TICKER = nvidia_eco.ANCHOR_TICKER
NVDA_ECO_KEY = nvidia_eco.KEY

MODEL = "claude-haiku-4-5"
MAX_TOKENS = 4096

# Note on prompt caching: Haiku 4.5's minimum cacheable prefix is 4096 tokens.
# This system prompt is ~1.5k tokens, so `cache_control` will NOT actually
# engage today — it's wired up so that (a) it costs nothing if inert and
# (b) if the prompt grows past the threshold later, caching activates without
# any code change. Even at full size, the production use case is one call/day,
# so caching only helps during prompt-iteration regens within a 5-min window.
SYSTEM_PROMPT = """You are the morning analyst for an AI-infrastructure investing dashboard. You write a daily brief for a $4.99/mo retail product.

Your readers care about:
- NVIDIA and its suppliers (TSMC, ARM, Micron, SanDisk, Western Digital)
- Advanced packaging / OSAT (ASE, Amkor, Camtek)
- Wafer equipment (KLA, Lam Research, ASML, Keysight)
- Optical networking (Coherent, Corning, Fabrinet, Lumentum, Amphenol)
- Server OEMs (Dell, Super Micro, Jabil)
- AI data center power (Flex, Vertiv, Eaton, STMicro, Analog Devices, Monolithic Power, Navitas, onsemi)
- NVIDIA direct investments (CoreWeave, Nebius, Nokia, Synopsys)
- Hyperscaler capex from Meta, Google, Amazon, Microsoft

Tone: smart, terse, opinionated. Senior analyst writing for senior analysts.

Rules:
- Never speculate beyond the supplied data.
- Every bullet must connect to specific tickers — list them in `tickers`.
- Where possible, identify a supply-chain link the reader would miss looking at a single ticker (e.g., "TSM CoWoS tightening -> NVDA supply constraint -> SMCI guidance risk").
- `headline`: <= 12 words, punchy, no clickbait. State the move or thesis.
- Bullet `title`: 4-8 words.
- Bullet `body`: 1-2 sentences. State the fact, then the why-it-matters.
- `watch_today`: exactly 3 items. Concrete events with timing where known (e.g., "FOMC minutes 2pm ET", "NVDA earnings after close", "ISM Manufacturing 10am ET"). No filler.
- Exactly 5 bullets. Exactly 3 watch items.
- No markdown in any field.

Output strict JSON matching the provided schema."""


def _build_user_payload() -> dict:
    """Assemble today's facts as a structured payload for Claude."""
    # Ecosystem snapshot: NVDA + top 8 gainers + top 8 losers (so the model
    # sees concentration, not just the alphabet).
    grid = get_grid(NVDA_ECO_KEY)
    with_pct = [g for g in grid if g.get("change_pct") is not None]
    gainers = sorted(with_pct, key=lambda g: g["change_pct"], reverse=True)[:8]
    losers = sorted(with_pct, key=lambda g: g["change_pct"])[:8]
    nvda = next((g for g in grid if g["symbol"] == NVDA_TICKER), None)
    ecosystem_rows: list[dict] = []
    seen: set[str] = set()
    for row in ([nvda] if nvda else []) + gainers + losers:
        if not row or row["symbol"] in seen:
            continue
        seen.add(row["symbol"])
        ecosystem_rows.append({
            "symbol": row["symbol"],
            "name": row.get("name"),
            "category": row.get("category"),
            "price": row.get("price"),
            "change_pct": round(row["change_pct"], 2) if row.get("change_pct") is not None else None,
        })

    # News: most recent 25 across all tracked tickers.
    news_rows: list[dict] = []
    if finnhub_has_key():
        for n in get_news(NVDA_ECO_KEY)[:25]:
            news_rows.append({
                "ticker": n.get("ticker"),
                "headline": n.get("title"),
                "source": n.get("source"),
                "ts": n.get("timestamp"),
            })

    # Macro vitals (futures, rates, vix).
    macro = get_macro()

    # Earnings in the next 7 days only.
    upcoming: list[dict] = []
    if finnhub_has_key():
        today_iso = today_et()
        for e in get_earnings(NVDA_ECO_KEY, days_ahead=7):
            if e.get("date") and e["date"] >= today_iso:
                upcoming.append({
                    "date": e["date"],
                    "ticker": e["ticker"],
                    "hour": e.get("hour"),
                })

    return {
        "today_et": today_et(),
        "ecosystem": ecosystem_rows,
        "recent_news": news_rows,
        "macro": {
            "futures": macro["vitals"]["futures"],
            "rates": macro["vitals"]["rates"],
            "vix": macro["vitals"]["vix"],
            "us_indices": macro["tape"]["us"],
            "sectors": macro["sectors"],
        },
        "upcoming_earnings": upcoming,
    }


def _call_claude(payload: dict, schema: dict) -> str:
    """Single Claude call. Returns the raw JSON text from the response."""
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": json.dumps(payload, default=str, sort_keys=True),
            }
        ],
        output_config={"format": {"type": "json_schema", "schema": schema}},
    )
    # Find the text block in the response.
    for block in response.content:
        if getattr(block, "type", None) == "text":
            return block.text
    raise RuntimeError("Claude returned no text block")


def _parse(raw: str, generated_at: int) -> AiBriefResponse:
    data = json.loads(raw)
    # Stamp model + timestamp + date here so the schema we send to Claude
    # only contains the fields the model needs to fill in.
    return AiBriefResponse(
        date=today_et(),
        headline=data["headline"],
        bullets=[AiBriefBullet(**b) for b in data["bullets"]],
        watch_today=[AiBriefWatchItem(**w) for w in data["watch_today"]],
        model=MODEL,
        generated_at=generated_at,
    )


# Schema we hand to Claude — only the model-filled fields (no `date`, `model`, `generated_at`).
CLAUDE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["headline", "bullets", "watch_today"],
    "properties": {
        "headline": {"type": "string"},
        "bullets": {
            "type": "array",
            "minItems": 5,
            "maxItems": 5,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["title", "body", "tickers"],
                "properties": {
                    "title": {"type": "string"},
                    "body": {"type": "string"},
                    "tickers": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
            },
        },
        "watch_today": {
            "type": "array",
            "minItems": 3,
            "maxItems": 3,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["label"],
                "properties": {
                    "label": {"type": "string"},
                    "when": {"type": ["string", "null"]},
                },
            },
        },
    },
}


def generate_brief() -> AiBriefResponse:
    """Build inputs, call Claude, validate, retry once on schema failure."""
    if not settings.ANTHROPIC_API_KEY:
        raise RuntimeError("ANTHROPIC_API_KEY not configured")

    payload = _build_user_payload()
    now = int(time.time())

    try:
        raw = _call_claude(payload, CLAUDE_SCHEMA)
        return _parse(raw, generated_at=now)
    except (ValidationError, json.JSONDecodeError, KeyError) as first_err:
        # Retry once — structured outputs occasionally hiccup on first try.
        try:
            raw = _call_claude(payload, CLAUDE_SCHEMA)
            return _parse(raw, generated_at=int(time.time()))
        except (ValidationError, json.JSONDecodeError, KeyError) as second_err:
            raise RuntimeError(
                f"Brief generation failed both attempts: {first_err!r} / {second_err!r}"
            )
