# ours-caesar-cipher

- Condition: `baseline`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T20:53:50

## Initial prompt

Let's implement a Caesar cipher in Python with `encode(text, shift)` and `decode(text, shift)`. Preserve case; pass non-letters through unchanged.

---

## Turn 1

### Tutor

[Write(/repo/caesar.py)]
def _shift_char(ch: str, shift: int) -> str:
    """Shift a single alphabetic character by *shift* positions (wraps at 26)."""
    base = ord('A') if ch.isupper() else ord('a')
    return chr((ord(ch) - base + shift) % 26 + base)


def encode(text: str, shift: int) -> str:
    """Return *text* Caesar-encoded with the given *shift*.

    Letters are shifted forward (mod 26); case is preserved; non-letters are
    passed through unchanged.
    """
… (10 more lines)
  error: EROFS: read-only file system, mkdir '/repo'

[Bash(pwd && ls)]
  /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-66vwu1nl

[Write(/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-66vwu1nl/caesar.py)]
def _shift_char(ch: str, shift: int) -> str:
    """Shift a single alphabetic character by *shift* positions (wraps at 26)."""
    base = ord('A') if ch.isupper() else ord('a')
    return chr((ord(ch) - base + shift) % 26 + base)


def encode(text: str, shift: int) -> str:
    """Return *text* Caesar-encoded with the given *shift*.

    Letters are shifted forward (mod 26); case is preserved; non-letters are
    passed through unchanged.
    """
… (10 more lines)
  File created successfully at: /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-66vwu1nl/caesar.py

Tutor: Now let's verify it works with a quick smoke test:

[Bash(cd /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-66vwu1nl && python3 - <<'EOF'
from caesar import encode, decode

# Basic ROT-13
assert encode("Hello, World!", 13) == "Uryyb, Jbeyq!"
assert decode("Uryyb, Jbeyq!", 13) == "Hello, World!"

# Round-trip: decode(encode(x)) == x for any shift
for shift in range(1, 26):
    msg = "The Quick Brown Fox Jumps Over The Lazy Dog 123!"
    assert decode(encode(msg, shift), shift) == msg, f"round-trip failed at shift={shift}"

# Wrap-around: shift by 26 is identity
assert encode("abcXYZ", 26) == "abcXYZ"

# Negative / large shifts
assert encode("abc", -1) == "zab"
assert encode("abc", 27) == "bcd"   # 27 mod 26 == 1

# Case preservation
assert encode("abcABC", 1) == "bcdBCD"

# Non-letters pass through
assert encode("Hello, World! 123", 3) == "Khoor, Zruog! 123"

print("All assertions passed.")
EOF)]
  All assertions passed.

Tutor: All good. Here's a walkthrough of the implementation:

---

### `caesar.py`

```python
def _shift_char(ch: str, shift: int) -> str:
    base = ord('A') if ch.isupper() else ord('a')
    return chr((ord(ch) - base + shift) % 26 + base)

def encode(text: str, shift: int) -> str:
    return ''.join(_shift_char(ch, shift) if ch.isalpha() else ch for ch in text)

def decode(text: str, shift: int) -> str:
    return encode(text, -shift)
```

---

### How it works

| Concern | Approach |
|---|---|
| **Case preservation** | `base` is `ord('A')` or `ord('a')` depending on `ch.isupper()`, so the result stays in the same alphabet block. |
| **Wrap-around** | `(ord(ch) - base + shift) % 26` keeps the result in `[0, 25]`, handling any positive, negative, or large shift correctly. |
| **Non-letters** | The generator in `encode` passes `ch` through unchanged when `ch.isalpha()` is false. |
| **`decode`** | Simply calls `encode` with `-shift`. Since `% 26` handles negatives in Python, no extra clamping is needed. |

**Example:**
```python
encode("Hello, World!", 13)  # → "Uryyb, Jbeyq!"
decode("Uryyb, Jbeyq!", 13)  # → "Hello, World!"
```

### Student

