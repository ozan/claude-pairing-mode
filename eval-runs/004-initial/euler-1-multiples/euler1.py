def sum_multiples(k, n):
    m = (n - 1) // k
    return k * m * (m + 1) // 2

result = (sum_multiples(3, 1000)
        + sum_multiples(5, 1000)
        - sum_multiples(15, 1000))
print(result)
