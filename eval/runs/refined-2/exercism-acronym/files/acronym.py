import re


def abbreviate(words):
    parts = re.split(r'[\s-]+', words)
    return ''.join(next(c for c in p if c.isalpha())
                   for p in parts if any(c.isalpha() for c in p)).upper()
