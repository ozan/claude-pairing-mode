def maxCoins(nums):
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]

    # dp[l][r] = max coins bursting all balloons strictly between l and r
    # recurrence: try each k as last balloon to burst in (l, r)
    #   dp[l][r] = max(dp[l][k] + nums[l]*nums[k]*nums[r] + dp[k][r])

    for length in range(2, n):
        for l in range(0, n - length):
            r = l + length
            for k in range(l + 1, r):
                dp[l][r] = max(dp[l][r],
                    dp[l][k] + nums[l]*nums[k]*nums[r] + dp[k][r])
    return dp[0][n - 1]
