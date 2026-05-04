# leetcode-edit-distance

- Source: `leetcode`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:37:27.563Z

---

## Turn 1

**User:**

Let's solve Leetcode #72, 'Edit Distance'. Compute the minimum number of single-character insertions, deletions, or substitutions needed to convert one string into another.

**Pair:**

Assistant: Classic DP problem. Let me start with the most important decision — the recurrence. Given `dp[i][j]` = min edits to convert `word1[:i]` → `word2[:j]`, here's the core question:

[Bash(ls edit_distance.py 2>/dev/null && echo exists || echo missing)]
  missing

Assistant: When `word1[i-1] != word2[j-1]`, which recurrence is right?

**Option A**
```diff
+++ edit_distance.py
@@ -0,0 +1,3 @@
+  else:
+      dp[i][j] = 1 + min(dp[i-1][j],    # delete word1[i-1]
+                         dp[i][j-1],    # insert word2[j-1]
+                         dp[i-1][j-1]) # substitute
```

**Option B**
```diff
+++ edit_distance.py
@@ -0,0 +1,3 @@
+  else:
+      dp[i][j] = min(dp[i-1][j] + 1,    # delete word1[i-1]
+                     dp[i][j-1] + 1,    # insert word2[j-1]
+                     dp[i-1][j-1] + 2)  # substitute (remove + add)
```

Which recurrence is correct — A or B?

---

## Turn 2

**User:**

Looking at the operations, I need to think through what each transition represents:

1. **`dp[i-1][j]`**: We've solved up to `word1[:i-1]` and `word2[:j]`. To handle `word1[i-1]`, we **delete** it → cost is `+1`
2. **`dp[i][j-1]`**: We've solved up to `word1[:i]` and `word2[:j-1]`. To handle `word2[j-1]`, we **insert** it → cost is `+1`
3. **`dp[i-1][j-1]`**: We've solved up to `word1[:i-1]` and `word2[:j-1]`. Now we **substitute** (one atomic operation) → cost is `+1`

**Option A is correct.** 

The key insight: substitution is a *single operation* that costs 1, not a compound "remove + add" that would cost 2. Option B's comment is the distractor — it misunderstands substitution as two operations.

Option A factoring out the `1 +` is just algebraic; it's equivalent to `min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+1)`.

I choose **Option A**.

**Pair:**

Assistant: Exactly right. Substitution replaces one character in one step — cost 1, full stop. The `1 +` factored out is just algebra; it's identical to writing `+1` on each branch.

Let me write the skeleton with the recurrence in place:

[Write(edit_distance.py)]
def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)

    # dp[i][j] = min edits to convert word1[:i] -> word2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # base cases: converting to/from empty string
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

… (20 more lines)

[Bash(python edit_distance.py)]
  error: Exit code 127

[Bash(python3 edit_distance.py)]
  all tests passed

Assistant: All green. Current complexity: **O(m×n) time, O(m×n) space**.

Now — this works, but the full table allocates `m×n` cells when we only ever look at the *previous row* to compute the current one. Here's the space-optimization question:

**Option A** — Two-row rolling buffer:
```diff
+++ edit_distance.py
@@ -4,7 +4,8 @@
-    dp = [[0] * (n + 1) for _ in range(m + 1)]
-    for i in range(m + 1):
-        dp[i][0] = i
-    for j in range(n + 1):
-        dp[0][j] = j
+    prev = list(range(n + 1))
+    for i in range(1, m + 1):
+        curr = [i] + [0] * n
```

**Option B** — Single row, updated in-place:
```diff
+++ edit_distance.py
@@ -4,6 +4,5 @@
-    dp = [[0] * (n + 1) for _ in range(m + 1)]
-    for i in range(m + 1):
-        dp[i][0] = i
-    for j in range(n + 1):
-        dp[0][j] = j
+    row = list(range(n + 1))
+    for i in range(1, m + 1):
+        row[0] = i
```

Both aim for O(n) space. Which approach is actually correct?

---

## Turn 3

**User:**

