def solve_loop(limit=1000):
    return sum(x for x in range(limit) if x % 3 == 0 or x % 5 == 0)

def sum_multiples(k, limit):
    m = (limit - 1) // k
    return k * m * (m + 1) // 2

def solve_formula(limit=1000):
    return sum_multiples(3, limit) + sum_multiples(5, limit) - sum_multiples(15, limit)

print(solve_loop())    # 233168
print(solve_formula()) # 233168 — same answer, O(1)
