from urllib.parse import urlparse

def url_check(url):
    score = 0
    reasons = []

    parsed = urlparse(url)

    # Rule 1: HTTP instead of HTTPS
    if parsed.scheme != "https":
        score += 1
        reasons.append("Uses HTTP instead of HTTPS")

    # Rule 2: Suspicious words in domain
    suspicious_words = ["login", "verify", "secure", "account"]
    for word in suspicious_words:
        if word in parsed.netloc.lower():
            score += 1
            reasons.append(f"Suspicious word in domain: {word}")

    # Rule 3: Suspicious TLD
    suspicious_tlds = [".ru", ".tk", ".ml", ".ga", ".cf"]
    for tld in suspicious_tlds:
        if parsed.netloc.endswith(tld):
            score += 1
            reasons.append(f"Suspicious domain extension: {tld}")

    return score, reasons
