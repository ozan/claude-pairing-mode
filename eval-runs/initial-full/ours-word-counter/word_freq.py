import string
from collections import Counter


def word_frequency(text):
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    cleaned = text.lower().translate(translator)
    return dict(Counter(cleaned.split()))
