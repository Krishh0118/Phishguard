# engine/link_intel.py

import re

def check_link_intel(url: str):
    score = 0
    reasons = []

    url_lower = url.lower()

    # Rule 1: Login keyword
    if "login" in url_lower or "signin" in url_lower:
        score += 15
        reasons.append("Login-related keyword found")

    # Rule 2: URL shortening services
    shorteners = ["bit.ly", "tinyurl", "t.co", "goo.gl"]
    if any(s in url_lower for s in shorteners):
        score += 25
        reasons.append("URL shortener detected")

    # Rule 3: Excessive subdomains
    if url_lower.count(".") > 4:
        score += 15
        reasons.append("Too many subdomains")

    # Rule 4: Suspicious parameters
    if "@" in url_lower or "redirect" in url_lower:
        score += 20
        reasons.append("Suspicious redirect pattern")

    return score, reasons
def check_link_intel(url: str):
    score = 0
    reasons = []

    if "login" in url:
        score += 15
        reasons.append("Login keyword in URL")

    return {
        "score": score,
        "reasons": reasons
    }
    5b7c4ae (Add missing engine modules (risk, domain, link))
