def phishing_check(message):
    red_flags = [
        "urgent",
        "click here",
        "verify",
        "account blocked",
        "login now",
        "free",
        "winner",
        "limited time",
        "password",
        "bank"
    ]

    score = 0
    for word in red_flags:
        if word in message.lower():
            score += 1

    if score >= 2:
        return "⚠ PHISHING", score
    else:
        return "✅ LEGIT", score


msg = input("Enter the message to check: ")
result, score = phishing_check(msg)

print("\nResult:", result)
print("Risk score:", score)
