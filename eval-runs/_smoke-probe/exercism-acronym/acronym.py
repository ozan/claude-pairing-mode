import re


def abbreviate(words):
    parts = re.split(r'[\s-]+', words)
    return ''.join(p[0] for p in parts if p).upper()
