def d(n):
    s, i = 1, 2
    while i * i <= n:
        if n % i == 0:
            s += i + (n // i if n // i != i else 0)
        i += 1
    return s if n > 1 else 0

total = 0
for n in range(2, 10000):
    b = d(n)
    if b != n and d(b) == n:
        total += n

print(total)
