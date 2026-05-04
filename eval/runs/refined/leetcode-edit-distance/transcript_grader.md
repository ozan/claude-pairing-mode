# leetcode-edit-distance

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:40:07

## Initial prompt

Let's solve Leetcode #72, 'Edit Distance'. Compute the minimum number of single-character insertions, deletions, or substitutions needed to convert one string into another.

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Tutor: Classic DP problem. Let's start with the core approach:

OPTIONS:
[A] Top-down with memoization
Recurse on `(i, j)` — the edit distance between `word1[:i]` and `word2[:j]` — and cache results. The base cases fall out naturally: if either index hits 0, return the other (pure insertions/deletions).

[B] Bottom-up 2D table
Build a `(m+1) × (n+1)` table iteratively. Row 0 and column 0 are initialized to `0..m` and `0..n` (the base cases), then fill left-to-right, top-to-bottom.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach would you like to use?

### Student

I'll go with **B** — the bottom-up 2D table approach. I think seeing the table fill up iteratively will help me understand the state transitions more clearly than recursion would. Plus, it feels more straightforward to implement without worrying about the memoization setup.

Should we start by setting up the table structure and initialization?

---

## Turn 2

### Tutor

Tutor: Good instinct. Let's lay down the full structure. The crux is the recurrence — which of these fills the table correctly?

OPTIONS:
[A] Always take the min + 1
```diff
+++ edit_distance.py
@@ -0,0 +1,13 @@
+def min_distance(word1: str, word2: str) -> int:
+    m, n = len(word1), len(word2)
+    dp = [[0] * (n + 1) for _ in range(m + 1)]
+    for i in range(m + 1):
+        dp[i][0] = i
+    for j in range(n + 1):
+        dp[0][j] = j
+    for i in range(1, m + 1):
+        for j in range(1, n + 1):
+            dp[i][j] = 1 + min(dp[i-1][j],
+                                dp[i][j-1],
+                                dp[i-1][j-1])
+    return dp[m][n]
```

[B] Branch on character match
```diff
+++ edit_distance.py
@@ -0,0 +1,15 @@
+def min_distance(word1: str, word2: str) -> int:
+    m, n = len(word1), len(word2)
+    dp = [[0] * (n + 1) for _ in range(m + 1)]
+    for i in range(m + 1):
+        dp[i][0] = i
+    for j in range(n + 1):
+        dp[0][j] = j
+    for i in range(1, m + 1):
+        for j in range(1, n + 1):
+            if word1[i-1] == word2[j-1]:
+                dp[i][j] = dp[i-1][j-1]
+            else:
+                dp[i][j] = 1 + min(dp[i-1][j],
+                                    dp[i][j-1],
+                                    dp[i-1][j-1])
+    return dp[m][n]
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which recurrence looks right to you — and why?

### Student

I think it's **B** — branch on character match.

Here's my reasoning: when the characters match (`word1[i-1] == word2[j-1]`), we don't need to do anything. We've already aligned those characters, so the cost stays the same as `dp[i-1][j-1]` (the distance for the prefixes without those matching characters).

But when they *don't* match, we have three options:
- Delete from `word1`: cost is `dp[i-1][j] + 1`
- Insert into `word1`: cost is `dp[i][j-1] + 1`
- Substitute: cost is `dp[i-1][j-1] + 1`

And we pick whichever is cheapest.

Option A always adds 1 regardless of whether the characters match, which would overcounted when we have matching characters — we'd be charging ourselves for an operation we don't actually need.

Does that logic check out?

---

## Turn 3

### Tutor

Tutor: Exactly right. The diagonal `dp[i-1][j-1]` is the "do nothing" move — you already aligned those two characters for free. Option A would compute `min_distance("abc", "abc") = 3` instead of `0`.

Let me write the file:

[Write(edit_distance.py)]
def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
… (5 more lines)
  File created successfully at: edit_distance.py

Tutor: This is O(mn) time and O(mn) space. Notice that when filling row `i`, you only ever look at row `i-1` and the current row — never anything further back. That opens up a question:

OPTIONS:
[A] Keep the full 2D table
Leave it as-is. The full `(m+1) × (n+1)` table is O(mn) space but is clear and easy to debug — you can inspect any cell after the fact.

[B] Roll to two rows O(n)
```diff
+++ edit_distance.py
@@ -2,11 +2,11 @@
-    dp = [[0] * (n + 1) for _ in range(m + 1)]
-    for i in range(m + 1):
-        dp[i][0] = i
-    for j in range(n + 1):
-        dp[0][j] = j
+    prev = list(range(n + 1))
     for i in range(1, m + 1):
+        curr = [i] + [0] * n
         for j in range(1, n + 1):
