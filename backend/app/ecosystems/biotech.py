"""Hot Biotech — GLP-1 / obesity, gene & cell therapy, AI drug discovery, mRNA."""

KEY = "biotech"
NAME = "Hot Biotech"
GROUP = "Healthcare"
DESCRIPTION = "The biotech themes most-discussed by investors today: GLP-1 / obesity, gene and cell therapy, AI drug discovery, and mRNA."
ANCHOR_TICKER = "LLY"

ECOSYSTEM: dict[str, list[str]] = {
    "GLP-1 / Obesity":        ["LLY", "NVO", "AMGN", "VKTX", "ALT", "ZLDPF"],
    "Gene & Cell Therapy":    ["VRTX", "CRSP", "BEAM", "NTLA"],
    "AI Drug Discovery":      ["RXRX", "SDGR", "ABCL", "TEM"],
    "mRNA":                   ["MRNA", "BNTX"],
}

ROLES: dict[str, str] = {
    "LLY":   "Eli Lilly — Zepbound / Mounjaro (tirzepatide) leader; expanding into Alzheimer's and oncology.",
    "NVO":   "Novo Nordisk — Wegovy / Ozempic (semaglutide) leader; next-gen amycretin and CagriSema in development.",
    "AMGN":  "Amgen — MariTide (monthly GLP-1 + GIP antagonist) in obesity development.",
    "VKTX":  "Viking Therapeutics — VK2735 dual GLP-1/GIP in Phase 2 obesity trials.",
    "ALT":   "Altimmune — pemvidutide GLP-1/glucagon dual agonist in obesity and NASH.",
    "ZLDPF": "Zealand Pharma (OTC ADR) — broad GLP-1 / amylin pipeline; partnerships with Novo and Boehringer.",
    "VRTX":  "Vertex Pharmaceuticals — CRISPR-based Casgevy approved for sickle cell; non-opioid pain (suzetrigine).",
    "CRSP":  "CRISPR Therapeutics — Casgevy co-developer; in vivo gene-editing pipeline.",
    "BEAM":  "Beam Therapeutics — base editing for sickle cell and other genetic diseases.",
    "NTLA":  "Intellia Therapeutics — in vivo CRISPR delivery; lead programs in ATTR and HAE.",
    "RXRX":  "Recursion Pharmaceuticals — AI-driven drug discovery; NVIDIA partnership.",
    "SDGR":  "Schrodinger — physics-based computational drug discovery platform.",
    "ABCL":  "AbCellera — AI-enabled antibody discovery platform.",
    "TEM":   "Tempus AI — clinical-grade AI for oncology and life sciences.",
    "MRNA":  "Moderna — mRNA platform; oncology, RSV, flu, CMV pipeline.",
    "BNTX":  "BioNTech — mRNA platform; oncology and infectious disease pipeline.",
}

CATEGORY_DESC: dict[str, str] = {
    "GLP-1 / Obesity":        "GLP-1 leaders and emerging dual / triple agonists.",
    "Gene & Cell Therapy":    "CRISPR and base-editing pure-plays plus approved gene-therapy franchises.",
    "AI Drug Discovery":      "AI- and ML-driven drug discovery platforms.",
    "mRNA":                   "mRNA platform companies beyond COVID vaccines.",
}
