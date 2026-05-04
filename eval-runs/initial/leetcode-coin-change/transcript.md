# leetcode-coin-change

- Source: `leetcode`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:37:27.562Z

---

## Turn 1

**User:**

Let's solve Leetcode #322, 'Coin Change'. Given coin denominations and a target amount, return the fewest number of coins to make that amount, or -1 if impossible.

**Pair:**

Assistant: Classic DP problem. Before we write any code, let me ask the key algorithmic question first.

Assistant: The `propose_options` tool isn't available in this session, so I'll present this directly.

---

**Key question before writing code: greedy or DP?**

A tempting approach: *always pick the largest coin that fits*, repeat until done. Simple, fast — but it **fails**. Try `coins = [1, 3, 4]`, `amount = 6`:

- Greedy: `4 + 1 + 1 = 3 coins`  
- Optimal: `3 + 3 = 2 coins`

Greedy only works for specific coin systems (like US currency). For the general case, we need **dynamic programming**.

---

**The DP idea:** Build a table `dp[0..amount]` where `dp[i]` = minimum coins to make amount `i`.

- Base case: `dp[0] = 0`
- For every amount `i` from 1 to `amount`, try every coin `c`: if `c <= i`, then `dp[i] = min(dp[i], dp[i - c] + 1)`
- Answer: `dp[amount]`, or `-1` if it stayed at infinity

This is **O(amount × len(coins))** time, **O(amount)** space. Let me write it:

```python
def coinChange(coins: list[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for c in coins:
            if c <= i:
                dp[i] = min(dp[i], dp[i - c] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1
```

---

**Walk-through** with `coins = [1, 3, 4]`, `amount = 6`:

| i | best coin | dp[i] |
|---|-----------|-------|
| 0 | — | 0 |
| 1 | 1 | 1 |
| 2 | 1 | 2 |
| 3 | 3 | 1 |
| 4 | 4 or 1+3 | 1 |
| 5 | 4+1 | 2 |
| 6 | **3+3** | **2** ✓ |

Greedy would've said 3 — the DP correctly finds 2.

---

Want to extend this (e.g. also return *which* coins were used, not just the count), or dig into the top-down memoized version for comparison?

---

## Turn 2

**User:**

Great! I've laid out the DP approach with a concrete example. Now, a couple of directions we could go:

1. **Implement & test it** — write the actual solution to a file, test with a few cases (including edge cases like `amount = 0`, impossible cases, etc.)
2. **Compare approaches** — show the top-down memoized recursion version side-by-side so you see both directions work
3. **Reconstruct the coins** — extend it to also return *which* coins were used, not just the count

Which would be most useful? Or did you want to just run with the solution above and test it yourself?

**Pair:**

Assistant: Let's do **option 1** — writing and testing is the most grounding step. Once the solution is solid against edge cases, the other extensions are easy to layer on.

Let me check the directory first, then write the file.

[Glob(coin_change*)]
  No files found

