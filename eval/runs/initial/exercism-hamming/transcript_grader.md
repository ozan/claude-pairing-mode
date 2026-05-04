# exercism-hamming

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:00:35

## Initial prompt

Exercism 'Hamming': write `distance(a, b)` returning the number of positions at which two equal-length DNA strands differ. Raise on length mismatch.

---

## Turn 1

### Tutor

[Glob(hamming*)]
  No files found

Tutor: Good, starting fresh. Quick question before we write it:

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] zip + generator
```diff
+++ hamming.py
@@ -0,0 +1,5 @@
+def distance(a, b):
+    if len(a) != len(b):
+        raise ValueError("Strands must be of equal length")
+    return sum(x != y for x, y in zip(a, b))
```

[B] zip without length check
```diff
+++ hamming.py
@@ -0,0 +1,3 @@
+def distance(a, b):
+    return sum(x != y for x, y in zip(a, b))
```
Shorter — `zip` pairs up characters, so extra chars in the longer strand are just ignored.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which do you prefer?

### Student

I'd go with **A**.

Option B is shorter, but the problem says we need to raise an error on length mismatch, right? So we can't just silently ignore extra characters with `zip`. Option A checks the lengths upfront and raises `ValueError` if they don't match, which is what the spec asks for.

Plus, option A is still pretty clean and readable — the length check is explicit and clear about what's happening.

---

## Turn 2

### Tutor

Tutor: Exactly right. `zip` is one of those things that looks safe but silently swallows data — it truncates to the shorter iterable with no warning. Always worth knowing when a builtin can lie to you like that.

Let me write the file:

[Write(hamming.py)]
def distance(a, b):
    if len(a) != len(b):
        raise ValueError("Strands must be of equal length")
    return sum(x != y for x, y in zip(a, b))

  File created successfully at: hamming.py

Tutor: Clean and done. A few things worth noting:

- **`bool` is a subclass of `int` in Python** — `True == 1` and `False == 0`, so `sum(x != y ...)` works naturally without an explicit `if`.
- The generator expression inside `sum(...)` is lazy — it doesn't build an intermediate list, just streams values one at a time. That matters if strands are very long.
- `zip` itself is also lazy in Python 3, so the whole thing is O(n) time, O(1) extra space.

### Student

That's really helpful context, thanks. I didn't realize that `bool` subclasses `int` — that's a neat trick that makes the one-liner work so naturally. And I appreciate the note about laziness; I can see how building an intermediate list would be wasteful when you could just accumulate the count as you go.

One quick question: is there a reason we chose `ValueError` specifically for the length mismatch, or would any exception type work for the tests?

---

## Turn 3

### Tutor

Tutor: Both reasons, actually:

1. **The tests check for it specifically.** Exercism's test suite calls `pytest.raises(ValueError)`, so any other exception type — even a custom one — would fail.

2. **It's also semantically correct.** Python's exception hierarchy has a clear convention:
   - `TypeError` → wrong *type* (e.g. passing an `int` instead of a string)
   - `ValueError` → right type, but *inappropriate value* (e.g. two strings that can't be compared because they're different lengths)

   The strands here are valid strings — the problem is what they *represent* is incompatible. That's squarely a `ValueError`.

Compare: `int("abc")` raises `ValueError` for the same reason — `"abc"` is a valid string, just not one that makes sense in that context. Same logic applies here.

### Student

Ah, that makes sense. I appreciate both angles — the practical (tests expect it) and the conceptual (it's the right semantic choice). I'll remember that distinction between `TypeError` and `ValueError`; it's a useful pattern to keep in mind for future code.

I think the solution is solid and we're good to go. The implementation handles the edge case, the exception is correct, and the laziness is a nice bonus for performance. Thanks for walking through this!

<done/>

---

**Run end:** done after 3 turn(s) in 50.9s
