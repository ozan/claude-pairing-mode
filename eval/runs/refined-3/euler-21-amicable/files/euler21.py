LIMIT = 10001

# Sieve: d[n] = sum of proper divisors of n
d = [0] * LIMIT
for i in range(1, LIMIT // 2 + 1):
    for j in range(2 * i, LIMIT, i):
        d[j] += i

total = sum(
    n for n in range(2, LIMIT)
    if d[n] != n and d[n] < LIMIT and d[d[n]] == n
)

print(total)
