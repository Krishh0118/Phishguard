from urllib.parse import urlparse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# ---------------- AI SETUP ----------------
messages = [
    "urgent verify your bank account",
    "click here to reset password",
    "your account is blocked",
    "hi how are you",
    "let's meet tomorrow",
    "happy birthday have fun"
]
labels = [1, 1, 1, 0, 0, 0]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(messages)

model = LogisticRegression()
model.fit(X, labels)


# ---------------- RULE CHECK ----------------
def rule_check(message):
    red_flags = [
        "urgent", "click", "verify", "account",
        "password", "bank", "login"
    ]
    score = 0
    for word in red_flags:
        if word in message.lower():
            score += 1
    return score


# ---------------- URL CHECK ----------------
def url_check(url):
    score = 0
    parsed = urlparse(url)

    if parsed.scheme != "https":
        score += 1

    suspicious_words = ["login", "verify", "secure"]
    for word in suspicious_words:
        if word in parsed.netloc.lower():
            score += 1

    suspicious_tlds = [".ru", ".tk", ".ml", ".ga"]
    for tld in suspicious_tlds:
        if parsed.netloc.endswith(tld):
            score += 1

    return score


# ---------------- MAIN ENGINE ----------------
choice = input("Check (1) Message or (2) URL? ")

if choice == "1":
    msg = input("Enter message: ")

    rule_score = rule_check(msg)
    ai_pred = model.predict(vectorizer.transform([msg]))[0]

    total_score = rule_score + ai_pred

    if total_score >= 2:
        print("\n⚠ PHISHING DETECTED")
    else:
        print("\n✅ MESSAGE IS SAFE")

    print("Rule score:", rule_score)
    print("AI score:", ai_pred)

elif choice == "2":
    url = input("Enter URL: ")

    url_score = url_check(url)

    if url_score >= 2:
        print("\n⚠ PHISHING URL")
    else:
        print("\n✅ URL IS SAFE")

    print("URL risk score:", url_score)

else:
    print("Invalid choice")
