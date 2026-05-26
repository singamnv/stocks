"""Automotive AI — ADAS, autonomy, EV compute and sensing."""

KEY = "automotive"
NAME = "Automotive AI"
GROUP = "AI"
DESCRIPTION = "Self-driving and ADAS — OEMs, compute platforms, sensors, lidar, EV power semis, and charging."
ANCHOR_TICKER = "TSLA"

ECOSYSTEM: dict[str, list[str]] = {
    "OEMs":           ["TSLA", "GM", "F", "RIVN", "LCID", "XPEV", "NIO", "LI"],
    "ADAS / Compute": ["MBLY", "NVDA", "QCOM"],
    "Sensors":        ["AMBA", "ON", "STM", "NXPI"],
    "Lidar":          ["LAZR", "OUST", "INVZ", "AEVA"],
    "EV Charging":    ["CHPT", "EVGO"],
    "Power Semis":    ["WOLF"],
}

ROLES: dict[str, str] = {
    "TSLA": "Tesla — vertically integrated FSD compute (Dojo, AI5), most aggressive autonomy ambitions among OEMs.",
    "GM":   "Cruise (paused) and Super Cruise; Ultium platform integrates significant compute and power semis.",
    "F":    "Ford — BlueCruise hands-free L2; partnerships with Mobileye and others on next-gen ADAS stacks.",
    "RIVN": "Rivian — in-house compute and software stack; growing OEM partner for Amazon delivery fleet.",
    "LCID": "Lucid — focus on EV powertrain efficiency; AI features behind broader market.",
    "XPEV": "XPeng — Chinese EV leader on assisted-driving features; vertically integrated XNGP stack.",
    "NIO":  "NIO — Chinese EV with NAD assisted-driving system and ET / ES vehicle lineup.",
    "LI":   "Li Auto — Chinese EV / EREV leader with growing autonomy investment.",
    "MBLY": "Mobileye — EyeQ ADAS chips and SuperVision platform across global OEMs.",
    "NVDA": "NVIDIA — DRIVE Thor centralized compute platform adopted by Mercedes, JLR, Volvo, BYD, others.",
    "QCOM": "Qualcomm — Snapdragon Ride / Cockpit; rapidly winning OEM design slots against Mobileye and NVIDIA.",
    "AMBA": "Ambarella — CV imaging and perception SoCs for ADAS, in-cabin, and L3+ autonomy.",
    "ON":   "onsemi — image sensors and silicon carbide for ADAS and EV powertrain inverters.",
    "STM":  "STMicroelectronics — MCUs, SiC, and analog content per vehicle rising sharply with EV adoption.",
    "NXPI": "NXP — radar SoCs, MCUs, secure connectivity, battery management for next-gen vehicles.",
    "LAZR": "Luminar — Iris lidar shipping with Volvo EX90 and others; pure-play long-range lidar.",
    "OUST": "Ouster — solid-state digital lidar for automotive, industrial, and smart-infrastructure markets.",
    "INVZ": "Innoviz — perception lidar shipping into BMW and additional programs.",
    "AEVA": "Aeva — FMCW lidar (range + velocity) targeting automotive and industrial use.",
    "CHPT": "ChargePoint — largest US public EV charging network.",
    "EVGO": "EVgo — DC fast-charging network expanding alongside EV penetration.",
    "WOLF": "Wolfspeed — silicon-carbide wafers and power devices critical to EV traction inverters.",
}

CATEGORY_DESC: dict[str, str] = {
    "OEMs":           "Vehicle manufacturers — the buyers of automotive AI silicon and software.",
    "ADAS / Compute": "Centralized compute platforms for assisted and autonomous driving.",
    "Sensors":        "Cameras, radar, image sensors, and analog content per vehicle.",
    "Lidar":          "Lidar pure-plays — long-range sensing for L3+ autonomy.",
    "EV Charging":    "Public charging networks scaling with EV adoption.",
    "Power Semis":    "SiC and high-voltage semis enabling efficient EV powertrains.",
}
