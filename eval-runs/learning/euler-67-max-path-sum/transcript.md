# euler-67-max-path-sum

- Source: `project-euler`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Output style: `Learning`
- Started: 2026-05-03T20:00:23.463Z

---

## Turn 1

**User:**

Project Euler #67: find the maximum top-to-bottom path sum through a triangle of numbers, where each step moves to an adjacent number on the row below. Use a small example triangle hard-coded inline (10 rows is fine).

**Pair:**

[Bash(python3 - <<'EOF'
# Project Euler #67: Maximum path sum through a triangle
# Strategy: dynamic programming, working bottom-up.
# Replace each cell with the best total reachable FROM that cell downward.

triangle = [
    [3],
    [7, 4],
    [2, 4, 6],
    [8, 5, 9, 3],
    [2, 4, 6, 8, 1],
    [5, 1, 7, 3, 9, 2],
    [4, 6, 8, 1, 5, 3, 7],
    [1, 3, 5, 7, 9, 2, 4, 6],
    [2, 4, 6, 8, 1, 3, 5, 7, 9],
    [6, 5, 7, 1, 8, 3, 9, 4, 2, 6],
]

# Work from the second-to-last row up to the apex.
# At each cell, add whichever of its two children is larger.
dp = [row[:] for row in triangle]   # deep copy so we don't mutate the input

for row in range(len(dp) - 2, -1, -1):
    for col in range(len(dp[row])):
        left  = dp[row + 1][col]
        right = dp[row + 1][col + 1]
        dp[row][col] += max(left, right)

print("Maximum path sum:", dp[0][0])
EOF
)]
  Maximum path sum: 67

Assistant: Here's the full solution with explanation:

```python
triangle = [
    [3],
    [7, 4],
    [2, 4, 6],
    [8, 5, 9, 3],
    [2, 4, 6, 8, 1],
    [5, 1, 7, 3, 9, 2],
    [4, 6, 8, 1, 5, 3, 7],
    [1, 3, 5, 7, 9, 2, 4, 6],
    [2, 4, 6, 8, 1, 3, 5, 7, 9],
    [6, 5, 7, 1, 8, 3, 9, 4, 2, 6],
]

dp = [row[:] for row in triangle]

for row in range(len(dp) - 2, -1, -1):
    for col in range(len(dp[row])):
        dp[row][col] += max(dp[row + 1][col], dp[row + 1][col + 1])

print(dp[0][0])  # 67
```

---

### How it works

The naive approach — trying every path — is exponential (2ⁿ paths for an *n*-row triangle). The key insight is that **optimal substructure** lets you collapse the whole search into one linear pass.

**Bottom-up DP:** Start at the second-to-last row and work upward. For each cell, replace its value with *"the best total I can achieve from here downward"*:

```
dp[row][col] += max(dp[row+1][col],   ← left child
                    dp[row+1][col+1]) ← right child
```

After the pass, `dp[0][0]` holds the answer — the apex now "knows" the best path through the entire triangle.

**Why this is efficient:**
| Approach | Complexity |
|---|---|
| Brute-force (try all paths) | O(2ⁿ) |
| Bottom-up DP | **O(n²)** — one pass over every cell |

Every cell is visited exactly once, and each visit does O(1) work. For the real Euler #67 (100-row triangle), brute force would need ~10³⁰ operations; DP handles it instantly.

---

## Turn 2 (final)

**User:**

Perfect! Your solution is **correct and efficient**. Let me walk through what makes it elegant:

### The Algorithm

Your code uses **bottom-up dynamic programming**. The genius move: instead of exploring every possible path (exponential), you *fold information upward* one row at a time.

**Step-by-step for your example:**
1. Start at row 8 (`[2, 4, 6, 8, 1, 3, 5, 7, 9]`) — these values don't change yet.
2. Move to row 7 and update each cell:
   - `dp[7][0] = 1 + max(2, 4) = 1 + 4 = 5`
   - `dp[7][1] = 3 + max(4, 6) = 3 + 6 = 9`
   - ...and so on.
3. By the time you reach the apex (row 0), `dp[0][0]` contains the complete answer: **67**.

Each cell now represents *"the maximum sum I can achieve from here to the bottom,"* without explicitly constructing paths.

### Why This Beats Brute Force

| Approach | Time | For 10 rows | For 100 rows |
|---|---|---|---|
| Try all paths | O(2ⁿ) | ~1000 ops | ~10³⁰ ops (impossible) |
| **Your DP** | **O(n²)** | **~100 ops** | **~10,000 ops** ✓ |

For Project Euler #67's full 100-row triangle, brute force would timeout; your solution handles it instantly.

### Code quality
✓ Space-efficient (reuses triangle structure)  
✓ Clear loop bounds (bottom-to-top with `range(len(dp) - 2, -1, -1)`)  
✓ Correct adjacent-child math (`[col]` and `[col + 1]`)

The solution is production-ready. Well done!

<done/>

---

**Run end**: done after 1 turn (43s)
