# leetcode-edit-distance

- Source: `leetcode`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T05:18:47.557Z

---

## Turn 1

**User:**

Let's solve Leetcode #72, 'Edit Distance'. Compute the minimum number of single-character insertions, deletions, or substitutions needed to convert one string into another.

**Pair:**

Assistant: Classic DP problem — let's build it up carefully. The key insight is defining what `dp[i][j]` means: **the edit distance between the first `i` chars of `word1` and the first `j` chars of `word2`**.

Before writing any code, let's nail the recurrence. When `word1[i-1] != word2[j-1]`, we pick the cheapest of the three operations. Which recurrence is right?

Assistant: No tool available, so I'll just lay it out directly and ask you.

When characters **don't** match, consider these two options for the recurrence:

---

**Option A**
```python
dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1])
```

**Option B**
```python
dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
```

---

Which do you think is correct, and can you say what each sub-expression (`dp[i-1][j]`, `dp[i][j-1]`, `dp[i-1][j-1]`) represents in terms of the three edit operations?

---

## Turn 2

**User:**

Option B is correct.

Here's my reasoning:

- `dp[i-1][j-1] + 1` = **replace** `word1[i-1]` with `word2[j-1]`. We've already solved the subproblem for the first i-1 and j-1 characters, so now we just swap the mismatched character.
- `dp[i-1][j] + 1` = **delete** from `word1`. We've transformed the first i-1 chars of word1 into the first j chars of word2, so now we delete the i-th character.
- `dp[i][j-1] + 1` = **insert** into `word1`. We've transformed the first i chars of word1 into the first j-1 chars of word2, so now we insert the j-th character.

Option A misses the replace operation (`dp[i-1][j-1]`), which means it would only use insertions and deletions. That's suboptimal — sometimes a single replacement is cheaper than delete + insert.

Ready to code this up?

**Pair:**

Assistant: Exactly right — A would always pay 2 ops (delete + insert) for a mismatch even when 1 substitution suffices. Perfect reasoning.

Let's build it. I'll start with the 2D DP solution:

[Bash(ls edit_distance.py 2>/dev/null && echo exists || echo missing)]
  missing

[Write(edit_distance.py)]
def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    # dp[i][j] = edit distance between word1[:i] and word2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases: transforming to/from empty string
    for i in range(m + 1):
        dp[i][0] = i  # delete all i chars
    for j in range(n + 1):
        dp[0][j] = j  # insert all j chars

    for i in range(1, m + 1):
… (26 more lines)

[Bash(python edit_distance.py)]
  error: Exit code 127

[Bash(python3 edit_distance.py)]
  ✓ min_distance('horse', 'ros') = 3  (expected 3)
  ✓ min_distance('intention', 'execution') = 5  (expected 5)
  ✓ min_distance('', 'abc') = 3  (expected 3)
  ✓ min_distance('abc', 'abc') = 0  (expected 0)
  ✓ min_distance('a', 'b') = 1  (expected 1)

Assistant: All green. This runs in **O(m·n)** time and **O(m·n)** space. 

Now — notice that each row `dp[i]` only ever looks at the *previous* row `dp[i-1]`. That means we should be able to compress this to a single 1D array and get **O(n)** space. Here's the question: when you collapse to one row and compute left-to-right, there's a subtle hazard. Which of these is the correct in-place update?

---

**Option A**
```diff
+++ edit_distance.py
@@ -1,0 +1,12 @@
+def min_distance_opt(word1: str, word2: str) -> int:
+    m, n = len(word1), len(word2)
+    dp = list(range(n + 1))
+    for i in range(1, m + 1):
+        dp[0] = i
+        for j in range(1, n + 1):
+            if word1[i-1] == word2[j-1]:
+                dp[j] = dp[j-1]
+            else:
+                dp[j] = 1 + min(dp[j], dp[j-1], dp[j])
+    return dp[n]
```

**Option B**
```diff
+++ edit_distance.py
@@ -1,0 +1,14 @@
+def min_distance_opt(word1: str, word2: str) -> int:
+    m, n = len(word1), len(word2)
+    dp = list(range(n + 1))
+    for i in range(1, m + 1):
+        prev = dp[0]
+        dp[0] = i
+        for j in range(1, n + 1):
+            temp = dp[j]
+            if word1[i-1] == word2[j-1]:
+                dp[j] = prev
+            else:
+                dp[j] = 1 + min(dp[j], dp[j-1], prev)
+            prev = temp
+    return dp[n]
```

---

What's the flaw in the wrong option?

---

## Turn 3

**User:**

Option B is correct.

The flaw in **Option A** is subtle but critical: look at the else branch:
```python
dp[j] = 1 + min(dp[j], dp[j-1], dp[j])
```

You have `dp[j]` **twice** in the min. That means you're effectively computing:
```python
dp[j] = 1 + min(dp[j], dp[j-1])
```

