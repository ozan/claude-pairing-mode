def _shift_char(c, shift):
    if c.isalpha():
        base = ord('A') if c.isupper() else ord('a')
        return chr((ord(c) - base + shift) % 26 + base)
    return c


def encode(text, shift):
    return ''.join(_shift_char(c, shift) for c in text)


def decode(text, shift):
    return encode(text, -shift)
