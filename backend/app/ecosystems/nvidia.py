"""NVIDIA ecosystem — GPUs, suppliers, partners, direct investments."""

KEY = "nvidia"
NAME = "NVIDIA"
GROUP = "AI"
DESCRIPTION = "NVIDIA's GPU stack and its supply chain — fab, memory, packaging, networking, power, OEMs, and direct investments."
ANCHOR_TICKER = "NVDA"

ECOSYSTEM: dict[str, list[str]] = {
    "IP":                 ["ARM"],
    "Fab":                ["TSM", "INTC"],
    "Memory":             ["MU", "SNDK", "WDC"],
    "Packaging":          ["ASX", "AMKR", "CAMT"],
    "Equipment":          ["KLAC", "LRCX", "ASML", "KEYS"],
    "Networking":         ["COHR", "GLW", "FN", "LITE", "APH"],
    "Server OEMs":        ["DELL", "SMCI", "JBL"],
    "Power Systems":      ["FLEX", "VRT", "ETN"],
    "Power Electronics":  ["STM", "ADI", "MPWR", "NVTS", "ON"],
    "Direct Investments": ["CRWV", "NBIS", "NOK", "SNPS"],
}

ROLES: dict[str, str] = {
    "NVDA": "NVIDIA — the platform at the center of the ecosystem this dashboard tracks.",
    "ARM":  "Designs the Arm CPU architecture licensed inside Grace and Grace Hopper superchips; NVIDIA is a major Arm licensee.",
    "TSM":  "Sole foundry for NVIDIA's Hopper, Blackwell, and upcoming Rubin GPUs; manufactures on N4/N3 and packages with CoWoS.",
    "INTC": "Foundry alternative being qualified for select NVIDIA workloads and a supplier of x86 host CPUs in AI server platforms.",
    "MU":   "Supplies HBM3E to NVIDIA Hopper and Blackwell accelerators; ramping HBM4 for next-gen Rubin.",
    "SNDK": "Post-spinoff SanDisk supplies NAND and SSDs used across NVIDIA DGX and HGX storage tiers.",
    "WDC":  "Provides enterprise HDDs and SSDs for AI data-lake storage tiers behind NVIDIA GPU clusters.",
    "ASX":  "ASE Technology — leading OSAT for advanced packaging (CoWoS / FOPLP) used on NVIDIA accelerators.",
    "AMKR": "OSAT partner for advanced packaging and test of high-performance compute chips, including NVIDIA SKUs.",
    "CAMT": "Camtek — inspection and metrology tools used in HBM and advanced-packaging lines feeding NVIDIA volume.",
    "KLAC": "Process-control / wafer-inspection tools used across the foundry steps that produce NVIDIA silicon.",
    "LRCX": "Lam Research — etch and deposition equipment critical for HBM and leading-edge logic used in NVIDIA chips.",
    "ASML": "Sole supplier of EUV lithography systems used by TSMC to print NVIDIA's most advanced GPUs.",
    "KEYS": "Keysight — high-speed test and measurement instruments used to validate NVIDIA networking and silicon.",
    "COHR": "Coherent — supplies optical transceivers and laser sources for NVIDIA's InfiniBand and Spectrum-X networking.",
    "GLW":  "Corning — optical fiber and connectivity for the AI fabrics that interconnect NVIDIA GPU clusters.",
    "FN":   "Fabrinet — manufacturing partner producing optical modules used in NVIDIA networking equipment.",
    "LITE": "Lumentum — lasers and optical components for the transceivers that link NVIDIA GPUs across clusters.",
    "APH":  "Amphenol — high-speed cables and connectors used across NVIDIA NVLink and InfiniBand backplanes.",
    "DELL": "Builds branded PowerEdge XE and DGX-class servers around NVIDIA's HGX and Blackwell platforms.",
    "SMCI": "Super Micro — top OEM of NVIDIA HGX servers; tightly aligned on liquid-cooled GB200 NVL racks.",
    "JBL":  "Jabil — contract manufacturer assembling NVIDIA server, networking, and reference platforms.",
    "FLEX": "Flex — contract manufacturer for power shelves, BBUs, and rack integration in AI data centers.",
    "VRT":  "Vertiv — thermal management and power infrastructure (CDUs, liquid cooling) for NVIDIA GPU clusters.",
    "ETN":  "Eaton — UPS, switchgear, and busways powering hyperscale AI sites built around NVIDIA hardware.",
    "STM":  "STMicroelectronics — analog and power devices used in NVIDIA reference platforms and Drive automotive stacks.",
    "ADI":  "Analog Devices — power management and signal-chain ICs used across NVIDIA boards and networking gear.",
    "MPWR": "Monolithic Power — high-density power-stage solutions for GPU VRMs in NVIDIA accelerators.",
    "NVTS": "Navitas — GaN and SiC power ICs targeting 48V AI-data-center power architectures used with NVIDIA GPUs.",
    "ON":   "onsemi — SiC and power-management devices used in AI data center power delivery and EV platforms.",
    "CRWV": "CoreWeave — NVIDIA-invested GPU cloud and one of the largest deployers of Hopper and Blackwell capacity.",
    "NBIS": "Nebius — NVIDIA-invested AI cloud (former Yandex assets) building large-scale GPU infrastructure.",
    "NOK":  "Nokia — NVIDIA strategic investment to co-develop AI-RAN platforms combining 5G and GPU compute.",
    "SNPS": "Synopsys — EDA tools NVIDIA uses to design every chip; partnership extends to AI-driven chip design.",
}

CATEGORY_DESC: dict[str, str] = {
    "IP":                 "Intellectual Property — chip designs NVIDIA licenses (Arm cores in Grace).",
    "Fab":                "Fabrication — foundries that manufacture NVIDIA GPUs.",
    "Memory":             "Memory — HBM, DRAM, and NAND used in NVIDIA accelerators and DGX systems.",
    "Packaging":          "Packaging / OSAT — advanced packaging, test, and metrology for the chips.",
    "Equipment":          "Wafer Equipment — etch, deposition, lithography, inspection used by foundries.",
    "Networking":         "Networking — optical transceivers, lasers, cables, and connectors for GPU clusters.",
    "Server OEMs":        "Server OEMs — companies that build NVIDIA-powered AI servers.",
    "Power Systems":      "Power Systems — cooling, UPS, switchgear, busways for AI data centers.",
    "Power Electronics":  "Power Electronics — VRMs, GaN/SiC, power-management ICs for GPU power delivery.",
    "Direct Investments": "Direct Investments — companies NVIDIA has a strategic equity stake in.",
}
