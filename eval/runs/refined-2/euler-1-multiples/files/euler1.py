def solve_brute(n):
    return sum(x for x in range(n) if x % 3 == 0 or x % 5 == 0)

def sum_multiples(m, n):
    k = (n - 1) // m
    return m * k * (k + 1) // 2

def solve_closed(n):
    return sum_multiples(3, n) + sum_multiples(5, n) - sum_multiples(15, n)

print(solve_brute(1000))
print(solve_closed(1000))
assert solve_brute(1000) == solve_closed(1000), "mismatch!"
print("Both match.")
