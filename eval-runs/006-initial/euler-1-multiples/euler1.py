def sum_multiples(k, n):
    m = n // k
    return k * m * (m + 1) // 2

result = (sum_multiples(3, 999)
        + sum_multiples(5, 999)
        - sum_multiples(15, 999))
print(result)
