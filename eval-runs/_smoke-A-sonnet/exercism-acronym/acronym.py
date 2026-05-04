import re


def abbreviate(words):
    cleaned = re.sub(r"[^a-zA-Z\s-]", "", words)
    return ''.join(re.findall(r'\b\w', cleaned)).upper()
