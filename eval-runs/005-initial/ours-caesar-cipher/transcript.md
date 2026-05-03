# ours-caesar-cipher

- Source: `ours`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T02:06:44.107Z

---

## Turn 1

**User:**

Let's implement a Caesar cipher in Python with `encode(text, shift)` and `decode(text, shift)`. Preserve case; pass non-letters through unchanged.

**Pair:**

Assistant: Good project. The core of the cipher is the character-shift formula — let's nail that first.

OPTIONS:
[A] Wrap the full expression
```diff
+++ caesar.py
@@ -0,0 +1,10 @@
+def encode(text: str, shift: int) -> str:
+    result = []
+    for c in text:
+        if c.isalpha():
+            base = ord('A') if c.isupper() else ord('a')
+            result.append(chr((ord(c) - base + shift) % 26 + base))
+        else:
+            result.append(c)
+    return ''.join(result)
```

[B] Normalize shift up front
```diff
+++ caesar.py
@@ -0,0 +1,11 @@
+def encode(text: str, shift: int) -> str:
+    shift = shift % 26
+    result = []
+    for c in text:
+        if c.isalpha():
+            base = ord('A') if c.isupper() else ord('a')
+            result.append(chr(ord(c) - base + shift + base))
+        else:
+            result.append(c)
+    return ''.join(result)
```

(Reply with A or B, or ask a follow-up question.)

Assistant: Which of these handles `encode('z', 1) == 'a'` correctly?

---

## Turn 2

**User:**

**A**

In option A, the modulo wraps the shifted position: `(ord(c) - base + shift) % 26 + base`. For 'z' (position 25), that's `(25 + 1) % 26 + base = 0 + base = 'a'`. ✓

Option B skips the modulo in the chr calculation—it just does `ord(c) - base + shift + base`, which for 'z' gives `122 - 97 + 1 + 97 = 123` (the '{' character). The pre-computed `shift % 26` doesn't help if you don't apply it to the final position.

**Pair:**

Assistant: Exactly right. `% 26` has to wrap the whole `(position + shift)` expression — normalizing shift beforehand buys nothing if you don't wrap the result.

[Bash(ls /Users/oz/dev/ai-pair-proto/caesar.py 2>/dev/null && echo exists || echo missing)]
  /Users/oz/dev/ai-pair-proto/caesar.py
  exists

[Read(/Users/oz/dev/ai-pair-proto/caesar.py)]
  1	"""Caesar cipher — encode and decode with case preservation."""
  2	
  3	
  4	def encode(text: str, shift: int) -> str:
  5	    """Shift each letter in *text* forward by *shift* positions (mod 26).
  6	
  7	    Case is preserved; non-letter characters pass through unchanged.
  8	    Negative shifts and shifts > 26 are handled correctly.
  9	    """
  10	    result: list[str] = []
  11	    for ch in text:
  12	        if ch.isalpha():
  … (11 more lines)

Assistant: Good. The file already has `encode` with the correct formula. Now for `decode`:

OPTIONS:
[A] Delegate to encode
```diff
+++ caesar.py
@@ -20,3 +20,2 @@
+def decode(text: str, shift: int) -> str:
+    return encode(text, -shift)
```

[B] Own loop, shift back
```diff
+++ caesar.py
@@ -20,6 +20,6 @@
+def decode(text: str, shift: int) -> str:
+    result = []
+    for c in text:
+        if c.isalpha():
+            base = ord('A') if c.isupper() else ord('a')
+            result.append(chr((ord(c) - base - shift) % 26 + base))
+        else:
+            result.append(c)
+    return ''.join(result)
```

(Reply with A or B, or ask a follow-up question.)

---

## Turn 3

**User:**

**A**

Option A is simpler and leverages the fact that decoding is just encoding with a negative shift. Since `encode` already handles modulo correctly (wrapping negative positions), delegating avoids duplicating the logic and potential inconsistencies. Option B repeats the entire loop—extra code that's harder to maintain if we ever update the shift formula.

**Pair:**

Assistant: Right — and there's a deeper reason: `encode(text, -shift)` means decode is *mathematically* provably correct, not just "looks right." Since `encode` applies `(pos + shift) % 26`, applying it with `-shift` gives `(pos + shift - shift) % 26 = pos % 26`. No independent logic to drift.

