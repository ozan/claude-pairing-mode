# leetcode-coin-change

- Source: `leetcode`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Output style: `Learning`
- Started: 2026-05-03T19:55:55.995Z

---

## Turn 1

**User:**

Let's solve Leetcode #322, 'Coin Change'. Given coin denominations and a target amount, return the fewest number of coins to make that amount, or -1 if impossible.

**Pair:**

Assistant: ## Coin Change — Dynamic Programming

### Why Greedy Fails First

It's tempting to always grab the largest coin. But with coins `[1, 3, 4]` and amount `6`:
- **Greedy**: 4 + 1 + 1 = **3 coins** ❌
- **Optimal**: 3 + 3 = **2 coins** ✅

We need to explore all sub-problems — that means **DP**.

---

### The Core Idea

Define a 1-D table where:

```
dp[i] = fewest coins needed to make amount i
```

**Recurrence:** To make amount `i`, try every coin `c`. If we use coin `c`, we need `dp[i - c]` coins for the remainder, plus 1 for this coin:

```
dp[i] = min( dp[i - c] + 1 )   for each coin c ≤ i
```

**Base case:** `dp[0] = 0` — zero coins needed for amount zero.

---

### Trace Through an Example

`coins = [1, 5, 11]`, `amount = 15`

| i | best via coin 1 | best via coin 5 | best via coin 11 | dp[i] |
|---|---|---|---|---|
| 0 | — | — | — | **0** |
| 1 | dp[0]+1 = 1 | — | — | **1** |
| 5 | dp[4]+1 = 5 | dp[0]+1 = 1 | — | **1** |
| 10 | … | dp[5]+1 = 2 | — | **2** |
| 11 | … | dp[6]+1 = 3 | dp[0]+1 = 1 | **1** |
| 15 | … | dp[10]+1 = 3 | dp[4]+1 = 5 | **3** ← (5+5+5) |

---

### Code

```python
def coinChange(coins: list[int], amount: int) -> int:
    # Initialize all amounts as "impossible" (infinity)
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # base case

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:                          # coin is usable
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1
```

---

### Complexity

| | |
|---|---|
| **Time** | O(amount × \|coins\|) — fill each cell by trying every coin |
| **Space** | O(amount) — the dp table |

---

### Key Insight to Remember

> **"What's the cheapest way to reach `i`?"** = try leaving one coin's worth of gap, and look up the pre-solved answer for that gap.

This is the classic **bottom-up DP** pattern: solve all smaller sub-problems first, then combine them. The `inf` sentinel naturally propagates impossibility — if `dp[i - coin]` is `inf`, adding 1 still stays `inf`.

---

## Turn 2 (final)

**User:**

Got it! I've explained the approach. Now let me write and test the working solution.Perfect! ✅ All tests pass. Here's the final solution:

## Solution Summary

The **dynamic programming bottom-up** approach solves Coin Change efficiently:

**Key points:**
- **DP table:** `dp[i]` = min coins to make amount `i`
- **Recurrence:** For each amount, try every coin and pick the best
- **Base case:** `dp[0] = 0`
- **Sentinel:** Use `inf` to mark impossible amounts; it naturally propagates

**Why this works:**
- Each sub-problem (amount `i`) is solved exactly once
- When we reach amount `i`, we've already solved all smaller amounts
- We can safely look up `dp[i - coin]` without worrying about cycles

**Test coverage:**
- Standard cases (greedy would fail)
- Edge cases (no coins, amount 0)
- Impossible amounts (returns -1)
- Large amounts (efficient O(amount × coins) time)

The algorithm is optimal for this problem — you can't do better than exploring all amounts up to the target.

<done/>

---

**Run end**: done after 1 turn (56s)
