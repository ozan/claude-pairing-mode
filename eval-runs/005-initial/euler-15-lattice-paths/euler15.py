import math

n = 20

# --- DP approach ---
dp = [[1] * (n + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    for j in range(1, n + 1):
        dp[i][j] = dp[i-1][j] + dp[i][j-1]

dp_answer = dp[n][n]

# --- Closed form ---
closed_answer = math.comb(2 * n, n)

print(f"DP:         {dp_answer}")
print(f"C(40, 20):  {closed_answer}")
print(f"Match: {dp_answer == closed_answer}")
