# exercism-hamming

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:23:43

## Initial prompt

Exercism 'Hamming': write `distance(a, b)` returning the number of positions at which two equal-length DNA strands differ. Raise on length mismatch.

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

[Glob(hamming.py)]
  No files found

Tutor: The file doesn't exist yet. First design decision — how to count mismatches:

OPTIONS:
[A] zip over characters
```diff
+++ hamming.py
@@ -0,0 +1,5 @@
+def distance(a, b):
+    if len(a) != len(b):
+        raise ValueError("Strands must be of equal length")
+    return sum(c1 != c2 for c1, c2 in zip(a, b))
```

[B] index with range
```diff
+++ hamming.py
@@ -0,0 +1,5 @@
+def distance(a, b):
+    if len(a) != len(b):
+        raise ValueError("Strands must be of equal length")
+    return sum(1 for i in range(len(a)) if a[i] != b[i])
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which counting approach do you prefer?

### Student

I'll go with **A** — the `zip` approach.

I like it because it's more Pythonic and cleaner. We don't need to manage indices ourselves; `zip` pairs up the characters naturally, and the generator expression `c1 != c2` is straightforward to read. Option B works fine too, but feels a bit more verbose with the `range(len(a))` and indexing.

Let's start with A and see if it works.

---

## Turn 2

### Tutor

Tutor: Exactly right — and worth keeping in mind: `zip` silently truncates to the shorter strand, so if the length check were missing, `distance("AAGT", "A")` would return `0` instead of raising. The guard *must* come first.

[Write(hamming.py)]
def distance(a, b):
    if len(a) != len(b):
        raise ValueError("Strands must be of equal length")
    return sum(c1 != c2 for c1, c2 in zip(a, b))

  File created successfully at: hamming.py

Tutor: Clean and done. Quick mental test:

| call | result |
|---|---|
| `distance("GAGCCTACTAACGGGAT", "CATCGTAATGACGGCCT")` | `7` |
| `distance("", "")` | `0` |
| `distance("AAA", "AA")` | `ValueError` |

`c1 != c2` returns `True`/`False`, and `sum` treats those as `1`/`0` — so no need for an explicit `if` or `1 for …` inside the generator.

Want to run the Exercism tests, or explore anything about the solution?

### Student

That all makes sense. The mental test cases cover the main scenarios well — longer strings with differences, empty strands, and the length mismatch error.

I'm confident in the solution as-is. Let's run the Exercism tests to make sure it passes.

---

## Turn 3

### Tutor

[Glob(*test*)]
  No files found

[Bash(exercism download --exercise=hamming --track=python 2>&1 | head -5)]
  /usr/local/bin/bash: line 1: exercism: command not found

Tutor: No exercism CLI or test file in the directory. Let me run the standard Exercism Hamming test cases directly:

[Bash(python3 -c "
from hamming import distance

# identical strands
assert distance('', '') == 0
assert distance('GGACTGAAATCTG', 'GGACTGAAATCTG') == 0

# single differences
assert distance('A', 'G') == 1
assert distance('GGACGGATTCTG', 'AGGACGGATTCT') == 9

# known distance
assert distance('GAGCCTACTAACGGGAT', 'CATCGTAATGACGGCCT') == 7

# length mismatch raises
try:
    distance('AATG', 'AAA')
    assert False, 'should have raised'
except ValueError as e:
    pass

print('All tests passed!')
"
)]
  All tests passed!

Tutor: All green. The solution handles identical strands, known distances, and the `ValueError` on mismatch. Four lines, no imports needed — hard to make it much tighter than this.

### Student

Perfect! All tests pass. The solution is solid — it's clean, efficient, and handles all the edge cases correctly. I appreciate the explanation about `zip` silently truncating and why the length check has to come first; that's a gotcha I'll remember.

<done/>

---

**Run end:** done after 3 turn(s) in 65.4s
