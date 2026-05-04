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
    ([1],            0),    # 0 coins   = 0
]

for coins, amount in cases:
    print(f"coins={coins}, amount={amount} -> {coinChange(coins, amount)}")
