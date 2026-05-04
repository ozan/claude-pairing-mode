with open("triangle.txt") as f:
    triangle = [list(map(int, line.split())) for line in f]

dp = [row[:] for row in triangle]

for i in range(len(dp) - 2, -1, -1):
    for j in range(len(dp[i])):
        dp[i][j] += max(dp[i + 1][j], dp[i + 1][j + 1])

print(dp[0][0])

# Recover the path by re-reading decisions from the DP table
path = []
j = 0
for i in range(len(triangle)):
    path.append(triangle[i][j])
    if i < len(triangle) - 1:
        j += 0 if dp[i + 1][j] >= dp[i + 1][j + 1] else 1

print(" → ".join(map(str, path)))
