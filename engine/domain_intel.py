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
