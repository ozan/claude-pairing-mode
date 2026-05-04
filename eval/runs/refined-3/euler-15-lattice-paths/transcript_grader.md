# euler-15-lattice-paths

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:53:25

## Initial prompt

Project Euler #15: how many distinct routes are there through a 20×20 grid moving only right or down? Closed-form is fine but discuss the DP path too.

---

## Turn 1

### Tutor

Tutor: Good problem. A 20×20 grid has 21×21 lattice points; every path from top-left to bottom-right is exactly 40 steps — 20 right + 20 down — so the closed form is **C(40,20) = 137,846,528,640**.

But the DP path is worth understanding. Before I write anything, one real decision worth thinking through:

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Full 2D grid O(n²)
```diff
+++ euler15.py
@@ -0,0 +1,8 @@
+def count_paths(n):
+    dp = [[1] * (n + 1) for _ in range(n + 1)]
+    for i in range(1, n + 1):
+        for j in range(1, n + 1):
+            dp[i][j] = dp[i-1][j] + dp[i][j-1]
+    return dp[n][n]
```
Stores the whole grid. `dp[i][j]` = paths to cell (i,j); edges stay 1 (only one way to reach any top/left border cell).

[B] Rolling row O(n)
```diff
+++ euler15.py
@@ -0,0 +1,7 @@
+def count_paths(n):
+    row = [1] * (n + 1)
+    for i in range(1, n + 1):
+        for j in range(1, n + 1):
+            row[j] += row[j-1]
+    return row[n]
```
Keeps only one row, updating left-to-right each pass. Uses O(n) space instead of O(n²).

(Reply with A or B, or ask a follow-up question.)

Tutor: Which of these would you go with for the DP implementation?

### Student

I think I'll go with **B** — the rolling row approach.

My reasoning: since we're just trying to solve this one problem and get the answer for a 20×20 grid, the O(n) space is nice. And honestly, I want to understand how it works rather than just seeing the straightforward 2D grid solution. The rolling row feels like it requires me to actually think through *why* we only need one row at a time.

Let me make sure I understand the logic before we code it up though: each cell's path count is the sum of the cell above it and the cell to its left, right? And because we process row by row left-to-right, by the time we update `row[j]`, the value at `row[j-1]` is already the new count for the current row, and `row[j]` still holds the old count from the previous row — which is what we need. Is that the right mental model?

---

## Turn 2

### Tutor

Tutor: That's exactly right. To make it concrete:

```
Before updating row[j] in pass i:
  row[j]   = dp[i-1][j]   ← paths from above (not yet touched this pass)
  row[j-1] = dp[i][j-1]   ← paths from the left (just updated)
  
row[j] += row[j-1]  →  dp[i][j] = dp[i-1][j] + dp[i][j-1]  ✓
```

The update order is load-bearing — right-to-left would corrupt the "left" values before you use them. Great mental model, let's write it.

[Bash(ls euler15.py 2>/dev/null && echo exists || echo missing)]
  missing

Tutor: Now, one more decision before the final file — how to express the closed form alongside the DP:

OPTIONS:
[A] math.comb builtin
```diff
+++ euler15.py
@@ -0,0 +1,3 @@
+import math
+def closed_form(n):
+    return math.comb(2 * n, n)
```
`math.comb(40, 20)` directly. Introduced in Python 3.8; uses an optimized internal algorithm.

[B] Factorial formula
```diff
+++ euler15.py
@@ -0,0 +1,3 @@
+import math
+def closed_form(n):
+    return math.factorial(2*n) // (math.factorial(n) ** 2)
```
Spells out C(2n, n) = (2n)! / (n! · n!) explicitly — matches the formula you'd write by hand.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which would you use for the closed-form expression?

### Student

I'll go with **A** — `math.comb`.

Here's my thinking: `math.comb` is purpose-built for this and will be more efficient internally (it's optimized to avoid computing huge factorials). Plus, it's clearer at a glance what we're computing — the binomial coefficient C(40, 20) — without having to mentally parse the factorial formula. And since Python 3.8 is pretty standard now, I don't think we need to worry about compatibility.

Option B is nice for showing the math explicitly, but `math.comb` is the better tool for the job.

So I'm ready — let me write out the full file with both approaches:

```python
import math

def count_paths_dp(n):
    """DP solution: rolling row, O(n) space."""
    row = [1] * (n + 1)
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            row[j] += row[j-1]
    return row[n]

def count_paths_closed(n):
    """Closed form: C(2n, n)."""
    return math.comb(2 * n, n)

if __name__ == "__main__":
    n = 20
    dp_answer = count_paths_dp(n)
    closed_answer = count_paths_closed(n)
    
    print(f"DP solution: {dp_answer}")
    print(f"Closed form: {closed_answer}")
    print(f"Match: {dp_answer == closed_answer}")
```

Does this look right to you?

---

## Turn 3

### Tutor

Tutor: Correct on all counts — and good reasoning on `math.comb`. Let me write and run it.

[Write(euler15.py)]
import math

def count_paths_dp(n):
    """DP solution: rolling row, O(n) space."""
    row = [1] * (n + 1)
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            row[j] += row[j-1]
    return row[n]

def count_paths_closed(n):
    """Closed form: C(2n, n)."""
… (11 more lines)
  File created successfully at: euler15.py

[Bash(python3 euler15.py)]
  DP solution: 137846528820
  Closed form: 137846528820
  Match: True

Tutor: **137,846,528,820** — and I owe a small correction: I said 137,846,528,640 up top; that was wrong. Python is right.

Both methods agree, code is clean. Before we close — one insight worth sitting with:

OPTIONS:
[A] Each cell is a binomial coefficient
In the full 2D grid, `dp[i][j] = C(i+j, i)` for every cell. Pascal's identity — `C(n,k) = C(n-1,k-1) + C(n-1,k)` — is exactly the recurrence in disguise. The whole grid is a rotated slice of Pascal's triangle.

[B] Interior cells have no closed form
The edge cells are trivially 1, but interior values grow in a complex pattern driven by the recurrence. You need the DP to compute them — there's no single formula that works for every `dp[i][j]`.

(Reply with A or B, or ask a follow-up question.)

Tutor: What do you think — do the interior DP cells have a closed form, or not?

### Student

I'll go with **A** — each cell is a binomial coefficient.

Actually, now that you mention it, that makes total sense. If `dp[i][j]` represents the number of paths to reach cell (i, j), then that's exactly the number of ways to choose i steps down out of (i+j) total steps, which is C(i+j, i). And Pascal's identity `C(n,k) = C(n-1,k-1) + C(n-1,k)` is literally saying: paths to (i,j) = paths from above + paths from the left, which is our recurrence.

So there *is* a closed form for every interior cell — it's just that the DP approach lets us compute them all incrementally without having to call `math.comb` for each one. That's pretty elegant.

The code works, both methods agree, and I understand why now. I'm satisfied with this solution.

<done/>

---

**Run end:** done after 3 turn(s) in 137.8s
