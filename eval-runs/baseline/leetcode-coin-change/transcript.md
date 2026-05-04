# leetcode-coin-change

- Source: `leetcode`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:26:20.037Z

---

## Turn 1

**User:**

Let's solve Leetcode #322, 'Coin Change'. Given coin denominations and a target amount, return the fewest number of coins to make that amount, or -1 if impossible.

**Pair:**

Assistant: ## Coin Change — Dynamic Programming

The key insight: build up solutions from `0 → amount`, using previously-solved sub-problems.

**State:** `dp[i]` = fewest coins to make amount `i`  
**Transition:** `dp[i] = min(dp[i - coin] + 1)` for every coin ≤ i  
**Base case:** `dp[0] = 0`

```python
def coinChange(coins: list[int], amount: int) -> int:
    # Initialize with amount+1 as a sentinel "infinity"
    # (you can never need more than `amount` coins of denomination 1)
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0  # base case: 0 coins needed to make amount 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] <= amount else -1


# ── Tests ────────────────────────────────────────────────────────────────────
assert coinChange([1, 5, 10, 25], 36) == 3   # 25 + 10 + 1
assert coinChange([1, 5, 10, 25], 30) == 2   # 25 + 5
assert coinChange([1, 2, 5],      11) == 3   # 5 + 5 + 1
assert coinChange([2],             3) == -1  # impossible
assert coinChange([1],             0) == 0   # edge: amount = 0
print("All tests passed!")
```

### How it builds up (coins=[1,2,5], amount=6)

| i | dp[i] | via coin |
|---|-------|----------|
| 0 | 0     | base     |
| 1 | 1     | 1        |
| 2 | 1     | 2        |
| 3 | 2     | 2 (dp[1]+1) |
| 4 | 2     | 2 (dp[2]+1) |
| 5 | 1     | 5        |
| **6** | **2** | **5 (dp[1]+1)** |

### Complexity

| | |
|---|---|
| **Time** | O(amount × n) — two nested loops |
| **Space** | O(amount) — the dp array |

### Why not greedy?
Greedy (always pick the largest coin) fails on cases like `coins=[1,3,4], amount=6` — greedy gives 4+1+1=**3 coins**, but 3+3=**2 coins** is optimal. DP explores *all* sub-problems and is guaranteed optimal.

---

## Turn 2

**User:**

I've walked you through the DP approach with explanation, traces, and test cases. **Does this solution make sense to you, or would you like to explore it further?**

Here are some natural next steps:

1. **Test it live** — I can run the Python code and confirm the test cases pass
2. **Trace through a specific case** — Pick an example (like `coins=[1,2,5], amount=6`) and I can walk you step-by-step through how the DP table fills in
3. **Explore alternatives** — BFS (shortest path on a graph of amounts) or memoized recursion give the same result but feel different to think about
4. **Implement in the TUI** — If you want the interactive "choose-between-two-approaches" pair-programming experience, we can set that up

What would help you learn best?

**Pair:**

Assistant: Just to clarify — I'm the one who wrote that solution! So the question is really: **what would *you* like to do next?**

Happy to help with any of those options:

