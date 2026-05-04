# euler-15-lattice-paths

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:03:55

## Initial prompt

Project Euler #15: how many distinct routes are there through a 20×20 grid moving only right or down? Closed-form is fine but discuss the DP path too.

---

## Turn 1

### Tutor

Tutor: Great problem — the combinatorial insight is elegant, and the DP path teaches something broadly useful.

**The math first:** any path from top-left to bottom-right of a 20×20 grid requires exactly 20 moves right and 20 moves down — 40 moves total. You're just choosing *which* 20 are rightward:

$$\binom{40}{20} = 137{,}846{,}528{,}640$$

For the DP version, let `dp[i][j]` = number of paths to reach lattice point `(i, j)`. The recurrence is:
```
dp[i][j] = dp[i-1][j] + dp[i][j-1]
```
with `dp[0][j] = dp[i][0] = 1` (only one way to travel along an edge). Note it's a **21×21** table — a 20×20 *grid* has 21×21 *intersection points*.

Before writing this up, a question on the DP implementation:

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Full 2D table
```diff
+++ euler15.py
@@ -0,0 +1,8 @@
+def count_paths_dp(n: int) -> int:
+    dp = [[1] * (n + 1) for _ in range(n + 1)]
+    for i in range(1, n + 1):
+        for j in range(1, n + 1):
+            dp[i][j] = dp[i-1][j] + dp[i][j-1]
+    return dp[n][n]
```

[B] 1D rolling array
```diff
+++ euler15.py
@@ -0,0 +1,6 @@
+def count_paths_dp(n: int) -> int:
+    dp = [1] * (n + 1)
+    for _ in range(1, n + 1):
+        for j in range(1, n + 1):
+            dp[j] += dp[j-1]
+    return dp[n]
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which would you use for the DP implementation?

### Student

I'd go with **B** — the 1D rolling array.

My reasoning: since each cell only depends on the cell above it and to the left, we don't actually need to keep the entire 2D table in memory. We can process row by row and update a single 1D array as we go. For n=20, that's a huge space saving (21² = 441 cells vs. just 21 cells).

Also, I'm curious — when we update `dp[j] += dp[j-1]` in the inner loop, that's accumulating both the "down" contribution (from the previous iteration, which is now the row above) and the "right" contribution (from `dp[j-1]` in the current row), right? That's the key insight that makes the 1D version work.

Should I code this up now and test it on n=20 to verify it gives 137,846,528,640?

---

## Turn 2

### Tutor

Tutor: Exactly right — that's the crux. `dp[j]` before the update *is* the above-row value (the "come from above" contribution), and `dp[j-1]` has already been updated this sweep so it carries the "come from left" contribution. The in-place left-to-right pass threads both directions through a single array.

Let's write it up:

[Glob(euler15.py)]
  No files found

[Write(euler15.py)]
import math


def count_paths_dp(n: int) -> int:
    """Count lattice paths through an n×n grid (right/down only) using a
    1D rolling array.  dp[j] starts each outer iteration holding the path
    count for the row above; updating left-to-right folds in the left
    neighbour from the current row, so no 2D table is needed.  O(n) space."""
    dp = [1] * (n + 1)          # base case: top row all 1s
    for _ in range(1, n + 1):   # iterate over rows 1..n
        for j in range(1, n + 1):
            dp[j] += dp[j - 1]  # above (dp[j] old) + left (dp[j-1] new)
… (19 more lines)
  File created successfully at: euler15.py

[Bash(python euler15.py)]
  DP answer:            137,846,528,820
  Combinatorial answer: 137,846,528,820
  ✓ Both agree.

Tutor: Both methods agree: **137,846,528,820**.

(I mis-stated the number earlier in prose — the code is the source of truth.)

A few things worth noting:

**Why the DP table is 21×21 conceptually, not 20×20** — a 20×20 *grid of squares* has 21×21 *intersection points*. The path ends at point `(20,20)`, which is why `dp` is length `n+1` and we return `dp[n]`.

**Why this DP *is* Pascal's triangle** — `dp[i][j] = C(i+j, i)`. Each point in the rolling array after row `i` holds `C(i+j, i)` for column `j`. The final answer `dp[20]` after 20 row sweeps is `C(40, 20)`, which is exactly the closed form. The two approaches aren't just numerically equal — they're computing the same thing from different angles.

**Space**: 21 integers vs 441 — a 21× saving. For `n=20` it's trivial, but the pattern matters at scale (e.g. counting paths in a 10,000×10,000 grid: 80 KB vs 800 MB).

### Student

That's really helpful — thanks for walking through it. I especially appreciate seeing how the DP is actually computing Pascal's triangle coefficients under the hood. That makes the connection to the combinatorial formula click.

A couple quick things I want to solidify:

1. **The indexing**: so when we initialize `dp = [1] * (n + 1)`, we're setting up the top row where there's only one way to reach any point along the top edge. Then in the outer loop, each iteration of `for _ in range(1, n + 1)` processes one new row of the grid. That means after the loop completes, `dp[j]` holds the cumulative path count for the entire column `j` across all rows up to row `n`. Is that the right mental model?

2. **The in-place update order**: because we iterate `j` left-to-right (from 1 to n), when we do `dp[j] += dp[j-1]`, the `dp[j-1]` value has *already* been updated in this iteration, so it's the "current row, left column" value. And the old `dp[j]` (before the += ) is the "previous row, same column" value. So the order matters — if we went right-to-left instead, `dp[j-1]` would still be the old value from the previous row, and we'd be adding wrong.

Is that accurate? I think seeing those two things clearly will help me apply this pattern to other grid DP problems.

---

## Turn 3

### Tutor

Tutor: Both mental models are exactly right. Let me make point 2 concrete with a trace so it really sticks.

**n=2 trace, left-to-right (correct):**
```
init:   dp = [1, 1, 1]        ← top row: one path to each point

