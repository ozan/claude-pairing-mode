# euler-15-lattice-paths

- Source: `project-euler`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Output style: `Learning`
- Started: 2026-05-03T20:00:02.138Z

---

## Turn 1

**User:**

Project Euler #15: how many distinct routes are there through a 20×20 grid moving only right or down? Closed-form is fine but discuss the DP path too.

**Pair:**

Assistant: ## Lattice Paths Through a 20×20 Grid

### Framing the problem

A 20×20 grid has **21 × 21 = 441 lattice points**. You travel from the top-left (0, 0) to the bottom-right (20, 20). Every valid path is exactly **40 steps**: 20 right (R) and 20 down (D), in any order.

---

### The DP path

Define `dp[i][j]` = number of distinct paths to reach point (i, j).

```
Base cases:   dp[0][j] = 1   (only one way along the top edge: all R)
              dp[i][0] = 1   (only one way along the left edge: all D)

Recurrence:   dp[i][j] = dp[i-1][j]   ← arrived from above
                        + dp[i][j-1]   ← arrived from the left
```

For a 4×4 corner of the table:

```
  j=0  j=1  j=2  j=3
i=0 [1]  [1]  [1]  [1]
i=1 [1]  [2]  [3]  [4]
i=2 [1]  [3]  [6]  [10]
i=3 [1]  [4]  [10] [20]
```

**Key observation:** each cell is C(i+j, i) — this table *is* Pascal's triangle, rotated 45°. So `dp[i][j] = C(i+j, i)`, and the DP and closed-form converge to the same place.

---

### Closed-form

A path is completely determined by choosing *which 20 of the 40 steps are R* (the remaining 20 are D):

$$\text{Answer} = \binom{40}{20} = \frac{40!}{20! \cdot 20!}$$

Computing step-by-step (each intermediate value stays an integer):

| Step | Value |
|------|-------|
| C(2,1) | 2 |
| C(4,2) | 6 |
| C(6,3) | 20 |
| C(10,5) | 252 |
| C(20,10) | 184,756 |
| C(30,15) | 155,117,520 |
| C(38,19) | 35,345,263,800 |
| **C(40,20)** | **137,846,528,820** |

Each step uses: C(2n, n) = C(2n−2, n−1) × (2n)(2n−1) / n².

---

### Why they're the same

The recurrence `dp[i][j] = dp[i−1][j] + dp[i][j−1]` is **Pascal's identity**:

$$\binom{i+j}{i} = \binom{(i-1)+j}{i-1} + \binom{i+(j-1)}{i}$$

So both approaches are literally computing the same object — Pascal's triangle — one by filling a 2D table, the other by formula.

---

### Answer

$$\boxed{137{,}846{,}528{,}820}$$

---

## Turn 2

**User:**

Great explanation! Now let me provide working implementations of both approaches so you can see them in action:

**Python (combinatorial proof):**

```python
from math import comb

# Closed-form: choose 20 steps to be "right" out of 40 total steps
answer = comb(40, 20)
print(f"C(40,20) = {answer}")
```

**Python (DP):**

```python
def lattice_paths_dp(n):
    """Paths through an n×n grid (n+1)×(n+1) lattice points."""
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    
    # Base cases: single row/column
    for i in range(n + 1):
        dp[i][0] = 1
        dp[0][i] = 1
    
    # Fill table
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    
    return dp[n][n]

print(f"DP approach: {lattice_paths_dp(20)}")
```

Both should output **137,846,528,820**.

---

### The teaching moment

Notice the **asymptotic difference**:
- **Closed-form:** O(1) time if you have `comb()` (or O(n) with naive division), O(1) space
- **DP:** O(n²) time and space, but you get the *entire path-count table* as a bonus—you can answer "how many paths to (5,7)?" instantly

For a 20×20 grid, DP uses ~400 integers (one 21×21 array). For a 100×100 grid, it's still just 101²; the closed-form never scales worse. But DP teaches you **memoization** and **optimal substructure** in a way that clicking a formula button doesn't.

**Would you like me to:**
1. Implement these in the TUI to see them side-by-side with didactic options?
2. Add visualization (maybe animate a random valid path)?
3. Move on to another Euler problem?

**Pair:**

Assistant: Both implementations are correct — a quick sanity check on the DP code before accepting it:

- `dp[i][0] = dp[0][i] = 1` ✓ (edges have exactly one route)
- `dp[i][j] = dp[i-1][j] + dp[i][j-1]` ✓ (Pascal's identity)
- Returns `dp[n][n]` = `dp[20][20]` ✓

One refinement worth knowing: the 2D DP can be collapsed to **O(n) space** since row `i` only reads row `i-1`:

```python
def lattice_paths_dp_1d(n):
    row = [1] * (n + 1)          # represents the top edge (all 1s)
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            row[j] += row[j-1]   # row[j] was dp[i-1][j]; row[j-1] is dp[i][j-1]
    return row[n]
```

Each pass over `row` simulates one new grid row in-place. Same answer, 21 integers instead of 441.

---

On your three options:

**Option 3** (next Euler problem) is the most pedagogically natural continuation — the techniques here generalize immediately. Good candidates that build directly on this:

| Problem | Connection |
|---------|-----------|
| **#14** (Collatz) | DP/memoization, no closed-form |
| **#18/#67** (Triangle sum) | 2D DP on a DAG, optimal substructure |
| **#31** (Coin sums) | Unbounded knapsack, same recurrence shape |

**#18** is especially satisfying because it *looks* like it wants brute force (2^64 paths for #67) but the same "paths through a grid" intuition from this problem kills it in O(n²).

Which direction interests you?

---

## Turn 3 (final)

**User:**

**Euler #15 is fully solved.** Both implementations verified, answer confirmed, teaching moment nailed. ✓

---

On direction: I'd lean toward **#18 (Maximum path sum triangle)** as the next problem.

Here's why it's the best pedagogical follow-up:

- **Same DP structure** as what we just built (2D grid → recurrence), but the *framing* is inverted: instead of "count paths," it's "maximize path weight." The recurrence morphs from addition to max, which teaches you that DP isn't about the operator—it's about **optimal substructure**.
- **Dramatic payoff:** brute force would try 2^100+ paths; DP solves it in O(n²) with a trivial inner loop.
- **Reading problem is faster than #14** (which requires memoizing Collatz sequence checks).

#18 is a 15-line problem but teaches the *generality* of what we just did in a way that makes you actually *use* the pattern, not just recognize it.

That said, if you want to dogfood the TUI for teaching—build #15 or #18 with the two-option interface—that's also compelling (showcasing the project itself).

**What does your instinct say?**

<done/>

---

**Run end**: done after 2 turns (314s)
