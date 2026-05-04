def solve(n):
    return sum(x for x in range(n) if x % 3 == 0 or x % 5 == 0)

print(solve(1000))
