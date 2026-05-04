# leetcode-edit-distance

- Condition: `baseline`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T20:50:19

## Initial prompt

Let's solve Leetcode #72, 'Edit Distance'. Compute the minimum number of single-character insertions, deletions, or substitutions needed to convert one string into another.

---

## Turn 1

### Tutor

Thinking: The user wants to solve LeetCode #72 - Edit Distance. This is a classic dynamic programming problem. Let me solve it with a clear explanation.
  
  **Problem**: Given two strings `word1` and `word2`, return the minimum number of operations required to convert `word1` to `word2`. Operations allowed:
  - Insert a character
  - Delete a character
  - Replace a character
  
  **Approach**: Dynamic Programming
  
  Let `dp[i][j]` = minimum edit distance between `word1[0..i-1]` and `word2[0..j-1]`
  
  **Base Cases**:
  - `dp[0][j] = j` (insert j characters to build word2 from empty string)
  
  
  - `dp[i][0] = i` (delete i characters to get to empty string)
  
  **Recurrence**: When characters match, no operation is needed. When they don't, I take the minimum of three operations—substituting the character, deleting from word1, or inserting into word1—and add 1 to the cost. The final answer is the value at `dp[m][n]`.
  
  The time and space complexity are both O(m × n), though I can optimize the space down to O(n) using a rolling array approach. Now I'll implement this with a clean Python solution.

Tutor: ## Edit Distance — LeetCode #72

This is a classic **Dynamic Programming** problem. The key insight is to build up the solution from smaller subproblems.

### Intuition

Define `dp[i][j]` = minimum edits to convert `word1[0..i-1]` → `word2[0..j-1]`.

At each cell, we ask: *"what's the cheapest way to align these prefixes?"*

| Case | Meaning | Cost |
|------|---------|------|
| `word1[i-1] == word2[j-1]` | Characters match — do nothing | `dp[i-1][j-1]` |
| `dp[i-1][j-1]` | **Substitute** last char of word1 with last char of word2 | `1 + dp[i-1][j-1]` |
| `dp[i-1][j]` | **Delete** last char of word1 | `1 + dp[i-1][j]` |
| `dp[i][j-1]` | **Insert** last char of word2 into word1 | `1 + dp[i][j-1]` |

**Base cases:** `dp[i][0] = i` (delete all), `dp[0][j] = j` (insert all).

### Solution

```python
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)

    # dp[i][j] = edit distance between word1[:i] and word2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases: transforming to/from an empty string
    for i in range(m + 1):
        dp[i][0] = i   # delete i characters
    for j in range(n + 1):
        dp[0][j] = j   # insert j characters

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]          # free — chars match
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j - 1],  # substitute
                    dp[i - 1][j],      # delete from word1
                    dp[i][j - 1],      # insert into word1
                )

    return dp[m][n]
```

### Space-Optimized Version — O(n)

Since each row only depends on the **previous row**, we can use a rolling 1-D array:

```python
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    prev = list(range(n + 1))   # base case: dp[0][j] = j

    for i in range(1, m + 1):
        curr = [i] + [0] * n    # base case: dp[i][0] = i
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(prev[j - 1], prev[j], curr[j - 1])
        prev = curr

    return prev[n]
```

### Walkthrough — `"horse"` → `"ros"`

```
     ""  r  o  s
""  [ 0  1  2  3 ]
h   [ 1  1  2  3 ]
o   [ 2  2  1  2 ]
r   [ 3  2  2  2 ]
s   [ 4  3  3  2 ]
e   [ 5  4  4  3 ]
                ^--- answer = 3
```

`"horse"` → `"rorse"` (substitute h→r) → `"rose"` (delete r) → `"ros"` (delete e) = **3 ops**.

### Complexity

| | Time | Space |
|---|---|---|
| 2-D DP | O(m × n) | O(m × n) |
| Optimized | O(m × n) | **O(n)** |

### Student

Thanks for the clear walkthrough! I think I understand the intuition now. Let me make sure I've got it right:

- We build a table where each cell `dp[i][j]` represents the minimum edits needed to transform the first `i` characters of `word1` into the first `j` characters of `word2`.
- At each step, if the characters match, we don't need to do anything extra. Otherwise, we pick the cheapest of three operations: substitute, delete, or insert.

A couple of things I want to clarify before I try coding this myself:

1. **Why those three operations?** I see we're always comparing `word1[i-1]` with `word2[j-1]`. If they don't match, why exactly do substitute, delete, and insert represent all the options we have?

2. **The space-optimized version** — I see we're only keeping `prev` and `curr` rows. How do we know that's enough? Is it because each cell only looks at the previous row and the current row?

