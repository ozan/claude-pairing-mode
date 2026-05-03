# ours-caesar-cipher

- Source: `ours`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T00:34:43.325Z

---

## Turn 1

**User:**

Let's implement a Caesar cipher in Python with `encode(text, shift)` and `decode(text, shift)`. Preserve case; pass non-letters through unchanged.

**Pair:**

Assistant: Good first decision: the core shift formula. Which of these is correct?

OPTIONS:
[A] Direct ord arithmetic
```diff
+++ caesar.py
@@ -0,0 +1,10 @@
+def encode(text, shift):
+    result = []
+    for c in text:
+        if not c.isalpha():
+            result.append(c)
+            continue
+        base = ord('A') if c.isupper() else ord('a')
+        result.append(chr((ord(c) + shift) % 26 + base))
+    return ''.join(result)
+
+def decode(text, shift):
+    return encode(text, -shift)
```

[B] Helper + normalised formula
```diff
+++ caesar.py
@@ -0,0 +1,12 @@
+def _shift_char(c, shift):
+    if not c.isalpha():
+        return c
+    base = ord('A') if c.isupper() else ord('a')
+    return chr((ord(c) - base + shift) % 26 + base)
+
+def encode(text, shift):
+    return ''.join(_shift_char(c, shift) for c in text)
+
+def decode(text, shift):
+    return encode(text, -shift)
```

(Reply with A or B, or ask a follow-up question.)

Assistant: Before applying the modulo, which space are you working in — and why does that matter here?

---

## Turn 2

**User:**

Looking at the two options, the critical issue is **which space the modulo operates in**.

Option A does `(ord(c) + shift) % 26 + base`. If I trace through with 'A' shifted by 1:
- `ord('A')` = 65
- `(65 + 1) % 26` = 66 % 26 = 14
- `14 + 65` = 79 = 'O'

That's wrong! It should wrap to 'B' (66).

Option B does `(ord(c) - base + shift) % 26 + base`. Same example:
- `ord('A') - ord('A')` = 0 (normalizes to 0-25 space)
- `(0 + 1) % 26` = 1
- `1 + 65` = 66 = 'B'

Correct!

The issue: **modulo in the 0-25 normalized space wraps correctly; modulo in the ASCII space (65-90) doesn't**. Option A tries to apply modulo to the raw ASCII value, which breaks the circular rotation. Option B normalizes first, applies modulo in the right space, then shifts back.

**B** is correct. It's cleaner too — the helper makes the logic reusable and easier to test.

**Pair:**

Assistant: Exactly right — and your trace is a great way to catch it. The `-base` / `+base` sandwich is the pattern: normalize → operate → denormalize. You'll see it all over bit manipulation and modular arithmetic.

[Glob(caesar.py)]
  No files found

[Write(caesar.py)]
def _shift_char(c, shift):
    if not c.isalpha():
        return c
    base = ord('A') if c.isupper() else ord('a')
    return chr((ord(c) - base + shift) % 26 + base)

def encode(text, shift):
    return ''.join(_shift_char(c, shift) for c in text)

def decode(text, shift):
    return encode(text, -shift)


Assistant: Now let's add tests. One decision worth making intentionally — how should we cover the wrap-around cases?

OPTIONS:
[A] Property-based roundtrip
```diff
+++ test_caesar.py
@@ -0,0 +1,10 @@
+import string, random
+from caesar import encode, decode
+
+def test_roundtrip():
+    for _ in range(200):
+        text = ''.join(random.choices(string.printable, k=40))
+        shift = random.randint(-100, 100)
+        assert decode(encode(text, shift), shift) == text
+
+def test_known(): assert encode('Hello, World!', 13) == 'Uryyb, Jbeyq!'
```

[B] Explicit boundary cases
```diff
+++ test_caesar.py
@@ -0,0 +1,12 @@
+from caesar import encode, decode
+
+def test_basic():    assert encode('Hello, World!', 13) == 'Uryyb, Jbeyq!'
+def test_case():     assert encode('abc', 1) == 'bcd'
+def test_wrap():     assert encode('xyz', 3) == 'abc'
+def test_upper():    assert encode('XYZ', 3) == 'ABC'
+def test_nonalpha(): assert encode('a1!', 1) == 'b1!'
+def test_shift26():  assert encode('Hello', 26) == 'Hello'
+def test_neg():      assert encode('bcd', -1) == 'abc'
+
+def test_decode():
+    assert decode(encode('Secret msg 42!', 7), 7) == 'Secret msg 42!'
```

(Reply with A or B, or ask a follow-up question.)

Assistant: Which testing strategy gives you higher confidence in correctness — and why?

---

## Turn 3

**User:**

**B** — explicit boundary cases give me higher confidence here.

Here's my reasoning:

**Why B wins:**
1. **Wrap-around is the most error-prone part** — the core algorithm. Option B explicitly tests `'xyz' + 3 → 'abc'`, which directly validates the normalize-modulo-denormalize pattern we just carefully chose. Option A tests it randomly, but if there's a subtle bug where both `encode` and `decode` fail in sync, a roundtrip could still pass and hide it.

2. **Shift by 26 should be identity** — `encode('Hello', 26) == 'Hello'`. This is a critical invariant that I want to *know* works, not hope a random iteration hits it.

