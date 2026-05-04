import string
from collections import Counter


def word_frequencies(text: str) -> dict[str, int]:
    """Return a mapping of each lowercased word to its frequency in text."""
    cleaned = text.translate(str.maketrans('', '', string.punctuation))
    words = cleaned.lower().split()
    return dict(Counter(words))
