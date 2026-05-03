# ours-caesar-cipher

- Source: `ours`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T02:52:33.945Z

---

## Turn 1

**User:**

Let's implement a Caesar cipher in Python with `encode(text, shift)` and `decode(text, shift)`. Preserve case; pass non-letters through unchanged.

**Pair:**

[Glob(caesar*.py)]
  No files found

Assistant: Good, starting fresh. The core question is how to implement the single-character shift — everything else builds on it.

OPTIONS:
[A] Modular arithmetic
```diff
+++ caesar.py
@@ -0,0 +1,5 @@
+def _shift_char(c, shift):
+    if c.isalpha():
+        base = ord('A') if c.isupper() else ord('a')
+        return chr((ord(c) - base + shift) % 26 + base)
+    return c
```

[B] Conditional wrap
```diff
+++ caesar.py
@@ -0,0 +1,7 @@
+def _shift_char(c, shift):
+    if c.isalpha():
+        base = ord('A') if c.isupper() else ord('a')
+        shifted = ord(c) + shift
+        if shifted > base + 25: shifted -= 26
+        elif shifted < base: shifted += 26
+        return chr(shifted)
+    return c
```

(Reply with A or B, or ask a follow-up question.)

Assistant: Which handles `shift=30` correctly?

---

## Turn 2

**User:**

A, definitely. 

With shift=30 for 'A': modulo handles it → `(0 + 30) % 26 = 4`, lands on 'E'. 

Option B's conditionals only catch one wrap in each direction. If shift were 56, Option B would overshoot the alphabet entirely and return garbage (or an out-of-range character). Modulo always contracts to [0, 25] no matter how large or negative the shift is.

**Pair:**

Assistant: Exactly right. Now let me write the file with that foundation, then we'll wire up `encode` and `decode`.

[Write(caesar.py)]
def _shift_char(c, shift):
    if c.isalpha():
        base = ord('A') if c.isupper() else ord('a')
        return chr((ord(c) - base + shift) % 26 + base)
    return c


Assistant: Now for `encode` and `decode`. One decision worth pausing on:

OPTIONS:
[A] decode calls encode
```diff
+++ caesar.py
@@ -5,0 +6,6 @@
+
+def encode(text, shift):
+    return ''.join(_shift_char(c, shift) for c in text)
+
+def decode(text, shift):
+    return encode(text, -shift)
```

[B] decode re-implements shift
```diff
+++ caesar.py
@@ -5,0 +6,6 @@
+
+def encode(text, shift):
+    return ''.join(_shift_char(c, shift) for c in text)
+
+def decode(text, shift):
+    return ''.join(_shift_char(c, 26 - shift) for c in text)
```

(Reply with A or B, or ask a follow-up question.)

Assistant: Which `decode` would you go with?

---

## Turn 3

**User:**

A. `decode` should call `encode` with `-shift`.

It's the DRY principle — shifting backward by N is the same as shifting forward by -N, and we've already proven that modulo handles negative shifts correctly. Option B duplicates the shift logic, which means if there's ever a bug in `_shift_char`, or if we want to change how shifting works, we'd have to remember to fix it in two places. 

Option A makes the relationship between encode and decode explicit in the code: decoding is just encoding with a negated shift. Cleaner and less error-prone.

**Pair:**

Assistant: Spot on.

[Edit(caesar.py)]
--- before
def _shift_char(c, shift):
    if c.isalpha():
        base = ord('A') if c.isupper() else ord('a')
        return chr((ord(c) - base + shift) % 26 + base)
    return c
--- after
def _shift_char(c, shift):
    if c.isalpha():
        base = ord('A') if c.isupper() else ord('a')
        return chr((ord(c) - base + shift) % 26 + base)
    return c


def encode(text, shift):
    return ''.join(_shift_char(c, shift) for c in text)


def decode(text, shift):
    return encode(text, -shift)

Assistant: That's a complete, correct implementation. Let's verify it quickly:

[Bash(cd /Users/oz/dev/ai-pair-proto && python3 -c "
from caesar import encode, decode

# Basic
print(encode('Hello, World!', 3))   # Khoor, Zruog!
print(decode('Khoor, Zruog!', 3))   # Hello, World!

# Large shift
print(encode('ABC', 30))            # EFG (30%26=4)

# Negative shift
print(encode('Hello', -3))          # Ebiil
print(decode('Ebiil', -3))          # Hello

# Round-trip
msg = 'The Quick Brown Fox 123!'
assert decode(encode(msg, 13), 13) == msg
print('round-trip OK')
"
)]
  Khoor, Zruog!
  Hello, World!
  EFG
  Ebiil
  Hello
  round-trip OK
  Shell cwd was reset to /Users/oz/dev/ai-pair-proto/eval-runs/006-initial/ours-caesar-cipher

Assistant: All good. Here's the final file:

```python
def _shift_char(c, shift):
    if c.isalpha():
        base = ord('A') if c.isupper() else ord('a')
        return chr((ord(c) - base + shift) % 26 + base)
    return c

def encode(text, shift):
    return ''.join(_shift_char(c, shift) for c in text)

def decode(text, shift):
    return encode(text, -shift)
```

Three decisions, three clean properties: `% 26` makes any shift value safe, `_shift_char` keeps case handling in one place, and `decode = encode(-shift)` makes the inverse relationship explicit. Nothing duplicated.

---

## Turn 4 (final)

**User:**

Looks good. You made the right calls at each decision point — leveraging modulo for robustness, and using DRY to keep encode and decode tightly coupled through negation rather than duplicating logic. The tests confirm it handles all the edge cases: large shifts, negative shifts, mixed case, punctuation, and round-trip integrity.

<done/>

---

**Run end**: done after 3 turns (96s)
