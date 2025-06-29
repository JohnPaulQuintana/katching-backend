from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
from sqlalchemy.orm import Session
import models

model = None
vectorizer = None

def train_model(db: Session):
    global model, vectorizer
    expenses = db.query(models.Expense).filter(models.Expense.category != "").all()
    if len(expenses) > 5:
        df = pd.DataFrame([(e.note, e.category) for e in expenses], columns=["note", "category"])
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(df["note"])
        y = df["category"]
        model = MultinomialNB()
        model.fit(X, y)

def predict_category(note: str):
    if model and vectorizer:
        X = vectorizer.transform([note])
        return model.predict(X)[0]
    return "Uncategorized"

def generate_tags(note: str):
    tags = []
    keywords = {
        "transport": ["grab", "jeep", "taxi", "bus", "uber", "train"],
        "food": ["dinner", "lunch", "snack", "coffee", "restaurant", "jollibee", "mcdo"],
        "utilities": ["electric", "water", "internet", "bill"]
    }
    note_lower = note.lower()
    for tag, words in keywords.items():
        if any(word in note_lower for word in words):
            tags.append(tag)
    return tags or ["misc"]
