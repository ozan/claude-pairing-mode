import re

def abbreviate(words):
    return ''.join(w[0] for w in re.findall(r"[a-zA-Z][a-zA-Z']*", words)).upper()
