# leetcode-coin-change

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:51:22

## Initial prompt

Let's solve Leetcode #322, 'Coin Change'. Given coin denominations and a target amount, return the fewest number of coins to make that amount, or -1 if impossible.

---

## Turn 1

### Tutor

Tutor: Great problem. Before writing any code — which approach do you want to take?

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Greedy: largest coin first
At each step, pick the largest coin that fits the remaining amount. Simple and fast — O(amount) time, O(1) space.

[B] Dynamic programming
Build `dp[0..amount]` where `dp[i]` = min coins to reach `i`. For each amount, try every coin denomination. O(amount × coins) time, O(amount) space.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach would you go with?

### Student

I'd like to go with **B — Dynamic Programming**.

I know greedy sounds faster, but I have a feeling it doesn't always work for coin change. Like, if the coins are `[1, 3, 4]` and the amount is `6`, greedy would pick `4` first, then need two `1`s (total 3 coins), but the optimal is two `3`s (total 2 coins). So I think I need DP to explore all possibilities systematically.

Can we start by building the `dp` array and walking through the logic?

---

## Turn 2

### Tutor

Tutor: Exactly right — you nailed the counterexample. That intuition is the core reason DP exists for this class of problem.

Now let's talk about building the `dp` array. `dp[i]` will hold the min coins to make amount `i`, with `dp[0] = 0`. The key question is: what do we fill the rest of the array with initially?

OPTIONS:
[A] Initialize to zero
```diff
+++ coin_change.py
@@ -0,0 +1,3 @@
+def coinChange(coins, amount):
+    dp = [0] * (amount + 1)
+    # dp[0] = 0 naturally; fill the rest during iteration
```
Uncomputed slots start at 0, and we overwrite as we find solutions.

[B] Initialize to amount + 1
```diff
+++ coin_change.py
@@ -0,0 +1,3 @@
+def coinChange(coins, amount):
+    dp = [amount + 1] * (amount + 1)
+    dp[0] = 0
```
Treat unvisited slots as "unreachable"; any valid answer must be ≤ `amount`.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which initialization would you use?

### Student

I'd go with **B — Initialize to amount + 1**.

Here's my thinking: if I initialize to zero, I can't tell the difference between "I haven't computed this amount yet" and "this amount is reachable with 0 coins" (which should only be true for amount 0). 

With `amount + 1`, I'm using it as a sentinel value that means "unreachable" — since the maximum coins needed is `amount` (if all coins were 1), any valid answer will be less than `amount + 1`. That way, when I check `dp[i]` at the end, if it's still `amount + 1`, I know it was impossible to make that amount, and I can return -1.

Should we code up the iteration part now?

---

## Turn 3

### Tutor

Tutor: Perfect reasoning — that's exactly right. Now for the core recurrence. Once we have the `dp` array, we iterate and for each amount `i`, we try every coin. Here's the question:

OPTIONS:
[A] Guard against unreachable states
```diff
+++ coin_change.py
@@ -0,0 +1,5 @@
+    for i in range(1, amount + 1):
+        for c in coins:
+            if c <= i and dp[i - c] <= amount:
+                dp[i] = min(dp[i], dp[i - c] + 1)
+    return dp[amount] if dp[amount] <= amount else -1
```
Skip the update if the sub-problem is still "unreachable."

[B] Guard only against negative index
```diff
+++ coin_change.py
@@ -0,0 +1,5 @@
+    for i in range(1, amount + 1):
+        for c in coins:
+            if c <= i:
+                dp[i] = min(dp[i], dp[i - c] + 1)
+    return dp[amount] if dp[amount] <= amount else -1
```
Just prevent a negative index; let `min()` do the rest.

(Reply with A or B, or ask a follow-up question.)

Tutor: Think about what happens mathematically when `dp[i - c]` is still the sentinel `amount + 1`. Does the extra guard in A actually change anything?

### Student

Hmm, let me think through this...

If `dp[i - c]` is still `amount + 1` (unreachable), and I do `dp[i - c] + 1`, that becomes `amount + 2`.

Then `min(dp[i], dp[i - c] + 1)` compares `dp[i]` (which is `amount + 1`) against `amount + 2`. Since `amount + 1 < amount + 2`, the `min()` keeps `dp[i]` as `amount + 1`.

So the extra guard in **A** doesn't actually change the result — it just avoids doing that arithmetic and comparison when we know the sub-problem is unreachable. It's an optimization, but mathematically **B** is correct too.

I'd go with **B** because it's simpler and cleaner. The sentinel value does the work for us.

Should we put it all together and test it on an example?

---

## Turn 4

### Tutor

Tutor: Exactly right — the sentinel does the work. Let's put it all together.

[Glob(coin_change.py)]
  No files found

[Write(coin_change.py)]
def coinChange(coins: list[int], amount: int) -> int:
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for c in coins:
            if c <= i:
                dp[i] = min(dp[i], dp[i - c] + 1)

    return dp[amount] if dp[amount] <= amount else -1


… (8 more lines)
  File created successfully at: coin_change.py

[Bash(python coin_change.py)]
  All tests passed.

Tutor: All green, including the `[1,3,4], 6` case that would trip up greedy.

Now a quick "look back" question — worth thinking about before calling it done:

OPTIONS:
[A] O(amount × len(coins))
The outer loop runs `amount` times; the inner loop runs `len(coins)` times. Every cell is filled in one pass.

[B] O(amount²)
For each of the `amount` cells, we might scan up to `amount` previous cells to find the best sub-problem.

(Reply with A or B, or ask a follow-up question.)

Tutor: What's the time complexity of this solution?

### Student

It's **A — O(amount × len(coins))**.

The outer loop iterates from 1 to `amount`, so that's `amount` iterations. The inner loop tries every coin in `coins`, which is `len(coins)` iterations. Inside the inner loop, we just do constant-time work: a comparison, an addition, and a `min()` call.

So we're doing `amount × len(coins)` basic operations total. We don't revisit any cells or do nested scanning of previous amounts — we just fill each `dp[i]` once by looking at `dp[i - c]` for each coin `c`.

That's why DP beats greedy here: we get a guaranteed correct answer in polynomial time, and it scales linearly with both the amount and the number of coin types.

I think we're done! The solution works, I understand the reasoning (sentinel values, the recurrence, the complexity), and all tests pass.

<done/>

---

**Run end:** done after 4 turn(s) in 118.0s
