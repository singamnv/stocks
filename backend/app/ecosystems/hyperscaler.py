"""Hyperscaler Custom Silicon — every cloud is designing its own AI chip."""

KEY = "hyperscaler"
NAME = "Hyperscaler Silicon"
GROUP = "AI"
DESCRIPTION = "The 'in-house chip' thesis — hyperscalers, their fabless silicon partners (Broadcom, Marvell, Credo), and the surrounding fabric."
ANCHOR_TICKER = "AVGO"

ECOSYSTEM: dict[str, list[str]] = {
    "Hyperscalers":      ["META", "GOOGL", "AMZN", "MSFT", "ORCL"],
    "Silicon Partners":  ["AVGO", "MRVL", "CRDO", "SNPS"],
    "Networking":        ["ANET", "JNPR", "CSCO", "COHR"],
    "Memory":            ["MU"],
    "Fab":               ["TSM"],
    "Power Systems":     ["VRT", "ETN"],
}

ROLES: dict[str, str] = {
    "META":  "Designs MTIA accelerators with Broadcom; massive AI capex commitments.",
    "GOOGL": "Designs TPU v5p/v6 with Broadcom; AI training and inference at scale.",
    "AMZN":  "AWS Trainium / Inferentia designed with Marvell-derived team Annapurna Labs.",
    "MSFT":  "Azure Maia accelerator co-designed with Marvell; major AI capex driver.",
    "ORCL":  "Oracle Cloud Infrastructure — large GPU and custom silicon deployments tied to OpenAI deals.",
    "AVGO":  "Broadcom — co-designs custom AI ASICs for Google (TPU), Meta (MTIA), and emerging customers including OpenAI.",
    "MRVL":  "Marvell — co-designs Trainium / Maia / Microsoft and AWS custom silicon; also DPU/SmartNIC.",
    "CRDO":  "Credo — interconnect SerDes IP and AECs used in Trainium and Maia AI clusters.",
    "SNPS":  "Synopsys — EDA tools and silicon IP behind every hyperscaler custom chip program.",
    "ANET":  "Arista — Ethernet switching dominant in hyperscaler AI fabrics.",
    "JNPR":  "Juniper — AI-cluster networking; HPE acquisition adds depth to AI campus builds.",
    "CSCO":  "Cisco — Silicon One for hyperscaler fabrics plus Splunk observability across AI infra.",
    "COHR":  "Coherent — 800G / 1.6T optics for hyperscaler AI scale-out fabrics.",
    "MU":    "Micron — HBM supplier across hyperscaler custom accelerators and merchant GPUs alike.",
    "TSM":   "Manufactures TPU, MTIA, Trainium, Maia and the rest of the hyperscaler custom-silicon roadmap.",
    "VRT":   "Vertiv — power and cooling for hyperscaler AI data centers irrespective of silicon choice.",
    "ETN":   "Eaton — UPS, switchgear, busways for AI data center build-out.",
}

CATEGORY_DESC: dict[str, str] = {
    "Hyperscalers":     "Cloud / AI buyers designing their own AI silicon.",
    "Silicon Partners": "Fabless co-designers behind the hyperscaler ASICs.",
    "Networking":       "Ethernet, optical, and DPU/SmartNIC vendors in hyperscaler fabrics.",
    "Memory":           "HBM and DRAM behind hyperscaler accelerators.",
    "Fab":              "Foundry that prints the custom silicon.",
    "Power Systems":    "Power and cooling infrastructure for hyperscaler AI sites.",
}
