def sum_primes_below(n):
    sieve = bytearray([1]) * n
    sieve[0] = sieve[1] = 0
    for p in range(2, int(n**0.5) + 1):
        if sieve[p]:
            for i in range(p*p, n, p):
                sieve[i] = 0
    return sum(i for i, v in enumerate(sieve) if v)

print(sum_primes_below(2_000_000))
