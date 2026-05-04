import re


def abbreviate(phrase):
    words = re.split(r'[\s-]+', phrase)
    firsts = (re.search(r'[a-zA-Z]', w) for w in words)
    return ''.join(m.group() for m in firsts if m).upper()
