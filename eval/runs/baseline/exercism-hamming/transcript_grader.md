# exercism-hamming

- Condition: `baseline`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T20:50:37

## Initial prompt

Exercism 'Hamming': write `distance(a, b)` returning the number of positions at which two equal-length DNA strands differ. Raise on length mismatch.

---

## Turn 1

### Tutor

[Glob(**/*hamming*)]
  No files found

[Glob(**/*.py)]
  No files found

Tutor: No existing files — I'll create the solution from scratch:

[Write(/hamming.py)]
def distance(strand_a, strand_b):
    if len(strand_a) != len(strand_b):
        raise ValueError("Strands must be of equal length")
    return sum(a != b for a, b in zip(strand_a, strand_b))

  error: EROFS: read-only file system, open '/hamming.py'

[Glob(*)]
  No files found

[Bash(pwd && ls -la)]
  /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-j4dgu853
  total 0
  drwx------    2 oz  staff    64  4 May 20:50 .
  drwx------@ 222 oz  staff  7104  4 May 20:50 ..

[Write(/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-j4dgu853/hamming.py)]
def distance(strand_a, strand_b):
    if len(strand_a) != len(strand_b):
        raise ValueError("Strands must be of equal length")
    return sum(a != b for a, b in zip(strand_a, strand_b))

  File created successfully at: /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-j4dgu853/hamming.py

Tutor: Here's the solution:

```python
def distance(strand_a, strand_b):
    if len(strand_a) != len(strand_b):
        raise ValueError("Strands must be of equal length")
    return sum(a != b for a, b in zip(strand_a, strand_b))
```

**How it works:**

| Step | Detail |
|---|---|
| **Guard clause** | Raises `ValueError` immediately if the strands have different lengths — before doing any work |
| **`zip(strand_a, strand_b)`** | Pairs up characters at the same position |
| **`a != b`** | Evaluates to `True` (= 1) when the bases differ, `False` (= 0) when they match |
| **`sum(...)`** | Counts up all the `True` values → the Hamming distance |

**Examples:**
```python
distance("GAGCCTACTAACGGGAT", "CATCGTAATGACGGCCT")  # → 7
distance("GGACGGATTCTG", "AGGACGGATTCT")             # raises ValueError
distance("", "")                                      # → 0
distance("A", "A")                                    # → 0
distance("A", "T")                                    # → 1
```

### Student

Thanks for walking through that! I can see how the solution works now. Let me make sure I understand the key parts:

1. **The guard clause** makes sense — we need to catch mismatched lengths right away and raise the error before we try to compare anything.

2. **The `zip` + comparison trick** is clever. By zipping the two strands together, we automatically pair up characters at the same positions, and then `a != b` gives us `True` or `False` for each pair.

3. **Using `sum()` on booleans** — I forget that `True` counts as 1 and `False` as 0 in Python, so summing them up gives us the count of differences. That's elegant.

So if I had `"AG"` and `"AT"`, it would zip to `[('A', 'A'), ('G', 'T')]`, then `a != b` gives `[False, True]`, and `sum()` gives `1`. Perfect.

One question: what happens if one or both strands are empty strings? The guard clause would pass (both have length 0), and then `zip` on two empty strings would produce no pairs, so `sum()` would return 0. Is that the expected behavior?

---

## Turn 2

### Tutor

Tutor: Yes, your trace-through is exactly right, and `distance("", "")` → `0` is the **correct, expected behavior** — not a quirk to worry about.

It's mathematically consistent with the definition: the Hamming distance is the number of *positions* at which the strands differ. Two empty strands have zero positions total, so they differ at zero of them. It's the same logic as why the sum of an empty list is 0 — the [identity element](https://en.wikipedia.org/wiki/Empty_sum) for addition.

You can verify the guard clause still does its job cleanly at the boundary:

```python
distance("", "")   # → 0  ✅ lengths match (0 == 0), no pairs, sum = 0
distance("", "A")  # → ValueError ✅ lengths mismatch (0 != 1)
distance("A", "")  # → ValueError ✅ lengths mismatch (1 != 0)
```

The only thing worth noting is that `zip` silently stops at the shorter strand if the lengths *differ* — e.g. `zip("AG", "A")` gives just `[('A', 'A')]`, dropping the `'G'` entirely. That's exactly why the **guard clause must come first**: without it, `zip` would quietly ignore the tail of the longer strand and return a wrong answer instead of raising. The explicit length check is what gives the function its correct behaviour for mismatched inputs.

### Student

Ah, that makes total sense! I really appreciate the clarification on why the guard clause has to come *first*. If we didn't check lengths upfront, `zip` would just silently truncate to the shorter strand and we'd get a wrong answer instead of an error. That's a sneaky bug waiting to happen.

And you're right about the empty case — it's not special; it just naturally falls out from how the algorithm works. The math checks out: zero positions means zero differences.

I feel like I've got a solid grasp on this now:
- Guard clause for the error case
- `zip` to pair up positions
- Compare each pair with `!=`
- Sum the `True` values to get the count

The solution is clean and works correctly for all the test cases. I'm happy with it!

<done/>

---

**Run end:** done after 2 turn(s) in 35.4s
