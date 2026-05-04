from math import comb

def dp_routes(n: int) -> int:
    """Count lattice paths through an n×n grid (right/down only) via DP."""
    # dp[i][j] = number of routes to reach cell (i, j)
    # Row 0 and col 0 are all 1s: only one way to reach any edge cell.
    dp = [[1] * (n + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

    return dp[n][n]


def closed_form_routes(n: int) -> int:
    """C(2n, n): choose which n of 2n steps go right."""
    return comb(2 * n, n)


if __name__ == "__main__":
    n = 20
    dp_answer = dp_routes(n)
    cf_answer = closed_form_routes(n)

    print(f"Grid size : {n}×{n}")
    print(f"DP answer : {dp_answer:,}")
    print(f"C(40,20)  : {cf_answer:,}")
    assert dp_answer == cf_answer, "Mismatch!"
    print("Both agree ✓")

    # Show the filled grid for a small example so the Pascal structure is visible
    small = 4
    dp_small = [[1] * (small + 1) for _ in range(small + 1)]
    for i in range(1, small + 1):
        for j in range(1, small + 1):
            dp_small[i][j] = dp_small[i - 1][j] + dp_small[i][j - 1]

    print(f"\nDP grid for {small}×{small} (rows = down, cols = right):")
    for row in dp_small:
        print("  " + "  ".join(f"{v:3}" for v in row))
