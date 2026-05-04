# leetcode-coin-change

- Condition: `learning`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:04:09

## Initial prompt

Let's solve Leetcode #322, 'Coin Change'. Given coin denominations and a target amount, return the fewest number of coins to make that amount, or -1 if impossible.

---

## Turn 1

### Tutor

Thinking: The user wants to solve LeetCode #322 - Coin Change. This is a classic dynamic programming problem. Let me explain and solve it clearly.
  
  **Problem:**
  - Given an array of coin denominations and a target amount
  - Return the minimum number of coins needed to make that amount
  - Return -1 if it's impossible
  
  **Approach - Bottom-up Dynamic Programming:**
  
  The key insight is:
  - Define `dp[i]` = minimum coins needed to make amount `i`
  - Base case: `dp[0] = 0` (0 coins needed to make amount 0)
  
  
  - For each amount, I try using each coin and take the minimum: `dp[i] = min(dp[i - coin] + 1)` for all valid coins
  - I initialize all dp values to `amount + 1` as a sentinel value representing "impossible", since the maximum coins needed would be `amount` itself (using all 1-denomination coins)
  
  Now I'll write out the Python solution with clear logic.
  
  Let me trace through a concrete example to verify the approach works: coins = [1, 5, 11], amount = 15. The greedy approach would pick 11 + four 1s = 5 coins, but dynamic programming finds the optimal solution of three 5s = 3 coins. Working through the DP table, I start with dp[0] = 0, then build up each position by checking which coin gives the minimum count.
  
  Writing the Python code... I'm recalculating the values more carefully—let me trace through the coin combinations for amount 15 with coins [1, 5, 11]. The optimal solution should be three 5-coin pieces, so dp[15] should equal 3, which I can get by taking dp[10]+1 (since dp[10]=2 from using two 5-coins).
  
  Actually, I think the standard LeetCode example uses coins [1, 2, 5] with amount 11, which also gives 3 coins as the answer (5+5+1), so let me switch to that for clarity.

Tutor: ## LeetCode #322 — Coin Change

### 🧠 The Core Insight

**Greedy fails here.** With coins `[1, 3, 4]` and amount `6`, greedy picks `4+1+1` = 3 coins, but `3+3` = **2 coins** is optimal. We need **Dynamic Programming**.

---

### 🏗️ Building the DP Table

Define `dp[i]` = *fewest coins to make amount `i`*.

**Key recurrence:**
```
dp[i] = min(dp[i - coin] + 1)   for each coin ≤ i
```
> "To make amount `i`, try removing each coin — whichever sub-problem is cheapest, plus 1."

**Base case:** `dp[0] = 0` — zero coins needed for amount zero.

---

### 🔍 Trace Example

`coins = [1, 5, 11]`, `amount = 15`

| amount | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | **15** |
|--------|---|---|---|---|---|---|---|---|---|---|----|----|----|----|----|----|
| dp     | 0 | 1 | 2 | 3 | 4 | 1 | 2 | 3 | 4 | 5 | 2  | 1  | 2  | 3  | 4  | **3**  |

