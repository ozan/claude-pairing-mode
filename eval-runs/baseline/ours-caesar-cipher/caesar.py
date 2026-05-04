def _shift_char(ch: str, shift: int) -> str:
    """Shift a single letter by *shift* positions, preserving case."""
    base = ord('A') if ch.isupper() else ord('a')
    return chr(base + (ord(ch) - base + shift) % 26)


def encode(text: str, shift: int) -> str:
    """Caesar-encode *text*, rotating each letter forward by *shift* positions.

    Case is preserved; non-letter characters are passed through unchanged.
    """
    return ''.join(_shift_char(ch, shift) if ch.isalpha() else ch for ch in text)


def decode(text: str, shift: int) -> str:
    """Caesar-decode *text*, rotating each letter backward by *shift* positions.

    Case is preserved; non-letter characters are passed through unchanged.
    """
    return encode(text, -shift)
