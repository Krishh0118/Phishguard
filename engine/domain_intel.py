# engine/domain_intel.py

from urllib.parse import urlparse
import re

def domain_intel(url: str):
    score = 0
    reasons = []

    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
    except Exception:
        return 0, ["Invalid URL format"]

    # Rule 1: Suspicious TLDs
    suspicious_tlds = [".xyz", ".top", ".tk", ".ml", ".ga"]
    if any(domain.endswith(tld) for tld in suspicious_tlds):
        score += 20
        reasons.append("Suspicious top-level domain")

    # Rule 2: Too many hyphens
    if domain.count("-") >= 3:
        score += 15
        reasons.append("Too many hyphens in domain")

    # Rule 3: Brand impersonation
    brands = ["google", "paypal", "facebook", "amazon", "microsoft"]
    for brand in brands:
        if brand in domain and not domain.endswith(f"{brand}.com"):
            score += 25
            reasons.append(f"Possible {brand} impersonation")
            break

    # Rule 4: IP-based domain
    if re.match(r"\d+\.\d+\.\d+\.\d+", domain):
        score += 30
        reasons.append("IP address used as domain")

    return score, reasons
def domain_intel(url: str):
    score = 0
    reasons = []

    if url.endswith(".xyz"):
        score += 20
        reasons.append("Suspicious TLD (.xyz)")

    return {
        "score": score,
        "reasons": reasons
    }
 5b7c4ae (Add missing engine modules (risk, domain, link))
