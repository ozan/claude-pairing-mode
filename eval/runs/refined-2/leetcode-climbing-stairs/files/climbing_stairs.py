def climb_stairs(n: int) -> int:
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


if __name__ == "__main__":
    tests = [(1, 1), (2, 2), (3, 3), (4, 5), (5, 8), (10, 89)]
    for n, expected in tests:
        result = climb_stairs(n)
        status = "✓" if result == expected else "✗"
        print(f"{status} n={n}: got {result}, expected {expected}")
