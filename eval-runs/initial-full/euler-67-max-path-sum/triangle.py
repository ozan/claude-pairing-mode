triangle = [
    [75],
    [95, 64],
    [17, 47, 82],
    [18, 35, 87, 10],
    [20,  4, 82, 47, 65],
    [19,  1, 23, 75,  3, 34],
    [88,  2, 77, 73,  7, 63, 67],
    [99, 65,  4, 28,  6, 16, 70, 92],
    [41, 41, 26, 56, 83, 40, 80, 70, 33],
    [41, 48, 72, 33, 47, 32, 37, 16, 94, 29],
]


def max_path_sum(tri):
    dp = tri[-1][:]                   # start with a copy of the bottom row
    for row in reversed(tri[:-1]):
        for j, val in enumerate(row):
            dp[j] = val + max(dp[j], dp[j + 1])
    return dp[0]


print(max_path_sum(triangle))
