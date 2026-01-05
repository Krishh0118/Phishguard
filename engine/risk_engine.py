def calculate_risk(rule_score: int, ai_confidence: float, intel_score: int):
    """
    Combines rule-based score, AI confidence, and intelligence score
    to calculate overall phishing risk.
    """

    total_score = rule_score + intel_score + int(ai_confidence / 4)

    if total_score >= 70:
        return {
            "label": "HIGH RISK ⚠️",
            "level": "High",
            "score": total_score
        }
    elif total_score >= 40:
        return {
            "label": "MEDIUM RISK ⚠️",
            "level": "Medium",
            "score": total_score
        }
    else:
        return {
            "label": "LOW RISK ✅",
            "level": "Low",
            "score": total_score
        }
