def _shift_char(c, shift):
    """Shift a single character by the given amount, preserving case."""
    if c.isupper():
        base = ord('A')
    elif c.islower():
        base = ord('a')
    else:
        return c  # non-letter, pass through unchanged

    return chr((ord(c) - base + shift) % 26 + base)


def encode(text, shift):
    """Encode text with a Caesar cipher."""
    return ''.join(_shift_char(c, shift) for c in text)


def decode(text, shift):
    """Decode text encoded with a Caesar cipher."""
    return encode(text, -shift)