- **Run it** — I can execute the code right now and show you the output
- **Step-by-step trace** — Tell me an example (`coins`, `amount`) and I'll walk through the dp table row by row
- **Alternative approaches** — The BFS approach is particularly elegant and worth seeing if you're interviewing
- **Variations** — e.g. *Coin Change 2* (#518) asks for the number of combinations instead of minimum coins, which flips the DP slightly

What's most useful for you?

---

## Turn 3

**User:**

I appreciate the walkthrough! The DP approach makes sense to me — the key click for me was realizing that we're building a *lookup table* from the ground up so we never re-solve the same sub-problem, and the sentinel `amount + 1` is clever for detecting impossibility.

Here's what I'd find most helpful:

**I'd like to run the code and then trace a failing case.** 

Specifically:
1. **Run the tests** — seeing it actually work on paper vs. the interpreter is different
2. **Then trace `coins=[1,3,4], amount=6` step-by-step** 

Why that case? Because you mentioned greedy fails here (it picks 4+1+1=3 coins when 3+3=2 is better), and I want to *see* how the DP table discovers that 3+3 is optimal while the greedy approach misses it. That'll cement why we can't just pick the largest coin.

Should I go ahead and run the Python code?

**Pair:**

Assistant: Yes — let's run it right now, then trace the greedy-failure case together.

[Bash(python3 << 'EOF'
def coinChange(coins: list[int], amount: int) -> int:
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] <= amount else -1


# Original tests
assert coinChange([1, 5, 10, 25], 36) == 3   # 25 + 10 + 1
assert coinChange([1, 5, 10, 25], 30) == 2   # 25 + 5
assert coinChange([1, 2, 5],      11) == 3   # 5 + 5 + 1
assert coinChange([2],             3) == -1  # impossible
assert coinChange([1],             0) == 0   # edge: amount = 0
print("All original tests passed!")

# The greedy-failure case
result = coinChange([1, 3, 4], 6)
print(f"\ncoinChange([1,3,4], 6) = {result}  (expected 2, greedy would give 3)")

# Also print the full dp table for tracing
coins, amount = [1, 3, 4], 6
dp = [amount + 1] * (amount + 1)
dp[0] = 0
for i in range(1, amount + 1):
    for coin in coins:
        if coin <= i:
            dp[i] = min(dp[i], dp[i - coin] + 1)

print(f"\nFull dp table for coins=[1,3,4], amount=6:")
for i, val in enumerate(dp):
    print(f"  dp[{i}] = {val}")
EOF
)]
  All original tests passed!
  
  coinChange([1,3,4], 6) = 2  (expected 2, greedy would give 3)
  
  Full dp table for coins=[1,3,4], amount=6:
    dp[0] = 0
    dp[1] = 1
    dp[2] = 2
    dp[3] = 1
    dp[4] = 1
    dp[5] = 2
    dp[6] = 2

Assistant: All tests pass. Now let's trace exactly how the table fills in and where greedy goes wrong.

---

### Step-by-step trace: `coins=[1,3,4], amount=6`

At each `i`, we try every coin and take the best:

| i | Try coin 1 | Try coin 3 | Try coin 4 | **dp[i]** | Winning move |
|---|---|---|---|---|---|
| 0 | — | — | — | **0** | base case |
| 1 | dp[0]+1 = **1** | — | — | **1** | coin 1 |
| 2 | dp[1]+1 = **2** | — | — | **2** | coin 1 |
| 3 | dp[2]+1 = 3 | dp[0]+1 = **1** | — | **1** | coin 3 |
| 4 | dp[3]+1 = 2 | dp[1]+1 = 2 | dp[0]+1 = **1** | **1** | coin 4 |
| 5 | dp[4]+1 = 2 | dp[2]+1 = **2** | dp[1]+1 = 2 | **2** | coin 3 or 4 |
| 6 | dp[5]+1 = 3 | dp[3]+1 = **2** | dp[2]+1 = 3 | **2** | coin 3 ✓ |

**The decisive moment is `dp[6]`:**
- Greedy grabs the largest coin first: 4 → leftover 2 → must use 1+1, **total 3 coins**
- DP checks `dp[6 - 3] + 1 = dp[3] + 1 = 1 + 1 = 2` — it *already knows* dp[3]=1 (one coin of 3), so 3+3=**2 coins**

This is the core of why greedy fails: it locks in a local choice (biggest coin first) without knowing that a smaller coin now would open up a better sub-problem later. DP avoids this by trying *all* coins at every step and trusting previously-computed optimal answers.

---

## Turn 4 (final)

**User:**

Perfect — you've got it. That's exactly the mental model: **greedy commits to decisions locally without foresight; DP explores all paths and leans on previously-solved sub-problems.**

One more observation that might stick: notice how `dp[3] = 1` gets *reused* when computing `dp[6]`. That's the whole win. Greedy would recompute (or just pick 4), but DP memoizes "the best way to make 3" and then asks "can I make 6 by using a coin that leaves me with a sub-problem I've already solved optimally?" The answer is yes: coin 3 leaves us at `dp[3]`, which is already 1, so total is 2.

---

### Summary
✓ Code runs + all tests pass  
✓ Greedy failure case traced: DP finds 3+3=2, greedy finds 4+1+1=3  
✓ Core insight: DP reuses optimal sub-solutions, greedy doesn't look ahead  

You've got a solid understanding now. If you ever need to revisit this (interviews, Coin Change 2, BFS variant), the key is: *build a lookup table bottom-up, and at each step check every coin to find the minimum*.

<done/>

---

**Run end**: done after 3 turns (76s)
