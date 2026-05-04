# ours-caesar-cipher

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:54:21

## Initial prompt

Let's implement a Caesar cipher in Python with `encode(text, shift)` and `decode(text, shift)`. Preserve case; pass non-letters through unchanged.

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Tutor: Good starting point. Let's nail down the core shift mechanism first — there are two natural ways to map a character to its shifted equivalent:

OPTIONS:
[A] ascii index lookup
```diff
+++ caesar.py
@@ -0,0 +1,10 @@
+import string
+
+def encode(text, shift):
+    result = []
+    for ch in text:
+        if ch.isupper():
+            i = string.ascii_uppercase.index(ch)
+            result.append(string.ascii_uppercase[(i + shift) % 26])
+        elif ch.islower():
+            i = string.ascii_lowercase.index(ch)
+            result.append(string.ascii_lowercase[(i + shift) % 26])
+        else:
+            result.append(ch)
+    return ''.join(result)
```

[B] ord / chr arithmetic
```diff
+++ caesar.py
@@ -0,0 +1,9 @@
+def encode(text, shift):
+    result = []
+    for ch in text:
+        if ch.isupper():
+            result.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
+        elif ch.islower():
+            result.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
+        else:
+            result.append(ch)
+    return ''.join(result)
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach would you use for the per-character shift, and why?

### Student

I think I'll go with **B** — the `ord`/`chr` arithmetic approach.

Here's my reasoning: Option B feels more direct to me. We're doing math on character codes, which is straightforward and doesn't require importing anything. Option A works fine too, but it feels like we're using `string` as a lookup table when we could just do the calculation ourselves.

Also, Option B scales better mentally — if I ever needed to debug or extend this, the math is self-contained in each branch. With Option A, I'd have to think about what's in `string.ascii_uppercase` each time.

Should I start coding up the `encode` and `decode` functions using Option B?

---

## Turn 2

### Tutor

Tutor: Exactly right — and there's a sharper performance point too: `.index()` is a linear scan through the alphabet string for *every character* in the input, so it's O(26·n) vs O(n). Doesn't matter for short strings, but it's the kind of thing worth noticing.

Let me lay down the file with `encode`, then we'll decide how to wire up `decode`.

[Write(caesar.py)]
def encode(text, shift):
    result = []
    for ch in text:
        if ch.isupper():
            result.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
        elif ch.islower():
            result.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
        else:
            result.append(ch)
    return ''.join(result)

  File created successfully at: caesar.py

Tutor: Now, how should `decode` be implemented?

OPTIONS:
[A] delegate to encode
```diff
+++ caesar.py
@@ -9,0 +10,3 @@
+
+def decode(text, shift):
+    return encode(text, -shift)
```

[B] mirror encode independently
```diff
+++ caesar.py
@@ -9,0 +10,9 @@
+
+def decode(text, shift):
+    result = []
+    for ch in text:
+        if ch.isupper():
+            result.append(chr((ord(ch) - ord('A') - shift) % 26 + ord('A')))
+        elif ch.islower():
+            result.append(chr((ord(ch) - ord('a') - shift) % 26 + ord('a')))
+        else:
+            result.append(ch)
+    return ''.join(result)
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which would you pick?

### Student

I'd pick **A** — delegate to `encode`.

Here's my thinking: decoding is just encoding with a negative shift. The math works out the same way because of the modulo operation — `(x - shift) % 26` is equivalent to `(x + (-shift)) % 26`. 

Using Option A keeps the code DRY and means if we ever need to fix a bug in the shift logic, we only fix it in one place. Option B duplicates the entire loop, which feels unnecessary.

The only downside I can think of is maybe a tiny bit of clarity — someone reading `decode` might need a second to realize it's just a negated shift — but that's worth it to avoid duplication.

Should I add the `decode` function using Option A?

---

## Turn 3

### Tutor

Tutor: Spot on — Python's `%` always returns non-negative for a positive right operand, so `-shift` wraps correctly without any extra handling. Good instinct on the DRY point too.

