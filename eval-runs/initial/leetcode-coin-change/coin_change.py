def coinChange(coins: list[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for c in coins:
            if c <= i:
                dp[i] = min(dp[i], dp[i - c] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1


if __name__ == "__main__":
    cases = [
        # (coins, amount, expected)
        ([1, 5, 10, 25], 36,  3),   # 25+10+1
        ([1, 3, 4],      6,   2),   # 3+3, greedy trap
        ([2],            3,  -1),   # impossible
        ([1],            0,   0),   # amount = 0
        ([1],            1,   1),   # single coin exact
        ([186, 419, 83, 408], 6249, 20),  # larger case
    ]

    all_pass = True
    for coins, amount, expected in cases:
        result = coinChange(coins, amount)
        status = "PASS" if result == expected else "FAIL"
        if status == "FAIL":
            all_pass = False
        print(f"[{status}] coins={coins}, amount={amount} → {result} (expected {expected})")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED.")
