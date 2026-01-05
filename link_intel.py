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
