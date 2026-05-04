# euler-6-sum-square-diff

- Source: `project-euler`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Output style: `Learning`
- Started: 2026-05-04T00:15:05.376Z

---

## Turn 1

**User:**

Project Euler #6: find the difference between the square of the sum and the sum of the squares of the first 100 natural numbers.

**Pair:**

Assistant: ## Project Euler #6

### The Two Quantities

**Sum of squares** — add up each number's square:
$$1^2 + 2^2 + \cdots + 100^2 = \frac{n(n+1)(2n+1)}{6} = \frac{100 \cdot 101 \cdot 201}{6} = 338{,}350$$

**Square of sum** — sum the numbers first, then square:
$$(1 + 2 + \cdots + 100)^2 = \left(\frac{n(n+1)}{2}\right)^2 = 5050^2 = 25{,}502{,}500$$

### The Difference

$$25{,}502{,}500 - 338{,}350 = \boxed{25{,}164{,}150}$$

---

### Why the Gap is so Large

For any $n$, the difference has a closed form:

$$\left(\frac{n(n+1)}{2}\right)^2 - \frac{n(n+1)(2n+1)}{6} = \frac{n(n+1)(n-1)(3n+2)}{12}$$

This grows as **$O(n^4)$**, so it explodes quickly — at $n=100$ the square-of-sum is already ~75× larger than the sum-of-squares.

---

## Turn 2

**User:**

That's a really clear walkthrough — I can see why the difference explodes at $O(n^4)$. 

Should we code this up to verify the answer? I'm thinking we could implement both the direct approach (sum up the squares, compute the sum and square it) and maybe also use that closed form you derived. Which language would work best here, and do you want to start with the straightforward version first to make sure I understand the problem, or jump straight to the optimized formula?

**Pair:**

Assistant: **Python** is the natural fit — clean syntax, arbitrary-precision integers, and no boilerplate.

Start with the direct version. It makes the problem definition executable, so if the formula version ever gives a wrong answer you have a trustworthy reference to diff against.

```python
def direct(n):
    sum_of_squares = sum(i**2 for i in range(1, n + 1))
    square_of_sum  = sum(range(1, n + 1)) ** 2
    return square_of_sum - sum_of_squares

def formula(n):
    square_of_sum  = (n * (n + 1) // 2) ** 2
    sum_of_squares =  n * (n + 1) * (2*n + 1) // 6
    return square_of_sum - sum_of_squares

print(direct(100))   # 25164150
print(formula(100))  # 25164150
print(direct(100) == formula(100))  # True
```

### Key ideas to notice

| | `direct` | `formula` |
|---|---|---|
| Work per call | $O(n)$ — loops through every number | $O(1)$ — three multiplications |
| Risk of error | Low — almost reads like the problem statement | Higher — easy to mis-transcribe a coefficient |
| Best use | Ground-truth check | Production / large $n$ |

The equality assertion at the end is the real payoff — running both and confirming they agree is a lightweight proof that your algebra was right. For $n = 100$ the difference is undetectable, but try `n = 10_000_000` and the $O(n)$ loop will take noticeable time while the formula returns instantly.

---

## Turn 3

**User:**

Got it — I like how the direct version reads almost exactly like the problem statement. That makes it a solid sanity check.

Should we save this to a file and run it to verify both approaches give 25164150? And is there a specific structure you want (like a `project_euler/` directory with numbered files, or just a single script)?

**Pair:**

Assistant: A numbered file inside a `project_euler/` folder scales well as you add more problems:

```
project_euler/
  p006_sum_square_difference.py
  p001_...  ← easy to add later
```

[Bash(mkdir -p project_euler)]
  (Bash completed with no output)

[Write(/root/project_euler/p006_sum_square_difference.py)]
"""
Project Euler #6 — Sum Square Difference
Find the difference between the square of the sum and the sum of the
squares of the first 100 natural numbers.
"""


def direct(n: int) -> int:
    """O(n): loops through every number — mirrors the problem statement."""
    sum_of_squares = sum(i**2 for i in range(1, n + 1))
    square_of_sum  = sum(range(1, n + 1)) ** 2
    return square_of_sum - sum_of_squares
… (18 more lines)

[Bash(mkdir -p ~/project_euler && echo "dir: $(realpath ~/project_euler)")]
  dir: /Users/oz/project_euler

[Write(/Users/oz/project_euler/p006_sum_square_difference.py)]
"""
Project Euler #6 — Sum Square Difference
Find the difference between the square of the sum and the sum of the
squares of the first 100 natural numbers.
"""


def direct(n: int) -> int:
    """O(n): loops through every number — mirrors the problem statement."""
    sum_of_squares = sum(i**2 for i in range(1, n + 1))
    square_of_sum  = sum(range(1, n + 1)) ** 2
    return square_of_sum - sum_of_squares
… (18 more lines)

[Bash(python3 /Users/oz/project_euler/p006_sum_square_difference.py)]
  Direct:  25164150
  Formula: 25164150
  Match:   True
  
  Answer: 25164150

Assistant: Both agree. File is at `~/project_euler/p006_sum_square_difference.py`.

### What the output confirms

- **`Match: True`** is the meaningful line — it means the $O(n)$ loop and the $O(1)$ formula are consistent, which validates the algebra, not just the arithmetic.
- The naming convention `p006_...` keeps files sorted numerically in any file explorer, so `p001` through `p100` will always list in order.

When you tackle the next problem, just drop a `p007_...py` in the same folder and the structure stays tidy.

---

## Turn 4 (final)

**User:**

Perfect — I like that the structure scales cleanly, and I can see how the `Match: True` line is the real proof that the algebra holds up. Next problem, same pattern: verify with a direct approach, then optimize.

<done/>

---

**Run end**: done after 3 turns (67s)
