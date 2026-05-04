def is_pangram(text):
    return set('abcdefghijklmnopqrstuvwxyz') <= set(text.lower())
