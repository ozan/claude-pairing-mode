def coinChange(coins: list[int], amount: int) -> int:
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for c in coins:
            if c <= i:
                dp[i] = min(dp[i], dp[i - c] + 1)

    return dp[amount] if dp[amount] <= amount else -1


# --- tests ---
assert coinChange([1, 5, 6, 9], 11) == 2   # 5+6
assert coinChange([1, 3, 4], 6) == 2        # 3+3  (greedy would give 3)
assert coinChange([2], 3) == -1             # impossible
assert coinChange([1], 0) == 0              # base case
assert coinChange([1, 2, 5], 11) == 3       # 5+5+1
print("All tests passed.")
