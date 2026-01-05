from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

texts = [
    "tea coffee hotel",
    "bus train travel",
    "rent house",
    "salary credit income",
]

labels = ["Food", "Travel", "Rent", "Income"]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression()
model.fit(X, labels)

def predict_category(note):
    if not note:
        return "Others"
    return model.predict(vectorizer.transform([note]))[0]