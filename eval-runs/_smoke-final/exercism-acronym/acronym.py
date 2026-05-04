import re


def abbreviate(phrase):
    phrase = re.sub(r'([a-z])([A-Z])', r'\1 \2', phrase)  # split CamelCase
    words = re.split(r'[\s-]+', phrase)
    initials = (re.search(r'[a-zA-Z]', w) for w in words)
    return ''.join(m.group().upper() for m in initials if m)