[Edit(caesar.py)]
--- before
    return ''.join(result)

--- after
    return ''.join(result)


def decode(text, shift):
    return encode(text, -shift)

  The file caesar.py has been updated successfully.

Tutor: The implementation is essentially done. One last question — how would you verify it's correct?

OPTIONS:
[A] spot-check known values
```diff
+++ caesar.py
@@ -12,0 +13,7 @@
+
+if __name__ == "__main__":
+    assert encode("Hello, World!", 3) == "Khoor, Zruog!"
+    assert decode("Khoor, Zruog!", 3) == "Hello, World!"
+    assert encode("Z", 1) == "A"
+    assert encode("z", 1) == "a"
+    print("All tests passed.")
```

[B] round-trip property test
```diff
+++ caesar.py
@@ -12,0 +13,7 @@
+
+if __name__ == "__main__":
+    import string
+    for shift in range(27):
+        for text in ["Hello, World!", string.printable]:
+            assert decode(encode(text, shift), shift) == text
+    print("All tests passed.")
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which gives you more confidence in the implementation?

### Student

I'd go with **B** — the round-trip property test.

Here's why: Option A catches a few specific cases, which is good, but it's still just a sample. Option B is more exhaustive — it tests *every* shift value (0–26) and verifies that encoding then decoding always gets us back to the original text. That's a mathematical property we can trust: if round-tripping works for all shifts and various inputs, the implementation is correct.

Option A is useful for documentation (showing what the cipher should do), but Option B actually *proves* correctness in a more rigorous way. Plus, Option B will catch edge cases I might not have thought to spot-check manually.

The only thing I'd maybe tweak is whether `range(27)` should be `range(26)` since shift 26 is the same as shift 0 (full rotation), but either way the test is solid.

Should I add Option B to the file?

---

## Turn 4

### Tutor

Tutor: Great reasoning. Sharp catch on `range(27)` — shift 26 is a full rotation so it's redundant, but it's also exactly the boundary worth exercising explicitly (does `% 26` produce 0 cleanly?). Keeping it is fine.

[Edit(caesar.py)]
--- before
def decode(text, shift):
    return encode(text, -shift)

--- after
def decode(text, shift):
    return encode(text, -shift)


if __name__ == "__main__":
    import string
    for shift in range(27):
        for text in ["Hello, World!", string.printable]:
            assert decode(encode(text, shift), shift) == text
    print("All tests passed.")

  The file caesar.py has been updated successfully.

[Bash(python caesar.py)]
  All tests passed.

Tutor: All green. Here's the final file:

[Read(caesar.py)]
  1	def encode(text, shift):
  2	    result = []
  3	    for ch in text:
  4	        if ch.isupper():
  5	            result.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
  6	        elif ch.islower():
  7	            result.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
  8	        else:
  9	            result.append(ch)
  10	    return ''.join(result)
  11	
  12	
  … (11 more lines)

Tutor: Clean and complete. Three things worth carrying forward from this:

1. **`ord`/`chr` is O(1)** — string index lookups look innocent but hide a linear scan.
2. **`decode` = `encode(-shift)`** — when an inverse operation is just a parameter negation, don't duplicate the loop.
3. **Round-trip properties > spot-checks** — they express *what must always be true*, not just what happens to be true for one example. This scales to randomized testing tools like `hypothesis` if you ever want to go further.

### Student

Thanks — that's really helpful to have spelled out. I can see now why those patterns matter:

1. The performance thing makes intuitive sense; I'll be more conscious about `.index()` scans going forward.

2. The delegation approach feels obvious in retrospect, but I appreciate the emphasis on DRY — it's easy to just copy-paste the logic and move on.

3. The round-trip property test is elegant. It's a way of expressing the *contract* of the cipher, not just checking one example. I like that mindset.

The code is solid and all tests pass. I think we're done here — this scratches the problem we set out to solve.

<done/>

---

**Run end:** done after 4 turn(s) in 111.9s
