import re
from collections import Counter

def word_freq(text):
    words = re.findall(r'[a-z]+', text.lower())
    return dict(Counter(words))
