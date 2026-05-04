# ours-caesar-cipher

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:05:14

## Initial prompt

Let's implement a Caesar cipher in Python with `encode(text, shift)` and `decode(text, shift)`. Preserve case; pass non-letters through unchanged.

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Tutor: Good starting point. The crux of this whole thing is the shift formula. Which of these do you think is correct?

OPTIONS:
[A] Skip base normalization
```diff
+++ caesar.py
@@ -0,0 +1,12 @@
+def encode(text, shift):
+    out = []
+    for c in text:
+        if c.isalpha():
+            base = ord('A') if c.isupper() else ord('a')
+            out.append(chr((ord(c) + shift) % 26 + base))
+        else:
+            out.append(c)
+    return ''.join(out)
+
+def decode(text, shift):
+    return encode(text, -shift)
```

[B] Normalize to 0–25 first
```diff
+++ caesar.py
@@ -0,0 +1,12 @@
+def encode(text, shift):
+    out = []
+    for c in text:
+        if c.isalpha():
+            base = ord('A') if c.isupper() else ord('a')
+            out.append(chr((ord(c) - base + shift) % 26 + base))
+        else:
+            out.append(c)
+    return ''.join(out)
+
+def decode(text, shift):
+    return encode(text, -shift)
```

(Reply with A or B, or ask a follow-up question.)

### Student

I think **B** is correct.

Let me work through why: In option A, we're doing `(ord(c) + shift) % 26 + base`. The problem is that `ord(c)` is already a large number (65+ for uppercase, 97+ for lowercase), so taking `(large_number + shift) % 26` gives us a remainder that's between 0–25, but then we add `base` back on. That would actually work mathematically, but it's confusing because we're mixing the actual ASCII value with the modulo result.

In option B, we first normalize the character to 0–25 by subtracting the base (`ord(c) - base`), then add the shift, then take modulo 26 to wrap around, and finally add the base back. This way we're always working within the 0–25 range before applying the shift, which feels cleaner and more correct.

Actually, wait—let me reconsider option A. If `ord('A')` is 65 and we have 'A' with shift 1: `(65 + 1) % 26 + 65 = 66 % 26 + 65 = 14 + 65 = 79`. That's not 'B' (66). So option A is definitely wrong.

With option B on 'A' + 1: `(65 - 65 + 1) % 26 + 65 = 1 % 26 + 65 = 1 + 65 = 66`, which is 'B'. That's correct.

So the answer is **B**.

---

## Turn 2

### Tutor

Tutor: Exactly right — and you nailed the key insight: `ord('A')` is 65, not 0, so `% 26` on the raw value scrambles the alphabet. Subtracting `base` first is what makes the modular arithmetic actually model a 26-letter ring.

Let me write the file:

[Write(caesar.py)]
def encode(text, shift):
    out = []
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            out.append(chr((ord(c) - base + shift) % 26 + base))
        else:
            out.append(c)
    return ''.join(out)

def decode(text, shift):
    return encode(text, -shift)
… (1 more lines)
  File created successfully at: caesar.py

Tutor: One small bonus: `decode` delegates to `encode` with `-shift`. Python's `%` always returns a non-negative result when the divisor is positive, so `(-3) % 26 == 23` — wrapping works correctly in both directions with no extra code.

Want to add tests, or move on to anything else?

### Student

I'd like to add some quick tests to make sure it actually works! Let me write a few test cases to verify the encode and decode functions handle the main scenarios—uppercase, lowercase, mixed case, non-letters, and that decode reverses encode properly.

Can we add a simple test file to check those cases?

---

## Turn 3

### Tutor

OPTIONS:
[A] pytest functions
```diff
+++ test_caesar.py
@@ -0,0 +1,20 @@
+from caesar import encode, decode
+
+def test_encode_lowercase():
+    assert encode("hello", 3) == "khoor"
+
+def test_encode_uppercase():
+    assert encode("HELLO", 3) == "KHOOR"
+
+def test_encode_mixed_and_nonletters():
+    assert encode("Hello, World!", 3) == "Khoor, Zruog!"
+
+def test_wrap_around():
+    assert encode("xyz", 3) == "abc"
+
+def test_decode_reverses_encode():
+    assert decode(encode("Hello, World!", 13), 13) == "Hello, World!"
```
Run with `pytest test_caesar.py`.

[B] Plain assert script
```diff
+++ test_caesar.py
@@ -0,0 +1,16 @@
+from caesar import encode, decode
+
+assert encode("hello", 3) == "khoor"
+assert encode("HELLO", 3) == "KHOOR"
+assert encode("Hello, World!", 3) == "Khoor, Zruog!"
+assert encode("xyz", 3) == "abc"
+assert decode(encode("Hello, World!", 13), 13) == "Hello, World!"
+
+print("All tests passed!")
```
Run with `python test_caesar.py`.

(Reply with A or B, or ask a follow-up question.)

### Student

I'll go with **B** for now. Since this is a small problem with just a few test cases, the plain assert script is simpler and faster to run without needing pytest installed. I can see all the assertions right there and get immediate feedback.

Let's create that and run it to verify everything works!

---

## Turn 4

### Tutor

Tutor: Fair enough for a quick check. Worth knowing though: when a plain assert fails you only get `AssertionError` with no context — pytest would show you the actual vs expected values, which saves real time when debugging. Easy to switch later.

Let me write and run it:

[Write(test_caesar.py)]
from caesar import encode, decode

assert encode("hello", 3) == "khoor"
assert encode("HELLO", 3) == "KHOOR"
assert encode("Hello, World!", 3) == "Khoor, Zruog!"
assert encode("xyz", 3) == "abc"
assert decode(encode("Hello, World!", 13), 13) == "Hello, World!"

print("All tests passed!")

  File created successfully at: test_caesar.py

[Bash(python test_caesar.py)]
  All tests passed!

Tutor: All green. The wrap-around case (`xyz` → `abc`) and the round-trip decode are both working correctly.

The implementation is complete — `caesar.py` with `encode`/`decode`, and a test file covering the main cases. Anything else you'd like to add or extend?

### Student

Nope, I think we're good! The Caesar cipher is working correctly—it handles uppercase, lowercase, mixed case, non-letters, and wrapping around the alphabet. The decode function cleverly reuses encode with a negative shift, and Python's modulo operator handles the wraparound for us automatically.

The tests confirm everything works as expected. I learned a lot about why normalizing to 0–25 before applying modular arithmetic is crucial, and how to structure a simple cipher implementation.

<done/>

---

**Run end:** done after 4 turn(s) in 89.9s
