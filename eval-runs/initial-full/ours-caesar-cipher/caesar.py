def shift_char(c, shift):
    """Shift a single alphabetic character by `shift` positions, preserving case.
    Non-letter characters are returned unchanged."""
    if not c.isalpha():
        return c
    base = ord('A') if c.isupper() else ord('a')
    return chr((ord(c) - base + shift) % 26 + base)


def encode(text, shift):
    """Caesar-cipher encode: shift each letter forward by `shift` positions."""
    return ''.join(shift_char(c, shift) for c in text)


def decode(text, shift):
    """Caesar-cipher decode: reverse the shift."""
    return encode(text, -shift)
