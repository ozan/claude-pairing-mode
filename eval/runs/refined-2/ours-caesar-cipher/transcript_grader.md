# ours-caesar-cipher

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:26:50

## Initial prompt

Let's implement a Caesar cipher in Python with `encode(text, shift)` and `decode(text, shift)`. Preserve case; pass non-letters through unchanged.

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Tutor: Good starting point. First decision: how to implement the per-character shift.

OPTIONS:
[A] ord/chr arithmetic
```diff
+++ caesar.py
@@ -0,0 +1,8 @@
+def encode(text, shift):
+    result = []
+    for c in text:
+        if c.isalpha():
+            base = ord('A') if c.isupper() else ord('a')
+            result.append(chr((ord(c) - base + shift) % 26 + base))
+        else:
+            result.append(c)
+    return ''.join(result)
```

[B] str.maketrans lookup
```diff
+++ caesar.py
@@ -0,0 +1,9 @@
+import string
+
+def encode(text, shift):
+    shift %= 26
+    lo, hi = string.ascii_lowercase, string.ascii_uppercase
+    table = str.maketrans(
+        lo + hi, lo[shift:] + lo[:shift] + hi[shift:] + hi[:shift]
+    )
+    return text.translate(table)
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach do you prefer for the core shift logic?

### Student

I think I'll go with **A** — the `ord/chr` arithmetic approach.

It's more explicit and easier for me to follow: I can see the logic of each step (checking if it's a letter, finding the base character, doing the modulo arithmetic to wrap around). Even though it's a bit more code, I think it'll be clearer when I come back to debug or explain it later.

Option B is clever with the translation table, but I'd have to think harder about what's happening with all those string slices. For learning purposes, A feels like the right move.

Should I go ahead and write out the full solution with both `encode` and `decode` functions?

---

## Turn 2

### Tutor

Tutor: Agreed — and the math stays honest when shifts are negative too, which matters for the next question.

[Glob(caesar.py)]
  No files found

[Write(caesar.py)]
def encode(text, shift):
    result = []
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            result.append(chr((ord(c) - base + shift) % 26 + base))
        else:
            result.append(c)
    return ''.join(result)

  File created successfully at: caesar.py

Tutor: Now, how should `decode` work?

OPTIONS:
[A] Decode as its own loop
```diff
+++ caesar.py
@@ -8,0 +9,8 @@
+
+def decode(text, shift):
+    result = []
+    for c in text:
+        if c.isalpha():
+            base = ord('A') if c.isupper() else ord('a')
+            result.append(chr((ord(c) - base - shift) % 26 + base))
+        else:
+            result.append(c)
+    return ''.join(result)
```

[B] Decode delegates to encode
```diff
+++ caesar.py
@@ -8,0 +9,3 @@
+
+def decode(text, shift):
+    return encode(text, -shift)
```

(Reply with A or B, or ask a follow-up question.)

Tutor: How should `decode` be implemented?

### Student

**B** — decode delegates to encode.

That's much cleaner. Since we're using `ord/chr` arithmetic with modulo, negative shifts work perfectly (the tutor just mentioned that). So instead of duplicating the loop logic, I can just call `encode(text, -shift)` and it'll handle everything: the modulo will wrap the negative shift around correctly, and case/non-letters stay preserved.

It's DRY and leverages the math we already have. Let me go with that.

---

## Turn 3

### Tutor

Tutor: Exactly right — Python's `%` always returns non-negative for a positive divisor, so `-3 % 26 == 23`, and the math just works.

[Edit(caesar.py)]
--- before
def encode(text, shift):
    result = []
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            result.append(chr((ord(c) - base + shift) % 26 + base))
        else:
            result.append(c)
    return ''.join(result)
--- after
def encode(text, shift):
    result = []
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            result.append(chr((ord(c) - base + shift) % 26 + base))
        else:
            result.append(c)
    return ''.join(result)

def decode(text, shift):
    return encode(text, -shift)
  The file caesar.py has been updated successfully.

Tutor: The core is done. One structural question before we call it finished:

OPTIONS:
[A] Keep encode as-is
Leave `encode` with its explicit loop. It's readable and self-contained — no need to split it further for a function this small.

[B] Extract a char helper
```diff
+++ caesar.py
@@ -0,0 +1,9 @@
+def _shift_char(c, shift):
+    if c.isalpha():
+        base = ord('A') if c.isupper() else ord('a')
+        return chr((ord(c) - base + shift) % 26 + base)
+    return c
+
+def encode(text, shift):
+    return ''.join(_shift_char(c, shift) for c in text)
```

(Reply with A or B, or ask a follow-up question.)

### Student

I'll go with **A** — keep encode as-is.

The function is already pretty short and readable. Extracting a helper feels like it would add an extra layer of indirection for not much gain here. The loop is clear enough that I can understand what's happening without having to jump to another function definition.

If this were part of a larger system where we needed to shift characters in different contexts, or if the logic got more complex, then a helper would make sense. But for this problem, keeping it straightforward feels right.

Is the implementation ready to test now?

---

## Turn 4

### Tutor

Tutor: Fair call — the "extract when it earns its keep" instinct is good. The one thing worth keeping in mind: `_shift_char` would be the natural unit to test in isolation (and to reuse if you later wanted, say, `encode_file`). But for this scope, the loop reads fine.

Let's verify it works:

[Bash(cd /Users/samanthawilliams/projects && python3 -c "
from caesar import encode, decode

# Basic round-trip
assert decode(encode('Hello, World!', 3), 3) == 'Hello, World!'

# Case preservation
assert encode('Hello', 13) == 'Uryyb'
assert encode('HELLO', 13) == 'URYYB'

# Non-letters pass through
assert encode('foo-bar!', 1) == 'gpp-cbs!'

# Wrap-around
assert encode('xyz', 3) == 'abc'
assert encode('XYZ', 3) == 'ABC'

# Large / zero shift
assert encode('Hello', 0) == 'Hello'
assert encode('Hello', 26) == 'Hello'

print('All tests passed.')
"
)]
  error: Exit code 1

[Bash(python3 -c "
from caesar import encode, decode

# Basic round-trip
assert decode(encode('Hello, World!', 3), 3) == 'Hello, World!'

# Case preservation
assert encode('Hello', 13) == 'Uryyb'
assert encode('HELLO', 13) == 'URYYB'

# Non-letters pass through
assert encode('foo-bar!', 1) == 'gpp-cbs!'

# Wrap-around
assert encode('xyz', 3) == 'abc'
assert encode('XYZ', 3) == 'ABC'

# Large / zero shift
assert encode('Hello', 0) == 'Hello'
assert encode('Hello', 26) == 'Hello'

print('All tests passed.')
"
)]
  All tests passed.

Tutor: All green. Here's the final state:

[Read(caesar.py)]
  1	def encode(text, shift):
  2	    result = []
  3	    for c in text:
  4	        if c.isalpha():
  5	            base = ord('A') if c.isupper() else ord('a')
  6	            result.append(chr((ord(c) - base + shift) % 26 + base))
  7	        else:
  8	            result.append(c)
  9	    return ''.join(result)
  10	
  11	def decode(text, shift):
  12	    return encode(text, -shift)
  … (1 more lines)

Tutor: Clean and complete. A few things worth noting about what you now have:

- **`% 26` does double duty** — it handles wrap-around *and* makes negative shifts (decode) work for free
- **`decode` is one line** because it's mathematically identical to `encode` with an inverted shift — no duplicated logic
- **Shift 13 is ROT13**, a special case where `encode == decode` (fun to verify: `encode(encode('Hello', 13), 13) == 'Hello'`)

### Student

That's really helpful context. I appreciate you pointing out those patterns — especially how the modulo arithmetic makes negative shifts "just work" and how that lets `decode` be just a one-liner. It's elegant.

And yeah, ROT13 being self-inverse is a neat property to keep in mind. The math actually *forces* that outcome naturally, which feels right.

The solution is solid and all the test cases pass. I'm satisfied with how this turned out — readable code, minimal duplication, and it handles all the edge cases (case preservation, non-letters, wrap-around, negative shifts).

<done/>

---

**Run end:** done after 4 turn(s) in 110.5s
