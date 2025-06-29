from sqlalchemy.orm import Session
import models

# This replaces the ML-based prediction
def guess_category(note: str) -> str:
    note_lower = note.lower()
    keywords = {
        "transport": ["grab", "jeep", "taxi", "bus", "uber", "train"],
        "food": ["dinner", "lunch", "snack", "coffee", "restaurant", "jollibee", "mcdo"],
        "utilities": ["electric", "water", "internet", "bill"],
        "shopping": ["shopee", "lazada", "mall", "clothes", "shoes"],
        "entertainment": ["movie", "netflix", "games", "concert"],
    }

    for category, words in keywords.items():
        if any(word in note_lower for word in words):
            return category
    return "Uncategorized"


def generate_tags(note: str):
    tags = []
    keywords = {
        "transport": ["grab", "jeep", "taxi", "bus", "uber", "train"],
        "food": ["dinner", "lunch", "snack", "coffee", "restaurant", "jollibee", "mcdo"],
        "utilities": ["electric", "water", "internet", "bill"],
        "shopping": ["shopee", "lazada", "mall", "clothes", "shoes"],
        "entertainment": ["movie", "netflix", "games", "concert"],
    }

    note_lower = note.lower()
    for tag, words in keywords.items():
        if any(word in note_lower for word in words):
            tags.append(tag)
    return tags or ["misc"]
