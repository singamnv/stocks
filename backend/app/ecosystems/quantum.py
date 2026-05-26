"""Quantum Computing — pure-play start-ups, big-tech programs, quantum-adjacent components."""

KEY = "quantum"
NAME = "Quantum"
GROUP = "Tech"
DESCRIPTION = "Quantum-computing pure-plays, big-tech quantum efforts, and the adjacent photonic and component supply chain."
ANCHOR_TICKER = "IONQ"

ECOSYSTEM: dict[str, list[str]] = {
    "Pure-Play Quantum":          ["IONQ", "RGTI", "QBTS", "QUBT", "ARQQ"],
    "Big-Tech Quantum Programs":  ["IBM", "GOOGL", "MSFT", "HON"],
    "Quantum-Adjacent":           ["COHR"],
}

ROLES: dict[str, str] = {
    "IONQ":  "IonQ — trapped-ion quantum computing; most-traded quantum pure-play.",
    "RGTI":  "Rigetti — superconducting quantum systems; on-cloud quantum compute.",
    "QBTS":  "D-Wave — quantum annealing for optimization problems.",
    "QUBT":  "Quantum Computing Inc — photonic quantum hardware and software.",
    "ARQQ":  "Arqit — quantum-safe encryption.",
    "IBM":   "IBM Quantum — superconducting quantum systems; Eagle / Heron / Condor roadmap.",
    "GOOGL": "Google Quantum AI — Sycamore / Willow superconducting chips; quantum error correction milestones.",
    "MSFT":  "Microsoft — Majorana topological qubit program; Azure Quantum.",
    "HON":   "Honeywell — Quantinuum trapped-ion systems (majority-owned via spinout).",
    "COHR":  "Coherent — photonic components used in quantum networking and trapped-ion systems.",
}

CATEGORY_DESC: dict[str, str] = {
    "Pure-Play Quantum":          "Public quantum-computing start-ups.",
    "Big-Tech Quantum Programs":  "Mega-cap quantum efforts inside larger franchises.",
    "Quantum-Adjacent":           "Component and connectivity suppliers to quantum systems.",
}