I want to make sure I understand *why* this works before I write the code, so when I encounter similar DP problems, I can reason through them myself.

---

## Turn 2

### Tutor

Thinking: The user wants a deeper conceptual explanation of two things:
  1. Why do substitute, delete, and insert cover all possible operations?
  2. Why is keeping just `prev` and `curr` rows sufficient for the space optimization?
  
  Let me think through these carefully to give a really clear, intuitive explanation.
  
  **Question 1: Why do those three operations cover all cases?**
  
  The key insight is about what `dp[i][j]` *means* and what the adjacent cells represent. When `word1[i-1] != word2[j-1]`, we need to make one more edit. The question is: what edit do we make, and what subproblem does that leave us with?
   
  At any position `(i, j)`, there are exactly three ways we could have arrived there. If we came from `dp[i-1][j-1]`, we're saying we already transformed the first `i-1` characters of word1 into the first `j-1` characters of word2, and now we substitute the mismatched character. If we came from `dp[i-1][j]`, we've already handled transforming the first `i-1` characters into all `j` characters of word2, so we delete the current character from word1. If we came from `dp[i][j-1]`, we've transformed the first `i` characters into the first `j-1` characters, so we insert the missing character from word2. These three transitions are exhaustive because they represent all the ways to build up a solution from smaller subproblems. from each string (word1[i-1] and word2[j-1]), delete consumes only from word1, and insert consumes only from word2 — these are the only three ways to advance through both strings.
  
  For the space optimization, the recurrence only depends on the previous row and the current row, so I only need to track two rows at a time instead of the entire DP table.

Tutor: Great questions — these are exactly the right things to pin down. Let me build up the intuition carefully for both.

---

## 1. Why do those three operations cover *everything*?

The key is to think about what each **neighboring cell** in the table *means*. When you're at `dp[i][j]` and the characters don't match, you're asking:

> *"What's the cheapest problem I could have already solved, plus one operation to finish?"*

There are exactly **three adjacent cells**, and each one corresponds to a different way of consuming the two strings:

```
dp[i-1][j-1]  dp[i-1][j]
dp[i  ][j-1]  dp[i  ][j]  ← computing this
```

| Previous state | Meaning | Operation to reach `(i,j)` |
|---|---|---|
| `dp[i-1][j-1]` | Aligned `word1[:i-1]` with `word2[:j-1]` | **Substitute** `word1[i-1]` → `word2[j-1]` |
| `dp[i-1][j]` | Aligned `word1[:i-1]` with `word2[:j]` | **Delete** `word1[i-1]` (it was "extra") |
| `dp[i][j-1]` | Aligned `word1[:i]` with `word2[:j-1]` | **Insert** `word2[j-1]` at the end |

Another way to see it — every operation **consumes characters** from one or both strings:

```
Substitute → advance both  i and j  (one char from each)
Delete     → advance only  i        (one char from word1)
Insert     → advance only  j        (one char from word2)
```

Those are the **only three ways** to move through the two strings. There's no fourth option. So the three cells are exhaustive — not by convention, but because they map 1-to-1 onto every possible move.

---

## 2. Why is keeping just `prev` + `curr` enough?

Look at the recurrence again and circle *which row each dependency lives in*:

```
dp[i][j] = 1 + min(
    dp[i-1][j-1],   ← row i-1  (previous)
    dp[i-1][j],     ← row i-1  (previous)
    dp[i][j-1],     ← row i    (current, already computed)
)
```

Every value in row `i` depends **only on row `i-1` and earlier values in row `i` itself** — never on row `i-2` or older. Visually:

```
Row i-2:  ░░░░░░░░░░  ← never touched again once row i-1 is built
Row i-1:  ▓▓▓▓▓▓▓▓▓▓  ← "prev" — read-only as we fill row i
Row i  :  ▓▓▓▓▓░░░░░  ← "curr" — built left to right
                 ^
                 filling this cell right now
```

Once you finish row `i`, row `i-1` is **dead weight** — nothing that comes after will ever look at it again. So you can discard it and promote `curr` → `prev`.

This is actually a general rule worth internalizing:

> **If `dp[i][j]` only depends on `dp[i-1][...]` and `dp[i][...]`, you can always compress to O(n) space by keeping one rolling row.**

---

## The mental model to carry forward

For any DP table problem, ask two questions:

1. **What does each cell *mean*?** (the subproblem definition)
2. **Which cells does it depend on?** (the recurrence shape)

