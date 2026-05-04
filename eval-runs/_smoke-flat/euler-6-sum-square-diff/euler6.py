def solve(n: int) -> int:
    # Closed-form: sum of first n integers and sum of squares
    sum_of_n   = n * (n + 1) // 2
    sum_of_sq  = n * (n + 1) * (2 * n + 1) // 6
    return sum_of_n ** 2 - sum_of_sq


# Brute-force for verification
def solve_brute(n: int) -> int:
    return sum(range(1, n + 1)) ** 2 - sum(x**2 for x in range(1, n + 1))


n = 100
answer = solve(n)
assert answer == solve_brute(n), "mismatch!"
print(f"Answer: {answer}")
