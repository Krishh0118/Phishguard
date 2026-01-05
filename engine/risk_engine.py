def calculate_risk(rule_score: int, ai_confidence: float, intel_score: int):
    total = rule_score + intel_score + int(ai_confidence * 0.5)

    if total >= 70:
        level = "HIGH"
        label = "🚨 HIGH RISK"
    elif total >= 40:
        level = "MEDIUM"
        label = "⚠️ MEDIUM RISK"
    else:
        level = "LOW"
        label = "✅ LOW RISK"

    return {
        "score": total,
        "level": level,
        "label": label
    }
def calculate_risk(rule_score: int, ai_confidence: float, intel_score: int):
    total = rule_score + intel_score + int(ai_confidence * 0.5)

    if total >= 70:
        level = "HIGH"
        label = "🚨 HIGH RISK"
    elif total >= 40:
        level = "MEDIUM"
        label = "⚠️ MEDIUM RISK"
    else:
        level = "LOW"
        label = "✅ LOW RISK"

    return {
        "score": total,
        "level": level,
        "label": label
    }
    5b7c4ae (Add missing engine modules (risk, domain, link))
