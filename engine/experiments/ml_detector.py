from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# Training examples
messages = [
    "urgent verify your bank account",
    "click here to reset password",
    "your account is blocked",
    "hi how are you",
    "let's meet tomorrow",
    "happy birthday have fun"
]

# 1 = phishing, 0 = legit
labels = [1, 1, 1, 0, 0, 0]

# Convert text to numbers
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(messages)

# Train model
model = LogisticRegression()
model.fit(X, labels)

# User input
test_msg = input("Enter message to check: ")
test_vector = vectorizer.transform([test_msg])

prediction = model.predict(test_vector)

if prediction[0] == 1:
    print("⚠ PHISHING (AI Prediction)")
else:
    print("✅ LEGIT (AI Prediction)")
