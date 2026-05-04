# euler-15-lattice-paths

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:44:15

## Initial prompt

Project Euler #15: how many distinct routes are there through a 20×20 grid moving only right or down? Closed-form is fine but discuss the DP path too.

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Start with DP
Fill a 21×21 table where `dp[i][j]` = paths to reach cell `(i,j)`. Base cases: entire top row and left column are 1. Recurrence: `dp[i][j] = dp[i-1][j] + dp[i][j-1]`. Answer is `dp[20][20]`. The table *is* Pascal's triangle, which explains why the closed-form falls out naturally.

[B] Jump to closed-form
Any path is exactly 40 steps: 20 right + 20 down. The answer is the number of ways to arrange those steps: `C(40, 20) = 137,846,528,640`. One line of math, directly computable with `math.comb(40, 20)`.

(Reply with A or B, or ask a follow-up question.)

Tutor: Two solid approaches — which do you want to lead with?

### Student

I'll go with **A** — the DP approach first.

I think seeing how the table builds up will help me understand *why* the closed-form works, rather than just jumping to the combinatorial answer. Plus, I'm curious to see that Pascal's triangle connection you mentioned.

Let me start by sketching out the solution in code and walking through a smaller example to make sure I've got the logic right.

---

## Turn 2

### Tutor

Tutor: Great instinct. Before I write code, one decision worth thinking about:

OPTIONS:
[A] Initialize all cells to 1
```diff
+++ euler15.py
@@ -0,0 +1,5 @@
+def grid_paths(n):
+    dp = [[1] * (n + 1) for _ in range(n + 1)]
+    for i in range(1, n + 1):
+        for j in range(1, n + 1):
+            dp[i][j] = dp[i-1][j] + dp[i][j-1]
```
Every cell in row 0 or column 0 genuinely has exactly 1 path, so pre-filling with 1 is correct — no separate base-case loop needed.

[B] Zero-init, set borders explicitly
```diff
+++ euler15.py
@@ -0,0 +1,8 @@
+def grid_paths(n):
+    dp = [[0] * (n + 1) for _ in range(n + 1)]
+    for k in range(n + 1):
+        dp[0][k] = dp[k][0] = 1
+    for i in range(1, n + 1):
+        for j in range(1, n + 1):
+            dp[i][j] = dp[i-1][j] + dp[i][j-1]
```
Make the base cases explicit before running the recurrence.

(Reply with A or B, or ask a follow-up question.)

Tutor: How would you initialize the table?

### Student

I'll go with **A** — initialize all cells to 1.

It's cleaner and more direct. Since we know that every cell in row 0 and column 0 genuinely represents exactly one path (you can only go right along the top, or down along the left), pre-filling with 1 makes sense and saves us from an extra setup loop. The recurrence then naturally builds from there without needing to special-case the borders.

Let me write it out and test it on a small example first — say a 2×2 grid — to verify the logic before running it on the full 20×20:

```python
def grid_paths(n):
    dp = [[1] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    return dp[n][n]

# Test on 2x2
print(grid_paths(2))  # Should be 6
```

For a 2×2 grid:
- dp[1][1] = dp[0][1] + dp[1][0] = 1 + 1 = 2
- dp[1][2] = dp[0][2] + dp[1][1] = 1 + 2 = 3
- dp[2][1] = dp[1][1] + dp[2][0] = 2 + 1 = 3
- dp[2][2] = dp[1][2] + dp[2][1] = 3 + 3 = 6

That looks right — 6 paths through a 2×2 grid. Now let me run it on 20×20:

```python
print(grid_paths(20))
```

What answer do I get?

---

## Turn 3

### Tutor

Tutor: Your 2×2 trace is exactly right. Let me run it:

[Bash(python3 -c "
def grid_paths(n):
    dp = [[1] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    return dp[n][n]

print('2x2:', grid_paths(2))
print('20x20:', grid_paths(20))

# Print the 4x4 table to show Pascal's triangle
n = 4
dp = [[1] * (n + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    for j in range(1, n + 1):
        dp[i][j] = dp[i-1][j] + dp[i][j-1]

print()
print('4x4 table:')
for row in dp:
    print([str(x).rjust(4) for x in row])
"
)]
  2x2: 6
  20x20: 137846528820
  
  4x4 table:
  ['   1', '   1', '   1', '   1', '   1']
  ['   1', '   2', '   3', '   4', '   5']
  ['   1', '   3', '   6', '  10', '  15']
  ['   1', '   4', '  10', '  20', '  35']
  ['   1', '   5', '  15', '  35', '  70']

[Bash(python3 -c "import math; print('C(40,20) =', math.comb(40, 20))")]
  C(40,20) = 137846528820

Tutor: **137,846,528,820** — and the DP and `math.comb` agree perfectly.

Now look at that 4×4 table — do you see it?

```
 1   1   1   1   1
 1   2   3   4   5
 1   3   6  10  15
 1   4  10  20  35
 1   5  15  35  70
```

Those are binomial coefficients. Specifically, `dp[i][j] = C(i+j, i)`. You can verify:
- `dp[2][2] = C(4,2) = 6` ✓  
- `dp[3][3] = C(6,3) = 20` ✓  
- `dp[4][4] = C(8,4) = 70` ✓

**Why?** Each cell `dp[i][j]` counts paths using exactly `i` down-moves and `j` right-moves — that's just choosing which `i` of the `i+j` total steps are "down": `C(i+j, i)`. The DP recurrence (`dp[i][j] = dp[i-1][j] + dp[i][j-1]`) is exactly Pascal's identity (`C(n,k) = C(n-1,k-1) + C(n-1,k)`). The table is Pascal's triangle, rotated 45°.

So `dp[20][20] = C(40, 20)` isn't a coincidence — it's what the DP was computing all along, just spelled out cell by cell.

**The one-liner, now earned:**
```python
import math
print(math.comb(40, 20))  # 137846528820
```

You could have started here, but now you know *why* it's `C(40, 20)` and not, say, `C(40, 2)` or `20²`. The combinatorial argument — every path is a sequence of 20 R's and 20 D's, choose which 20 steps are R — follows directly from reading what the DP cells are counting.

### Student

Wow, that's really elegant. I see it now — the DP table *is* Pascal's triangle, and that's not just a neat pattern, it's the fundamental reason why the closed-form is `C(40, 20)`.

I love how the connection works:
- DP builds up by counting: "how many ways to reach this cell?"
- At `dp[i][j]`, we've implicitly counted all sequences of `i` down-moves and `j` right-moves
- Choosing which `i` of `i+j` steps are down is exactly `C(i+j, i)`
- So the recurrence `dp[i][j] = dp[i-1][j] + dp[i][j-1]` is literally Pascal's identity playing out

And for the 20×20 grid: 40 total steps (20 right + 20 down), choose which 20 are down (or equivalently, which 20 are right) → `C(40, 20) = 137,846,528,820`.

The DP approach made it concrete and visible. Starting with the formula would've been faster, but I wouldn't have understood *why* it works. This way, I can see how the combinatorial structure emerges naturally from the recurrence.

Thanks for walking through both angles — it's much clearer now why they give the same answer and how they're actually computing the same thing from different directions.

<done/>

---

**Run end:** done after 3 turn(s) in 89.4s
