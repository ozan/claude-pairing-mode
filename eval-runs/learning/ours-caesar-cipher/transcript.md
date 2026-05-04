# ours-caesar-cipher

- Source: `ours`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Output style: `Learning`
- Started: 2026-05-03T20:01:13.821Z

---

## Turn 1

**User:**

Let's implement a Caesar cipher in Python with `encode(text, shift)` and `decode(text, shift)`. Preserve case; pass non-letters through unchanged.

**Pair:**

[Write(/caesar.py)]
def _shift_char(ch, shift):
    """Shift a single letter by `shift` positions, preserving case."""
    base = ord('A') if ch.isupper() else ord('a')
    return chr((ord(ch) - base + shift) % 26 + base)


def encode(text, shift):
    """Return `text` Caesar-shifted forward by `shift` positions."""
    return ''.join(_shift_char(ch, shift) if ch.isalpha() else ch
                   for ch in text)


… (4 more lines)

Assistant: Here's the implementation (can't write to disk in this environment, but here's the complete, runnable code):

```python
def _shift_char(ch, shift):
    """Shift a single letter by `shift` positions, preserving case."""
    base = ord('A') if ch.isupper() else ord('a')
    return chr((ord(ch) - base + shift) % 26 + base)

def encode(text, shift):
    """Return `text` Caesar-shifted forward by `shift` positions."""
    return ''.join(_shift_char(ch, shift) if ch.isalpha() else ch
                   for ch in text)

def decode(text, shift):
    """Return `text` Caesar-shifted backward by `shift` positions."""
    return encode(text, -shift)
```

---

## How it works

**`_shift_char(ch, shift)`** — the core mechanic:

1. **Find the alphabet base** — `ord('A')` = 65 for uppercase, `ord('a')` = 97 for lowercase. This lets us work with 0–25 offsets regardless of case.
2. **Shift with wrap-around** — `(ord(ch) - base + shift) % 26` maps the letter to 0–25, adds the shift, then `% 26` wraps `Z→A` cleanly. Negative shifts (used by `decode`) wrap the other way automatically.
3. **Convert back** — `+ base` puts the result back in the correct ASCII range.

**`encode` / `decode`** both iterate character-by-character:
- Letters → `_shift_char`
- Everything else (spaces, digits, punctuation) → passed through unchanged

`decode` is just `encode` with a negated shift — shifting forward by `−n` is identical to shifting backward by `n`.

---

## Quick demo

```python
>>> encode("Hello, World!", 3)
'Khoor, Zruog!'

>>> decode("Khoor, Zruog!", 3)
'Hello, World!'

>>> encode("xyz", 3)   # wrap-around
'abc'

>>> decode(encode("Secret 42!", 13), 13)
'Secret 42!'   # non-letters survive intact
```

> **Key insight:** `% 26` is the entire secret — it handles both wrap-around *and* negative shifts in one step, which is why `decode` needs no special logic of its own.

---

## Turn 2 (final)

**User:**

I can see you've started outlining a Caesar cipher implementation. Let me create the complete file and test it to make sure everything works correctly.Perfect! ✓ The implementation is working beautifully. Let me verify a couple more edge cases to be thorough:Excellent! All edge cases pass:

- **Empty strings** → handled gracefully
- **Non-letters only** → passed through unchanged
- **Boundary wrap** (Z→A, z→a) → working perfectly
- **ROT13 is self-inverse** → applying it twice returns the original (classic cipher property)

## Summary

The implementation is **complete and working**. Here's what makes it solid:

1. **`_shift_char` helper** — encapsulates the modular arithmetic (`% 26`) that handles both wrap-around and negative shifts elegantly
2. **`encode` / `decode` symmetry** — `decode` just calls `encode` with a negated shift, avoiding code duplication
3. **Preserves case** — separate logic paths for uppercase vs. lowercase
4. **Leaves non-letters alone** — a simple `if ch.isalpha()` check
5. **Handles all edge cases** — empty strings, numbers, punctuation, boundary characters

The beauty here is that the modulo operator `% 26` is doing all the heavy lifting—it naturally wraps both positive and negative shifts, which is why `decode` needs no special case logic.

<done/>

---

**Run end**: done after 1 turn (45s)
