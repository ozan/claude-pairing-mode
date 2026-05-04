# euler-67-max-path-sum

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:44:42

## Initial prompt

Project Euler #67: find the maximum top-to-bottom path sum through a triangle of numbers, where each step moves to an adjacent number on the row below. Use a small example triangle hard-coded inline (10 rows is fine).

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Top-down DP
Build a `dp` table the same shape as the triangle. Set `dp[0][0] = triangle[0][0]`, then fill each row using `dp[i][j] = triangle[i][j] + max(dp[i-1][j-1], dp[i-1][j])` (clamping at edges). Answer is `max(dp[-1])`.

[B] Bottom-up DP
Start with a copy of the bottom row. Walk upward: each cell becomes `triangle[i][j] + max(row[j], row[j+1])`. After processing all rows, `row[0]` is the answer — no `max` over a whole row needed.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach do you want to use?

### Student

I think I'd like to go with **B**.

I've done a bit of top-down DP before, and the bottom-up approach seems cleaner to me here — we only need to keep one row in memory at a time instead of building a whole table, and there's no edge-clamping logic to worry about. Plus, the final answer is just `row[0]` at the end, which feels more straightforward than taking the max of the last row.

Let me start coding it up and see where I get stuck.

---

## Turn 2

### Tutor

Tutor: Great reasoning — all of it correct. Let me scaffold the triangle and the outer structure, then we'll nail the one subtle decision in the inner loop.

[Glob(triangle.py)]
  No files found

[Write(triangle.py)]
triangle = [
    [3],
    [7, 4],
    [2, 4, 6],
    [8, 5, 9, 3],
    [20, 4, 82, 47, 65],
    [19, 1, 23, 75, 3, 34],
    [88, 2, 77, 73, 7, 63, 67],
    [99, 65, 4, 28, 6, 16, 70, 92],
    [41, 41, 26, 56, 83, 40, 80, 70, 33],
    [41, 48, 72, 33, 47, 32, 37, 16, 94, 29],
]
… (10 more lines)
  File created successfully at: triangle.py

Tutor: Now the one decision worth pausing on — the inner loop direction. We're modifying `dp` in-place as we go across each row:

OPTIONS:
[A] Left-to-right (j = 0 … i)
```diff
+++ triangle.py
@@ -12,2 +12,2 @@
-        for j in range(len(tri[i])):          # 0, 1, 2, …
+        for j in range(len(tri[i])):          # 0 → i
             dp[j] = tri[i][j] + max(dp[j], dp[j + 1])
```

[B] Right-to-left (j = i … 0)
```diff
+++ triangle.py
@@ -12,2 +12,2 @@
-        for j in range(len(tri[i])):
+        for j in range(len(tri[i]) - 1, -1, -1):   # i → 0
             dp[j] = tri[i][j] + max(dp[j], dp[j + 1])
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which direction should the inner loop go — and why does it matter?

### Student

Hmm, let me think through this carefully.

If we go **left-to-right (A)**, we'd be updating `dp[j]` while we're still going to use `dp[j+1]` later in the same row. But wait — we're reading `dp[j+1]` to compute the new value of `dp[j]`. If we've already updated `dp[j+1]` in this same loop (because we came from the left), we'd be using the *new* value instead of the old value from the previous row. That would mix values from different rows, which breaks the logic.

If we go **right-to-left (B)**, we start from the rightmost element and work backward. When we update `dp[j]`, we read from `dp[j+1]`, which hasn't been touched yet in this row — it still has the old value from the previous row. So we're always comparing against the correct previous-row values.

I think the answer is **B** — right-to-left. The direction matters because we need to make sure we're reading the *old* values from the previous row, not accidentally using values we just updated in the current iteration.

---

## Turn 3

### Tutor

Tutor: Your logic is close, but the direction is flipped! Let's trace it carefully with a concrete example. Say `dp = [8, 5, 9, 3]` (bottom row) and we're processing `[2, 4, 6]` above it.

**Right-to-left (j = 2, 1, 0):**
- `j=2`: `dp[2] = 6 + max(9, 3) = 15` ← fine so far
- `j=1`: `dp[1] = 4 + max(5, dp[2])` — but `dp[2]` is now **15**, not the original **9**. We're reading a value we just overwrote. ✗

**Left-to-right (j = 0, 1, 2):**
- `j=0`: `dp[0] = 2 + max(8, 5) = 10`. We read `dp[1]=5` — untouched. ✓
- `j=1`: `dp[1] = 4 + max(5, 9) = 13`. We read `dp[2]=9` — untouched. ✓
- `j=2`: `dp[2] = 6 + max(9, 3) = 15`. We read `dp[3]=3` — untouched. ✓

The key insight: going left-to-right, we write `dp[j]` and then read `dp[j+1]` — which is always *ahead* of where we've written. Right-to-left does the opposite: we write `dp[j]` and then read `dp[j-1]`... which is fine, but the *other* operand `dp[j+1]` is what we already corrupted on the previous iteration.

The code as written (option A, left-to-right) is already correct. Let's run it:

[Bash(cd /tmp 2>/dev/null; python3 triangle.py 2>/dev/null || python3 /Users/$(whoami)/triangle.py 2>/dev/null || python3 triangle.py)]
  error: Exit code 2

[Bash(python3 triangle.py)]
  438

Tutor: Works. Answer is **438** for this 10-row triangle.

One small thing worth noting — we do `tri[-1][:]` to copy the bottom row rather than using it directly. Here's the tradeoff there:

OPTIONS:
[A] Copy the bottom row
```diff
+++ triangle.py
@@ -11,1 +11,1 @@
-    dp = tri[-1][:]   # copy
+    dp = tri[-1][:]   # copy — tri is unchanged after the call
```
The caller's data is never modified, which makes the function safe to call multiple times or in tests.

[B] Mutate in-place
```diff
+++ triangle.py
@@ -11,3 +11,3 @@
-    dp = tri[-1][:]
-    for i in range(len(tri) - 2, -1, -1):
-        for j in range(len(tri[i])):
-            dp[j] = tri[i][j] + max(dp[j], dp[j + 1])
-    return dp[0]
+    for i in range(len(tri) - 2, -1, -1):
+        for j in range(len(tri[i])):
+            tri[i][j] += max(tri[i + 1][j], tri[i + 1][j + 1])
+    return tri[0][0]
```
No extra allocation; writes results back into `tri` directly.

(Reply with A or B, or ask a follow-up question.)

Tutor: Both are valid, but one has a subtle downside for reuse — which do you prefer?

### Student

I'd go with **A** — copy the bottom row.

Even though it uses a bit more memory, it keeps the function pure and non-destructive. If someone calls this function twice on the same triangle, or wants to use the original triangle data for something else afterward, option B would silently corrupt it. That feels like a bug waiting to happen.

Plus, in the context of Project Euler, we're probably only calling this once per input anyway, so the memory savings from option B don't really matter. Better to be safe and predictable.

<done/>

---

**Run end:** done after 3 turn(s) in 126.1s
