import re

def word_freq(text):
    text = re.sub(r'[^a-z\s]', '', text.lower())
    words = text.split()
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq
