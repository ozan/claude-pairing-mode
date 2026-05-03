def _shift_char(c, shift):
    if not c.isalpha():
        return c
    base = ord('A') if c.isupper() else ord('a')
    return chr((ord(c) - base + shift) % 26 + base)

def encode(text, shift):
    return ''.join(_shift_char(c, shift) for c in text)

def decode(text, shift):
    return encode(text, -shift)
