# euler-15-lattice-paths

- Source: `project-euler`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T00:32:05.933Z

---

## Turn 1

**User:**

Project Euler #15: how many distinct routes are there through a 20×20 grid moving only right or down? Closed-form is fine but discuss the DP path too.

**Pair:**

Assistant: **The insight:** any route through a 20×20 grid is a sequence of exactly 40 moves — 20 right (R) and 20 down (D). The question is just "how many ways can you arrange 20 R's among 40 slots?"

```
C(40, 20) = 40! / (20! · 20!) = 137,846,528,640
```

**The DP path:** build a 21×21 table where `dp[i][j]` = routes to reach that corner. Base cases: entire top row and left column are 1 (only one way to travel along an edge). Interior: `dp[i][j] = dp[i-1][j] + dp[i][j-1]`. You're adding "came from above" + "came from left." `dp[20][20]` is your answer — and if you stare at the table, it's Pascal's triangle rotated 45°, which is why the closed form lands on a binomial coefficient.

Now, the O(N²) table works, but you can cut to **O(N)** with a single row. Here's the question — which update order is correct?

OPTIONS:
[A] Left → right
```diff
+++ euler15.py
@@ -0,0 +1,5 @@
+dp = [1] * 21
+for i in range(1, 21):
+    for j in range(1, 21):
+        dp[j] += dp[j-1]
+print(dp[20])
```

[B] Right → left
```diff
+++ euler15.py
@@ -0,0 +1,5 @@
+dp = [1] * 21
+for i in range(1, 21):
+    for j in range(20, 0, -1):
+        dp[j] += dp[j-1]
+print(dp[20])
```

(Reply with A or B, or ask a follow-up question.)

Assistant: Which update direction gives the right answer, and why?

---

## Turn 2

**User:**

**A.**

When we process left → right and update `dp[j]`, we're reading `dp[j-1]` *after* it's been updated in this same iteration. So `dp[j-1]` holds the current row's value, and we get:
- `dp[j] = (old dp[j] from prev row) + (new dp[j-1] from curr row)` = `dp[i-1][j] + dp[i][j-1]` ✓

Right → left breaks it: `dp[j-1]` would still be the old value from the previous row, so you'd be adding `dp[i-1][j] + dp[i-1][j-1]` — a diagonal dependency that doesn't match Pascal's triangle. First row would incorrectly get `[1, 2, 2, 2, ...]` instead of `[1, 2, 3, 4, ...]`.

**Pair:**

Assistant: Exactly right. The in-place update is the trick — by the time you write `dp[j]`, `dp[j-1]` is already the *current* row's value, which is exactly the "came from left" term you need. It's the same principle behind the 1D knapsack optimization.

One fun footnote: the right-to-left version isn't computing Pascal's triangle — it's computing `dp[i][j] = dp[i-1][j] + dp[i-1][j-1]`, which with all-1 base rows doubles every step, giving `2^20 = 1,048,576`. Completely different beast.

Here's the full solution:

```python
import math

# Closed form: choose 20 "right" moves from 40 total
answer = math.comb(40, 20)
print(answer)  # 137846528640

# DP verification (O(N) space)
dp = [1] * 21
for i in range(1, 21):
    for j in range(1, 21):
        dp[j] += dp[j-1]
assert dp[20] == answer
```

The closed form is one line with `math.comb`. The DP is worth understanding because the same "reuse updated value left-to-right" trick appears constantly — 0/1 knapsack, edit distance, coin change. The direction of your inner loop determines whether you're reading from the current or previous "virtual row."

---

## Turn 3 (final)

**User:**

<done/>

---

**Run end**: done after 2 turns (96s)
