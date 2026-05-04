import re
from collections import Counter


def word_frequency(text: str) -> dict[str, int]:
    """Return a mapping of each word (lowercased) to its frequency in text."""
    words = re.sub(r'[^\w\s]', '', text).lower().split()
    return dict(Counter(words))
