import re

def abbreviate(words):
    words = re.sub(r'([a-z])([A-Z])', r'\1 \2', words)
    cleaned = re.sub(r"[^a-zA-Z\s-]", '', words)
    return ''.join(w[0].upper() for w in re.split(r'[\s-]+', cleaned) if w)
