# leetcode-edit-distance

- Condition: `learning`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:04:47

## Initial prompt

Let's solve Leetcode #72, 'Edit Distance'. Compute the minimum number of single-character insertions, deletions, or substitutions needed to convert one string into another.

---

## Turn 1

### Tutor

Thinking: The user wants to solve Leetcode #72 - Edit Distance. This is a classic dynamic programming problem. Let me explain and implement it clearly.
  
  The problem: Given two strings `word1` and `word2`, return the minimum number of operations (insert, delete, substitute a single character) to convert `word1` into `word2`.
  
  **Approach: Dynamic Programming**
  
  We build a 2D DP table where `dp[i][j]` = minimum edit distance between `word1[0..i-1]` and `word2[0..j-1]`.
  
  
  The base cases initialize the table: when one string is empty, the distance is just the length of the other string. For the recurrence relation, if characters match, we take the previous diagonal value without adding any cost. Otherwise, we take the minimum of three operations—substitution, deletion, or insertion—and add one to the cost.
  
  Now I'm writing clean Python code to implement this edit distance algorithm.

Tutor: ## Leetcode #72 — Edit Distance

### The Core Insight

Think of building a **2D DP table** where `dp[i][j]` = the minimum edits to convert `word1[:i]` → `word2[:j]`.

Every cell answers: *"What's the cheapest way to align the first `i` chars of word1 with the first `j` chars of word2?"*

---

### The Recurrence

```
If word1[i-1] == word2[j-1]:          # characters match — free!
    dp[i][j] = dp[i-1][j-1]

Else:                                  # pick the cheapest of 3 ops:
    dp[i][j] = 1 + min(
        dp[i-1][j-1],   # ← substitute  (align both, pay 1)
        dp[i-1][j],     # ← delete      (shrink word1, pay 1)
        dp[i][j-1]      # ← insert      (shrink word2, pay 1)
    )
```

### Table Walkthrough — `"horse"` → `"ros"`

```
      ""  r  o  s
  ""  0   1  2  3   ← base case: insert j chars
  h   1   1  2  3
  o   2   2  1  2
  r   3   2  2  2
  s   4   3  3  2
  e   5   4  4  3   ← answer: dp[5][3] = 3
```

---

### Implementation

```python
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)

    # dp[i][j] = min edits to convert word1[:i] -> word2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # ── Base cases ──────────────────────────────────────────
    for i in range(m + 1):
        dp[i][0] = i          # delete all i chars from word1
    for j in range(n + 1):
        dp[0][j] = j          # insert all j chars from word2

    # ── Fill table ──────────────────────────────────────────
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i-1][j-1]          # chars match: free ride
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j-1],   # substitute
                    dp[i-1][j],     # delete  from word1
                    dp[i][j-1],     # insert  into word1
                )

    return dp[m][n]


# ── Tests ────────────────────────────────────────────────────
assert minDistance("horse", "ros")    == 3   # horse→rorse→rose→ros
assert minDistance("intention", "execution") == 5
assert minDistance("", "abc")         == 3   # 3 insertions
assert minDistance("abc", "")         == 3   # 3 deletions
assert minDistance("abc", "abc")      == 0   # identical
assert minDistance("a", "b")          == 1   # 1 substitution
print("All tests passed ✓")
```

---

### Space-Optimized Version — O(n) Space

Since each row only looks at the **previous row**, you only need two 1D arrays (or one, with a rolling variable):

```python
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    prev = list(range(n + 1))          # represents dp[i-1][*]

    for i in range(1, m + 1):
        curr = [i] + [0] * n           # curr[0] = i (delete i chars)
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(prev[j-1], prev[j], curr[j-1])
        prev = curr

    return prev[n]
```

---

### Complexity

| Version | Time | Space |
|---|---|---|
| 2D DP | O(m × n) | O(m × n) |
| Space-optimized | O(m × n) | **O(n)** |

---

### Key Mental Model

| `dp[i-1][j-1]` | `dp[i-1][j]` | `dp[i][j-1]` |
|---|---|---|
| **Substitute** the i-th char | **Delete** from word1 | **Insert** into word1 |
| Diagonal ↖ | Up ↑ | Left ← |

Every cell picks the cheapest of its three neighbors, plus 1 — unless the characters already match (then borrow the diagonal for free). 🎯

### Student

Thanks for walking me through this! I can see the intuition now—building up from smaller subproblems and always picking the cheapest operation at each step.

Let me make sure I understand the recurrence by tracing through a small example myself. For `"horse"` → `"ros"`, when we hit `dp[2][2]` (comparing `"ho"` to `"ro"`):
- `word1[1]` is `'o'` and `word2[1]` is `'o'`, so they match
- We take `dp[1][1]` for free, which is `1` (the cost of converting `"h"` to `"r"`)
- So `dp[2][2] = 1` ✓

And then at `dp[4][3]` (comparing `"hors"` to `"ros"`):
- `word1[3]` is `'s'` and `word2[2]` is `'s'`, they match
- We take `dp[3][2] = 2` for free
- So `dp[4][3] = 2` ✓

That makes sense. The key insight is: **when characters match, we just inherit the cost from the diagonal without paying anything extra, because that alignment was already "optimal" for the smaller problem.**

