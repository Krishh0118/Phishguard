from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Simple in-memory training data (we improve later)
PHISHING_SAMPLES = [
    "verify your account immediately",
    "your account has been suspended",
    "urgent login required",
    "click here to secure your account",
    "confirm your password now",
]

SAFE_SAMPLES = [
    "meeting scheduled tomorrow",
    "invoice attached for your reference",
    "project update and status",
    "team lunch tomorrow",
    "please review the document",
]

texts = PHISHING_SAMPLES + SAFE_SAMPLES
labels = [1] * len(PHISHING_SAMPLES) + [0] * len(SAFE_SAMPLES)

vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(texts)

model = LogisticRegression()
model.fit(X, labels)

def ai_predict(message: str):
    if not message or len(message.strip()) < 5:
        return 0, 0

    vec = vectorizer.transform([message])
    prob = model.predict_proba(vec)[0][1]  # phishing probability

    score = 1 if prob > 0.65 else 0
    confidence = round(prob * 100, 2)

    return score, confidence
