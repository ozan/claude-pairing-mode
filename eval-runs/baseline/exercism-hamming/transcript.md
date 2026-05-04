# exercism-hamming

- Source: `exercism`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:28:09.062Z

---

## Turn 1

**User:**

Exercism 'Hamming': write `distance(a, b)` returning the number of positions at which two equal-length DNA strands differ. Raise on length mismatch.

**Pair:**

[Glob(**/*hamming*)]
  No files found

[Bash(ls)]
  (Bash completed with no output)

Assistant: No existing files — I'll create the solution from scratch:

[Write(/hamming.py)]
def distance(strand_a, strand_b):
    if len(strand_a) != len(strand_b):
        raise ValueError("Strands must be of equal length")
    return sum(a != b for a, b in zip(strand_a, strand_b))


[Bash(pwd && ls -la)]
  /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-hamming-97ybMj
  total 0
  drwx------    2 oz  staff    64  3 May 20:28 .
  drwx------@ 182 oz  staff  5824  3 May 20:28 ..

[Write(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-hamming-97ybMj/hamming.py)]
def distance(strand_a, strand_b):
    if len(strand_a) != len(strand_b):
        raise ValueError("Strands must be of equal length")
    return sum(a != b for a, b in zip(strand_a, strand_b))


Assistant: Here's the implementation:

```python
def distance(strand_a, strand_b):
    if len(strand_a) != len(strand_b):
        raise ValueError("Strands must be of equal length")
    return sum(a != b for a, b in zip(strand_a, strand_b))
```

**How it works:**

1. **Length guard** — raises `ValueError` immediately if the two strands differ in length, as the Hamming distance is undefined in that case.
2. **Pairwise comparison** — `zip(strand_a, strand_b)` pairs up characters at matching positions, then `a != b` yields `True` (== `1`) for each mismatch.
3. **`sum(...)`** — counts all the `True` values, giving the total number of differing positions.

A few examples:
| `strand_a` | `strand_b` | result |
|---|---|---|
| `"GAGCCTACTAACGGGAT"` | `"CATCGTAATGACGGCCT"` | `7` |
| `"GGACGGATTCTG"` | `"AGGACGGATTCT"` | raises `ValueError` |
| `""` | `""` | `0` |

---

## Turn 2 (final)

**User:**

The solution is complete! I've created `hamming.py` with the `distance(a, b)` function that:

- **Validates equal length** — raises `ValueError` if strands differ in length
- **Counts mismatches** — uses `zip()` to pair characters position-by-position and sums the count of positions where `a != b`
- **Handles edge cases** — empty strands return 0 (no differences)

The implementation is concise, efficient (O(n) time, O(1) space), and follows Pythonic idioms. Ready to test against the Exercism test suite!

<done/>

---

**Run end**: done after 1 turn (33s)
