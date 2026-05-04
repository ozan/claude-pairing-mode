def sum_primes(limit):
    sieve = bytearray([1]) * limit
    sieve[0] = sieve[1] = 0
    for p in range(2, int(limit**0.5) + 1):
        if sieve[p]:
            for m in range(p*p, limit, p):
                sieve[m] = 0
    return sum(i for i, v in enumerate(sieve) if v)

print(sum_primes(2_000_000))
