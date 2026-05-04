# exercism-hamming

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:00:35

## Initial prompt

Exercism 'Hamming': write `distance(a, b)` returning the number of positions at which two equal-length DNA strands differ. Raise on length mismatch.

---

## Turn 1

### Tutor

Thinking: The user wants to implement the Hamming distance exercise from Exercism. Let me first check if there's already a file for this.

[Glob(hamming*)]
  No files found

Tutor: Good, starting fresh. Quick question before we write it:

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Thinking: Let me propose two options for implementing the Hamming distance function. I'll think about the core implementation.
  
  Option A: Use `zip` with a sum/generator expression - this is clean and Pythonic
  Option B: Use `zip_longest` or index-based loop - slightly less clean
  
  Actually, let me think about a more interesting didactic question. The two implementations I want to compare:
  
  1. `sum(x != y for x, y in zip(a, b))` - this uses zip which silently truncates if lengths differ. So we need the length check separately.
  
  2. A loop with enumerate - more verbose but equivalent.
  
  Actually the more interesting question is about how `zip` behaves with unequal lengths - it silently truncates. 
  
  The key insight here is that `zip` truncates without warning, so the real pedagogical value is showing whether to validate lengths upfront or use `zip_longest` to handle mismatches explicitly. The most instructive comparison is between explicit indexing with `range(len(a))` versus the more Pythonic `zip` approach, but the subtle gotcha is that `zip` silently stops at the shorter sequence. I'm leaning toward the generator expression approach since it avoids creating an intermediate list, then I'll show both the zip-based and index-based implementations as concrete examples to illustrate the difference.

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

PRIVATE: best=A
PRIVATE: rationale=zip silently truncates to the shorter iterable, so "AAGT" vs "AA" would return 0 instead of raising. The spec requires raising on length mismatch, so the length check is mandatory. Option B looks clean but produces silently wrong results — it never raises and undercounts differences when lengths differ.

Tutor: Which do you prefer?

### Student

I'd go with **A**.

Option B is shorter, but the problem says we need to raise an error on length mismatch, right? So we can't just silently ignore extra characters with `zip`. Option A checks the lengths upfront and raises `ValueError` if they don't match, which is what the spec asks for.

Plus, option A is still pretty clean and readable — the length check is explicit and clear about what's happening.

---

## Turn 2

### Tutor

Thinking: The user picked the correct option (A) and gave good reasoning. Let me write the file and confirm.

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

Thinking: The user is asking about why `ValueError` specifically. This is a good question. In Exercism's test suite, they typically test for `ValueError` specifically. But more broadly, `ValueError` is the semantically correct exception - it's for when a function receives an argument of the right type but an inappropriate value. The strands are the right type (strings) but their values are incompatible (wrong length). This is in contrast to `TypeError` (wrong type) or a custom exception.
  
  Let me answer this directly without needing a propose_options call since it's a clarifying/factual question rather than a design decision.

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