Before I implement, one clarification: in the three operations (substitute, delete, insert), am I thinking about them correctly?
- **Substitute**: we fix one char in word1, move both pointers right → `dp[i-1][j-1] + 1`
- **Delete**: we remove a char from word1, move only word1's pointer → `dp[i-1][j] + 1`
- **Insert**: we add a char to word1 (to match word2), move only word2's pointer back → `dp[i][j-1] + 1`

Is that the right mental model?

---

## Turn 2

### Tutor

Thinking: The user is asking for confirmation of their mental model about the three operations in the edit distance DP. Let me think about this carefully.
  
  They're asking about:
  - **Substitute**: `dp[i-1][j-1] + 1` — fix one char in word1, move both pointers → correct
  - **Delete**: `dp[i-1][j] + 1` — remove a char from word1, move only word1's pointer → correct
  - **Insert**: `dp[i][j-1] + 1` — add a char to word1, move only word2's pointer back → correct
  
  Their mental model is exactly right. Let me explain this clearly.
  
  
  For delete, we're looking at `dp[i-1][j]`, which represents having already processed `i-1` characters of word1 and all `j` characters of word2—so we delete the current character from word1 and move forward. For insert, `dp[i][j-1]` means we've processed all `i` characters of word1 but only `j-1` of word2, so we insert the missing character from word2 to match. Both framings work equally well — whether I think of it as moving only word2's pointer or as satisfying word2's j-th character with an insertion at position i, the logic is the same. Now I want to create a visualization that shows what each operation actually does to the remaining subproblem.

Tutor: Yes — your mental model is **exactly right**. The pointer framing is the cleanest way to think about it.

Here's a slightly sharper way to state each one, which makes the pointer movement feel *inevitable* rather than memorized:

---

### Why Each Pointer Moves That Way

Each operation answers: *"What smaller subproblem am I reducing to?"*

```
dp[i][j]: converting word1[:i] → word2[:j]

┌──────────────┬──────────────────────────────────────────┬──────────────────┐
│  Operation   │  What you do                             │  Reduces to      │
├──────────────┼──────────────────────────────────────────┼──────────────────┤
│  Substitute  │  Replace word1[i-1] with word2[j-1]      │  dp[i-1][j-1]    │
│              │  → both chars are now "consumed"         │  (diagonal)      │
├──────────────┼──────────────────────────────────────────┼──────────────────┤
│  Delete      │  Remove word1[i-1] entirely              │  dp[i-1][j]      │
│              │  → word1 shrinks, word2 unchanged        │  (up)            │
├──────────────┼──────────────────────────────────────────┼──────────────────┤
│  Insert      │  Insert word2[j-1] into word1            │  dp[i][j-1]      │
│              │  → that word2 char is now matched,       │  (left)          │
│              │     word1 unchanged                      │                  │
└──────────────┴──────────────────────────────────────────┴──────────────────┘
```

The insert one trips people up the most, so it's worth dwelling on:

> *"I insert `word2[j-1]` at the end of `word1[:i]`. That character is now perfectly matched — so I've fully handled the `j`-th character of `word2`. But I haven't touched any of `word1`, so I still need to convert the full `word1[:i]` into the remaining `word2[:j-1]`."*

That's why only word2's pointer moves: you satisfied a word2 character without spending any of word1.

---

### A Unified Way to Remember All Three

```
         word2 pointer
              ↓
    j-1       j
i-1  [sub]  [del]    ← word1 pointer
 i   [ins]  [?]  ← we're filling this cell
```

- **Diagonal** (↖): both chars consumed → substitute
- **Up** (↑): only word1 char consumed → delete it
- **Left** (←): only word2 char consumed → insert to match it

Once you see the table geometrically, the recurrence is just reading off the three neighbors. You've got it. ✓

### Student

Ah, that really clicks now! The geometric intuition makes it much clearer—each direction on the table tells you which pointer(s) moved.

I especially like how you framed the insert case: *"I've satisfied a word2 character without touching word1, so word1's pointer stays put."* That's way more intuitive than trying to memorize "left = insert."

Okay, I'm ready to code this up. Let me implement the 2D version first to make sure I have it right, then I can test it:

```python
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    
    # dp[i][j] = min edits to convert word1[:i] -> word2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases
    for i in range(m + 1):
        dp[i][0] = i  # delete all i chars
    for j in range(n + 1):
        dp[0][j] = j  # insert all j chars
    
    # Fill the table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # free match
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j - 1],  # substitute
                    dp[i - 1][j],      # delete
                    dp[i][j - 1]       # insert
                )
    
    return dp[m][n]


# Test it
print(minDistance("horse", "ros"))        # expect 3
print(minDistance("intention", "execution"))  # expect 5
print(minDistance("", "abc"))             # expect 3
print(minDistance("abc", ""))             # expect 3
print(minDistance("abc", "abc"))          # expect 0
print(minDistance("a", "b"))              # expect 1
```

Let me trace through one more time to be confident: for `"horse"` → `"ros"`, I start with base cases filled, then build up row by row. When I hit matching characters like `'o'` and `'s'`, I borrow the diagonal cost. When they don't match, I pick the minimum of the three neighbors plus 1.

Does this look correct to you? Once I verify it works on the test cases, I think I'll be done.

<done/>

---

**Run end:** done after 2 turn(s) in 52.5s
