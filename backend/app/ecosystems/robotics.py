"""Robotics & Industrial Automation — industrial robots, surgical robots, semi automation, humanoids."""

KEY = "robotics"
NAME = "Robotics"
GROUP = "Tech"
DESCRIPTION = "Industrial robotics, surgical robotics, semi-fab automation, and the emerging humanoid / physical-AI trade."
ANCHOR_TICKER = "ABBNY"

ECOSYSTEM: dict[str, list[str]] = {
    "Industrial Robotics":     ["ABBNY", "FANUY", "YASKY", "ROK"],
    "Surgical Robotics":       ["ISRG", "SYK"],
    "Semi & Test Automation":  ["TER", "COHU"],
    "Humanoid / Physical AI":  ["NVDA", "RBOT", "KSCP", "SYM"],
    "Industrial AI Software":  ["PTC", "EMR"],
}

ROLES: dict[str, str] = {
    "ABBNY": "ABB (ADR) — global leader in industrial robots and factory automation; ABB Robotics business.",
    "FANUY": "Fanuc (ADR) — top Japanese industrial robot maker; CNC controllers and articulated arms.",
    "YASKY": "Yaskawa (ADR) — Motoman robots and servomotor leadership.",
    "ROK":   "Rockwell Automation — US industrial automation and control systems.",
    "ISRG":  "Intuitive Surgical — da Vinci surgical robotic system; dominant in soft-tissue surgery.",
    "SYK":   "Stryker — Mako orthopedic surgical robotics; broad medtech franchise.",
    "TER":   "Teradyne — semiconductor and electronics test equipment; also owns Universal Robots cobots.",
    "COHU":  "Cohu — semiconductor test handlers and inspection.",
    "NVDA":  "NVIDIA — Project GR00T humanoid foundation models; Isaac robotics platform.",
    "RBOT":  "Vicarious Surgical — surgical robotics development; high beta, pre-revenue.",
    "KSCP":  "Knightscope — autonomous security robots.",
    "SYM":   "Symbotic — AI-powered warehouse automation; Walmart anchor customer.",
    "PTC":   "PTC — industrial CAD/PLM (Creo) and IoT (ThingWorx) for connected factories.",
    "EMR":   "Emerson Electric — automation solutions and process control software.",
}

CATEGORY_DESC: dict[str, str] = {
    "Industrial Robotics":     "Articulated arm and cobot vendors for factories.",
    "Surgical Robotics":       "Robotics platforms for soft-tissue and orthopedic surgery.",
    "Semi & Test Automation":  "Equipment that automates wafer and electronics test.",
    "Humanoid / Physical AI":  "The new humanoid + physical-AI trade.",
    "Industrial AI Software":  "Software stacks for the connected factory.",
}
