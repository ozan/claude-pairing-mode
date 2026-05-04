# leetcode-coin-change

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T20:59:17

## Initial prompt

Let's solve Leetcode #322, 'Coin Change'. Given coin denominations and a target amount, return the fewest number of coins to make that amount, or -1 if impossible.

---

## Turn 1

### Tutor

Tutor: Classic DP problem. Before I write any code, there's a key design decision worth thinking through.

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Tutor: The plan: build a `dp` array where `dp[i]` = fewest coins to make amount `i`. We set `dp[0] = 0`, then fill up to the target. The question is — what should we initialize `dp[i]` to for `i > 0`?

OPTIONS:
[A] Initialize to -1
Use `-1` to signal "not yet computed", matching the problem's own sentinel for impossible.

```diff
+++ coin_change.py
@@ -0,0 +1,4 @@
+def coinChange(coins, amount):
+    dp = [-1] * (amount + 1)
+    dp[0] = 0
+    # fill dp[1..amount]
```

[B] Initialize to float('inf')
Use `float('inf')` so that `min()` comparisons during filling always prefer any real solution over the default.

```diff
+++ coin_change.py
@@ -0,0 +1,4 @@
+def coinChange(coins, amount):
+    dp = [float('inf')] * (amount + 1)
+    dp[0] = 0
+    # fill dp[1..amount]
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which initialization do you prefer?

### Student

I think I'd go with **B** — `float('inf')`.

Here's my reasoning: when we're filling the DP array, we'll be doing something like `dp[i] = min(dp[i - coin] + 1, dp[i])` for each coin. If we initialize to `-1`, we'd have to add extra logic to check "is this value actually valid or just the sentinel?" before comparing. But with `float('inf')`, the `min()` operation naturally handles it — any real coin count will be less than infinity, so we don't need conditional checks.

It feels cleaner and more idiomatic for DP problems.

Should I start writing the filling logic now?

---

## Turn 2

### Tutor

Tutor: Exactly right — and well explained. `inf + 1` is still `inf` in Python, so the `min()` stays clean with zero extra branching.

Go ahead and think about the filling loop. Here's the key question — which condition guards the inner step correctly?

OPTIONS:
[A] Guard with coin < i
```diff
+++ coin_change.py
@@ -4,4 +4,6 @@
+    for i in range(1, amount + 1):
+        for coin in coins:
+            if coin < i:
+                dp[i] = min(dp[i], dp[i - coin] + 1)
+    return dp[amount] if dp[amount] != float('inf') else -1
```

[B] Guard with coin <= i
```diff
+++ coin_change.py
@@ -4,4 +4,6 @@
+    for i in range(1, amount + 1):
+        for coin in coins:
+            if coin <= i:
+                dp[i] = min(dp[i], dp[i - coin] + 1)
+    return dp[amount] if dp[amount] != float('inf') else -1
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which guard is correct?

### Student

**B** — `coin <= i`.

If the coin equals the amount we're trying to make, we should be able to use it. For example, if we're at `i = 5` and we have a coin of value `5`, we should be able to do `dp[5] = min(dp[5], dp[0] + 1) = 1`. That's a valid solution with just one coin.

With option A (`coin < i`), we'd skip that case and miss it, which would be wrong.

---

## Turn 3

### Tutor

Tutor: Spot on. `dp[0] = 0` exists precisely to anchor that case — it would be wasted if we never let `coin == i` reach it.

Let's put the whole thing together now.

[Glob(coin_change.py)]
  No files found

[Write(coin_change.py)]
def coinChange(coins: list[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1


… (8 more lines)
  File created successfully at: coin_change.py

[Bash(python coin_change.py)]
  All tests passed.

Tutor: All green. Here's the complexity summary:

| | |
|---|---|
| **Time** | O(amount × len(coins)) |
| **Space** | O(amount) |

A few things worth noting about this solution:

- **Why bottom-up?** We build from subproblems we've already solved. Each `dp[i]` only looks back at `dp[i - coin]`, which was computed earlier in the same pass.
- **The `dp[0] = 0` anchor** isn't just an edge case — it's the base that every valid solution ultimately traces back to. Without it, no coin count would ever be less than `inf`.
- This is essentially **unbounded knapsack** — the same coin can be reused, which is why we scan `i` forward (not backward like in 0/1 knapsack). That's a useful pattern to recognize.

Want to explore the memoized top-down version, or try a harder variant like Coin Change 2 (counting the number of combinations)?

### Student

I appreciate the offer, but I think I'm good for now. I came in to solve Coin Change #322, and we've got a working solution that I understand pretty well. The explanation about why we iterate forward (unbounded reuse) vs. backward (0/1 knapsack) was really helpful for understanding the pattern.

I feel like I've got the core idea locked down — build up from smaller amounts using the anchor at zero, use `inf` to keep comparisons clean, and guard properly so we don't access invalid indices. That's enough for me to feel confident tackling similar DP problems.

Thanks for walking through this methodically!

<done/>

---

**Run end:** done after 3 turn(s) in 89.0s