The recurrence shape tells you both *why the formula is correct* (each neighbor = one valid prior state) and *how much space you actually need* (only keep the rows/columns you still read from).

Once you've answered those two questions for a new problem, the code almost writes itself.

### Student

Okay, that really clicks for me now. I see it — the three operations aren't arbitrary; they're the *only* three ways to progress through both strings. And the space optimization is just exploiting the fact that we only look back one row, so we can reuse memory.

Let me try implementing this myself now. I'll start with the 2-D version to be safe, and then maybe optimize if it feels natural:

```python
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    
    # dp[i][j] = min edits to convert word1[:i] to word2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    # Fill the table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                # Characters match, no operation needed
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # Take minimum of three operations
                dp[i][j] = 1 + min(
                    dp[i - 1][j - 1],  # substitute
                    dp[i - 1][j],      # delete
                    dp[i][j - 1]       # insert
                )
    
    return dp[m][n]
```

Let me test this mentally with the `"horse"` → `"ros"` example to make sure the logic is right:

- Base: row 0 is `[0, 1, 2, 3]`, column 0 is `[0, 1, 2, 3, 4, 5]`
- `dp[1][1]`: `'h'` vs `'r'` → don't match → `1 + min(0, 1, 1) = 1` ✓
- `dp[2][2]`: `'o'` vs `'o'` → match! → `dp[1][1] = 1` ✓
- Continue filling...
- `dp[5][3]` should be 3 ✓

Does this look right? Should I also write the space-optimized version, or is the 2-D version good enough to call this solved?

---

## Turn 3

### Tutor

Thinking: The user has implemented the 2-D version correctly and is asking:
  1. Does the implementation look right?
  2. Should they also write the space-optimized version?
  
  Their implementation is correct. Let me verify their mental walkthrough and give them honest feedback.
  
  Their code looks correct - it matches exactly what I explained earlier. The logic is right.
  
  For the question about whether to implement the space-optimized version: I should give them honest advice. The 2-D version is perfectly fine for an interview setting and is correct. The space-optimized version is a nice follow-up if the interviewer asks about it. I should encourage them to try it since they seem to understand the concept.
  
  
  Now I'm walking through their trace with the "horse" and "ros" example to verify the calculations are working as expected - checking the base cases and then spot-checking a couple of the DP transitions to make sure the recurrence relation is being applied correctly.
  
  Their solution is solid and ready for an interview, though I should mention that optimizing the space complexity down to O(n) is worth exploring since that's a common follow-up question. The tricky part with the space-optimized version is preserving the diagonal value before it gets overwritten during the computation. The two-array approach keeps things straightforward since we're not overwriting values we still need, whereas a single-array optimization would require saving the diagonal before it gets clobbered—worth understanding but not essential if the two-array version is already clear to you.

Tutor: Your implementation is **correct** — the logic, base cases, and recurrence all match perfectly. Your mental walkthrough is right too.

---

## Should you also write the space-optimized version?

**Short answer:** yes, and you're ready to — you already understand *why* it works, which is the hard part. The code is a small mechanical step from there.

Here's a good rule of thumb for interviews:

> Lead with the 2-D version, explain it clearly, then offer the optimization unprompted. It signals you understand the tradeoffs, not just the algorithm.

---

## One subtle gotcha to watch for

When you collapse to a single array and update **in-place**, the diagonal value `dp[i-1][j-1]` gets **overwritten** before you use it:

```python
# ⚠️ In-place update — diagonal is clobbered!
for j in range(1, n + 1):
    if word1[i-1] == word2[j-1]:
        dp[j] = dp[j-1]        # dp[j-1] is curr row, not prev!
    else:
        dp[j] = 1 + min(...)   # dp[j-1] was already updated this row
```

The two-array approach (`prev` / `curr`) sidesteps this entirely because you never mutate `prev` while reading it. If you ever want to do it with **one array**, you just need to save the diagonal before overwriting it:

```python
prev_diag = dp[j - 1]   # save before it's overwritten
dp[j] = ...             # now safe to update
```

---

## Your implementation is interview-ready as-is

To summarize what you got right:

| | Your Code |
|---|---|
| Subproblem definition | ✅ `dp[i][j]` = min edits for `word1[:i]` → `word2[:j]` |
| Base cases | ✅ Row 0 and col 0 filled correctly |
| Match branch | ✅ Free diagonal carry |
| Mismatch branch | ✅ `1 + min` of all three neighbors |
| Return value | ✅ `dp[m][n]` |

Go ahead and try the space-optimized version — given that you can already explain *why* two rows suffice, the code will feel straightforward.

### Student

