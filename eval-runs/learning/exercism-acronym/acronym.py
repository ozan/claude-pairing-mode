import re


def abbreviate(words):
    return "".join(w[0].upper() for w in re.split(r"[\s\-]+", words) if w)
