from math import comb

n = 20

# DP approach: dp[i][j] = number of routes to cell (i, j)
# from top-left, moving only right or down.
# Base: dp[0][j] = dp[i][0] = 1 (single path along each edge)
# Recurrence: dp[i][j] = dp[i-1][j] + dp[i][j-1]
dp = [[1] * (n + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    for j in range(1, n + 1):
        dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

dp_answer = dp[n][n]

# Closed-form: choose 20 "right" steps out of 40 total steps
closed_form_answer = comb(2 * n, n)

print(f"DP answer:          {dp_answer}")
print(f"Closed-form C(40,20): {closed_form_answer}")
assert dp_answer == closed_form_answer, "Mismatch!"
print("Both agree ✓")
