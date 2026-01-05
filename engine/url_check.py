from urllib.parse import urlparse

SUSPICIOUS_TLDS = [".click", ".xyz", ".top", ".zip", ".ru"]

def url_check(url: str):
    parsed = urlparse(url)
    score = 0
    reasons = []

    if not url.startswith("https"):
        score += 25
        reasons.append("Uses HTTP instead of HTTPS")

    for tld in SUSPICIOUS_TLDS:
        if parsed.netloc.endswith(tld):
            score += 30
            reasons.append(f"Suspicious TLD detected ({tld})")

    if any(brand in url.lower() for brand in ["paypal", "google", "bank"]):
        score += 30
        reasons.append("Possible brand impersonation")

    return min(score, 100), reasons