Looking at the memory dependencies: when computing `row[j]`, we need:
- `row[j]` *before the update* (old value = previous row) → for the "delete" branch
- `row[j-1]` (just computed in this row) → for the "insert" branch  
- The *diagonal* (old `row[j-1]`) → for the "substitute" branch

**Option A is correct.**

With two separate `prev` and `curr`, there's no ambiguity. When we compute `curr[j]`:
- `prev[j]` is untouched
- `curr[j-1]` is already computed
- `prev[j-1]` (the diagonal) is untouched

**Option B's hidden trap**: updating a single `row` in-place loses the diagonal before we use it. At iteration `j`, after we compute and overwrite `row[j-1]`, we can't access the old diagonal value anymore. Option B would need to save the diagonal *before* each update:

```python
prev_diag = 0
for j in range(1, n + 1):
    temp = row[j]              # save before overwrite
    row[j] = 1 + min(temp, row[j-1], prev_diag)
    prev_diag = temp
```

But that's not shown in the option, making Option B subtly broken or at best incomplete.

**I choose Option A** — it's clearer and doesn't hide complexity.

**Pair:**

Assistant: Spot on — and you nailed the exact failure mode. The diagonal (`prev[j-1]`) gets clobbered by the time you need it in the in-place version, so you'd need that `prev_diag` bookkeeping. Option A keeps everything clean with no hidden state.

Let me apply the full two-row transformation:

[Read(edit_distance.py)]
  1	def min_distance(word1: str, word2: str) -> int:
  2	    m, n = len(word1), len(word2)
  3	
  4	    # dp[i][j] = min edits to convert word1[:i] -> word2[:j]
  5	    dp = [[0] * (n + 1) for _ in range(m + 1)]
  6	
  7	    # base cases: converting to/from empty string
  8	    for i in range(m + 1):
  9	        dp[i][0] = i
  10	    for j in range(n + 1):
  11	        dp[0][j] = j
  12	
  … (20 more lines)

[Edit(edit_distance.py)]
--- before
    # dp[i][j] = min edits to convert word1[:i] -> word2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # base cases: converting to/from empty string
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j],    # delete word1[i-1]
                                   dp[i][j-1],    # insert word2[j-1]
                                   dp[i-1][j-1])  # substitute

    return dp[m][n]
--- after
    # prev[j] = min edits to convert word1[:i-1] -> word2[:j]
    prev = list(range(n + 1))

    for i in range(1, m + 1):
        curr = [i] + [0] * n          # curr[0] = i deletions to reach empty word2
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                curr[j] = prev[j-1]   # chars match: inherit diagonal, no op needed
            else:
                curr[j] = 1 + min(prev[j],      # delete word1[i-1]
                                  curr[j-1],    # insert word2[j-1]
                                  prev[j-1])    # substitute
        prev = curr

    return prev[n]

[Bash(python3 edit_distance.py)]
  all tests passed

Assistant: Still green. We're now at **O(m×n) time, O(n) space** — only two rows in memory at once.

Final solution:
```
word1[:i] → word2[:j]
  match:    curr[j] = prev[j-1]
  mismatch: curr[j] = 1 + min(prev[j], curr[j-1], prev[j-1])
```

Worth noting: you could squeeze to **O(min(m,n))** by always iterating over the *shorter* string in the inner loop — just swap `word1`/`word2` if `m < n`. For LeetCode constraints it rarely matters, but it's a clean one-liner trick if you want it.

---

## Turn 4 (final)

**User:**

Perfect. You've worked through both critical decisions:

1. **Recurrence** — substitution is one atomic operation (cost 1), not a compound remove-then-add (cost 2). Option A.
2. **Space optimization** — two-row rolling buffer preserves the diagonal dependency; in-place update would lose it. Option A again.

The solution is solid: **O(m×n) time, O(n) space**, and you understand *why* each piece works. The code passes tests, and you've seen the exact failure mode that makes Option B subtly broken (the clobbered diagonal).

If you want the bonus O(min(m,n)) optimization later, it's just one line — swap word1/word2 if m < n so you only allocate space for the shorter string's width. But the current version is complete and correct.

You've got Edit Distance. 

<done/>

---

**Run end**: done after 3 turns (161s)
