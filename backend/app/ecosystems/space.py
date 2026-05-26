"""Space — launch, satellites, defense primes, earth observation, components."""

KEY = "space"
NAME = "Space"
GROUP = "Tech"
DESCRIPTION = "Space launch, satellites and connectivity, defense primes with space exposure, earth-observation, and the subsystem supply chain."
ANCHOR_TICKER = "RKLB"

ECOSYSTEM: dict[str, list[str]] = {
    "Launch":                     ["RKLB", "ASTS", "LUNR"],
    "Satellites & Connectivity":  ["IRDM", "GSAT", "VSAT"],
    "Defense Primes":             ["LMT", "NOC", "BA", "RTX"],
    "Earth Observation":          ["PL", "BKSY"],
    "Components & Subsystems":    ["KTOS", "MRCY", "HEI"],
}

ROLES: dict[str, str] = {
    "RKLB":  "Rocket Lab — Electron small-sat launch and Neutron medium-lift in development; spacecraft systems business.",
    "ASTS":  "AST SpaceMobile — direct-to-cellphone satellite connectivity; commercial service ramping.",
    "LUNR":  "Intuitive Machines — lunar landers and NASA CLPS payloads.",
    "IRDM":  "Iridium — global L-band satellite voice and data network.",
    "GSAT":  "Globalstar — MSS network; Apple iPhone emergency-SOS partner.",
    "VSAT":  "Viasat — broadband satellite; Inmarsat acquisition expanded global reach.",
    "LMT":   "Lockheed Martin — defense prime with large space systems franchise (missile warning, GPS).",
    "NOC":   "Northrop Grumman — defense prime; Cygnus cargo, missile defense, classified space.",
    "BA":    "Boeing — Starliner, GPS III, ULA stake (joint venture being divested).",
    "RTX":   "RTX — Raytheon space systems and Collins Aerospace.",
    "PL":    "Planet Labs — daily earth-observation constellation; defense and commercial customers.",
    "BKSY":  "BlackSky — high-revisit SAR and EO imagery; defense-heavy customer mix.",
    "KTOS":  "Kratos Defense — unmanned systems, hypersonics, satellite ground systems.",
    "MRCY":  "Mercury Systems — defense / space electronics and processing subsystems.",
    "HEI":   "HEICO — defense / commercial aerospace components and electronics.",
}

CATEGORY_DESC: dict[str, str] = {
    "Launch":                     "Public small-and-medium-lift launch providers.",
    "Satellites & Connectivity":  "Operators of satellite voice / data / broadband networks.",
    "Defense Primes":             "Large primes with significant space-systems exposure.",
    "Earth Observation":          "EO and SAR imagery providers serving defense and commercial.",
    "Components & Subsystems":    "Defense electronics and aerospace component suppliers.",
}
