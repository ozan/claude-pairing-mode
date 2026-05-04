import string


def is_pangram(text):
    return set(text.lower()) >= set(string.ascii_lowercase)
