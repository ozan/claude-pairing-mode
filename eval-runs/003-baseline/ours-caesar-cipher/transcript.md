# ours-caesar-cipher

- Source: `ours`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-02T23:34:20.360Z

---

## Turn 1

**User:**

Let's implement a Caesar cipher in Python with `encode(text, shift)` and `decode(text, shift)`. Preserve case; pass non-letters through unchanged.

**Pair:**

[Glob(**/caesar*.py)]
  No files found

Assistant: No existing file — I'll create it fresh.

[Write(/Users/oz/dev/ai-pair-proto/caesar.py)]
"""Caesar cipher — encode and decode with case preservation."""


def encode(text: str, shift: int) -> str:
    """Shift each letter in *text* forward by *shift* positions (mod 26).

    Case is preserved; non-letter characters pass through unchanged.
    Negative shifts and shifts > 26 are handled correctly.
    """
    result: list[str] = []
    for ch in text:
        if ch.isalpha():
… (11 more lines)

Assistant: Done. Here's a quick walkthrough of the design choices:

**`encode(text, shift)`**
- For each character, `ch.isalpha()` gates the shift — non-letters are appended as-is.
- `base = ord("A") if ch.isupper() else ord("a")` pins the arithmetic to the right alphabet half, so case is preserved automatically.
- `(ord(ch) - base + shift) % 26` normalises the offset into `[0, 25]` — this handles negative shifts and shifts > 26 for free, so `encode("A", -1)` → `"Z"` and `encode("A", 27)` → `"B"` both work correctly.

**`decode(text, shift)`**
- Just `encode(text, -shift)` — decoding is encoding with the inverse shift, so there's no logic to duplicate.

**Quick sanity check:**
```python
from caesar import encode, decode

encode("Hello, World!", 3)  # → "Khoor, Zruog!"
decode("Khoor, Zruog!", 3)  # → "Hello, World!"
encode("xyz", 3)            # → "abc"  (wraps)
encode("ABC", -1)           # → "ZAB"  (negative shift)
```

---

## Turn 2 (final)

**User:**

Looks solid. The logic is clean:
- `(ord(ch) - base + shift) % 26` wraps correctly for any shift
- Case preservation via the `base` trick is elegant
- `decode` correctly reuses `encode` with negated shift

Let me just verify the wrap-around works as expected with a quick mental check: `encode("Z", 1)` should give `"A"`. `(ord("Z") - ord("A") + 1) % 26 + ord("A")` = `(25 + 1) % 26 + ord("A")` = `0 + ord("A")` = `"A"`. ✓

And `encode("a", -1)` should give `"z"`. `(ord("a") - ord("a") - 1) % 26 + ord("a")` = `(-1) % 26 + ord("a")` = `25 + ord("a")` = `"z"`. ✓ (Python's modulo on negatives does the right thing here.)

The implementation matches the spec and the design explanation. Looks ready.

<done/>

---

**Run end**: done after 1 turn (34s)
