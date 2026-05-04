import re


def abbreviate(words):
    """Return the acronym of a phrase in uppercase.

    Hyphens are treated as word separators; other punctuation is ignored.
    e.g. 'Portable Network Graphics' -> 'PNG'
         'Complementary metal-oxide semiconductor' -> 'CMOS'
         "Halley's Comet" -> 'HC'
    """
    # Also split camelCase: "HyperText" -> "Hyper Text"
    words = re.sub(r'([a-z])([A-Z])', r'\1 \2', words)
    tokens = re.split(r'[\s\-]+', words)
    return ''.join(
        next(c for c in token if c.isalpha()).upper()
        for token in tokens
        if any(c.isalpha() for c in token)
    )
