def solve(n: int) -> int:
    square_of_sum = (n * (n + 1) // 2) ** 2
    sum_of_squares = n * (n + 1) * (2 * n + 1) // 6
    return square_of_sum - sum_of_squares

print(solve(100))
