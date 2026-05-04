# euler-67-max-path-sum

- Source: `project-euler`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:32:11.421Z

---

## Turn 1

**User:**

Project Euler #67: find the maximum top-to-bottom path sum through a triangle of numbers, where each step moves to an adjacent number on the row below. Use a small example triangle hard-coded inline (10 rows is fine).

**Pair:**

[Bash(python3 - <<'EOF'
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

# Bottom-up DP: collapse each row into the one above it,
# keeping only the best reachable sum at each position.
dp = triangle[-1][:]                          # start with the bottom row

for row in reversed(triangle[:-1]):           # walk upward
    dp = [cell + max(dp[i], dp[i + 1])
          for i, cell in enumerate(row)]

print(f"Maximum path sum: {dp[0]}")
EOF
)]
  Maximum path sum: 696

Assistant: **Maximum path sum: 696**

Here's how it works:

### Algorithm — bottom-up dynamic programming

Instead of trying every path (2⁹ = 512 for 10 rows, but 2⁹⁹ for the real puzzle!), we work **upward** from the last row. At each position we keep only the best total reachable from that cell downward, then discard everything below.

```
Row 9  (bottom):  41 48 72 33 47 32 37 16 94 29   ← start here

Row 8:  each cell + max of its two neighbours below
        41+max(41,48)  41+max(48,72)  26+max(72,33) …  33+max(94,29)
      = 89  113  98  89 130  72 117 164  127

…keep collapsing upward one row at a time…

Row 0 (top):  single number → answer
```

### Why it's correct

Each `dp[i]` after processing a row represents **"the best sum you can achieve starting at position i in this row and walking to the bottom."** When we reach the apex there's only one cell — that's the global answer.

### Time & space complexity

| | |
|---|---|
| **Time** | O(n²) — one pass per row |
| **Space** | O(n) — one 1-D array, reused in place |

For the real Project Euler #67 (100-row triangle from a file) you'd just swap in the file-loaded data; the algorithm is identical and runs in microseconds.

---

## Turn 2 (final)

**User:**

Nice solution! You've nailed the key insight: **work backwards from the bottom**.

Let me trace through your logic once more to validate:

1. Start with `dp = [41, 48, 72, 33, 47, 32, 37, 16, 94, 29]` (row 9)
2. For row 8 `[41, 41, 26, 56, 83, 40, 80, 70, 33]`:
   - Position 0: `41 + max(41, 48) = 41 + 48 = 89`
   - Position 1: `41 + max(48, 72) = 41 + 72 = 113`
   - ...and so on
3. Continue upward until only one cell remains

The **beauty** of this approach:
- ✓ No recursion overhead or memoization dict
- ✓ Reuses the same array (O(n) space, not O(n²))
- ✓ Scales trivially to 100 rows (Project Euler's real #67)

For the actual puzzle you'd load the 100-row triangle from the data file and run the exact same algorithm—the time complexity is negligible. Well done! 

<done/>

---

**Run end**: done after 1 turn (38s)