row 1:  j=1: dp[1] = 1+1 = 2  (dp[0]=1 already updated this row → "left")
        j=2: dp[2] = 1+2 = 3  (dp[1]=2 already updated this row → "left")
        dp = [1, 2, 3]  ✓

row 2:  j=1: dp[1] = 2+1 = 3
        j=2: dp[2] = 3+3 = 6
        dp = [1, 3, 6]  → answer: 6 = C(4,2) ✓
```

**Same thing, right-to-left (silently wrong):**
```
init:   dp = [1, 1, 1]

row 1:  j=2: dp[2] = 1+1 = 2  (dp[1] not yet updated → stale "left")
        j=1: dp[1] = 1+1 = 2
        dp = [1, 2, 2]  ✗  (should be [1, 2, 3])

row 2:  → final answer: 4  (should be 6)
```

The right-to-left version computes `dp[i-1][j] + dp[i-1][j-1]` — both from the *previous* row — which is Pascal's triangle (binomial coefficients), not cumulative path sums. Related, but not what we want.

**The general pattern to internalize:** in rolling-array DP —
- **Left-to-right** → current row's already-updated left value feeds in → models "can reuse the current row" (path counting, unbounded knapsack)
- **Right-to-left** → stale previous-row value feeds in → models "each item used at most once" (0/1 knapsack)

That direction choice is the *entire* difference between 0/1 knapsack and unbounded knapsack. Worth filing away.

### Student

Oh wow, that trace is crystal clear — I can see exactly where right-to-left breaks it. When we go right-to-left, we're stuck using the old `dp[j-1]` from the previous row, so we end up computing something completely different (and getting 4 instead of 6).

And I really like that general pattern you laid out at the end. So:

- **Left-to-right** in rolling array = we're allowing the current iteration to "see" its own updates = models problems where we can reuse/revisit the same resource (unbounded knapsack, path counting)
- **Right-to-left** = we're forced to use only previous iteration's values = models problems where each thing is used at most once (0/1 knapsack)

That's a huge insight. It means the *direction* of the loop isn't just a detail — it fundamentally changes what recurrence we're computing. I'll definitely keep that in mind when I encounter other grid or DP problems.

For this specific problem, I've got the solution working (both the DP and the closed-form give 137,846,528,820), and I understand *why* each approach works and how they relate to each other. I think I'm good here.

Thanks for taking the time to trace through the edge cases and explain the broader pattern — that's going to be way more useful than just having the right answer.

<done/>

---

**Run end:** done after 3 turn(s) in 131.5s