3. **Debugging is cheap** — if `test_wrap()` fails, I immediately know the wrap-around is broken. If option A's random test fails, I'm digging through a random string and shift to reproduce it.

4. **The spec is small and explicit** — preserve case, non-letters pass through, wrap around. Option B maps 1:1 to the spec; option A tests emergent properties. For something this well-defined, explicit > random.

Option A is great for finding unexpected bugs in complex systems, but here the algorithm is short and the spec is clear. Explicit boundary testing is the right tool.

**Pair:**

Assistant: Solid reasoning — but one part worth poking at: you said a roundtrip could hide a bug where encode and decode fail in sync. Option A actually includes `test_known` which pins `encode('Hello...', 13)` to a literal string, independent of decode. That anchors the whole thing to ground truth just like your explicit cases do.

The real tradeoff:

- **B** maps directly to the spec, is trivially debuggable, and the Caesar cipher's surface area is small enough that you can enumerate the meaningful boundaries by hand.
- **A** would catch things you didn't think to write — e.g., `shift=0` with a non-ASCII printable like `'§'`, or very large negative shifts. The random corpus exercises far more of the input space.

For a 10-line function with a clear spec, B is a perfectly reasonable call. The argument I'd make for A is that the wrap-around case you care most about *will* be hit many times across 200 random trials, plus you get all the cases you didn't think of for free.

Want to stick with B, or switch to A — or take both (a few explicit anchors + the roundtrip)?

---

## Turn 4

**User:**

That's a fair push. You're right — **A's `test_known` does anchor to ground truth independently**, and I was dismissing the value of random coverage too quickly.

I'll go with **both**: explicit boundary cases (from B) + the roundtrip (from A). Here's why:

- **B's explicit cases** are self-documenting — they map directly to the spec and future maintainers can see at a glance what the cipher should do. They're cheap to read.
- **A's roundtrip** catches edge cases I didn't enumerate — like `shift=0`, or weird negative values — without me having to think of them. And it's a real invariant: if encode/decode are inverses, that's a meaningful property to lock in.

The extra lines are minimal, and I get both clarity *and* depth.

Should I write the combined version (explicit cases + roundtrip + the `test_known` anchor)?

**Pair:**

Assistant: Yes — good synthesis. Let me write it:

[Write(test_caesar.py)]
import string, random
from caesar import encode, decode

# --- explicit boundary cases (spec documentation) ---

def test_basic():    assert encode('Hello, World!', 13) == 'Uryyb, Jbeyq!'
def test_case():     assert encode('abc', 1) == 'bcd'
def test_wrap():     assert encode('xyz', 3) == 'abc'
def test_upper():    assert encode('XYZ', 3) == 'ABC'
def test_nonalpha(): assert encode('a1!', 1) == 'b1!'
def test_shift26():  assert encode('Hello', 26) == 'Hello'
def test_neg():      assert encode('bcd', -1) == 'abc'
… (12 more lines)

[Bash(cd /Users/oz/dev/ai-pair-proto && python -m pytest caesar.py test_caesar.py -v 2>&1)]
  error: Exit code 127

[Bash(cd /Users/oz/dev/ai-pair-proto && python3 -m pytest test_caesar.py -v 2>&1)]
  error: Exit code 1

[Bash(cd /Users/oz/dev/ai-pair-proto && python3 -m unittest discover -v 2>&1 || python3 test_caesar.py 2>&1 || pytest test_caesar.py -v 2>&1)]
  error: Exit code 127

[Bash(pip3 install pytest -q 2>&1 && python3 -m pytest /Users/oz/dev/ai-pair-proto/test_caesar.py -v 2>&1)]
  error: Exit code 4

[Bash(python3 -m pytest test_caesar.py -v 2>&1)]
  ============================= test session starts ==============================
  platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0 -- /Library/Developer/CommandLineTools/usr/bin/python3
  cachedir: .pytest_cache
  rootdir: /Users/oz/dev/ai-pair-proto/eval-runs/004-initial/ours-caesar-cipher
  collecting ... collected 9 items
  
  test_caesar.py::test_basic PASSED                                        [ 11%]
  test_caesar.py::test_case PASSED                                         [ 22%]
  test_caesar.py::test_wrap PASSED                                         [ 33%]
  test_caesar.py::test_upper PASSED                                        [ 44%]
  test_caesar.py::test_nonalpha PASSED                                     [ 55%]
  test_caesar.py::test_shift26 PASSED                                      [ 66%]
  … (5 more lines)

Assistant: 9/9 passing. Both files are clean:

**`caesar.py`** — the normalize→operate→denormalize pattern handles wrap, case, and non-letters correctly in 12 lines.

**`test_caesar.py`** — explicit cases document the spec; the roundtrip hunts edge cases you didn't enumerate. Together they give you both clarity and coverage depth.

---

## Turn 5 (final)

**User:**

Looks good — clean implementation and solid test coverage. Both files are working as intended. 

The Caesar cipher is complete: `encode()` and `decode()` correctly handle case preservation, non-letters, and wrap-around; the tests validate the spec explicitly while also catching edge cases through randomized roundtrips.

<done/>

---

**Run end**: done after 4 turns (194s)
