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

ds = [d(n) for n in range(10000)]
print(sum(
    a for a in range(1, 10000)
    if ds[a] < 10000 and ds[ds[a]] == a and ds[a] != a
))