[Write(coin_change.py)]
def coinChange(coins: list[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for c in coins:
            if c <= i:
                dp[i] = min(dp[i], dp[i - c] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1


… (21 more lines)

[Bash(python coin_change.py)]
  error: Exit code 127

[Bash(python3 coin_change.py)]
  [PASS] coins=[1, 5, 10, 25], amount=36 → 3 (expected 3)
  [PASS] coins=[1, 3, 4], amount=6 → 2 (expected 2)
  [PASS] coins=[2], amount=3 → -1 (expected -1)
  [PASS] coins=[1], amount=0 → 0 (expected 0)
  [PASS] coins=[1], amount=1 → 1 (expected 1)
  [PASS] coins=[186, 419, 83, 408], amount=6249 → 20 (expected 20)
  
  All tests passed!

Assistant: All 6 pass, including the noteworthy ones:

- **`[1,3,4], 6 → 2`** — the greedy trap case ✓  
- **`[2], 3 → -1`** — impossible (no odd coins) ✓  
- **`[1], 0 → 0`** — `dp[0] = 0` base case ✓  
- **Large case** — scales fine, no recursion depth issues ✓

---

One thing worth noticing: the inner loop checks `if c <= i` before using `dp[i - c]`. That guard ensures we never access a negative index. A subtle question —

**is that guard actually necessary, or is there an equally clean way to structure the loops that avoids needing it?**

Hint: think about what changes if you iterate `for i in range(c, amount + 1)` *inside* the coin loop rather than checking at runtime. Same result, slightly different structure. Worth knowing because the "outer loop over coins" shape is the basis for a related problem: the **unbounded knapsack**.

Want to tackle the coin reconstruction extension next (option 3), or curious about that loop-structure variant first?

---

## Turn 3

**User:**

Great hint! Let me try the variant where coins are the outer loop. I can see it — by starting the inner loop at `c`, we never reach `i - c < 0`, so the guard is unnecessary.

Let me write a version with that structure and test it:Perfect! Same results, and cleaner structure. I see the elegance now:

- **Coins outer loop** processes each denomination completely
- **Inner loop starts at `c`** — we're safe from negative indices, no guard needed
- By updating `dp[i]` based on `dp[i - c]` in the same coin iteration, we naturally allow *multiple uses* of the same coin (unbounded), which is why this is the unbounded knapsack pattern

---

Now I'm curious about **option 3: coin reconstruction**. The current solution tells us *how many*, but not *which* coins. Let me try extending it to track that.

The idea: keep a `parent` or `choice` array alongside `dp`. For each amount, record which coin we picked. Then backtrack from `amount` to 0, collecting coins as we go.

Should I write that variant myself based on the idea, or do you want to walk me through the details first?

**Pair:**

Assistant: Go for it — give it a shot. One decision you'll hit: how to write the **backtracking loop**. Quick question on that:

Assistant: The tool's not cooperating, so I'll put it directly:

**Two ways to write the backtracking loop — which would you pick, and why?**

**A — Iterative:**
```python
path = []
cur = amount
while cur > 0:
    path.append(choice[cur])
    cur -= choice[cur]
```

**B — Recursive:**
```python
def reconstruct(cur):
    if cur == 0: return []
    return [choice[cur]] + reconstruct(cur - choice[cur])

path = reconstruct(amount)
```

Both are correct in principle. One has a subtle failure mode for certain inputs — think about what determines the recursion depth in option B, and whether that's bounded.

Go ahead and write your full reconstruction version (your call on A vs B), and we'll test it. I'll weigh in after.

---

## Turn 4 (final)

**User:**

Great question! Let me think through this:

**Option A (iterative)** — keeps a pointer and walks backward step by step. Safe, no recursion stack.

**Option B (recursive)** — each call adds one coin to the result and recurses. The recursion depth depends on **how many coins we actually use**. In the worst case, `amount = 5000` with `coins = [1]` means 5000 recursive calls — you'd hit Python's default recursion limit (~1000) and crash.

**I'd pick A.** It's iterative, safe against large amounts, and has no overhead from list concatenation on each recursive call.

Let me write the full reconstruction version and test it:Perfect! Both versions work. Let me point out what we learned:

**The reconstruction looks solid:**
- `[1, 5, 10, 25], 36 → [25, 10, 1]` ✓ (verified: 25+10+1=36, count=3)
- The greedy-trap case `[1, 3, 4], 6 → [3, 3]` ✓ (2 coins, not 3)
- Impossible case handled cleanly ✓
- Edge case `amount=0` gives empty list ✓

**Why the iterative backtracking (Option A) was right:**

1. **Recursion depth is bounded by the solution size.** Even though in theory we could use up to `amount` coins (all 1-cent), Python's stack limit is ~1000. For large amounts with only small coins available, the recursive version would crash; the iterative version just loops.
   
2. **No list concatenation overhead.** The recursive version builds `[choice[cur]] + reconstruct(...)` on each call, which is O(n) per call. The iterative version appends in O(1).

3. **Clearer logic.** The `while cur > 0` loop directly mirrors the problem: "walk backward from the target to zero, collecting coins."

---

**One more observation:** Look at the large case output: 20 coins reconstructed correctly from `amount=6249`. That's the kind of input where a naive recursive backtracker could actually hit Python's recursion limit!

---

Want to go deeper (e.g., **top-down memoized recursion for contrast**, or **minimum coin path uniqueness**, or extend this to other DP variants)?

<done/>

---

**Run end**: done after 3 turns (155s)
