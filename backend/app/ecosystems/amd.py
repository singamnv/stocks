"""AMD AI ecosystem — MI300/MI400 stack and its partners."""

KEY = "amd"
NAME = "AMD AI"
GROUP = "AI"
DESCRIPTION = "AMD's AI accelerator stack (MI300, MI400) and its supplier and OEM ecosystem."
ANCHOR_TICKER = "AMD"

ECOSYSTEM: dict[str, list[str]] = {
    "Compute":           ["AMD", "INTC"],
    "Memory":            ["MU", "SNDK"],
    "Fab":               ["TSM"],
    "Networking":        ["AVGO", "MRVL", "COHR", "ANET"],
    "Packaging":         ["ASX", "AMKR"],
    "Server OEMs":       ["SMCI", "DELL", "HPE"],
    "Power Systems":     ["VRT", "ETN", "FLEX"],
    "Power Electronics": ["MPWR", "ADI", "STM"],
}

ROLES: dict[str, str] = {
    "AMD":  "Designs the Instinct MI300/MI400 accelerators; ROCm software stack competing with NVIDIA CUDA.",
    "INTC": "x86 host CPUs (EPYC competition) and Gaudi accelerators in AMD-adjacent AI server platforms.",
    "MU":   "HBM3E supplier to MI300X / MI325X; ramping HBM4 for MI400.",
    "SNDK": "Post-spinoff SanDisk — enterprise NAND used in AMD AI server SKUs.",
    "TSM":  "Manufactures MI300/MI400 dies (5 nm / 3 nm) plus CoWoS-S advanced packaging.",
    "AVGO": "Tomahawk / Jericho switching silicon used in fabrics around AMD AI clusters.",
    "MRVL": "Marvell — custom interconnect and switch silicon paired with AMD AI deployments.",
    "COHR": "Coherent — 800G / 1.6T optical transceivers for AMD-anchored AI data center fabrics.",
    "ANET": "Arista — Ethernet switching for AI clusters using AMD or Ethernet-based alternatives to NVLink.",
    "ASX":  "ASE Technology — OSAT for advanced packaging used on AMD Instinct accelerators.",
    "AMKR": "Amkor — packaging partner for high-performance compute, including AMD CPUs and accelerators.",
    "SMCI": "Super Micro — OEM building AMD MI300X servers competitive with NVIDIA HGX boxes.",
    "DELL": "Dell — PowerEdge servers with AMD EPYC CPUs and Instinct accelerators in select SKUs.",
    "HPE":  "HPE — Cray supercomputers (El Capitan) built around AMD MI300A APUs.",
    "VRT":  "Vertiv — power and thermal management for AMD AI data center deployments.",
    "ETN":  "Eaton — UPS and switchgear for AI sites including AMD-based clusters.",
    "FLEX": "Flex — contract manufacturer of power shelves and BBUs serving AMD-anchored builds.",
    "MPWR": "Monolithic Power — high-current VRM power stages used on AMD CPU and accelerator boards.",
    "ADI":  "Analog Devices — power management and signal chain ICs across AMD server platforms.",
    "STM":  "STMicroelectronics — analog and power devices in AMD reference designs.",
}

CATEGORY_DESC: dict[str, str] = {
    "Compute":           "AI accelerator silicon and competing host CPUs.",
    "Memory":            "HBM and NAND used in MI300 / MI400 systems.",
    "Fab":               "Foundries manufacturing AMD AI silicon.",
    "Networking":        "Switch silicon, optical, and Ethernet fabrics around AMD AI clusters.",
    "Packaging":         "OSAT partners for advanced packaging on AMD accelerators.",
    "Server OEMs":       "Companies that ship branded AMD AI servers.",
    "Power Systems":     "Cooling, UPS, switchgear for AMD AI data centers.",
    "Power Electronics": "VRMs and power ICs for AMD compute boards.",
}
