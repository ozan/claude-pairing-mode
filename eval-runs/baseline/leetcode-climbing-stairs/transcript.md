# leetcode-climbing-stairs

- Source: `leetcode`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:26:00.657Z

---

## Turn 1

**User:**

Let's solve Leetcode #70, 'Climbing Stairs'. Given n steps and you can climb 1 or 2 at a time, return the number of distinct ways to reach the top.

**Pair:**

Assistant: ## Climbing Stairs — Leetcode #70

### Key Insight

To reach step `n`, you must have come from either:
- Step `n-1` (taking **1 step**), or
- Step `n-2` (taking **2 steps**)

So: `ways(n) = ways(n-1) + ways(n-2)` — this is the **Fibonacci sequence**!

### Solution

```python
def climbStairs(n: int) -> int:
    if n <= 2:
        return n

    prev2, prev1 = 1, 2

    for _ in range(3, n + 1):
        prev2, prev1 = prev1, prev1 + prev2

    return prev1
```

### Walkthrough

| n | ways | reasoning |
|---|------|-----------|
| 1 | 1 | `{1}` |
| 2 | 2 | `{1+1}`, `{2}` |
| 3 | 3 | `{1+1+1}`, `{1+2}`, `{2+1}` |
| 4 | 5 | `{1+1+1+1}`, `{1+1+2}`, `{1+2+1}`, `{2+1+1}`, `{2+2}` |
| 5 | 8 | ... |

### Complexity

| | |
|---|---|
| **Time** | O(n) — single loop |
| **Space** | O(1) — only two variables |

The key optimization over naive recursion is using **two rolling variables** instead of an array, giving O(1) space. A memoized recursive solution would also be O(n) time but O(n) space due to the call stack.

---

## Turn 2 (final)

**User:**

I see you've shown me a solution approach! Let me verify this works correctly by testing it with the examples from the problem.Perfect! ✅ The solution is **correct and efficient**.

### Why This Works

1. **Base cases** (`n ≤ 2`): For 1 step, there's 1 way. For 2 steps, there are 2 ways.

2. **Recurrence relation**: To reach step `n`, you must come from either:
   - Step `n-1` (take 1 step)
   - Step `n-2` (take 2 steps)
   
   So: `ways(n) = ways(n-1) + ways(n-2)` — the Fibonacci sequence!

3. **Space optimization**: Instead of storing all n values (O(n) space), we only keep the **last two** values, sliding them forward as we iterate. This cuts space down to **O(1)**.

### Alternative Approach (for comparison)

If you wanted to verify the logic with recursion + memoization:

```python
def climbStairs(n: int) -> int:
    memo = {}
    def dp(i):
        if i <= 2:
            return i
        if i in memo:
            return memo[i]
        memo[i] = dp(i - 1) + dp(i - 2)
        return memo[i]
    return dp(n)
```

This also works but uses O(n) space for the memo + call stack. The iterative approach is cleaner for this problem.

All test cases pass (n=1 through n=6). The solution handles the problem constraints perfectly.

<done/>

---

**Run end**: done after 1 turn (34s)
