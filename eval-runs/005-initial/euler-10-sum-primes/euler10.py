from math import isqrt

def sum_primes_below(limit: int) -> int:
    sieve = bytearray([1]) * limit
    sieve[0] = sieve[1] = 0
    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            sieve[p * p :: p] = bytearray(len(sieve[p * p :: p]))
    return sum(i for i, v in enumerate(sieve) if v)

print(sum_primes_below(2_000_000))
