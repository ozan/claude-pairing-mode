# leetcode-edit-distance

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T20:59:58

## Initial prompt

Let's solve Leetcode #72, 'Edit Distance'. Compute the minimum number of single-character insertions, deletions, or substitutions needed to convert one string into another.

---

## Turn 1

### Tutor

Tutor: Classic DP problem. Before we write any code, let me ask a design question:

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Top-down with memoization
Define `dp(i, j)` recursively: the edit distance between `word1[:i]` and `word2[:j]`. Cache results with `@lru_cache`. Base cases: `dp(0, j) = j`, `dp(i, 0) = i`.

[B] Bottom-up DP table
Build an `(m+1) × (n+1)` table row by row. `dp[i][j]` = edit distance between `word1[:i]` and `word2[:j]`. This order naturally enables a later space optimization down to O(n).

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach do you want to start with?

### Student

I think I'll go with **[B] Bottom-up DP table**.

I like the idea of building it row by row because it feels more concrete to me—I can visualize filling in a grid. Plus, you mentioned it naturally leads to a space optimization later, which sounds like a good learning opportunity. Top-down with memoization is cool, but I feel like the bottom-up approach will help me understand the state transitions more clearly as I go.

Should we start by setting up the table and thinking through the base cases and recurrence?

---

## Turn 2

### Tutor

Tutor: Exactly right — and that intuition about visualizing the grid will pay off. Let me ask about the core recurrence before we write anything:

OPTIONS:
[A] Two-branch recurrence
```diff
+++ edit_distance.py
@@ -0,0 +1,6 @@
+if word1[i-1] == word2[j-1]:
+    dp[i][j] = dp[i-1][j-1]
+else:
+    dp[i][j] = 1 + min(
+        dp[i-1][j],    # delete
+        dp[i][j-1],    # insert
+        dp[i-1][j-1],  # substitute
+    )
```

[B] Two ops only, no substitute
```diff
+++ edit_distance.py
@@ -0,0 +1,5 @@
+if word1[i-1] == word2[j-1]:
+    dp[i][j] = dp[i-1][j-1]
+else:
+    dp[i][j] = 1 + min(
+        dp[i-1][j],    # delete
+        dp[i][j-1],    # insert
+    )
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which recurrence is correct?

### Student

It's **[A] Two-branch recurrence**.

The substitution operation is necessary because if the characters don't match, we have three choices:
- Delete from `word1` (move up in the table)
- Insert into `word1` (move left in the table)
- Replace the character in `word1` (move diagonally)

Option [B] without substitution would mean we can only delete or insert, but that's not enough—sometimes a single substitution is the cheapest way to align two characters. For example, converting "a" to "b" should cost 1 (one substitution), not 2 (delete + insert).

So [A] is correct. Should we start coding this up now?

---

## Turn 3

### Tutor

Tutor: Exactly right — and notice the diagonal `dp[i-1][j-1]` is what makes substitution cheap: you "consume" one character from each string simultaneously.

Let's build the file now:

[Write(edit_distance.py)]
def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)

    # dp[i][j] = edit distance between word1[:i] and word2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases: transforming to/from empty string
    for i in range(m + 1):
        dp[i][0] = i  # delete all of word1[:i]
    for j in range(n + 1):
        dp[0][j] = j  # insert all of word2[:j]

… (23 more lines)
  File created successfully at: edit_distance.py

[Bash(cd /Users/cody/lc && python edit_distance.py)]
  error: Exit code 1

[Bash(python edit_distance.py)]
  All tests passed.

Tutor: All green. Now — you mentioned the space optimization. Currently we're using **O(m·n)** space for the full grid. But look at the inner loop: `dp[i][j]` only ever reads from row `i-1` and the current row `i`. That's a hint.

OPTIONS:
[A] Keep one row, one prev value
```diff
+++ edit_distance.py
@@ -3,7 +3,9 @@
-    dp = [[0] * (n + 1) for _ in range(m + 1)]
-    for i in range(m + 1):
-        dp[i][0] = i
-    for j in range(n + 1):
-        dp[0][j] = j
+    dp = list(range(n + 1))   # represents the previous row
+
     for i in range(1, m + 1):
+        new_dp = [i] + [0] * n
+        prev = dp[0]           # holds dp[i-1][j-1] before overwrite
         for j in range(1, n + 1):
-            if word1[i - 1] == word2[j - 1]:
-                dp[i][j] = dp[i - 1][j - 1]
+            temp = dp[j]
+            if word1[i - 1] == word2[j - 1]:
+                new_dp[j] = prev
             else:
-                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
-    return dp[m][n]
+                new_dp[j] = 1 + min(dp[j], new_dp[j-1], prev)
+            prev = temp
+        dp = new_dp
+    return dp[n]
```

[B] Roll in-place, single array
```diff
+++ edit_distance.py
@@ -3,7 +3,9 @@
-    dp = [[0] * (n + 1) for _ in range(m + 1)]
-    for i in range(m + 1):
-        dp[i][0] = i
-    for j in range(n + 1):
-        dp[0][j] = j
+    dp = list(range(n + 1))
+
     for i in range(1, m + 1):
