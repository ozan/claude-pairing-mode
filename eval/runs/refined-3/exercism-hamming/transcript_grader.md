# exercism-hamming

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:51:22

## Initial prompt

Exercism 'Hamming': write `distance(a, b)` returning the number of positions at which two equal-length DNA strands differ. Raise on length mismatch.

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] zip + generator sum
```diff
+++ hamming.py
@@ -0,0 +1,5 @@
+def distance(strand_a, strand_b):
+    if len(strand_a) != len(strand_b):
+        raise ValueError("strands must be of equal length")
+    return sum(a != b for a, b in zip(strand_a, strand_b))
```

[B] range index loop
```diff
+++ hamming.py
@@ -0,0 +1,6 @@
+def distance(strand_a, strand_b):
+    if len(strand_a) != len(strand_b):
+        raise ValueError("strands must be of equal length")
+    return sum(1 for i in range(len(strand_a))
+               if strand_a[i] != strand_b[i])
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Quick question before we write the file — which counting approach do you prefer?

### Student

I'll go with **A**.

I like that `zip` pairs up the characters automatically, so we don't have to worry about index management. And the generator expression `a != b for a, b in zip(strand_a, strand_b)` is pretty readable — it directly expresses what we're checking. Option B works too, but it feels like extra work managing the index when `zip` does it for us.

Should I go ahead and create the file with option A?

---

## Turn 2

### Tutor

Tutor: Good reasoning — and worth keeping in mind: `zip` silently truncates to the shorter input, which is exactly why the guard must come *before* the `zip`, not after.

[Glob(hamming.py)]
  No files found

[Write(hamming.py)]
def distance(strand_a, strand_b):
    if len(strand_a) != len(strand_b):
        raise ValueError("strands must be of equal length")
    return sum(a != b for a, b in zip(strand_a, strand_b))

  File created successfully at: hamming.py

Tutor: Done. One more thing worth a quick look — there's a subtle Python feature baked into `sum(a != b ...)`:

OPTIONS:
[A] sum with explicit 1
```diff
+++ hamming.py
@@ -4,1 +4,1 @@
-    return sum(a != b for a, b in zip(strand_a, strand_b))
+    return sum(1 for a, b in zip(strand_a, strand_b) if a != b)
```
No implicit conversion — only yields `1` when there's a mismatch.

[B] sum booleans directly
```diff
+++ hamming.py
@@ -4,1 +4,1 @@
     return sum(a != b for a, b in zip(strand_a, strand_b))
```
Keeps the current form — relies on a Python guarantee about `bool`.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which form would you keep — and do you know *why* the current version works without an explicit `1`?

### Student

I'd keep **B** — the current form.

And yeah, I think I know why it works: in Python, `True` and `False` are actually subclasses of `int`, where `True == 1` and `False == 0`. So when we do `sum(a != b ...)`, each comparison returns a boolean, and `sum()` treats `True` as 1 and `False` as 0, giving us the count of mismatches.

Option A is more explicit, which could be clearer at a glance, but B is more Pythonic and still totally readable once you know that booleans work that way. It's a nice trick.

Does the solution look ready to test, or is there something else to check?

---

## Turn 3

### Tutor

Tutor: Exactly right — `bool` is literally a subclass of `int` in Python, it's not just coercion. `True is 1` is even `False`, but `True == 1` is `True` and `isinstance(True, int)` is `True`. Worth knowing cold.

The solution is solid. One quick sanity check mentally:

| call | expected | why |
|---|---|---|
| `distance("GAGCCTACTAACGGGAT", "CATCGTAATGACGGCCT")` | `7` | standard case |
| `distance("", "")` | `0` | `zip` of two empty → `sum([])` = 0 ✓ |
| `distance("AT", "A")` | `ValueError` | length guard fires ✓ |

All three fall out naturally from the implementation. Go ahead and run `pytest` (or `exercism test`) — this one's done.

### Student

Perfect — thanks for breaking that down. The mental model is clear now: booleans are actual integers, not just coerced to them.

And yeah, those three test cases all make sense with our implementation:
- The standard case just counts mismatches via the `zip` and sum.
- Empty strands pass the length check (equal length) and `zip` produces nothing, so `sum([])` = 0.
- Mismatched lengths trigger the guard before we even touch `zip`.

Running the tests now...

<done/>

---

**Run end:** done after 3 turn(s) in 79.5s
