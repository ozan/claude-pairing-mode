def climb_stairs(n: int) -> int:
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b


if __name__ == "__main__":
    cases = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 5),
        (5, 8),
        (10, 89),
    ]
    for n, expected in cases:
        result = climb_stairs(n)
        status = "✓" if result == expected else "✗"
        print(f"{status} climb_stairs({n}) = {result}  (expected {expected})")
