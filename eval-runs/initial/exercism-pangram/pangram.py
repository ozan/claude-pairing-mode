def is_pangram(text):
    return set('abcdefghijklmnopqrstuvwxyz').issubset(text.lower())
