def climb_stairs(n: int) -> int:
    """Distinct ways to climb n stairs taking 1 or 2 at a time. Requires n >= 1."""
    a, b = 1, 2
    for _ in range(n - 1):
        a, b = b, a + b
    return a
