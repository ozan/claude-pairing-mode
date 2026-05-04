import re


def abbreviate(words):
    words = re.sub(r'([a-z])([A-Z])', r'\1 \2', words)  # split camelCase
    parts = re.split(r'[\s\-_]+', words)
    return ''.join(p[0] for p in parts if p and p[0].isalpha()).upper()
