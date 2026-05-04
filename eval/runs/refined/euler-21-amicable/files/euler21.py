def d(n):
    s, i = 1, 2
    while i * i <= n:
        if n % i == 0:
            s += i
            if n // i != i:
                s += n // i
        i += 1
    return s

def solve():
    limit = 10000
    ds = [d(n) for n in range(limit)]
    return sum(n for n in range(2, limit)
               if ds[n] != n and ds[n] < limit and ds[ds[n]] == n)

print(solve())
