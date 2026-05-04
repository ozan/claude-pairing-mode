# exercism-hamming

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:40:33

## Initial prompt

Exercism 'Hamming': write `distance(a, b)` returning the number of positions at which two equal-length DNA strands differ. Raise on length mismatch.

---

## Turn 1

### Tutor

Thinking: The user wants to solve the Exercism "Hamming" problem - implementing a `distance(a, b)` function that calculates the Hamming distance between two DNA strands. Let me think about the best approach and present a teaching opportunity.
  
  First, let me check if there's already a file for this.

[Glob(hamming*)]
  No files found

Tutor: Good starting point. Before writing any code, here's the core counting question:

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Thinking: Now let me propose the two options for how to count differing positions.

OPTIONS:
[A] zip + sum
```diff
+++ hamming.py
@@ -0,0 +1,5 @@
+def distance(a, b):
+    if len(a) != len(b):
+        raise ValueError("Strands must be of equal length")
+    return sum(x != y for x, y in zip(a, b))
```

[B] enumerate + counter
```diff
+++ hamming.py
@@ -0,0 +1,7 @@
+def distance(a, b):
+    if len(a) != len(b):
+        raise ValueError("Strands must be of equal length")
+    count = 0
+    for i, c in enumerate(a):
+        if c != b[i]:
+            count += 1
+    return count
```

(Reply with A or B, or ask a follow-up question.)

PRIVATE: best=A
PRIVATE: rationale=Both are correct and O(n). The zip+sum approach is idiomatic Python: bool is a subclass of int so summing comparisons works cleanly, and zip pairs elements without needing index arithmetic. The enumerate approach is more verbose and uses index lookup (b[i]) where zip already handles pairing. The zip version is the canonical Pythonic answer.

Tutor: Which would you go with?

### Student

I think I'll go with **A**.

I like that it's more concise and Pythonic. The `zip` function pairs up characters from both strands automatically, and using `sum()` on a generator expression with `x != y` feels clean — each comparison produces `True` or `False`, which sum treats as 1 or 0.

Option B works too, but it feels more verbose for what's essentially the same logic. I'd rather let Python's built-in functions do the heavy lifting.

Should I go ahead and write that out?

---

## Turn 2

### Tutor

Thinking: The user picked option A (zip + sum), which is my preferred answer. They gave a great explanation of why - they understand that bool is a subclass of int in Python, so True/False sum as 1/0. Let me write the file and then maybe ask one more question about an interesting edge case or refinement.

Tutor: Exactly right — and you nailed the key insight: `bool` is a subclass of `int` in Python, so `sum()` over comparisons just works. Let me write it out.

[Write(hamming.py)]
def distance(a, b):
    if len(a) != len(b):
        raise ValueError("Strands must be of equal length")
    return sum(x != y for x, y in zip(a, b))

  File created successfully at: hamming.py

Tutor: Done. One more thing worth thinking about — `zip` has a subtle behavior when the two strings are *different lengths*:

OPTIONS:
[A] len check before zip
Check `len(a) != len(b)` first, then `zip`. If lengths differ, `zip` silently stops at the shorter strand — so without the guard, a mismatch would return a wrong (smaller) count instead of raising.

[B] zip catches mismatches fine
`zip` pairs every character, so if the strings differ in length it would naturally surface an error during iteration — no explicit length check needed.

(Reply with A or B, or ask a follow-up question.)

PRIVATE: best=A
PRIVATE: rationale=zip silently truncates to the shorter iterable — it does NOT raise on length mismatch. Without the explicit len check, distance("AAGT", "AAG") would return 0 instead of raising, which is a silent wrong answer. The guard is essential and must come before zip.

Tutor: Which statement is true about `zip` on mismatched lengths?

### Student

**A** is correct.

I remember now — `zip` stops at the shortest iterable. So if I had strands like `"AAAA"` and `"AA"`, `zip` would only pair up the first two characters and silently ignore the rest. That would give me a distance of 0 (or whatever the first two positions differ by), when I should actually raise an error because the lengths don't match.

That's why the length check *before* calling `zip` is essential — it catches the mismatch upfront and raises the ValueError, which is what the problem asks for. Without it, the function would return an incorrect answer instead of failing properly.

So keeping that `if len(a) != len(b)` guard at the top is the right move.

<done/>

---

**Run end:** done after 2 turn(s) in 33.9s
