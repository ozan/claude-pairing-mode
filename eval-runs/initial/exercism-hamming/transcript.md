# exercism-hamming

- Source: `exercism`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:38:32.839Z

---

## Turn 1

**User:**

Exercism 'Hamming': write `distance(a, b)` returning the number of positions at which two equal-length DNA strands differ. Raise on length mismatch.

**Pair:**

[Glob(hamming*)]
  No files found

Assistant: Good starting point. Let me ask a question worth thinking about before we write a line:

OPTIONS:
[A] zip + sum
```diff
+++ hamming.py
@@ -0,0 +1,5 @@
+def distance(a, b):
+    if len(a) != len(b):
+        raise ValueError("strands must be equal length")
+    return sum(x != y for x, y in zip(a, b))
```

[B] zip_longest + sum
```diff
+++ hamming.py
@@ -0,0 +1,6 @@
+from itertools import zip_longest
+def distance(a, b):
+    if len(a) != len(b):
+        raise ValueError("strands must be equal length")
+    return sum(x != y for x, y in zip_longest(a, b))
```

(Reply with A or B, or ask a follow-up question.)

Assistant: Which would you use?

---

## Turn 2 (final)

**User:**

**A** — I'd choose Option A.

Here's the reasoning:

Once we've verified that `len(a) == len(b)`, plain `zip` and `zip_longest` are behaviorally identical (both will iterate through all pairs). Using `zip_longest` after the length check is extra machinery that does nothing — it imports a function and applies logic we don't need.

Option A is simpler, doesn't require an extra import, and makes the intent clearer: the guard clause handles the only case where length matters, and then we just compare element by element.

**Option B has a subtle inefficiency**: it uses the more complex tool when the simpler one suffices. Not wrong, but unnecessary.

Let me write Option A:Done! ✓

The function:
1. **Guards first**: raises `ValueError` if the strands aren't the same length
2. **Counts mismatches**: zips the two strands together and sums the positions where characters differ (`x != y` evaluates to `True` = 1, `False` = 0)
3. **Is Pythonic**: generator expression + `sum` is the idiomatic approach

Quick mental tests:
- `distance("", "")` → `0` ✓
- `distance("AG", "CT")` → `2` ✓
- `distance("A", "")` → `ValueError` ✓

<done/>

---

**Run end**: done after 1 turn (27s)
