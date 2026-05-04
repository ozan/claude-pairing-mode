def solve(n: int) -> int:
    s = n * (n + 1) // 2
    sq = n * (n + 1) * (2 * n + 1) // 6
    return s * s - sq


print(solve(100))
