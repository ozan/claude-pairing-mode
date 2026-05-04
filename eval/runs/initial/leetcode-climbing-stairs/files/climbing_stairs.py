def climb_stairs(n: int) -> int:
    dp = [0] * (n + 1)
    dp[0], dp[1] = 1, 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]


# Tests
if __name__ == "__main__":
    cases = [(1, 1), (2, 2), (3, 3), (4, 5), (5, 8), (10, 89)]
    for n, expected in cases:
        result = climb_stairs(n)
        status = "OK" if result == expected else f"FAIL (got {result})"
        print(f"n={n}: {result} [{status}]")
