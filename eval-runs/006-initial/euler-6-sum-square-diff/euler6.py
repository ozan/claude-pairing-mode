def solve(n: int) -> int:
    sum_of = n * (n + 1) // 2
    sum_of_sq = n * (n + 1) * (2 * n + 1) // 6
    return sum_of ** 2 - sum_of_sq

print(solve(100))
