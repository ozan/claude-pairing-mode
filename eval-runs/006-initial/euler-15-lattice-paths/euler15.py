"""
Project Euler #15 — Lattice paths through a 20×20 grid.

Every route is exactly 40 steps: 20 right + 20 down, in any order.
Count = C(40, 20) = number of ways to choose which 20 steps are "right".

DP insight: dp[i][j] = ways to reach (i,j) = dp[i-1][j] + dp[i][j-1]
This builds Pascal's triangle in 2D, and dp[i][j] == C(i+j, i).
"""

import math


# --- Closed form -----------------------------------------------------------

def closed_form(n: int) -> int:
    """C(2n, n): choose n right-steps from 2n total steps."""
    return math.comb(2 * n, n)


# --- DP: O(n²) space -------------------------------------------------------
# Full grid; dp[i][j] = ways to reach cell (i, j).
# Invariant: dp[i][j] == C(i+j, i) — Pascal's triangle in 2D.

def routes_grid(n: int) -> int:
    dp = [[1] * (n + 1) for _ in range(n + 1)]   # top row & left col = 1
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[n][n]


# --- DP: O(n) space --------------------------------------------------------
# Collapse the grid to one row, updated left-to-right each pass.
#   row[j]   BEFORE update == dp[i-1][j]  ("above"  in the full grid)
#   row[j-1] AFTER  update == dp[i][j-1]  ("left"   in the full grid)

def routes_row(n: int) -> int:
    row = [1] * (n + 1)
    for _ in range(1, n + 1):
        for j in range(1, n + 1):
            row[j] += row[j - 1]
    return row[n]


# --- Trace helper -----------------------------------------------------------

def print_grid(n: int) -> None:
    """Print the full DP table for small n, confirming dp[i][j] == C(i+j,i)."""
    dp = [[1] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

    col_w = max(len(str(dp[n][n])), 3) + 1
    print(f"\n  dp table for {n}×{n}  (dp[i][j] = C(i+j, i)):\n")
    for i, row in enumerate(dp):
        row_str = "".join(f"{v:{col_w}}" for v in row)
        print(f"  row {i}: {row_str}")
    print()


# --- Verify & print --------------------------------------------------------

if __name__ == "__main__":
    # Side-by-side trace on a small grid
    print_grid(4)

    # Both DP versions and closed form must agree on n=20
    n = 20
    cf   = closed_form(n)
    grid = routes_grid(n)
    row  = routes_row(n)

    print(f"Grid size        : {n}×{n}")
    print(f"Closed form      : C({2*n},{n}) = {cf:,}")
    print(f"DP (O(n²) space) : {grid:,}")
    print(f"DP (O(n)  space) : {row:,}")
    print(f"All match        : {cf == grid == row}")

    print("\nSmall grids — C(2n,n):")
    for k in range(1, 6):
        print(f"  {k}×{k} : {closed_form(k):>6,}")