Thanks for the walkthrough! That all makes sense. I can see how the modulo arithmetic handles the wrap-around elegantly—even for negative shifts, Python's `%` operator does the right thing and keeps us in the `[0, 25]` range.

One thing I want to make sure I understand: when we do `decode(text, -shift)`, we're relying on the fact that shifting backward by `n` is the same as shifting forward by `26 - n` (mod 26). Is that right? Like, if I encode with shift 3, then decode with shift -3, the `% 26` takes care of making sure we land back where we started?

Also, I'm curious why `_shift_char` is a helper function—is that just for readability/testing, or is there another reason to extract it out?

---

## Turn 2

### Tutor

Tutor: Both great questions — let me be precise about each.

---

### 1. The modular arithmetic of `decode`

Yes, exactly right, and it's worth spelling out concretely.

For a letter at offset `k` (0–25), encoding with shift `s` gives:

```
(k + s) % 26
```

To reverse that, we need to find the value that, when added to `(k + s) % 26`, lands back on `k`. That's just `-s`, or equivalently `26 - s` (mod 26). They're the same thing:

```
-3 % 26  →  23   # Python guarantees this: result is always in [0, 25]
26 - 3   →  23   # Same value
```

So these two calls are **identical** in effect:

```python
decode("Khoor", 3)        # calls encode(text, -3)
encode("Khoor", 26 - 3)   # calls encode(text, 23)
```

The key Python detail: most languages (C, Java, JS) make `-3 % 26` give `-3`. Python instead defines `%` to always match the **sign of the divisor**, so `-3 % 26 = 23`. That's what lets `decode` be a one-liner — no manual `(26 - shift) % 26` clamping needed.

---

### 2. Why extract `_shift_char`?

It's primarily **readability and single-responsibility**, but there are three concrete benefits:

**① The encode generator stays declarative**

With the helper, `encode` reads as a clean policy statement — *"for each character: shift it if it's a letter, otherwise pass it through"* — with no arithmetic noise inline:

```python
# With helper — intent is obvious at a glance
''.join(_shift_char(ch, shift) if ch.isalpha() else ch for ch in text)

# Without helper — the reader has to parse arithmetic to understand structure
''.join(
    chr(((ord(ch) - (ord('A') if ch.isupper() else ord('a'))) + shift) % 26
        + (ord('A') if ch.isupper() else ord('a')))
    if ch.isalpha() else ch
    for ch in text
)
```

**② The two concerns are independent and can be tested independently**

The logic of *"how do you shift one character"* is completely separate from *"how do you apply that across a string"*. Extracting it makes both pieces individually verifiable:

```python
assert _shift_char('a', 1)  == 'b'   # basic forward
assert _shift_char('z', 1)  == 'a'   # wrap-around
assert _shift_char('Z', 1)  == 'A'   # uppercase wrap
assert _shift_char('a', -1) == 'z'   # negative shift
```

You can nail down the tricky edge cases (wrap, case, negative) in isolation without constructing full strings.

**③ The leading underscore signals intent**

The `_` prefix is a Python convention meaning *"internal implementation detail, not part of the public API."* Callers of this module are meant to use `encode` and `decode`. If the internal arithmetic ever needed to change, `_shift_char` is the single place to touch — `encode` and `decode` stay untouched.

### Student

Ah, that's really helpful—thank you. I was already a bit fuzzy on Python's modulo behavior with negatives, so seeing that spelled out clearly makes a big difference. And the explanation about the underscore convention and testability makes the design choice feel much less arbitrary.

I think I've got a solid grasp on this implementation now. The core ideas are:
- `_shift_char` handles the wrapping arithmetic for a single letter, isolated and testable
- `encode` is the glue that applies it character-by-character while preserving non-letters
- `decode` is just `encode` with the shift flipped, relying on Python's modulo to handle the inversion

And all the edge cases (negative shifts, large shifts, wrap-around, case preservation) fall out naturally from the math rather than needing special-case logic.

I'm satisfied with how this turned out—the code is concise, well-structured, and I understand why each piece exists. 

<done/>

---

**Run end:** done after 2 turn(s) in 52.1s
