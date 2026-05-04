# euler-15-lattice-paths

- Source: `project-euler`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T08:26:45.851Z

---

## Turn 1

**User:**

Project Euler #15: how many distinct routes are there through a 20×20 grid moving only right or down? Closed-form is fine but discuss the DP path too.

**Pair:**

Assistant: Great classic problem. Let me walk through both paths.

**The combinatorics insight:** Any route through a 20×20 grid takes exactly 40 steps — 20 right (R) and 20 down (D), in some order. So the answer is just the number of ways to arrange those 40 steps:

$$\binom{40}{20} = \frac{40!}{20! \cdot 20!} = 137{,}846{,}528{,}640$$

**The DP path:** Define `dp[i][j]` = number of routes to reach cell (i, j) from (0,0). The recurrence is:

```
dp[i][j] = dp[i-1][j] + dp[i][j-1]   (came from above or from the left)
dp[0][j]  = 1                          (top row: only one way — go right)
dp[i][0]  = 1                          (left col: only one way — go down)
```

This is literally Pascal's triangle laid out on a grid. `dp[n][n]` = C(2n, n).

Before I code it up — the DP can be done with a full 2D array **or** by noting you only need the previous row at any time. Which do you prefer here?

OPTIONS:
[A] 1D rolling array
Keep a single array of length n+1. Process left-to-right each row; `row[j] += row[j-1]` updates in-place. O(n) space.

[B] 2D grid
Allocate a full (n+1)×(n+1) matrix. `dp[i][j] = dp[i-1][j] + dp[i][j-1]`. O(n²) space, directly mirrors the recurrence.

(Reply with A or B, or ask a follow-up question.)

---

## Turn 2

**User:**

**B**

For learning purposes, the 2D grid is clearer — I can directly see the structure of Pascal's triangle emerge. Space isn't tight for n=20 (just 441 cells), and it's easier to verify the logic matches the recurrence. The rolling-array trick is neat but can obscure what's happening.

**Pair:**

Assistant: Totally fair. Clarity beats cleverness when you're building intuition, and 441 integers is nothing. The 1D trick matters when n is large enough that the grid itself becomes the bottleneck — not here.

Let me build it:

[Glob(euler15.py)]
  No files found

[Write(euler15.py)]
from math import comb

def dp_routes(n: int) -> int:
    """Count lattice paths through an n×n grid (right/down only) via DP."""
    # dp[i][j] = number of routes to reach cell (i, j)
    # Row 0 and col 0 are all 1s: only one way to reach any edge cell.
    dp = [[1] * (n + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

… (30 more lines)

[Bash(python euler15.py)]
  error: Exit code 127

[Bash(python3 euler15.py)]
  Grid size : 20×20
  DP answer : 137,846,528,820
  C(40,20)  : 137,846,528,820
  Both agree ✓
  
  DP grid for 4×4 (rows = down, cols = right):
      1    1    1    1    1
      1    2    3    4    5
      1    3    6   10   15
      1    4   10   20   35
      1    5   15   35   70

Assistant: **Answer: 137,846,528,820**

Look at that 4×4 grid — the Pascal's triangle structure you were after is right there. Each cell is the sum of the one above and the one to its left, and the diagonals are the binomial coefficients:

```
  1   1   1   1   1    ← C(0,0) C(1,1) C(2,2) ...
  1   2   3   4   5    ← C(1,0) C(2,1) C(3,2) ...
  1   3   6  10  15    ← C(2,0) C(3,1) C(4,2) ...
  1   4  10  20  35
  1   5  15  35  70    ← dp[4][4] = C(8,4) ✓
```

The bottom-right cell of an n×n DP grid is always C(2n, n) — that's not a coincidence, it's the same combinatorial identity from a different angle. The DP is just a constructive proof that the answer is C(2n, n).

---

## Turn 3 (final)

**User:**

<done/>

---

**Run end**: done after 2 turns (65s)
