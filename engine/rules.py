def rule_check(message):
    red_flags = [
        "urgent", "click", "verify", "account",
        "password", "bank", "login"
    ]

    found = []
    for word in red_flags:
        if word in message.lower():
            found.append(word)

    score = len(found)
    return score, found
