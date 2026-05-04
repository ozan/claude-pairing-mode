# euler-67-max-path-sum

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:26:11

## Initial prompt

Project Euler #67: find the maximum top-to-bottom path sum through a triangle of numbers, where each step moves to an adjacent number on the row below. Use a small example triangle hard-coded inline (10 rows is fine).

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Tutor: Before writing any code — which direction would you traverse the triangle?

OPTIONS:
[A] Top-down DP
Keep a `best[]` array the width of the current row. At each row, propagate the best reachable score into the next row's cells, then take `max(best)` at the end.

```diff
+++ triangle.py
@@ -0,0 +1,7 @@
+best = [triangle[0][0]]
+for row in triangle[1:]:
+    nxt = [0] * len(row)
+    for i, v in enumerate(row):
+        from_left  = best[i-1] if i > 0 else -inf
+        from_right = best[i]   if i < len(best) else -inf
+        nxt[i] = v + max(from_left, from_right)
+    best = nxt
```

[B] Bottom-up DP
Work from the second-to-last row upward. Replace each cell with itself plus the better of its two children. The answer is simply `triangle[0][0]` when done.

```diff
+++ triangle.py
@@ -0,0 +1,4 @@
+for r in range(len(triangle) - 2, -1, -1):
+    for c in range(len(triangle[r])):
+        triangle[r][c] += max(triangle[r+1][c],
+                              triangle[r+1][c+1])
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which do you prefer?

### Student

I think I prefer **[B] Bottom-up DP**.

It seems simpler to me — we're modifying the triangle in place and just comparing two adjacent children at each step. Plus, at the end the answer is already sitting right there at `triangle[0][0]` without needing to track a separate `best` array.

Let me try implementing that approach with a hard-coded triangle.

---

## Turn 2

### Tutor

Tutor: Exactly right on all counts. Let me lay down the triangle, then there's one more choice worth making deliberately.

[Write(triangle.py)]
triangle = [
    [75],
    [95, 64],
    [17, 47, 82],
    [18, 35, 87, 10],
    [20,  4, 82, 47, 65],
    [19,  1, 23, 75,  3, 34],
    [88,  2, 77, 73,  7, 63, 67],
    [99, 65,  4, 28,  6, 16, 70, 92],
    [41, 41, 26, 56, 83, 40, 80, 70, 33],
    [41, 48, 72, 33, 47, 32, 37, 16, 94, 29],
]
… (3 more lines)
  File created successfully at: triangle.py

Tutor: Now — the bottom-up loop will write back into each cell. Should we operate directly on `triangle`, or work on a copy?

OPTIONS:
[A] Mutate in-place
Run the DP directly on `triangle`. O(1) extra space; the answer is at `triangle[0][0]`.

```diff
+++ triangle.py
@@ -12,2 +12,5 @@
-# TODO: bottom-up DP here
+for r in range(len(triangle) - 2, -1, -1):
+    for c in range(len(triangle[r])):
+        triangle[r][c] += max(triangle[r+1][c], triangle[r+1][c+1])
+print(triangle[0][0])
```

[B] Work on a copy
Deep-copy the triangle first, leaving the original intact for printing or reuse.

```diff
+++ triangle.py
@@ -12,2 +12,6 @@
-# TODO: bottom-up DP here
+import copy
+dp = copy.deepcopy(triangle)
+for r in range(len(dp) - 2, -1, -1):
+    for c in range(len(dp[r])):
+        dp[r][c] += max(dp[r+1][c], dp[r+1][c+1])
+print(dp[0][0])
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which do you prefer?

### Student

I'll go with **[A] Mutate in-place**.

For this problem, we only need the final answer, so there's no reason to keep the original triangle around. In-place mutation is simpler, uses less memory, and is faster — no need for the overhead of a deep copy. The code is cleaner too.

Let me write out the complete solution:

```python
triangle = [
    [75],
    [95, 64],
    [17, 47, 82],
    [18, 35, 87, 10],
    [20,  4, 82, 47, 65],
    [19,  1, 23, 75,  3, 34],
    [88,  2, 77, 73,  7, 63, 67],
    [99, 65,  4, 28,  6, 16, 70, 92],
    [41, 41, 26, 56, 83, 40, 80, 70, 33],
    [41, 48, 72, 33, 47, 32, 37, 16, 94, 29],
]

for r in range(len(triangle) - 2, -1, -1):
    for c in range(len(triangle[r])):
        triangle[r][c] += max(triangle[r+1][c], triangle[r+1][c+1])

print(triangle[0][0])
```

Does that look right? Should I test it?

---

## Turn 3

### Tutor

Tutor: Looks exactly right. Let me apply it and run it.

[Edit(triangle.py)]
--- before
# TODO: bottom-up DP here
--- after
for r in range(len(triangle) - 2, -1, -1):
    for c in range(len(triangle[r])):
        triangle[r][c] += max(triangle[r+1][c], triangle[r+1][c+1])

print(triangle[0][0])
  The file triangle.py has been updated successfully.

[Bash(python triangle.py)]
  696

Tutor: 696. Working perfectly.

One "look back" worth thinking about — PE #67 scales this to 100 rows. A naive recursive solution explores every root-to-leaf path. Which of these two recursive alternatives matches our DP's complexity?

OPTIONS:
[A] Plain recursion
```diff
+++ triangle.py
@@ -0,0 +1,5 @@
+def best(r, c):
+    if r == len(triangle) - 1:
+        return triangle[r][c]
+    return triangle[r][c] + max(best(r+1, c),
+                                best(r+1, c+1))
```

[B] Memoized recursion
```diff
+++ triangle.py
@@ -0,0 +1,6 @@
+from functools import lru_cache
+@lru_cache(maxsize=None)
+def best(r, c):
+    if r == len(triangle) - 1:
+        return triangle[r][c]
+    return triangle[r][c] + max(best(r+1, c),
+                                best(r+1, c+1))
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which one matches our iterative solution's complexity — and roughly how many calls does the *other* one make for 100 rows?

### Student

**[B] Memoized recursion** matches our iterative DP's complexity.

With memoization, each cell `(r, c)` is computed exactly once, so we make O(n²) calls total (where n is the number of rows). That's the same as our bottom-up loop, which visits each cell once.

Plain recursion without memoization explodes — it recomputes the same subproblems over and over. For 100 rows, I think it would be exponential... roughly 2^100 calls? Because each call branches into two recursive calls, and there's massive overlap between branches. That's completely infeasible.

So memoization turns the exponential problem into a polynomial one, which is why DP (either iterative or memoized) is the right approach here.

Our iterative bottom-up solution is still my preference though — it's direct, uses less overhead than function calls, and the logic is easy to follow.

<done/>

---

**Run end:** done after 3 turn(s) in 104.8s
