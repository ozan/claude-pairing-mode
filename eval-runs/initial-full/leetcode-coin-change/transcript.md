# leetcode-coin-change

- Source: `leetcode`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T05:12:00.905Z

---

## Turn 1

**User:**

Let's solve Leetcode #322, 'Coin Change'. Given coin denominations and a target amount, return the fewest number of coins to make that amount, or -1 if impossible.

**Pair:**

Assistant: Classic DP problem. Before we write any code, let me ask a foundational question about the approach:

OPTIONS:
[A] Greedy (largest coin first)
Always pick the largest coin that fits, subtract it, repeat. Simple and fast — O(amount) time, O(1) space.

[B] Bottom-up DP
Build a table dp[0..amount] where dp[i] = min coins to make i. Fill it left-to-right using previously solved sub-problems. O(amount × coins) time.

(Reply with A or B, or ask a follow-up question.)

Assistant: **A: Greedy (largest coin first)** — Always pick the largest coin that fits, subtract it, repeat. Simple and fast — O(amount) time, O(1) space.

**B: Bottom-up DP** — Build a table dp[0..amount] where dp[i] = min coins to make i. Fill it left-to-right using previously solved sub-problems. O(amount × coins) time.

---

## Turn 2

**User:**

**B: Bottom-up DP**

Greedy fails for some coin sets. For example, coins [1, 3, 4] and amount 6: greedy picks 4 + 1 + 1 = 3 coins, but 3 + 3 = 2 is optimal. DP considers all possibilities and finds the true minimum, which is what we need.

**Pair:**

Assistant: Exactly right — greedy is only optimal for "canonical" coin systems (like standard US currency). DP is the correct tool here.

Now let's write the solution. The DP table needs a sentinel value for "not yet reachable." Which initialization is right?

OPTIONS:
[A] Zero-initialize
```diff
+++ coin_change.py
@@ -0,0 +1,5 @@
+def coinChange(coins, amount):
+    dp = [0] * (amount + 1)
+    for i in range(1, amount + 1):
+        dp[i] = min((dp[i - c] + 1 for c in coins if c <= i), default=dp[i])
+    return dp[amount] if dp[amount] != 0 else -1
```

[B] Sentinel-initialize
```diff
+++ coin_change.py
@@ -0,0 +1,5 @@
+def coinChange(coins, amount):
+    dp = [0] + [amount + 1] * amount
+    for i in range(1, amount + 1):
+        dp[i] = min((dp[i - c] + 1 for c in coins if c <= i), default=dp[i])
+    return dp[amount] if dp[amount] <= amount else -1
```

(Reply with A or B, or ask a follow-up question.)

Assistant: **A: Zero-initialize**
```diff
+++ coin_change.py
@@ -0,0 +1,5 @@
+def coinChange(coins, amount):
+    dp = [0] * (amount + 1)
+    for i in range(1, amount + 1):
+        dp[i] = min((dp[i - c] + 1 for c in coins if c <= i), default=dp[i])
+    return dp[amount] if dp[amount] != 0 else -1
```

**B: Sentinel-initialize**
```diff
+++ coin_change.py
@@ -0,0 +1,5 @@
+def coinChange(coins, amount):
+    dp = [0] + [amount + 1] * amount
+    for i in range(1, amount + 1):
+        dp[i] = min((dp[i - c] + 1 for c in coins if c <= i), default=dp[i])
+    return dp[amount] if dp[amount] <= amount else -1
```

---

## Turn 3

**User:**

**B: Sentinel-initialize**

Option A uses 0 as a "not yet set" marker, but 0 is also the *correct* answer for amount=0 (needs 0 coins). This conflates two meanings and works only by accident. 

Option B uses `amount + 1` as the sentinel — a value that's impossible to reach naturally (you can't need more than `amount` coins of value ≥1 to make `amount`). When we compute `min(...)`, unreachable states stay at the sentinel, and reachable states drop below it. The final check `dp[amount] <= amount` is explicit and unambiguous.

Go ahead — write Option B to the file and test it with a few cases.

**Pair:**

Assistant: Perfectly reasoned. Writing it out and running a few cases:

[Write(coin_change.py)]
def coinChange(coins, amount):
    dp = [0] + [amount + 1] * amount
    for i in range(1, amount + 1):
        dp[i] = min((dp[i - c] + 1 for c in coins if c <= i), default=dp[i])
    return dp[amount] if dp[amount] <= amount else -1


# Tests
cases = [
    ([1, 5, 10, 25], 41),   # 25+10+5+1 = 4 coins
    ([1, 3, 4],      6),    # 3+3       = 2 coins  (greedy would give 3)
    ([2],            3),    # impossible = -1
… (6 more lines)

[Bash(python coin_change.py)]
  error: Exit code 127

[Bash(python3 coin_change.py)]
  coins=[1, 5, 10, 25], amount=41 -> 4
  coins=[1, 3, 4], amount=6 -> 2
  coins=[2], amount=3 -> -1
  coins=[1], amount=0 -> 0

Assistant: All four cases pass — including the two tricky ones: `[1,3,4], 6 → 2` (beats greedy's 3), and `[1], 0 → 0` (the edge case Option A would have mangled).

The solution is clean and complete. A quick complexity summary:
- **Time:** O(amount × len(coins)) — two nested loops
- **Space:** O(amount) — the dp table

One thing worth noticing: the `default=dp[i]` in the `min(...)` call handles the edge case where *no* coin fits at position `i` (e.g., smallest coin is larger than `i`). Without it, `min()` on an empty generator would raise a `ValueError`. It keeps the sentinel in place instead, which is exactly what we want.

Want to explore the top-down memoized version, or are you happy with this one?

---

## Turn 4 (final)

**User:**

I'm happy with this one. We made the right call on the approach (DP beats greedy for non-canonical coin systems), we caught the subtle initialization bug (0 conflates "not set" with "correct answer 0"), and the tests confirm it works — including the edge cases that would trip up a naive solution.

The sentinel initialization is cleaner than it first looks, and `default=dp[i]` is a nice touch that keeps unreachable states marked properly.

Unless there's something specific about the memoized version you want to see for learning, I think we're done here.

<done/>

---

**Run end**: done after 3 turns (118s)