-            if word1[i-1] == word2[j-1]:
-                dp[i][j] = dp[i-1][j-1]
+            if word1[i-1] == word2[j-1]:
+                curr[j] = prev[j-1]
             else:
-                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
-    return dp[m][n]
+                curr[j] = 1 + min(prev[j], curr[j-1], prev[j-1])
+        prev = curr
+    return prev[n]
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which would you go with?

### Student

I'll stick with **A** — keep the full 2D table.

Here's my thinking: the space optimization to two rows is clever, and I appreciate understanding *why* it works (we only need the previous row and current row). But for solving this problem right now, I want to make sure the solution is correct and easy to verify. The full table is O(mn) space, which is reasonable for most inputs, and it's much simpler to reason about and debug.

If I were optimizing for production or dealing with huge strings, then yes, the space-rolling optimization would make sense. But for learning the core algorithm, clarity matters more to me than shaving off a factor in space complexity.

Let me test the current solution with a few examples to make sure it works:

Should I trace through a simple case like `word1 = "horse"` and `word2 = "ros"` to verify the table fills correctly?

---

## Turn 4

### Tutor

Tutor: Fair call — clarity first, optimize when you have a reason to. Let's run it:

[Bash(cd / && python3 -c "
from edit_distance import min_distance

cases = [
    ('horse', 'ros', 3),
    ('intention', 'execution', 5),
    ('', '', 0),
    ('a', '', 1),
    ('', 'a', 1),
    ('abc', 'abc', 0),
    ('abc', 'axc', 1),
]
for w1, w2, expected in cases:
    result = min_distance(w1, w2)
    status = '✓' if result == expected else '✗'
    print(f'{status}  min_distance({w1!r}, {w2!r}) = {result}  (expected {expected})')
"
)]
  error: Exit code 1

[Bash(python3 -c "
from edit_distance import min_distance

cases = [
    ('horse', 'ros', 3),
    ('intention', 'execution', 5),
    ('', '', 0),
    ('a', '', 1),
    ('', 'a', 1),
    ('abc', 'abc', 0),
    ('abc', 'axc', 1),
]
for w1, w2, expected in cases:
    result = min_distance(w1, w2)
    status = '✓' if result == expected else '✗'
    print(f'{status}  min_distance({w1!r}, {w2!r}) = {result}  (expected {expected})')
"
)]
  ✓  min_distance('horse', 'ros') = 3  (expected 3)
  ✓  min_distance('intention', 'execution') = 5  (expected 5)
  ✓  min_distance('', '') = 0  (expected 0)
  ✓  min_distance('a', '') = 1  (expected 1)
  ✓  min_distance('', 'a') = 1  (expected 1)
  ✓  min_distance('abc', 'abc') = 0  (expected 0)
  ✓  min_distance('abc', 'axc') = 1  (expected 1)

Tutor: All green. Now let's trace `"horse" → "ros"` — here's the completed table (rows = `horse` prefixes, cols = `ros` prefixes):

```
      ""  r  o  s
  ""   0  1  2  3
   h   1  1  2  3
   o   2  2  1  2
   r   3  2  2  2
   s   4  3  3  2
   e   5  4  4  3
```

Read it as: `dp[i][j]` = cost to convert `word1[:i]` → `word2[:j]`.

- **Row 0 / Col 0**: base cases — pure insertions or deletions
- **`dp[2][2]` ("ho"→"ro")**: `o==o` match, inherit `dp[1][1]=1` for free
- **`dp[5][3]` ("horse"→"ros") = 3**: delete `h`, `r==r` free, `o==o` free, substitute `s`→`s` wait — actually: delete `h`, keep `or`, substitute `se`→`s`. The table finds the cheapest path automatically.

The bottom-right cell `dp[5][3] = 3` is your answer. Does the diagonal "free move" on matches make more sense now seeing it in action?

### Student

Yes, absolutely! Seeing it laid out like that really clarifies it. 

When I trace through `dp[2][2]` ("ho" → "ro"), the characters match (`o == o`), so we take `dp[1][1]` for free. That cell already represents the cost to convert "h" to "r" (which is 1 — one substitution). By matching the `o`s, we don't add any cost on top of that.

And then at `dp[5][3]` ("horse" → "ros"), the `3` comes from the algorithm automatically finding the cheapest sequence of operations — I don't have to trace it manually because the DP table has already solved all the subproblems optimally on the way down.

The key insight that clicked for me: **when characters match, the diagonal move is "free"** because those characters are already aligned and contribute nothing to the cost. The recurrence naturally finds the minimum cost path by always taking the cheapest of the three options (delete, insert, substitute) when they don't match.

The solution is working correctly on all the test cases. I think I've got a solid understanding of the algorithm now — the recurrence, why we branch on character match, and how the table builds up from base cases to the final answer.

<done/>

---

**Run end:** done after 4 turn(s) in 112.6s
