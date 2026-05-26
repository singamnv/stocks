"""Fintech & Payments — networks, neobanks/brokers, BNPL, card/POS. Crypto names live in `crypto.py`."""

KEY = "fintech"
NAME = "Fintech"
GROUP = "Finance"
DESCRIPTION = "Payment networks, neobanks and brokers, buy-now-pay-later, and card/POS hardware."
ANCHOR_TICKER = "V"

ECOSYSTEM: dict[str, list[str]] = {
    "Payment Networks":       ["V", "MA", "AXP", "PYPL"],
    "Neobanks & Brokers":     ["SOFI", "HOOD", "NU"],
    "Buy-Now-Pay-Later":      ["AFRM", "UPST"],
    "Card / POS Hardware":    ["XYZ", "FOUR", "FISV"],
}

ROLES: dict[str, str] = {
    "V":     "Visa — dominant global card-network rails; interchange and cross-border fee revenue.",
    "MA":    "Mastercard — second card network; faster international growth than Visa.",
    "AXP":   "American Express — closed-loop card network with affluent cardholder franchise.",
    "PYPL":  "PayPal — branded checkout and Braintree merchant platform.",
    "SOFI":  "SoFi — neobank with lending, brokerage, and crypto.",
    "HOOD":  "Robinhood — retail brokerage with rising crypto and derivatives revenue.",
    "NU":    "Nubank — Brazilian neobank serving Latin America at scale.",
    "AFRM":  "Affirm — buy-now-pay-later checkout; major Amazon, Apple, Shopify integrations.",
    "UPST":  "Upstart — AI-driven consumer lending platform; rate-cycle-sensitive.",
    "XYZ":   "Block (rebranded from Square / SQ) — Square seller ecosystem and Cash App; bitcoin treasury exposure.",
    "FOUR":  "Shift4 — payment processing for hospitality and verticals.",
    "FISV":  "Fiserv — core banking and merchant acquiring at scale (Clover POS).",
}

CATEGORY_DESC: dict[str, str] = {
    "Payment Networks":       "Card networks and payment-processing franchises.",
    "Neobanks & Brokers":     "Mobile-first banks and brokerages.",
    "Buy-Now-Pay-Later":      "BNPL and AI-driven consumer lending.",
    "Card / POS Hardware":    "Card processing, POS systems, and merchant tech.",
}