The file already has this. Let's write tests. Here's a design question worth thinking about:

OPTIONS:
[A] Round-trip only
```diff
+++ test_caesar.py
@@ -0,0 +1,7 @@
+from caesar import encode, decode
+
+def test_round_trip():
+    assert decode(encode('Hello, World!', 13), 13) == 'Hello, World!'
+
+def test_zero_shift():
+    assert encode('abc', 0) == 'abc'
```

[B] Round-trip + boundary cases
```diff
+++ test_caesar.py
@@ -0,0 +1,13 @@
+from caesar import encode, decode
+
+def test_round_trip():
+    assert decode(encode('Hello, World!', 13), 13) == 'Hello, World!'
+
+def test_wrap_around():
+    assert encode('xyz', 3) == 'abc'
+    assert encode('XYZ', 3) == 'ABC'
+
+def test_non_letters_pass_through():
+    assert encode('Hello, World!', 3) == 'Khoor, Zruog!'
+
+def test_large_shift():
+    assert encode('a', 27) == 'b'
```

(Reply with A or B, or ask a follow-up question.)

Assistant: Which test suite would you go with — A or B?

---

## Turn 4

**User:**

**B**

Option A only tests round-trip and zero shift—both too broad to catch edge cases. But the docstring explicitly says "Negative shifts and shifts > 26 are handled correctly," and the original problem specifies "Preserve case; pass non-letters through unchanged." These aren't aspirational—they're requirements.

Option B's tests are narrow and specific:
- `test_wrap_around` directly checks the core logic (z→a wrapping)
- `test_non_letters_pass_through` verifies the stated requirement
- `test_large_shift` tests something the docstring commits to

A round-trip test would catch *some* bugs, but it's too forgiving. If the modulo was missing and 'z' + 1 became '{', the round-trip would still pass because '{' − 1 would undo it. You need explicit boundary tests.

**Pair:**

Assistant: Exactly right — correlated bugs cancel in round-trips. The round-trip test is still worth keeping (it catches *different* bugs like swapped encode/decode), but it can't stand alone.

[Bash(ls /Users/oz/dev/ai-pair-proto/test_caesar.py 2>/dev/null && echo exists || echo missing)]
  missing

[Write(/Users/oz/dev/ai-pair-proto/test_caesar.py)]
from caesar import encode, decode


def test_round_trip():
    assert decode(encode('Hello, World!', 13), 13) == 'Hello, World!'


def test_wrap_around():
    assert encode('xyz', 3) == 'abc'
    assert encode('XYZ', 3) == 'ABC'


… (7 more lines)

[Bash(cd /Users/oz/dev/ai-pair-proto && python -m pytest test_caesar.py -v 2>&1)]
  error: Exit code 127

[Bash(cd /Users/oz/dev/ai-pair-proto && python3 -m pytest test_caesar.py -v 2>&1)]
  ============================= test session starts ==============================
  platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0 -- /Library/Developer/CommandLineTools/usr/bin/python3
  cachedir: .pytest_cache
  rootdir: /Users/oz/dev/ai-pair-proto
  collecting ... collected 4 items
  
  test_caesar.py::test_round_trip PASSED                                   [ 25%]
  test_caesar.py::test_wrap_around PASSED                                  [ 50%]
  test_caesar.py::test_non_letters_pass_through PASSED                     [ 75%]
  test_caesar.py::test_large_shift PASSED                                  [100%]
  
  ============================== 4 passed in 0.00s ===============================
  … (1 more lines)

Assistant: 4/4. The implementation is solid — we've got the core formula right, a clean single-source decode, and tests that can actually catch the bugs they claim to cover.

---

## Turn 5 (final)

**User:**

Perfect. The Caesar cipher is complete and tested:

- **`encode`** applies the core shift formula with proper modulo wrapping to handle any shift value (including negatives and shifts > 26).
- **`decode`** reuses `encode` with negated shift — mathematically provable correctness with no duplication.
- **Tests** are specific enough to catch the actual bugs (wrap-around, case preservation, non-letters, large shifts) rather than relying on forgiving round-trip assertions alone.

All four tests pass. You've got a solid, maintainable implementation.

<done/>

---

**Run end**: done after 4 turns (207s)
