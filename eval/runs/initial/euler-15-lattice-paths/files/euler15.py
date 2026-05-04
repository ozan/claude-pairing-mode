import math


def count_paths_dp(n: int) -> int:
    """Count lattice paths through an n×n grid (right/down only) using a
    1D rolling array.  dp[j] starts each outer iteration holding the path
    count for the row above; updating left-to-right folds in the left
    neighbour from the current row, so no 2D table is needed.  O(n) space."""
    dp = [1] * (n + 1)          # base case: top row all 1s
    for _ in range(1, n + 1):   # iterate over rows 1..n
        for j in range(1, n + 1):
            dp[j] += dp[j - 1]  # above (dp[j] old) + left (dp[j-1] new)
    return dp[n]


def count_paths_combinatorial(n: int) -> int:
    """Any path is 2n moves: choose n of them to be rightward → C(2n, n)."""
    return math.comb(2 * n, n)


if __name__ == "__main__":
    n = 20
    dp_ans   = count_paths_dp(n)
    comb_ans = count_paths_combinatorial(n)

    print(f"DP answer:            {dp_ans:,}")
    print(f"Combinatorial answer: {comb_ans:,}")

    assert dp_ans == comb_ans, "mismatch!"
    print("✓ Both agree.")
