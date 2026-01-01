from urllib.parse import urlparse

def check_url(url):
    score = 0

    parsed = urlparse(url)
    domain = parsed.netloc

    # Rule 1: HTTP instead of HTTPS
    if parsed.scheme != "https":
        score += 1

    # Rule 2: Suspicious words
    suspicious_words = ["login", "verify", "secure", "account", "update"]
    for word in suspicious_words:
        if word in domain.lower():
            score += 1

    # Rule 3: Suspicious TLD
    suspicious_tlds = [".ru", ".tk", ".ml", ".ga", ".cf"]
    for tld in suspicious_tlds:
        if domain.endswith(tld):
            score += 1

    # Decision
    if score >= 2:
        return "⚠ PHISHING URL", score
    else:
        return "✅ LEGIT URL", score


url = input("Enter URL to check: ")
result, score = check_url(url)

print("\nResult:", result)
print("Risk score:", score)