You've lost the replacement operation (the diagonal `dp[i-1][j-1]`), just like in the first question. It only considers delete and insert — exactly the suboptimal approach we rejected before.

**Option B** uses a `prev` variable to track the diagonal value as it iterates:
- `temp = dp[j]` saves the old value (from the previous row, which becomes the diagonal for the next column)
- `prev` represents `dp[i-1][j-1]` 
- When we compute `1 + min(dp[j], dp[j-1], prev)`, we have all three operations: delete, insert, and replace
- `prev = temp` updates the diagonal tracker for the next iteration

This correctly maintains the diagonal reference while updating in-place. Nice catch with the redundant `dp[j]` — that's exactly the kind of bug that would silently give wrong answers.

Ready to add the optimized version to the file?

**Pair:**

Assistant: Spot on — `min(dp[j], dp[j-1], dp[j])` silently drops the diagonal, giving you the exact same bug as Option A in the first question. Easy to miss in a code review.

Let me apply Option B:

[Read(edit_distance.py)]
  1	def min_distance(word1: str, word2: str) -> int:
  2	    m, n = len(word1), len(word2)
  3	    # dp[i][j] = edit distance between word1[:i] and word2[:j]
  4	    dp = [[0] * (n + 1) for _ in range(m + 1)]
  5	
  6	    # Base cases: transforming to/from empty string
  7	    for i in range(m + 1):
  8	        dp[i][0] = i  # delete all i chars
  9	    for j in range(n + 1):
  10	        dp[0][j] = j  # insert all j chars
  11	
  12	    for i in range(1, m + 1):
  … (26 more lines)

[Edit(edit_distance.py)]
--- before
if __name__ == "__main__":
    cases = [
        ("horse", "ros", 3),
        ("intention", "execution", 5),
        ("", "abc", 3),
        ("abc", "abc", 0),
        ("a", "b", 1),
    ]
    for w1, w2, expected in cases:
        result = min_distance(w1, w2)
        status = "✓" if result == expected else "✗"
        print(f"{status} min_distance({w1!r}, {w2!r}) = {result}  (expected {expected})")
--- after
def min_distance_opt(word1: str, word2: str) -> int:
    """Space-optimized O(n) version using a single row."""
    m, n = len(word1), len(word2)
    dp = list(range(n + 1))  # base case: dp[j] = j
    for i in range(1, m + 1):
        prev = dp[0]   # holds dp[i-1][j-1] (diagonal) before it's overwritten
        dp[0] = i      # base case: dp[i][0] = i
        for j in range(1, n + 1):
            temp = dp[j]  # save before overwrite; becomes prev (diagonal) next iteration
            if word1[i - 1] == word2[j - 1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(
                    prev,     # substitute  (dp[i-1][j-1])
                    dp[j],    # delete      (dp[i-1][j])
                    dp[j-1],  # insert      (dp[i][j-1])
                )
            prev = temp
    return dp[n]


if __name__ == "__main__":
    cases = [
        ("horse", "ros", 3),
        ("intention", "execution", 5),
        ("", "abc", 3),
        ("abc", "abc", 0),
        ("a", "b", 1),
    ]
    for w1, w2, expected in cases:
        r1 = min_distance(w1, w2)
        r2 = min_distance_opt(w1, w2)
        status = "✓" if r1 == r2 == expected else "✗"
        print(f"{status} ({w1!r}, {w2!r}) 2D={r1}  1D={r2}  expected={expected}")

[Bash(python3 edit_distance.py)]
  ✓ ('horse', 'ros') 2D=3  1D=3  expected=3
  ✓ ('intention', 'execution') 2D=5  1D=5  expected=5
  ✓ ('', 'abc') 2D=3  1D=3  expected=3
  ✓ ('abc', 'abc') 2D=0  1D=0  expected=0
  ✓ ('a', 'b') 2D=1  1D=1  expected=1

Assistant: Both match on all cases. Here's the final complexity picture:

| | Time | Space |
|---|---|---|
| 2D DP | O(m·n) | O(m·n) |
| 1D DP | O(m·n) | **O(n)** |

The `prev` variable is doing real work — it's the only thing standing between you and silently re-using `dp[i][j-1]` instead of `dp[i-1][j-1]` for the substitute case. That's a gotcha that bites a lot of people when they first try to optimize this problem.

---

## Turn 4 (final)

**User:**

Perfect summary. This is a classic DP problem where the space optimization is elegant but demands care — one wrong index and the substitution cost disappears silently. You nailed both the conceptual structure (why the diagonal matters) and the implementation detail (why `prev` is necessary).

Both versions handle all edge cases correctly: empty strings, identical strings, single characters, and real work. The 2D version is clearer for interviews; the 1D version shows you understand the recurrence deeply enough to recognize what data you actually need to keep around.

<done/>

---

**Run end**: done after 3 turns (125s)
