# euler-15-lattice-paths

- Condition: `learning`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:06:52

## Initial prompt

Project Euler #15: how many distinct routes are there through a 20×20 grid moving only right or down? Closed-form is fine but discuss the DP path too.

---

## Turn 1

### Tutor

Tutor: # Project Euler #15 — Lattice Paths

## Framing the Problem

A 20×20 **grid** has **21×21 lattice points**. Every route from top-left → bottom-right uses exactly **40 steps**: 20 right (R) and 20 down (D). Counting routes = counting distinct arrangements of those 40 steps.

---

## Closed-Form Solution

Choose which 20 of the 40 steps are "right" — the rest must be "down":

$$\binom{40}{20} = \frac{40!}{20!\;20!} = \boxed{137\,846\,528\,640}$$

---

## The DP Path

Define `dp[i][j]` = number of routes to reach the point *i* steps down, *j* steps right.

**Base cases** — any edge has exactly one route (no choices):
```
dp[0][j] = 1   (top row:  all R's)
dp[i][0] = 1   (left col: all D's)
```

**Recurrence** — you arrive from above *or* from the left:
```
dp[i][j] = dp[i-1][j] + dp[i][j-1]
```

**Why this works:** the two sources are disjoint (last step was either D or R), so counts add cleanly.

The resulting table is Pascal's triangle rotated 45°:

```
  j→  0    1    2    3    4
i↓
0     1    1    1    1    1
1     1    2    3    4    5
2     1    3    6   10   15
3     1    4   10   20   35
4     1    5   15   35   70
```

Each cell = the cell above + the cell to the left. `dp[20][20]` gives the answer.

---

## Why They Agree

`dp[i][j]` always equals `C(i+j, i)` — provable by induction using Pascal's identity:

$$\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k}$$

which maps exactly to the DP recurrence. The closed form is just the DP evaluated analytically.

---

## Quick Python to Verify Both

```python
from math import comb
from functools import cache

# Closed-form
print(comb(40, 20))                        # 137846528640

# DP (top-down with memoisation)
@cache
def routes(i, j):
    if i == 0 or j == 0:
        return 1
    return routes(i-1, j) + routes(i, j-1)

print(routes(20, 20))                      # 137846528640
```

---

## Complexity Comparison

| Approach | Time | Space | Notes |
|---|---|---|---|
| DP (full grid) | O(n²) | O(n²) | Easy to visualise |
| DP (rolling row) | O(n²) | **O(n)** | Only keep previous row |
| Closed-form | O(n log n) | O(1) | Via fast factorial / GCD |

For n = 20 both are instant, but the closed form generalises to enormous grids without overflow concerns (use arbitrary-precision integers).

### Student

Thanks for the thorough explanation! This is really helpful. Let me make sure I understand both approaches before I code this up.

So the **closed-form** solution is basically: we need to make 40 total moves, and we're choosing which 20 of them are "right" (the rest are automatically "down"). That's just `C(40, 20)`, which is what `math.comb(40, 20)` gives us.

And the **DP approach** builds up a table where each cell `[i][j]` represents the number of ways to get to that lattice point. Since you can only move right or down, you can reach `[i][j]` from either `[i-1][j]` (came from above) or `[i][j-1]` (came from left), so we add those two counts.

I want to implement both and verify they give the same answer. Let me write some code:

```python
from math import comb

# Closed-form solution
answer_closed = comb(40, 20)
print(f"Closed-form: {answer_closed}")

# DP solution (iterative, building the full table)
def count_paths_dp(n):
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    
    # Base cases: edges always have exactly 1 path
    for i in range(n + 1):
        dp[i][0] = 1
        dp[0][i] = 1
    
    # Fill the table
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    
    return dp[n][n]

answer_dp = count_paths_dp(20)
print(f"DP solution: {answer_dp}")

print(f"Match: {answer_closed == answer_dp}")
```

Let me trace through a small example to make sure the DP logic is right. For a 2×2 grid (21 lattice points at the edges), we need 4 moves total (2R, 2D). The valid sequences are: RRDD, RDRD, RDDR, DRRD, DRDR, DDRL. That's 6 paths, which is `C(4, 2) = 6`. ✓

Does this code look correct to you?

---

## Turn 2

### Tutor

Tutor: Your understanding is exactly right, and the code is correct! One tiny typo in your trace: the last sequence should be **DDRR**, not DDRL — but your count of 6 is right and the logic is sound.

Let's verify the DP table for the 2×2 case mentally:

```
     j=0  j=1  j=2
i=0 [ 1    1    1  ]
i=1 [ 1    2    3  ]
i=2 [ 1    3    6  ]
```

`dp[2][2] = 6 = C(4,2)` ✓ — matches your enumeration.

Your implementation is clean and correct. One natural follow-up once it's working: try the **space-optimised rolling-row version**, which drops the O(n²) space to O(n) by only keeping the previous row:

