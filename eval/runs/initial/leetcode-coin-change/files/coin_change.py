def coinChange(coins: list[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1


# --- quick tests ---
assert coinChange([1, 5, 10, 25], 36) == 3   # 25 + 10 + 1
assert coinChange([1, 5, 10, 25], 30) == 2   # 25 + 5
assert coinChange([2], 3) == -1              # impossible
assert coinChange([1], 0) == 0              # zero amount
assert coinChange([5], 5) == 1              # exact match
print("All tests passed.")
