# euler-15-lattice-paths

- Source: `project-euler`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T02:49:31.850Z

---

## Turn 1

**User:**

Project Euler #15: how many distinct routes are there through a 20×20 grid moving only right or down? Closed-form is fine but discuss the DP path too.

**Pair:**

Assistant: Great problem — the DP and closed-form paths meet in an elegant place.

**Setup:** we want routes from the top-left to bottom-right corner of a 20×20 grid, moving only right (R) or down (D). There are 21×21 lattice points, so we traverse from `(0,0)` to `(20,20)`.

---

**DP path**

Define `dp[i][j]` = number of routes to reach `(i,j)`. The recurrence is immediate:

```
dp[i][j] = dp[i-1][j]   # arrived from above
          + dp[i][j-1]   # arrived from the left
```

with `dp[0][*] = dp[*][0] = 1` (only one way to reach any top-row or left-column cell). This is just Pascal's triangle rotated 45°.

---

**Closed form**

Every route is exactly 40 moves: 20 R's and 20 D's in some order. Count the arrangements:

$$\binom{40}{20} = \frac{40!}{20!\,20!} = \mathbf{137{,}846{,}528{,}640}$$

---

**Connection:** `dp[i][j]` = C(i+j, i), so `dp[20][20]` = C(40,20). The DP table literally computes binomial coefficients.

---

Now, the 2D DP uses O(n²) space but you can compress it to O(n) with a 1D rolling array — only one row needs to be live at a time. Before I write it out, a question about which direction to iterate:

OPTIONS:
[A] Left → right (j: 1…20)
```diff
+++ euler15.py
@@ -0,0 +1,5 @@
+dp = [1] * 21
+for _ in range(20):
+    for j in range(1, 21):      # forward
+        dp[j] += dp[j-1]
+print(dp[20])
```

[B] Right → left (j: 20…1)
```diff
+++ euler15.py
@@ -0,0 +1,5 @@
+dp = [1] * 21
+for _ in range(20):
+    for j in range(20, 0, -1):  # backward
+        dp[j] += dp[j-1]
+print(dp[20])
```

(Reply with A or B, or ask a follow-up question.)

Assistant: Both snippets look nearly identical — the only difference is iteration direction. Which computes the right answer, and why?

---

## Turn 2

**User:**

**A** — left to right.

Here's why: when we update `dp[j] += dp[j-1]`, we need `dp[j-1]` to already be the *updated value from the current row*, not the old value. 

If we go **left to right (A)**:
- When we reach column j, column j-1 has already been updated in this row
- So `dp[j] += dp[j-1]` gives us: (old row)[j] + (current row)[j-1] ✓

If we go **right to left (B)**:
- When we reach column j, column j-1 hasn't been updated yet
- So `dp[j-1]` still holds (old row)[j-1]
- We'd compute: (old row)[j] + (old row)[j-1], which is wrong — we're adding two values from the same row

B would systematically undercount. The iteration direction matters because we're reusing the same array for both the old row and the new row.

Ready for code?

**Pair:**

Assistant: Exactly right — and worth noting the backward version isn't just wrong, it computes `dp[i][j] = dp[i-1][j] + dp[i-1][j-1]`, which is the standard Pascal's triangle recurrence (C(n,k) = C(n-1,k) + C(n-1,k-1)). A different valid recurrence, wrong problem. This is also the mirror of 0/1 knapsack, where you *deliberately* go backward to prevent double-counting items.

[Glob(euler15.py)]
  No files found

[Write(euler15.py)]
from math import comb

N = 20

# --- Closed form -------------------------------------------
# Every route is 2N moves: N rights + N downs, in some order.
answer_cf = comb(2 * N, N)

# --- DP (1-D rolling array, O(N) space) --------------------
# dp[j] = routes to reach current row, column j.
# Invariant: scan left→right so dp[j-1] is already this row's value.
dp = [1] * (N + 1)
… (11 more lines)

[Bash(python3 euler15.py)]
  Grid size : 20×20
  Closed form  C(40,20) = 137,846,528,820
  DP (1-D rolling)         = 137,846,528,820

Assistant: Both approaches agree: **137,846,528,820**.

(I had a typo in my earlier mental arithmetic — Python's `math.comb` is authoritative.)

A few things worth knowing about the solution:

- **Space**: the 2D DP is O(n²) but this 1D rolling version is O(n) — only one row is live at a time, which is fine here but matters if you scale n up.
- **Overflow**: Python handles big integers natively; in C/Java you'd need 64-bit (`long`) since the answer is ~1.38 × 10¹¹, well within `int64` range.
- **`math.comb`** is the pragmatic answer for a contest — O(n) time and exact, no DP needed. But the DP derivation shows *why* the formula works.

---

## Turn 3 (final)

**User:**

<done/>

---

**Run end**: done after 2 turns (122s)
