from math import comb

N = 20

# --- Closed form -------------------------------------------
# Every route is 2N moves: N rights + N downs, in some order.
answer_cf = comb(2 * N, N)

# --- DP (1-D rolling array, O(N) space) --------------------
# dp[j] = routes to reach current row, column j.
# Invariant: scan left→right so dp[j-1] is already this row's value.
dp = [1] * (N + 1)
for _ in range(N):
    for j in range(1, N + 1):
        dp[j] += dp[j - 1]
answer_dp = dp[N]

# --- Verify & print -----------------------------------------
assert answer_cf == answer_dp
print(f"Grid size : {N}×{N}")
print(f"Closed form  C({2*N},{N}) = {answer_cf:,}")
print(f"DP (1-D rolling)         = {answer_dp:,}")
