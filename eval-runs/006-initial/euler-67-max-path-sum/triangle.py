triangle = [
    [3],
    [7, 4],
    [2, 4, 6],
    [8, 5, 9, 3],
    [2, 1, 8, 2, 5],
    [6, 5, 3, 4, 7, 1],
    [4, 2, 7, 3, 8, 6, 2],
    [9, 1, 5, 8, 2, 4, 7, 3],
    [3, 6, 2, 7, 5, 1, 9, 4, 8],
    [8, 4, 6, 3, 9, 2, 7, 5, 1, 6],
]

# Bottom-up DP: work from second-to-last row upward.
# Each cell absorbs the better of its two children.
dp = [row[:] for row in triangle]          # copy so we don't mutate the input

for r in range(len(dp) - 2, -1, -1):      # rows n-2 down to 0
    for c in range(len(dp[r])):
        dp[r][c] += max(dp[r + 1][c], dp[r + 1][c + 1])

print(dp[0][0])   # answer bubbles up to the apex
