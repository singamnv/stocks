"""AI Power & Cooling — the trade behind AI data center electricity demand."""

KEY = "power"
NAME = "AI Power & Cooling"
GROUP = "AI"
DESCRIPTION = "Data-center power and cooling infrastructure plus the IPPs, utilities, and nuclear pure-plays meeting AI's electricity demand."
ANCHOR_TICKER = "VRT"

ECOSYSTEM: dict[str, list[str]] = {
    "Cooling / Power Infra": ["VRT", "ETN", "FLEX", "GEV", "EMR"],
    "IPPs":                  ["VST", "CEG", "TLN", "NRG"],
    "Nuclear Pure-Play":     ["OKLO", "SMR", "BWXT", "LEU"],
    "Utilities":             ["NEE", "DUK", "SO", "AEP"],
    "Grid Buildout":         ["PWR", "MYRG"],
}

ROLES: dict[str, str] = {
    "VRT":  "Vertiv — direct beneficiary of AI capex; liquid cooling, power distribution, switchgear for GPU racks.",
    "ETN":  "Eaton — UPS, switchgear, busways, transformers — entire low-voltage power chain for AI data centers.",
    "FLEX": "Flex — contract manufacturing of power shelves, busbars, BBUs at hyperscaler scale.",
    "GEV":  "GE Vernova — gas turbines and grid equipment in high demand as utilities scale up generation for AI loads.",
    "EMR":  "Emerson — automation and cooling controls in data center build-out.",
    "VST":  "Vistra — IPP with the largest US nuclear fleet outside the regulated utilities; AI-data-center PPAs.",
    "CEG":  "Constellation Energy — biggest US nuclear IPP; Microsoft Three Mile Island PPA and Meta deals.",
    "TLN":  "Talen Energy — nuclear and natural gas IPP; signed AWS hyperscale campus PPA at Susquehanna.",
    "NRG":  "NRG — Texas-heavy power generation and retail; AI data-center demand re-rating thesis.",
    "OKLO": "Oklo — small modular reactor (SMR) developer targeting data-center campus deployment.",
    "SMR":  "NuScale — first NRC-certified small modular reactor design.",
    "BWXT": "BWX Technologies — nuclear components, fuel, and SMR work for government and commercial.",
    "LEU":  "Centrus Energy — HALEU fuel enrichment, critical for advanced reactors.",
    "NEE":  "NextEra — largest US renewables developer plus FPL utility; significant data-center power sales.",
    "DUK":  "Duke Energy — Carolinas utility with major data-center load growth from AI build-out.",
    "SO":   "Southern Company — Georgia / Alabama utility; Vogtle nuclear; growing data-center customer base.",
    "AEP":  "American Electric Power — Midwest / Texas footprint at the center of data-center demand growth.",
    "PWR":  "Quanta Services — utility-scale grid construction; massive backlog from data-center transmission builds.",
    "MYRG": "MYR Group — transmission and distribution contractor; same AI-grid build-out tailwind.",
}

CATEGORY_DESC: dict[str, str] = {
    "Cooling / Power Infra": "Vertiv-style power and cooling sold into AI data centers directly.",
    "IPPs":                  "Independent power producers selling generation to hyperscalers via PPA.",
    "Nuclear Pure-Play":     "SMR developers and nuclear-fuel pure-plays — the long-tail nuclear bet.",
    "Utilities":             "Regulated utilities seeing material load growth from AI data centers.",
    "Grid Buildout":         "Contractors building the transmission and substation capacity for new loads.",
}
