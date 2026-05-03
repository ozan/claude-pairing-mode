# euler-15-lattice-paths

- Source: `project-euler`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T02:03:43.086Z

---

## Turn 1

**User:**

Project Euler #15: how many distinct routes are there through a 20×20 grid moving only right or down? Closed-form is fine but discuss the DP path too.

**Pair:**

Assistant: **The combinatorics** — any route is exactly 40 steps: 20 right (R) and 20 down (D), in some order. You just choose which 20 of the 40 steps are R:

```
C(40, 20) = 40! / (20! × 20!) = 137,846,528,640
```

**The DP path** — let `dp[i][j]` = number of routes to reach lattice point `(i, j)` from `(0, 0)`. You can only arrive from the left or from above, so:

```
dp[i][j] = dp[i-1][j] + dp[i][j-1]
```

Base cases: the entire top row and left column are each reachable in exactly 1 way (no choices available).

Before we write the code — here's the crux of implementing the DP correctly:

OPTIONS:
[A] 21×21 grid
```diff
+++ euler15.py
@@ -0,0 +1,7 @@
+n = 20
+dp = [[1] * (n + 1) for _ in range(n + 1)]
+for i in range(1, n + 1):
+    for j in range(1, n + 1):
+        dp[i][j] = dp[i-1][j] + dp[i][j-1]
+print(dp[n][n])
```

[B] 20×20 grid
```diff
+++ euler15.py
@@ -0,0 +1,7 @@
+n = 20
+dp = [[1] * n for _ in range(n)]
+for i in range(1, n):
+    for j in range(1, n):
+        dp[i][j] = dp[i-1][j] + dp[i][j-1]
+print(dp[n-1][n-1])
```

(Reply with A or B, or ask a follow-up question.)

Assistant: Which grid size is right for a "20×20 grid"?

---

## Turn 2

**User:**

**A** — the 21×21 grid.

A "20×20 grid" means 20×20 *squares*, which requires 21 lattice *points* in each dimension (0 through 20 inclusive). Option [A] correctly represents all positions from (0,0) to (20,20).

Option [B] would only go up to (19,19), undercounting by one dimension.

**Pair:**

Assistant: Exactly right. The "grid" in the problem name refers to squares, but the DP indexes vertices — classic fence-post trap.

Let me write the file:

[Glob(euler15.py)]
  No files found

[Write(euler15.py)]
import math

n = 20

# --- DP approach ---
dp = [[1] * (n + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    for j in range(1, n + 1):
        dp[i][j] = dp[i-1][j] + dp[i][j-1]

dp_answer = dp[n][n]

… (7 more lines)

[Bash(python3 euler15.py)]
  DP:         137846528820
  C(40, 20):  137846528820
  Match: True

Assistant: **137,846,528,820** — both approaches agree. (I misstated it earlier as ...640; Python's the source of truth.)

Two things worth noting:

- The DP table is Pascal's triangle. `dp[i][j] = C(i+j, i)` — you can verify `dp[20][20] = C(40, 20)` directly.
- The DP has O(n²) time/space; you can compress it to O(n) space by filling one row at a time, since `dp[i][j]` only needs the row above. But `math.comb` makes it all moot for a single query.

---

## Turn 3 (final)

**User:**

Looks good! You've nailed both the fence-post conceptual trap and the implementation. The answer **137,846,528,820** is rock-solid, and you've got the key insight: a "20×20 grid" of *squares* needs 21 lattice points per dimension to index all the reachable positions.

The note about Pascal's triangle is nice too — it's not just that DP works, but that the recurrence you've written *is* the Pascal's triangle recurrence, so any path-counting problem on a grid falls out of combinatorics naturally.

<done/>

---

**Run end**: done after 2 turns (72s)
