import re


def abbreviate(words):
    cleaned = re.sub(r"[^a-zA-Z\s-]", "", words)
    return ''.join(p[0] for p in re.split(r'[\s-]+', cleaned) if p).upper()
