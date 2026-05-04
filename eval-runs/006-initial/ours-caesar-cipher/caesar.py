def _shift_char(c, shift):
    if c.isalpha():
        base = ord('A') if c.isupper() else ord('a')
        return chr((ord(c) - base + shift) % 26 + base)
    return c


def encode(text, shift):
    """Encrypt text using a Caesar cipher with the given shift."""
    return ''.join(_shift_char(c, shift) for c in text)


def decode(text, shift):
    """Decrypt text encoded with a Caesar cipher using the given shift."""
    return encode(text, -shift)