Thanks! I feel confident about the 2-D version, and I want to solidify my understanding by writing the space-optimized one. Let me give it a shot:

```python
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    
    # prev = previous row (dp[i-1])
    prev = list(range(n + 1))
    
    for i in range(1, m + 1):
        # curr = current row (dp[i])
        curr = [i] + [0] * n
        
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(
                    prev[j - 1],  # substitute
                    prev[j],      # delete
                    curr[j - 1]   # insert
                )
        
        # Slide rows forward
        prev = curr
    
    return prev[n]
```

I think I've got it. The key is:
- `prev[j-1]` gives us the diagonal from the previous row (before it gets overwritten)
- `prev[j]` gives us the cell directly above
- `curr[j-1]` gives us the cell to the left in the current row (which we've already computed)

Then at the end, `prev` points to the last row we computed, so `prev[n]` is our answer.

Is this correct? And does this feel like a natural stopping point for the problem, or is there something else I should explore?

---

## Turn 4

### Tutor

Thinking: The user's space-optimized implementation is correct. Let me verify it:
  
  1. `prev = list(range(n + 1))` - initializes the base case row 0: [0, 1, 2, ..., n] ✓
  2. For each row `i`, `curr = [i] + [0] * n` - sets the base case dp[i][0] = i ✓
  3. `prev[j-1]` = dp[i-1][j-1] (diagonal) ✓ - because prev is the previous row and we haven't modified it
  
  
  4. `prev[j]` = dp[i-1][j] (above) ✓
  5. `curr[j-1]` = dp[i][j-1] (left) ✓ - already computed in this row iteration
  6. `prev = curr` slides the window forward ✓
  7. Returns `prev[n]` which is dp[m][n] ✓
  
  The explanation of the key points is solid. For additional exploration, I could mention edge cases like empty strings—though those are already handled by the base cases—or an early exit optimization if one string is empty, which would just return the length of the other string.
  
  There's also the option of choosing which dimension to iterate over based on the shorter string to minimize memory usage, or exploring the recursive top-down memoization approach as an alternative way to think about the same problem. The code is correct and this feels like a natural stopping point, but I can point out what deeper exploration would look like if they want to go further.

Tutor: Your implementation is **exactly right**, and your explanation of the three references is spot-on. This is a natural stopping point — you've gone from understanding the intuition, to the 2-D solution, to the space-optimized version, and you can explain *why* each step works. That's the full picture.

---

## One last micro-optimization worth knowing

You can guarantee the rolling array is always sized by the **shorter** string by swapping if necessary. This doesn't change the worst case, but it's a clean habit:

```python
def minDistance(word1: str, word2: str) -> int:
    # Always iterate over the longer string, roll over the shorter one
    if len(word1) < len(word2):
        word1, word2 = word2, word1

    m, n = len(word1), len(word2)
    prev = list(range(n + 1))

    for i in range(1, m + 1):
        curr = [i] + [0] * n
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(prev[j - 1], prev[j], curr[j - 1])
        prev = curr

    return prev[n]
```

Space is now `O(min(m, n))` instead of `O(n)` — a small but genuine improvement when the strings differ a lot in length.

---

## If you want to go further

Edit Distance sits at the center of a family of DP problems. Here's a map of where to go next, roughly in order of difficulty:

| Problem | How it connects |
|---|---|
| **LC #1143** Longest Common Subsequence | The "free diagonal" in Edit Distance is essentially LCS — characters that don't need to be edited |
| **LC #583** Delete Operations for Two Strings | Edit distance with only deletions allowed — reduces to `m + n - 2*LCS` |
| **LC #712** Minimum ASCII Delete Sum | Same structure, but weighted by character values instead of counting ops |
| **LC #115** Distinct Subsequences | Same 2-D table shape, different recurrence — good stress test |

The pattern to look for in all of them: *two sequences, choices at each cell that reduce to smaller subproblems*. Once you can draw the table and name what each cell means, the recurrence usually follows directly.

### Student

Thank you for that context! I appreciate the roadmap — it's helpful to know where these patterns show up again. That said, I want to stay focused on nailing this one problem rather than branch out to others right now.

I'm satisfied with my solution. I understand:
- **Why** the three operations are the only possibilities (they're the only ways to progress through both strings)
- **Why** the recurrence works (each cell picks the cheapest prior state + one operation)
- **Why** we can optimize to O(n) space (we only ever look back one row)
- **How** to implement both versions clearly

The code is correct, I've traced through the example, and I feel confident I could explain or debug this in an interview. This feels like a natural place to wrap up.

<done/>

---

**Run end:** done after 4 turn(s) in 106.9s
