import re


def abbreviate(words):
    words = re.sub(r'([a-z])([A-Z])', r'\1 \2', words)
    return ''.join(w[0].upper() for w in re.findall(r"[A-Za-z][A-Za-z']*", words))
