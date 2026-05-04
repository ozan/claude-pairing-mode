# ours-caesar-cipher

- Source: `ours`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T08:41:21.829Z

---

## Turn 1

**User:**

Let's implement a Caesar cipher in Python with `encode(text, shift)` and `decode(text, shift)`. Preserve case; pass non-letters through unchanged.

**Pair:**

Assistant: Good plan — clean, classic exercise. Let me start with the core shift logic, since there's a subtle trap worth knowing:

[Bash(ls caesar*.py 2>/dev/null || echo "none")]
  none

Assistant: Which implementation of the character-shift helper is correct?

Assistant: The `propose_options` tool isn't loading, so I'll just walk you through the key decision directly.

There's a classic operator-precedence trap here. Consider these two approaches for shifting a single character:

**Option A:**
```python
def shift_char(c, shift):
    base = ord('A') if c.isupper() else ord('a')
    return chr(ord(c) - base + shift % 26 + base)
```

**Option B:**
```python
def shift_char(c, shift):
    base = ord('A') if c.isupper() else ord('a')
    return chr((ord(c) - base + shift) % 26 + base)
```

The trap in A: `shift % 26` binds *before* the subtraction/addition, so you get `ord(c) + (shift % 26)` — which overflows past `'z'`/`'Z'` for edge cases like shifting `'z'` by 1. Option **B** is correct — `% 26` must wrap the entire offset expression.

Let me build the full file with B's approach:

[Write(caesar.py)]
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
… (6 more lines)

Assistant: Notice that `decode` is just `encode(text, -shift)` — no duplicated logic. Python's `%` always returns a non-negative result for a positive modulus (`-1 % 26 == 25`), so shifting by `-shift` wraps correctly without any special casing.

Let's verify it:

[Bash(python3 -c "
from caesar import encode, decode

# Basic round-trip
assert decode(encode('Hello, World!', 13), 13) == 'Hello, World!'

# ROT13 known value
assert encode('Hello', 13) == 'Uryyb'

# Wrap-around: z+1 = a
assert encode('z', 1) == 'a'
assert encode('Z', 1) == 'A'

# Preserve case and non-letters
assert encode('abc XYZ 123!', 3) == 'def ABC 123!'

# Negative shift
assert encode('d', -3) == 'a'

print('All tests passed.')
"
)]
  All tests passed.

Assistant: All good. Here's what the final file looks like:

```python
def shift_char(c, shift):
    if not c.isalpha():
        return c
    base = ord('A') if c.isupper() else ord('a')
    return chr((ord(c) - base + shift) % 26 + base)

def encode(text, shift):
    return ''.join(shift_char(c, shift) for c in text)

def decode(text, shift):
    return encode(text, -shift)
```

Key points:
- **`(ord(c) - base + shift) % 26`** — the `% 26` wraps the *whole* offset, not just `shift`
- **`base`** handles case by anchoring to `'A'` or `'a'`  
- **`decode`** delegates to `encode` with a negated shift — Python's `%` makes negative shifts work for free

---

## Turn 2 (final)

**User:**

Looks solid. The key insight about `% 26` needing to wrap the *entire* offset (not just the shift value) is the kind of subtle bug that's easy to miss, and I appreciate seeing it laid out explicitly. The fact that Python's `%` operator handles negative numbers correctly (returning non-negative results for positive modulus) is a nice bonus that makes `decode` simple.

Let me verify the file was actually written:

[Read(caesar.py)]

Perfect. The implementation is clean, the tests pass, and it handles all the edge cases (case preservation, non-letters, wrap-around, negative shifts via decode). 

<done/>

---

**Run end**: done after 1 turn (71s)
