# exercism-hamming

- Condition: `learning`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:05:00

## Initial prompt

Exercism 'Hamming': write `distance(a, b)` returning the number of positions at which two equal-length DNA strands differ. Raise on length mismatch.

---

## Turn 1

### Tutor

Thinking: The user wants me to solve the Exercism 'Hamming' exercise. Let me first look at the existing files to understand the structure.

[Glob(**/*hamming*)]
  No files found

[Bash(ls)]
  (Bash completed with no output)

[Bash(exercism download --exercise=hamming 2>/dev/null || echo "No exercism CLI or workspace found"; pwd)]
  No exercism CLI or workspace found
  /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-2ihcovk_

Tutor: No pre-existing scaffold — I'll create the solution file directly.

[Write(/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-2ihcovk_/hamming.py)]
def distance(strand_a, strand_b):
    """Return the Hamming distance between two equal-length DNA strands.

    Raises ValueError if the strands are not the same length.
    """
    if len(strand_a) != len(strand_b):
        raise ValueError("Strands must be of equal length")

    return sum(a != b for a, b in zip(strand_a, strand_b))

  File created successfully at: /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-2ihcovk_/hamming.py

[Bash(python3 -c "
from hamming import distance

# basic cases
assert distance('', '')           == 0
assert distance('A', 'A')         == 0
assert distance('A', 'T')         == 1
assert distance('GGACTGA', 'GGACTGA') == 0
assert distance('GGACTGA', 'TGACTGA') == 1
assert distance('GAGCCTACTAACGGGAT', 'CATCGTAATGACGGCCT') == 7

# length mismatch
try:
    distance('AATG', 'AAA')
    assert False, 'should have raised'
except ValueError as e:
    assert 'equal length' in str(e).lower()

print('All tests passed.')
"
)]
  All tests passed.

Tutor: All green. Here's what the solution does and *why* each piece is the way it is:

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

**1. Guard clause — length check**
```python
if len(strand_a) != len(strand_b):
    raise ValueError("Strands must be of equal length")
```
Hamming distance is only defined for equal-length sequences. We check *before* touching the strands so we always get a clear error instead of a silent wrong answer. `ValueError` is the idiomatic Python choice for bad argument values.

**2. `zip` pairs up positions**
```python
zip(strand_a, strand_b)   # → ('G','T'), ('A','A'), ('C','C'), …
```
`zip` stops at the shorter iterable, but we've already ensured equal length, so every position is covered exactly once.

**3. `a != b` produces `True`/`False` — which *are* integers**
```python
a != b   # True  → 1  (positions that differ)
         # False → 0  (positions that match)
```
Python's `bool` is a subclass of `int`, so `True == 1` and `False == 0`. This lets us count mismatches with a plain `sum`.

**4. Generator expression keeps it memory-efficient**
```python
sum(a != b for a, b in zip(strand_a, strand_b))
```
The `(... for ...)` inside `sum` is a *generator* — it yields one `0` or `1` at a time without building an intermediate list. For long strands this saves memory.

---

### Quick mental model

| Position | `GGACTGA` | `TGACTGA` | differ? |
|----------|-----------|-----------|---------|
| 0        | G         | T         | ✓ (+1)  |
| 1–6      | GACTGA    | GACTGA    | ✗       |

`distance("GGACTGA", "TGACTGA") → 1` ✓

### Student

Thanks! That's really helpful. I can see how the solution works now:

- The **guard clause** at the top catches mismatches early and gives a clear error message.
- **`zip`** elegantly pairs up characters position-by-position.
- The fact that **`True` and `False` are integers** (1 and 0) in Python is clever — it lets us count differences with a simple `sum`.
- Using a **generator expression** instead of a list keeps memory usage low, especially for very long DNA strands.

I especially like how clean and Pythonic this is. The logic is straightforward: check preconditions, then count positions where the characters differ. No loops, no index juggling, just functional tools doing their job.

One small thing I'm curious about — in the ValueError message, you wrote "Strands must be of equal length". Did you think about wording it differently, or did that phrasing feel like the clearest way to communicate the problem to whoever calls the function?

---

## Turn 2

### Tutor

Thinking: The user is asking about the wording of the ValueError message. This is a good question about API design and error message clarity. Let me think about this carefully.
  
  The message "Strands must be of equal length" is a prescriptive message - it tells you what the requirement is. Alternative phrasings could be:
  1. Descriptive: "Strands are not of equal length" - describes what went wrong
  2. Prescriptive: "Strands must be of equal length" - describes the requirement
  3. More specific: "strand_a and strand_b must have the same length" - uses parameter names
  
  
  4. Exercism-specific: Some exercises have specific expected error messages in their test suites
  
  For Exercism's Hamming exercise specifically, the test suite likely checks for a particular error message format, so the wording choice might be constrained by what the tests expect rather than being a free design decision.
  
  There's a broader design philosophy at play here though — descriptive messages like "Strands are not of equal length" tell you what went wrong, while prescriptive ones like "Strands must be of equal length" tell you what the requirement is and are often more actionable for fixing the problem. Both approaches are valid, but prescriptive messages tend to guide the user toward the solution more directly.

Tutor: Honestly, it was a small judgment call — and there's a real design consideration hiding in it worth unpacking.

---

### Two philosophies for error messages

| Style | Example | Emphasis |
|-------|---------|----------|
| **Descriptive** | `"Strands are not of equal length"` | What *went wrong* |
| **Prescriptive** | `"Strands must be of equal length"` | What *is required* |

I went prescriptive because it's slightly more **actionable** — it tells the caller what to fix, not just what broke. But both are reasonable.

A third option leans even harder into actionability by including the *actual* lengths:

```python
raise ValueError(
    f"Strands must be of equal length: got {len(strand_a)} and {len(strand_b)}"
)
```

That's often the most useful in practice — no need to add a print statement to diagnose the problem.

---

### One practical constraint: Exercism's test suite

Worth knowing: Exercism's official tests sometimes **assert on the exception message**, checking that specific text appears in it. If you're running `pytest` against the provided `hamming_test.py`, it might do something like:

```python
with pytest.raises(ValueError, match="equal length"):
    distance("AATG", "AAA")
```

So the wording isn't always purely aesthetic — it can be a **test contract**. Checking the test file first is a good habit before settling on a message.

---

### The general rule of thumb

> A good error message answers: *"What did I do wrong, and what should I do instead?"*

For `distance`, that's: the strands weren't the same length, and they need to be. The message I chose covers the *need* — adding the actual lengths covers the *what went wrong* half too.

### Student

Ah, that's really insightful. I didn't think about the error message being part of a test contract — that makes total sense. So the message isn't just for humans to read; it's actually *checked* by the test suite.

I like the prescriptive approach you went with, and I can see why including the actual lengths would be even more helpful in real debugging. Though I guess there's a trade-off: the simpler message keeps the test contract easier to maintain, while the detailed one is more practical when things actually go wrong.

Since we're solving the Exercism problem, should I check if there's a `hamming_test.py` file in the standard scaffold to see what the actual test contract expects? Or is the simple "equal length" check in the message probably safe enough for most Exercism exercises?

Actually, wait — looking back at what we've done, we already ran a full set of test cases and they all passed, including the error case. So the solution is working correctly. I think we're good here.

The code is clean, it handles all the requirements (counts mismatches, raises on length mismatch), and it's efficient. I feel confident with how this works now.

<done/>

---

**Run end:** done after 2 turn(s) in 51.8s
