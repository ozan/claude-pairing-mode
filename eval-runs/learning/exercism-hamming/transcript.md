# exercism-hamming

- Source: `exercism`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Output style: `Learning`
- Started: 2026-05-03T19:57:03.050Z

---

## Turn 1

**User:**

Exercism 'Hamming': write `distance(a, b)` returning the number of positions at which two equal-length DNA strands differ. Raise on length mismatch.

**Pair:**

[Glob(**/*)]
  .claude/settings.json

Assistant: No exercise files yet — I'll create the solution from scratch.

[Write(/hamming.py)]
def distance(strand_a, strand_b):
    if len(strand_a) != len(strand_b):
        raise ValueError("Strands must be of equal length")
    return sum(a != b for a, b in zip(strand_a, strand_b))


[Bash(pwd && ls)]
  /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-hamming-UR7X3K

[Write(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-hamming-UR7X3K/hamming.py)]
def distance(strand_a, strand_b):
    if len(strand_a) != len(strand_b):
        raise ValueError("Strands must be of equal length")
    return sum(a != b for a, b in zip(strand_a, strand_b))


Assistant: Here's the solution and the thinking behind it:

---

### `hamming.py`

```python
def distance(strand_a, strand_b):
    if len(strand_a) != len(strand_b):
        raise ValueError("Strands must be of equal length")
    return sum(a != b for a, b in zip(strand_a, strand_b))
```

---

### How it works

**Guard clause first** — before touching the strands, check lengths and raise immediately if they differ. Failing fast gives the caller a clear error rather than a silently wrong count.

**`zip` pairs each position** — `zip(strand_a, strand_b)` yields `(a, b)` tuples stopping at the shorter strand. Because we already confirmed equal lengths, no characters are silently skipped.

**`a != b` is a boolean** — in Python, `True == 1` and `False == 0`, so `sum(a != b for ...)` counts the number of mismatched positions directly — no `if`, no counter variable.

**Complexity:** O(n) time, O(1) extra space (generator, not a list).

---

## Turn 2 (final)

**User:**

I can see the solution is already in place and working well. Let me verify it handles the requirements correctly:

✓ **Equal-length guard**: raises `ValueError` if strands differ in length  
✓ **Hamming distance**: counts mismatches via the generator `a != b for a, b in zip(...)`  
✓ **Efficiency**: O(n) time, O(1) space (no intermediate lists)

The approach is clean — guard clause first, then a one-liner that leverages Python's boolean-as-integer coercion. No unnecessary complexity.

The solution is complete and correct for the Exercism Hamming kata.

<done/>

---

**Run end**: done after 1 turn (30s)
