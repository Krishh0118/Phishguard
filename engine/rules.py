PHISHING_KEYWORDS = [
    "urgent", "verify", "account", "bank", "login",
    "password", "click", "suspended", "security"
]

def rule_check(text: str):
    text = text.lower()
    found = [kw for kw in PHISHING_KEYWORDS if kw in text]
    score = min(len(found) * 15, 60)  # cap rule score
    return score, found
