def solve(n=100):
    total = 0
    sum_of_squares = 0
    for i in range(1, n + 1):
        total += i
        sum_of_squares += i * i
    return total * total - sum_of_squares

print(solve())
