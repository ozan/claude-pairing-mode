import re


def abbreviate(words):
    """Return the acronym for the given phrase in uppercase.

    Hyphens are treated as word separators; all other punctuation is ignored.
    CamelCase words (e.g. 'HyperText') are split at each lowercase→uppercase
    boundary so each component contributes a letter.
    """
    # Split camelCase: insert a space at every lowercase→uppercase boundary
    words = re.sub(r'([a-z])([A-Z])', r'\1 \2', words)
    # Now split on whitespace and hyphens
    tokens = re.split(r'[\s\-]+', words)
    result = []
    for token in tokens:
        for ch in token:
            if ch.isalpha():
                result.append(ch.upper())
                break
    return ''.join(result)
