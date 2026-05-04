# exercism-hamming

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:23:43

## Initial prompt

Exercism 'Hamming': write `distance(a, b)` returning the number of positions at which two equal-length DNA strands differ. Raise on length mismatch.

---

## Turn 1

### Tutor

Thinking: The user wants to implement the Hamming distance function for the Exercism problem. Let me think about the best approach and present an interesting option question.
  
  The core question here is about how to implement `distance(a, b)`. The main decision is how to count the differences. I'll present two options:
  1. Using `zip` with a generator expression / sum
  2. Using explicit loop with a counter
  
  Actually, there are a few interesting decisions:
  1. How to count differences (zip+sum vs loop)
  2. Whether to use `zip` (which silently truncates) or handle length checking carefully
  
  Let me think about the most interesting first decision. 
  
  The length mismatch check is straightforward - raise a ValueError. The interesting part is the counting mechanism. I could use `zip` with a sum of comparisons, or iterate through with explicit indexing. The `zip` approach is more Pythonic, but indexing is also valid and perhaps more explicit about what's happening.
  
  I should place the length check before any comparison logic to avoid subtle bugs. Now I'm thinking about which approach to present - the `zip` method is cleaner and more idiomatic Python, so that's probably the better teaching example. I'll create a `hamming.py` file with this solution.

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

[Glob(hamming.py)]
  No files found

Thinking: The file doesn't exist yet. Let me propose the first decision: how to count the mismatches. I'll present two options for the core counting logic.
  
  Option A: Use `zip` with a generator expression - `sum(c1 != c2 for c1, c2 in zip(a, b))`
  Option B: Use `range(len(a))` with indexing - `sum(1 for i in range(len(a)) if a[i] != b[i])`
  
  The best is Option A - it's more Pythonic and expressive. But there's an interesting subtle point: `zip` silently truncates to the shorter iterable. 
  
  Since I'm adding an explicit length check beforehand, the truncation behavior won't cause issues even if someone forgets to validate the inputs. Now I'm deciding whether to start with the overall structure or dive straight into the counting mechanism. Given how short this problem is, I'll jump to the counting logic since that's where the interesting trade-offs are.

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

PRIVATE: best=A
PRIVATE: rationale=zip is the idiomatic Python approach for parallel iteration - it avoids explicit indexing, reads naturally as "pair up characters", and works correctly on any iterable (not just sequences). The range+index version works but is more C-style; it also calls len(a) at runtime which is minor overhead. The subtle trap with zip is that it silently truncates on length mismatch, but since we guard with an explicit length check first, that's not an issue here. This is a good teaching moment about when zip is safe to use.

Tutor: Which counting approach do you prefer?

### Student

I'll go with **A** — the `zip` approach.

I like it because it's more Pythonic and cleaner. We don't need to manage indices ourselves; `zip` pairs up the characters naturally, and the generator expression `c1 != c2` is straightforward to read. Option B works fine too, but feels a bit more verbose with the `range(len(a))` and indexing.

Let's start with A and see if it works.

---

## Turn 2

### Tutor

Thinking: The user picked Option A (the `zip` approach). Let me create the file and then think about whether there's another interesting question to ask.
  
  One interesting follow-up: the `zip` behavior on mismatched lengths. Since `zip` silently truncates, if someone removed the length check, they'd get wrong results (always 0 for empty string paired with anything, or just the distance up to the shorter length). This is worth noting.
  
  Actually, let me just write the file and then consider if there's a follow-up question worth asking. 
  
  One thing worth asking: should we check length mismatch with `if len(a) != len(b)` or use a different approach? That's probably not very interesting.
  
  
  I could explore `zip_longest` as an alternative—using a fill value different from valid DNA characters would let us detect length mismatches and count differences in one pass, though it's more complex. But the current solution is clean and complete, so I'll just write it out and do a quick sanity check. a note.
  
  Actually wait - before I write the file, let me think of one more interesting question. The solution is 5 lines and quite complete. But there's a subtle thing worth asking: what if we used `zip_longest` instead? That would let us handle the length check differently. Let me think...
  
  Using `zip_longest` would actually make things more complicated - we'd still need the length check upfront, and we'd be adding unnecessary complexity without any real benefit. Not worth exploring.
  
  The real teaching moment here is reinforcing why the length check must come first given how `zip` truncates to the shorter sequence - that's the Pythonic insight the user appreciated about option A.

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

Thinking: The user wants to run the Exercism tests. Let me run them. The typical Exercism test command is `pytest` or `python -m pytest`. Let me check if there's a test file present.

[Glob(*test*)]
  No files found

[Bash(exercism download --exercise=hamming --track=python 2>&1 | head -5)]
  /usr/local/bin/bash: line 1: exercism: command not found

Thinking: The exercism CLI isn't available. Let me check if there's a test file somewhere or if we need to write one. I'll look for the standard Exercism Hamming test file or just run a quick inline test.
  
  Let me write a quick test inline using Python's unittest or just run some assertions.

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
