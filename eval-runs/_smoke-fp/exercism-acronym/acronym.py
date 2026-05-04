def abbreviate(words):
    parts = words.replace('-', ' ').split()
    return ''.join(p[0].upper() for p in parts)