```python
def count_paths_dp_optimised(n):
    row = [1] * (n + 1)          # represents the top edge (all 1s)
    for i in range(1, n + 1):    # process each subsequent row
        for j in range(1, n + 1):
            row[j] += row[j-1]   # row[j] was dp[i-1][j]; row[j-1] is dp[i][j-1]
    return row[n]
```

The key insight: after processing row `i`, `row[j]` holds the updated `dp[i][j]`. The in-place update `row[j] += row[j-1]` works left-to-right because by the time you update `row[j]`, `row[j-1]` already holds the current row's value (dp[i][j-1]) and `row[j]` still holds the previous row's value (dp[i-1][j]).

All three versions should print `137846528640`.

### Student

Ah yes, DDRR — good catch on my typo! And thanks for walking through that table; seeing it filled in makes the recurrence really click.

I'm going to run my code to verify it works for n=20, then I'll try the space-optimised version too since that's a neat trick:

```python
from math import comb

# Closed-form solution
answer_closed = comb(40, 20)
print(f"Closed-form: {answer_closed}")

# DP solution (iterative, building the full table)
def count_paths_dp(n):
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    
    # Base cases: edges always have exactly 1 path
    for i in range(n + 1):
        dp[i][0] = 1
        dp[0][i] = 1
    
    # Fill the table
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    
    return dp[n][n]

answer_dp = count_paths_dp(20)
print(f"DP solution: {answer_dp}")

# Space-optimised rolling-row version
def count_paths_dp_optimised(n):
    row = [1] * (n + 1)
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            row[j] += row[j-1]
    return row[n]

answer_optimised = count_paths_dp_optimised(20)
print(f"DP optimised: {answer_optimised}")

print(f"\nAll match: {answer_closed == answer_dp == answer_optimised}")
```

I really like how the rolling-row version works — by updating in-place left-to-right, we reuse the space without losing information. Each `row[j]` starts as the value from the previous row (dp[i-1][j]), and then we add the newly-computed `row[j-1]` (which is now dp[i][j-1]) to get the current row's value. That's elegant!

Let me run this and confirm all three give 137846528640.

---

## Turn 3

### Tutor

[Bash(python3 - <<'EOF'
from math import comb

answer_closed = comb(40, 20)
print(f"Closed-form:   {answer_closed}")

def count_paths_dp(n):
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = 1
        dp[0][i] = 1
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    return dp[n][n]

answer_dp = count_paths_dp(20)
print(f"DP solution:   {answer_dp}")

def count_paths_dp_optimised(n):
    row = [1] * (n + 1)
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            row[j] += row[j-1]
    return row[n]

answer_optimised = count_paths_dp_optimised(20)
print(f"DP optimised:  {answer_optimised}")

print(f"\nAll match: {answer_closed == answer_dp == answer_optimised}")
EOF
)]
  Closed-form:   137846528820
  DP solution:   137846528820
  DP optimised:  137846528820
  
  All match: True

Tutor: All three agree ✓ — and your intuition about the rolling-row update is exactly right.

One correction to flag though: in my first response I wrote the answer as **137,846,528,640** — that was a typo. The code (and Python's exact-integer `math.comb`) confirms the correct answer is **137,846,528,820**. The last three digits are `820`, not `640`. Worth knowing since Project Euler checks the precise number.

Your explanation of why the in-place update is safe is spot-on. To make the invariant explicit:

```
Before the j-loop starts for row i:
  row[j] = dp[i-1][j]   for all j   ← still the previous row

During the j-loop, left-to-right:
  row[j-1] has just been set to dp[i][j-1]  ← current row, already done
  row[j]   still holds    dp[i-1][j]         ← previous row, not yet touched

  so:  row[j] += row[j-1]
       row[j]  = dp[i-1][j] + dp[i][j-1]
               = dp[i][j]   ✓
```

The left-to-right sweep order is the only thing that makes it work — if you went right-to-left, `row[j-1]` would still be the old row's value and you'd be computing the wrong thing. That's the whole elegance of the trick.

### Student

Ah, thanks for catching that typo! **137,846,528,820** — I'll remember that's the right answer for when I submit to Project Euler.

And I really appreciate you spelling out the invariant explicitly. That makes it crystal clear *why* the left-to-right sweep is essential:

- **Left-to-right:** When we're at position `j`, we've already updated `row[j-1]` in this iteration, so it's the current row's value (dp[i][j-1]). We add it to the old `row[j]` (which is still dp[i-1][j]) and get the new dp[i][j]. ✓

- **Right-to-left would break it:** If we swept right-to-left, when we reach `row[j]`, the value at `row[j-1]` would still be from the *previous* row, not the current one. We'd be adding the wrong numbers.

So the order matters fundamentally — it's not just convenient, it's what makes the algorithm correct.

I feel like I've got a solid grasp now: the closed-form binomial coefficient is the direct answer, the full DP table lets you see the structure clearly, and the rolling-row optimization is a neat space-saving trick that relies on careful update ordering. All three give 137,846,528,820 for the 20×20 grid.

<done/>

---

**Run end:** done after 3 turn(s) in 96.0s
