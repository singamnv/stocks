"""Multi-ecosystem registry.

Each module under this package owns one ecosystem's curated data
(KEY / NAME / DESCRIPTION / ANCHOR_TICKER / ECOSYSTEM / ROLES / CATEGORY_DESC).
The registry below is the single point of lookup used by routers + services.

To add an ecosystem: create `ecosystems/<key>.py` and add it to the import +
ECOSYSTEMS list below. That's it.
"""
from types import ModuleType
from typing import Optional

from . import (
    amd,
    automotive,
    biotech,
    crypto,
    cyber,
    fintech,
    hyperscaler,
    nvidia,
    power,
    quantum,
    robotics,
    semis,
    space,
)

# Order here determines tab order in the UI.
_MODULES: list[ModuleType] = [
    nvidia, amd, hyperscaler, automotive, power,
    semis, robotics, quantum, cyber, space,
    fintech, crypto, biotech,
]
ECOSYSTEMS: dict[str, ModuleType] = {m.KEY: m for m in _MODULES}

DEFAULT_KEY = "nvidia"


def get(key: Optional[str]) -> ModuleType:
    """Resolve an ecosystem module by key, falling back to the default."""
    return ECOSYSTEMS.get(key or DEFAULT_KEY) or ECOSYSTEMS[DEFAULT_KEY]


def all_keys() -> list[str]:
    return [m.KEY for m in _MODULES]


def all_modules() -> list[ModuleType]:
    return list(_MODULES)


def all_tickers(eco: ModuleType) -> list[str]:
    return [t for tickers in eco.ECOSYSTEM.values() for t in tickers]


def ticker_to_category(eco: ModuleType) -> dict[str, str]:
    return {t: cat for cat, tickers in eco.ECOSYSTEM.items() for t in tickers}


def find_first_containing(symbol: str) -> Optional[ModuleType]:
    """Return the first ecosystem module that includes `symbol` (case-insensitive)."""
    symbol = symbol.upper()
    for m in _MODULES:
        if symbol == m.ANCHOR_TICKER or symbol in all_tickers(m):
            return m
    return None
