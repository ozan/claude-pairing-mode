# ours-caesar-cipher

- Condition: `learning`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:07:59

## Initial prompt

Let's implement a Caesar cipher in Python with `encode(text, shift)` and `decode(text, shift)`. Preserve case; pass non-letters through unchanged.

---

## Turn 1

### Tutor

[Bash(ls)]
  (Bash completed with no output)

[Write(/caesar.py)]
def _shift_char(ch: str, shift: int) -> str:
    """Shift a single letter by `shift` positions, wrapping within its case block."""
    if ch.isalpha():
        base = ord('A') if ch.isupper() else ord('a')
        return chr((ord(ch) - base + shift) % 26 + base)
    return ch   # digits, spaces, punctuation — pass through


def encode(text: str, shift: int) -> str:
    """Return `text` with every letter advanced by `shift` positions."""
    return ''.join(_shift_char(ch, shift) for ch in text)

… (20 more lines)
  error: EROFS: read-only file system, open '/caesar.py'

[Bash(cd /tmp && cat > caesar.py << 'EOF'
def _shift_char(ch: str, shift: int) -> str:
    """Shift a single letter by `shift` positions, wrapping within its case block."""
    if ch.isalpha():
        base = ord('A') if ch.isupper() else ord('a')
        return chr((ord(ch) - base + shift) % 26 + base)
    return ch   # digits, spaces, punctuation — pass through


def encode(text: str, shift: int) -> str:
    """Return `text` with every letter advanced by `shift` positions."""
    return ''.join(_shift_char(ch, shift) for ch in text)


def decode(text: str, shift: int) -> str:
    """Return `text` with every letter reversed by `shift` positions."""
    return encode(text, -shift)   # decoding is just a negative shift


# ── quick sanity checks ────────────────────────────────────────────────────────
if __name__ == '__main__':
    examples = [
        ('Hello, World!', 3),
        ('abc XYZ', 1),
        ('abc XYZ', 26),   # full wrap -> identity
        ('Zebra!', 2),
    ]
    for text, shift in examples:
        encoded = encode(text, shift)
        decoded = decode(encoded, shift)
        match = 'OK' if decoded == text else 'FAIL'
        print(f'  shift={shift:>2}  {text!r:20} -> {encoded!r:20} -> {decoded!r}  {match}')
EOF
python3 caesar.py)]
  shift= 3  'Hello, World!'      -> 'Khoor, Zruog!'      -> 'Hello, World!'  OK
    shift= 1  'abc XYZ'            -> 'bcd YZA'            -> 'abc XYZ'  OK
    shift=26  'abc XYZ'            -> 'abc XYZ'            -> 'abc XYZ'  OK
    shift= 2  'Zebra!'             -> 'Bgdtc!'             -> 'Zebra!'  OK
  Shell cwd was reset to /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-cob0jisb

Tutor: All four cases pass. Here's the full implementation:

```python
def _shift_char(ch: str, shift: int) -> str:
    """Shift a single letter by `shift` positions, wrapping within its case block."""
    if ch.isalpha():
        base = ord('A') if ch.isupper() else ord('a')
        return chr((ord(ch) - base + shift) % 26 + base)
    return ch   # digits, spaces, punctuation — pass through


def encode(text: str, shift: int) -> str:
    """Return `text` with every letter advanced by `shift` positions."""
    return ''.join(_shift_char(ch, shift) for ch in text)


def decode(text: str, shift: int) -> str:
    """Return `text` with every letter reversed by `shift` positions."""
    return encode(text, -shift)   # decoding is just a negative shift
```

---

### How it works

**`_shift_char` — the core math**

```
new_position = (old_position + shift) % 26
```

The `% 26` is what makes the alphabet wrap around (`Z + 1 → A`).
To keep case separate, we work in *zero-based offsets from the block's start*:

| step | expression | example (`'Y'`, shift `3`) |
|---|---|---|
| find block start | `base = ord('A')` | `65` |
| zero-based offset | `ord(ch) - base` | `24` |
| shift & wrap | `(24 + 3) % 26` | `1` |
| back to ASCII | `1 + base` | `66 → 'B'` |

**`decode` reuses `encode`** — shifting by `-shift` is mathematically identical to decoding, so there's no duplicated logic.

---

### Edge cases handled

| input | why it works |
|---|---|
| `'Z'` + shift `1` → `'A'` | `% 26` wraps at the boundary |
| `shift=26` → identity | `n % 26 == 0` means no net movement |
| `'!'`, `' '`, `'3'` → unchanged | `ch.isalpha()` guard passes them through |
| uppercase stays uppercase | separate `'A'`/`'a'` base keeps each case in its own 26-char block |

