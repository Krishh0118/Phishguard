from urllib.parse import urlparse


def check_link_intel(url: str):
    """
    Performs link-level intelligence checks.
    Returns (score, reasons)
    """

    score = 0
    reasons = []

    url_lower = url.lower()

    # Rule 1: URL shorteners
    shorteners = [
        "bit.ly", "tinyurl", "t.co", "goo.gl", "ow.ly", "is.gd", "buff.ly"
    ]
    if any(s in url_lower for s in shorteners):
        score += 25
        reasons.append("URL shortener detected")

    # Rule 2: Excessive subdomains
    if url_lower.count(".") > 4:
        score += 15
        reasons.append("Too many subdomains")

    # Rule 3: Suspicious parameters
    if "@" in url_lower or "redirect" in url_lower:
        score += 20
        reasons.append("Suspicious redirect pattern")

    # Rule 4: HTTPS missing
    parsed = urlparse(url)
    if parsed.scheme != "https":
        score += 10
        reasons.append("URL does not use HTTPS")

    return score, reasons
