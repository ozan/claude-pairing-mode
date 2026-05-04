def abbreviate(words: str) -> str:
    return ''.join(w[0].upper() for w in words.replace('-', ' ').split())