+        dp[0] = i
         for j in range(1, n + 1):
-            if word1[i - 1] == word2[j - 1]:
-                dp[i][j] = dp[i - 1][j - 1]
+            if word1[i - 1] == word2[j - 1]:
+                dp[j] = dp[j - 1]   # ← diagonal from *already-updated* row
             else:
-                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
-    return dp[m][n]
+                dp[j] = 1 + min(dp[j], dp[j - 1], dp[j - 1])
+    return dp[n]
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Both use a single 1-D array instead of the full grid — O(n) space. Which is correct?

### Student

I need to think through this carefully...

Option [B] looks wrong to me. In the line `if word1[i - 1] == word2[j - 1]: dp[j] = dp[j - 1]`, that's setting `dp[j]` to `dp[j - 1]`, but that's not the diagonal value—that's the value to the left in the current row, which would be an insertion cost, not a match.

Also in the else branch, `min(dp[j], dp[j - 1], dp[j - 1])` has `dp[j - 1]` twice, which doesn't make sense. We need three distinct values: the one above (old `dp[j]`), the one to the left (new `dp[j - 1]`), and the diagonal (the old value from before we updated `dp[j - 1]`).

Option [A] is correct because it explicitly saves the diagonal value in `prev` before overwriting it. So when we compute `new_dp[j]`, we have:
- `dp[j]` = the value above (old row)
- `new_dp[j-1]` = the value to the left (already computed in current row)
- `prev` = the diagonal (saved before overwrite)

That's **[A]**—it correctly preserves all three values we need.

---

## Turn 4

### Tutor

Tutor: Spot-on analysis — you identified both bugs in B independently. Let's apply it:

[Read(edit_distance.py)]
  1	def min_distance(word1: str, word2: str) -> int:
  2	    m, n = len(word1), len(word2)
  3	
  4	    # dp[i][j] = edit distance between word1[:i] and word2[:j]
  5	    dp = [[0] * (n + 1) for _ in range(m + 1)]
  6	
  7	    # Base cases: transforming to/from empty string
  8	    for i in range(m + 1):
  9	        dp[i][0] = i  # delete all of word1[:i]
  10	    for j in range(n + 1):
  11	        dp[0][j] = j  # insert all of word2[:j]
  12	
  … (23 more lines)

[Edit(edit_distance.py)]
--- before
    # dp[i][j] = edit distance between word1[:i] and word2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases: transforming to/from empty string
    for i in range(m + 1):
        dp[i][0] = i  # delete all of word1[:i]
    for j in range(n + 1):
        dp[0][j] = j  # insert all of word2[:j]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # delete word1[i-1]
                    dp[i][j - 1],      # insert word2[j-1]
                    dp[i - 1][j - 1],  # substitute
                )

    return dp[m][n]
--- after
    # dp[j] = edit distance between word1[:i] and word2[:j] for current row i
    dp = list(range(n + 1))  # base case: row 0 = [0, 1, 2, ..., n]

    for i in range(1, m + 1):
        new_dp = [i] + [0] * n      # new_dp[0] = i (delete all of word1[:i])
        prev = dp[0]                 # holds dp[i-1][j-1] before it's overwritten
        for j in range(1, n + 1):
            temp = dp[j]             # save dp[i-1][j] before we move on
            if word1[i - 1] == word2[j - 1]:
                new_dp[j] = prev     # no cost: consume one char from each
            else:
                new_dp[j] = 1 + min(
                    dp[j],           # delete  (above)
                    new_dp[j - 1],   # insert  (left in current row)
                    prev,            # substitute (diagonal)
                )
            prev = temp              # slide the diagonal forward
        dp = new_dp

    return dp[n]
  The file edit_distance.py has been updated successfully.

[Bash(python edit_distance.py)]
  All tests passed.

Tutor: All green. Here's the final picture:

| | complexity | notes |
|---|---|---|
| Time | O(m·n) | every cell computed once |
| Space | O(n) | single row, `prev` scalar for diagonal |

The key insight you nailed: updating in-place destroys the diagonal before you've read it. The `prev` variable is the minimal "memory" needed to recover it — you only ever need *one* extra scalar, not a whole second array.

The solution is clean and complete. Want to trace through a concrete example (`"horse" → "ros"`) to cement how the row evolves, or are you happy with it?

### Student

I'm happy with it! I feel like I understand the approach well now—especially the key insight about needing to save the diagonal value before it gets overwritten. The `prev` variable is elegant; I can see why that works.

I could trace through an example, but honestly I think I've learned what I needed to on this problem. The bottom-up DP table with the space optimization makes sense, and I can see how the three operations (delete, insert, substitute) map to the three adjacent cells in the recurrence.

Thanks for walking through this with me—I'll be able to apply this pattern to similar edit distance problems now.

<done/>

---

**Run end:** done after 4 turn(s) in 111.2s
