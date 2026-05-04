import string
from collections import Counter


def word_freq(text: str) -> dict[str, int]:
    cleaned = text.lower().translate(str.maketrans('', '', string.punctuation))
    return dict(Counter(cleaned.split()))
