import re
from urllib.parse import urlparse


def domain_intel(url: str):
    """
    Performs basic domain-level intelligence checks.
    Returns (score, reasons)
    """

    score = 0
    reasons = []

    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
    except Exception:
        return 30, ["Invalid URL structure"]

    # Rule 1: IP address instead of domain
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain):
        score += 30
        reasons.append("IP address used instead of domain")

    # Rule 2: Suspicious TLDs
    suspicious_tlds = [".tk", ".ml", ".ga", ".cf", ".zip", ".top"]
    if any(domain.endswith(tld) for tld in suspicious_tlds):
        score += 20
        reasons.append("Suspicious top-level domain")

    # Rule 3: Very long domain
    if len(domain) > 35:
        score += 15
        reasons.append("Unusually long domain name")

    # Rule 4: Hyphen abuse
    if domain.count("-") >= 3:
        score += 10
        reasons.append("Excessive hyphens in domain")

    return score, reasons
