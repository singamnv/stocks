"""Broad Semis — the non-AI semi market: memory, analog, equipment, foundry, wireless."""

KEY = "semis"
NAME = "Broad Semis"
GROUP = "Tech"
DESCRIPTION = "The non-AI semi market — memory, analog, MCUs, wafer equipment, foundries, and wireless connectivity."
ANCHOR_TICKER = "TXN"

ECOSYSTEM: dict[str, list[str]] = {
    "Memory & Storage":         ["MU", "SNDK", "WDC", "STX"],
    "Analog & Mixed-Signal":    ["TXN", "ADI", "MCHP", "ON"],
    "Equipment":                ["AMAT", "KLAC", "LRCX", "ASML"],
    "Foundry / IP":             ["TSM", "ARM"],
    "Auto / Embedded":          ["NXPI", "STM", "IFNNY"],
    "Wireless & Connectivity":  ["QCOM", "SWKS", "QRVO"],
}

ROLES: dict[str, str] = {
    "TXN":   "Texas Instruments — biggest pure-play analog by revenue; broad industrial and auto exposure.",
    "MU":    "Micron — DRAM and NAND across HBM, server, mobile, and auto markets.",
    "SNDK":  "SanDisk — post-spinoff NAND and SSD pure-play covering enterprise and consumer.",
    "WDC":   "Western Digital — enterprise HDDs and SSDs; nearline storage for data centers.",
    "STX":   "Seagate — HDD leader; mass-capacity HAMR drives shipping for hyperscale storage.",
    "ADI":   "Analog Devices — high-performance analog and signal-chain ICs; broad industrial / auto / comms.",
    "MCHP":  "Microchip — MCUs, analog, FPGAs, mixed-signal; deep industrial / auto exposure.",
    "ON":    "onsemi — SiC and image sensors; key auto and industrial power play.",
    "AMAT":  "Applied Materials — broadest wafer-equipment supplier; deposition, etch, ion implant.",
    "KLAC":  "KLA — wafer inspection and metrology; the process-control standard at every leading-edge fab.",
    "LRCX":  "Lam Research — etch and deposition equipment; especially levered to HBM and 3D NAND.",
    "ASML":  "ASML — sole supplier of EUV and high-NA EUV lithography.",
    "TSM":   "TSMC — dominant pure-play foundry; manufactures most leading-edge logic chips.",
    "ARM":   "Arm Holdings — instruction-set IP licensed across mobile, server, auto, and embedded.",
    "NXPI":  "NXP — auto MCU and radar leader; secure connectivity and battery management.",
    "STM":   "STMicroelectronics — analog, MCU, SiC; broad auto and industrial content.",
    "IFNNY": "Infineon (ADR) — leader in auto power and SiC; sometimes flaky on yfinance.",
    "QCOM":  "Qualcomm — smartphone modem leader expanding into auto (Snapdragon Ride) and PC.",
    "SWKS":  "Skyworks Solutions — RF front-end for smartphones; iPhone-cycle-sensitive.",
    "QRVO":  "Qorvo — RF and power semis for mobile and infrastructure.",
}

CATEGORY_DESC: dict[str, str] = {
    "Memory & Storage":         "DRAM, NAND, HBM, HDDs across enterprise and consumer.",
    "Analog & Mixed-Signal":    "Analog leaders with broad industrial and automotive exposure.",
    "Equipment":                "Wafer-fab equipment — etch, deposition, lithography, inspection.",
    "Foundry / IP":             "Foundry capacity and CPU/GPU instruction-set IP.",
    "Auto / Embedded":          "Auto-grade MCUs, MCU+analog content; SiC and radar.",
    "Wireless & Connectivity":  "RF front-end and wireless connectivity chips.",
}
