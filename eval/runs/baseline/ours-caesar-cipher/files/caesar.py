def _shift_char(ch: str, shift: int) -> str:
    """Shift a single alphabetic character by *shift* positions (wraps at 26)."""
    base = ord('A') if ch.isupper() else ord('a')
    return chr((ord(ch) - base + shift) % 26 + base)


def encode(text: str, shift: int) -> str:
    """Return *text* Caesar-encoded with the given *shift*.

    Letters are shifted forward (mod 26); case is preserved; non-letters are
    passed through unchanged.
    """
    return ''.join(_shift_char(ch, shift) if ch.isalpha() else ch for ch in text)


def decode(text: str, shift: int) -> str:
    """Return *text* Caesar-decoded with the given *shift*.

    Equivalent to encoding with the inverse shift (-shift mod 26).
    """
    return encode(text, -shift)
