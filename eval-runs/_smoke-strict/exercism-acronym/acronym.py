import re


def abbreviate(words):
    expanded = re.sub(r'([a-z])([A-Z])', r'\1 \2', words)
    return ''.join(w[0].upper() for w in re.findall(r"[a-zA-Z']+", expanded))
