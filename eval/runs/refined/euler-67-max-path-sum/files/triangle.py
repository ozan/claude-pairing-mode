triangle = [
    [3],
    [7, 4],
    [2, 4, 6],
    [8, 5, 9, 3],
    [20, 4, 82, 47, 65],
    [19, 1, 23, 75, 3, 34],
    [88, 2, 77, 73, 7, 63, 67],
    [99, 65, 4, 28, 6, 16, 70, 92],
    [41, 41, 26, 56, 83, 40, 80, 70, 33],
    [41, 48, 72, 33, 47, 32, 37, 16, 94, 29],
]

def max_path_sum(tri):
    dp = tri[-1][:]          # start with a copy of the bottom row
    for i in range(len(tri) - 2, -1, -1):
        for j in range(len(tri[i])):
            dp[j] = tri[i][j] + max(dp[j], dp[j + 1])
    return dp[0]

print(max_path_sum(triangle))
