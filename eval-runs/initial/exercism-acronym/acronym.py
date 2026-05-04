import re


def abbreviate(words):
    expanded = re.sub(r'([a-z])([A-Z])', r'\1 \2', words)
    cleaned = re.sub(r"[^a-zA-Z\s-]", "", expanded)
    return ''.join(p[0].upper() for p in re.split(r'[\s-]+', cleaned) if p)
