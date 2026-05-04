def sum_multiples(k, limit):
    n = (limit - 1) // k
    return k * n * (n + 1) // 2

print(sum_multiples(3, 1000) + sum_multiples(5, 1000) - sum_multiples(15, 1000))
