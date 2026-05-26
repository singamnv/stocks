"""Crypto — exchanges, treasury holders, miners, spot ETFs."""

KEY = "crypto"
NAME = "Crypto"
GROUP = "Finance"
DESCRIPTION = "Crypto exchanges and brokers, balance-sheet bitcoin holders, mining infrastructure, and spot ETF wrappers."
ANCHOR_TICKER = "COIN"

ECOSYSTEM: dict[str, list[str]] = {
    "Exchanges & Brokers":  ["COIN", "HOOD"],
    "Treasury Holders":     ["MSTR"],
    "Miners":               ["MARA", "RIOT", "CLSK", "BITF", "HUT", "CIFR"],
    "Spot ETFs":            ["IBIT", "FBTC", "ETHA", "GBTC"],
}

ROLES: dict[str, str] = {
    "COIN":  "Coinbase — largest US crypto exchange; revenue scales with trading volumes and on-chain activity.",
    "HOOD":  "Robinhood — retail brokerage with rapidly growing crypto trading revenue.",
    "MSTR":  "MicroStrategy — software company turned bitcoin treasury vehicle; largest corporate BTC holder.",
    "MARA":  "Marathon Digital — largest publicly traded US bitcoin miner.",
    "RIOT":  "Riot Platforms — vertically integrated US bitcoin miner.",
    "CLSK":  "CleanSpark — bitcoin miner with low-cost power footprint in Georgia and Mississippi.",
    "BITF":  "Bitfarms — Canadian-listed bitcoin miner with international operations.",
    "HUT":   "Hut 8 — bitcoin miner; partnership with Coatue / DRML and high-density compute hosting pivot.",
    "CIFR":  "Cipher Mining — pure-play US bitcoin miner.",
    "IBIT":  "iShares Bitcoin Trust — BlackRock spot bitcoin ETF; the dominant wrapper for new institutional inflows.",
    "FBTC":  "Fidelity Wise Origin Bitcoin Fund — Fidelity spot bitcoin ETF.",
    "ETHA":  "iShares Ethereum Trust — BlackRock spot ether ETF.",
    "GBTC":  "Grayscale Bitcoin Trust — legacy bitcoin trust converted to spot ETF.",
}

CATEGORY_DESC: dict[str, str] = {
    "Exchanges & Brokers":  "Public companies that monetize crypto trading volume.",
    "Treasury Holders":     "Operating companies holding bitcoin as primary treasury asset.",
    "Miners":               "Publicly traded bitcoin miners.",
    "Spot ETFs":            "Spot bitcoin and ether ETFs available to US retail.",
}
