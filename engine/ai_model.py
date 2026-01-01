from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

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

def ai_predict(message):
    vector = vectorizer.transform([message])
    prediction = model.predict(vector)[0]
    confidence = max(model.predict_proba(vector)[0]) * 100
    return prediction, round(confidence, 2)
