def d(n):
    if n < 2:
        return 0
    total = 1
    i = 2
    while i * i <= n:
        if n % i == 0:
            total += i + (n // i if n // i != i else 0)
        i += 1
    return total

print(sum(
    n for n in range(2, 10000)
    if (dn := d(n)) != n and d(dn) == n
))