`dp[15]`: try coin 5 → `dp[10] + 1 = 3` ✓  *(that's 5+5+5)*

---

### 💻 Solution

```python
def coinChange(coins: list[int], amount: int) -> int:
    # Use amount+1 as "infinity" — you'd never need more than `amount` coins
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0  # base case: 0 coins to make amount 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    # If dp[amount] is still "infinity", the amount is unreachable
    return dp[amount] if dp[amount] <= amount else -1
```

---

### 📊 Complexity

| | |
|---|---|
| **Time** | O(amount × len(coins)) — two nested loops |
| **Space** | O(amount) — the dp array |

---

### 🔑 Key Takeaways

| Concept | Why it matters |
|---|---|
| `dp[amount + 1]` as ∞ | Safe sentinel — the real max is `amount` (all 1-coins) |
| Build bottom-up | Each `dp[i]` only needs smaller sub-problems, already solved |
| Greedy ≠ optimal | Coin change lacks the "greedy choice property" in general |
| Final check `<= amount` | Distinguishes a valid answer from the sentinel "impossible" value |

The pattern here — *"fill a 1D table where each cell depends on earlier cells"* — is the same backbone used in **Unbounded Knapsack**, **Word Break**, and many other DP problems.

### Student

Thanks for walking me through this! I can see how the DP approach builds up from smaller amounts to the target amount, and why greedy doesn't work here.

Let me make sure I understand the code by tracing through a simple example myself. Let me try `coins = [2, 5]` and `amount = 5`:

- `dp = [0, 6, 6, 6, 6, 6]` initially (where 6 = amount+1)
- `dp[0] = 0`
- `i=1`: coin 2 > 1, coin 5 > 1, so `dp[1]` stays 6
- `i=2`: coin 2 ≤ 2, so `dp[2] = min(6, dp[0]+1) = 1`
- `i=3`: coin 2 ≤ 3, so `dp[3] = min(6, dp[1]+1) = min(6, 7) = 6` (no change)
- `i=4`: coin 2 ≤ 4, so `dp[4] = min(6, dp[2]+1) = min(6, 2) = 2`
- `i=5`: coin 2 ≤ 5 gives `dp[5] = min(6, dp[3]+1) = 6`, then coin 5 ≤ 5 gives `dp[5] = min(6, dp[0]+1) = 1`

So we return `1` for amount 5 (using one 5-coin). That makes sense!

One thing I want to double-check: in the final return statement, why do we compare `dp[amount] <= amount` instead of just checking `dp[amount] != amount + 1`? Are they equivalent, or is there a subtle difference I'm missing?

---

## Turn 2

### Tutor

Thinking: The user is asking a great question about the final return statement:
  
  ```python
  return dp[amount] if dp[amount] <= amount else -1
  ```
  
  vs
  
  ```python
  return dp[amount] if dp[amount] != amount + 1 else -1
  ```
  
  Are these equivalent? Let me think carefully.
  
  The sentinel value is `amount + 1`. So we're checking if `dp[amount]` is still the sentinel value (meaning it's unreachable).
  
  `dp[amount] <= amount` — this is true when `dp[amount]` was actually updated to a real answer (which would be between 0 and amount inclusive).
  
  
  `dp[amount] != amount + 1` — this directly checks whether we're still at the sentinel.
  
  Since valid answers always fall in the range [0, amount] and the sentinel is amount + 1, both conditions are checking the same thing from different angles. When the amount is reachable, both return true; when it's unreachable, both return false. So yes, they're equivalent.
  
  The `!= amount + 1` check is arguably more explicit because it directly tests whether we're still holding the sentinel value, whereas `<= amount` works but relies on understanding the mathematical constraint that the maximum possible answer is amount itself.

Tutor: Great trace — spot on! And that's a sharp thing to question. Let me address it directly.

---

### Are they equivalent?

**Yes, in this problem they're logically identical.** Here's why:

The dp values can only ever be:

| Case | Value of `dp[amount]` |
|---|---|
| Reachable | Some integer in **[0, amount]** |
| Unreachable | Exactly **amount + 1** (the sentinel, never touched by `min()`) |

Since the two possible "zones" are `[0, amount]` and `{amount + 1}` — with **no overlap and no gap** — both checks carve out the exact same boundary:

```
dp[amount] <= amount   ←→   dp[amount] != amount + 1
```

---

### Why the valid max is exactly `amount`

The tightest possible answer is using all denomination-1 coins — which costs exactly `amount` coins. So a real answer **can never reach** `amount + 1`. That's the whole reason `amount + 1` is a safe sentinel in the first place.

---

### Which is better style?

```python
dp[amount] if dp[amount] != amount + 1 else -1  # ✅ more explicit
dp[amount] if dp[amount] <= amount else -1       # ✅ also correct, slightly less obvious
```

`!= amount + 1` more directly reads as *"is this still the sentinel?"* — it exposes **intent**. The `<= amount` form works, but requires the reader to mentally reconstruct the valid range to understand why.

You'd commonly see both in practice; some authors prefer `<= amount` because it avoids the magic number `amount + 1` appearing twice, but `!= amount + 1` arguably tells the story more clearly.

---

### The takeaway

The sentinel trick works **because its value is chosen to sit just outside the valid answer range.** The two checks are equivalent *by design* — that gap between `amount` and `amount + 1` is intentional, not coincidental.

### Student

Ah, that makes perfect sense! I really like how the sentinel is specifically chosen to be unreachable—that's clever. And I appreciate you showing both forms; I can see now that `!= amount + 1` is actually more self-documenting because it explicitly says "is this still the sentinel value we never touched?"

I feel solid on the algorithm now. Let me implement it myself and test it on the example from your trace to make sure I've got it:

```python
def coinChange(coins: list[int], amount: int) -> int:
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != amount + 1 else -1

# Test with the trace example
print(coinChange([1, 5, 11], 15))  # Should be 3 (5+5+5)
print(coinChange([2, 5], 5))       # Should be 1 (one 5-coin)
print(coinChange([2], 3))          # Should be -1 (impossible)
```

This matches the solution you showed, and I traced through the logic. I'm confident this works correctly. Thanks for the careful explanation—especially clarifying the sentinel pattern and why both checks are equivalent!

<done/>

---

**Run end:** done after 2 turn(s) in 56.0s
