def solve(limit=4_000_000):
    a, b = 2, 8  # First two even Fibonacci numbers
    total = 0
    while a <= limit:
        total += a
        a, b = b, 4 * b + a
    return total

print(solve())
