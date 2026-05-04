def solve(n):
    total = sum(range(1, n+1))
    sum_sq = sum(i**2 for i in range(1, n+1))
    return total**2 - sum_sq

print(solve(100))
