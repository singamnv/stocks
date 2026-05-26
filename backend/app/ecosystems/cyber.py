"""Cybersecurity — endpoint, network, zero trust, data, legacy."""

KEY = "cyber"
NAME = "Cybersecurity"
GROUP = "Tech"
DESCRIPTION = "Endpoint, network, zero-trust, and data-security vendors plus legacy security franchises."
ANCHOR_TICKER = "CRWD"

ECOSYSTEM: dict[str, list[str]] = {
    "Next-Gen Endpoint":     ["CRWD", "S", "RBRK"],
    "Network & Firewall":    ["PANW", "FTNT"],
    "Zero Trust & Identity": ["ZS", "OKTA", "NET"],
    "Data Security":         ["VRNS", "TENB"],
    "Legacy Vendors":        ["CSCO"],
}

ROLES: dict[str, str] = {
    "CRWD":  "CrowdStrike — leader in cloud-delivered endpoint protection; Falcon platform expansion.",
    "S":     "SentinelOne — AI-driven endpoint and XDR competing directly with CrowdStrike.",
    "RBRK":  "Rubrik — data security and ransomware recovery.",
    "PANW":  "Palo Alto Networks — broad security platform; firewalls plus Prisma cloud and Cortex XDR.",
    "FTNT":  "Fortinet — firewall and SD-WAN with strong international and SMB footprint.",
    "ZS":    "Zscaler — zero-trust internet and private access; cloud-delivered.",
    "OKTA":  "Okta — identity and access management for workforce and customer identity.",
    "NET":   "Cloudflare — edge security, zero trust, and CDN with growing developer platform.",
    "VRNS":  "Varonis — data security and DSPM for unstructured data.",
    "TENB":  "Tenable — vulnerability management and exposure management.",
    "CSCO":  "Cisco — diversified networking; Splunk acquisition adds large SecOps franchise.",
}

CATEGORY_DESC: dict[str, str] = {
    "Next-Gen Endpoint":     "Cloud-delivered endpoint protection and XDR vendors.",
    "Network & Firewall":    "Firewall-anchored security platforms.",
    "Zero Trust & Identity": "Identity, zero-trust access, and edge security.",
    "Data Security":         "Data-loss prevention, DSPM, and exposure management.",
    "Legacy Vendors":        "Big-tent security franchises inside diversified vendors.",
}