### Student

Great! I can see the implementation is complete and all the test cases pass. Let me walk through what I'm seeing here to make sure I understand it:

The key insight is in `_shift_char` — by converting each letter to a zero-based offset (0–25) within its own case block, doing the shift with modulo wrapping, then converting back to ASCII, we handle all the tricky parts at once: wrapping from Z→A, preserving case, and leaving non-letters untouched.

And I like that `decode` just calls `encode` with a negative shift — that's elegant and eliminates code duplication.

Let me verify my understanding with one more quick test to be sure. What happens if we encode and decode with a negative shift directly?

```python
text = "Hello"
encoded = encode(text, -3)
decoded = decode(encoded, -3)
print(f"Original: {text}, Encoded with -3: {encoded}, Decoded back: {decoded}")
```

Does that work as expected, or is `decode` specifically meant to only be called after an `encode`?

---

## Turn 2

### Tutor

Tutor: Great question — let's just run it and reason through the math together.

[Bash(cd /tmp && python3 -c "
from caesar import encode, decode

text = 'Hello'
encoded = encode(text, -3)
decoded = decode(encoded, -3)
print(f'Original : {text!r}')
print(f'Encoded  : {encoded!r}  (shift -3)')
print(f'Decoded  : {decoded!r}  (decode with same -3)')
print(f'Round-trip OK: {decoded == text}')
print()

# Show letter-by-letter for H
import string
print('Letter trace for H (shift -3):')
print(f'  ord(H)=72, base=65, offset=7')
print(f'  (7 + -3) % 26 = {(7 + -3) % 26}  -> chr(65+4) = {chr(65+4)}')
print(f'  then decode: (4 + 3) % 26 = {(4 + 3) % 26}  -> chr(65+7) = {chr(65+7)}')
"
)]
  Original : 'Hello'
  Encoded  : 'Ebiil'  (shift -3)
  Decoded  : 'Hello'  (decode with same -3)
  Round-trip OK: True
  
  Letter trace for H (shift -3):
    ord(H)=72, base=65, offset=7
    (7 + -3) % 26 = 4  -> chr(65+4) = E
    then decode: (4 + 3) % 26 = 7  -> chr(65+7) = H
  Shell cwd was reset to /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-cob0jisb

Tutor: It works perfectly — and it's not a coincidence. Here's why:

### The algebra always cancels

`decode` is defined as `encode(text, -shift)`, so the full round-trip is:

```
decode(encode(text, s), s)
  = encode(encode(text, s), -s)
  = apply shift +s, then shift -s
  = net shift of 0
  = original text   ✓
```

This holds for **any integer `s`** — positive, negative, or zero. The sign of `s` is irrelevant because `decode` always applies the *opposite* of whatever was passed in.

### What a negative shift actually means

| call | net effect | example (`'H'`) |
|---|---|---|
| `encode(text, 3)` | shift forward 3 | `H → K` |
| `encode(text, -3)` | shift backward 3 | `H → E` |
| `decode(text, 3)` | shift backward 3 | `H → E` |
| `decode(text, -3)` | shift forward 3 | `H → K` |

So `encode(text, -3)` and `decode(text, 3)` are exactly the same operation — there's no special relationship between `encode` and `decode` other than "they apply opposite shifts." The names are just a convention for which direction is considered *encoding*.

> **`decode` isn't restricted to undoing a prior `encode` call** — it's simply `encode` with the shift sign flipped. The round-trip guarantee comes purely from the math, not from any bookkeeping.

### Student

Ah, that's really clear now — thank you! So the symmetry is baked right into the math. `encode(text, s)` followed by `decode(result, s)` always works because the shifts are literally opposites, and `(offset + s) % 26` followed by `(new_offset - s) % 26` cancels out to the original offset.

I see now that calling `decode(text, -3)` is just another way to shift forward by 3, and `encode(text, -3)` shifts backward by 3 — the function names are semantic labels for what we *intend*, not constraints on what we can do.

One small thing I want to confirm though: the problem asked for `encode(text, shift)` and `decode(text, shift)` functions, and we've got both. The implementation handles all the cases in the requirements:

- ✓ Case is preserved (separate blocks for uppercase and lowercase)
- ✓ Non-letters pass through unchanged  
- ✓ Wrapping works (the `% 26`)
- ✓ Round-trip works (all test cases passed)

The code is solid and the tests all pass. I think we're done here.

<done/>

---

**Run end:** done after 2 turn(s) in 49.7s
