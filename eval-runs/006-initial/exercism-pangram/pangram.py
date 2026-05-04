import string


def is_pangram(text):
    return set(string.ascii_lowercase) <= set(text.lower())
