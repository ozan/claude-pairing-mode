import math

def sum_primes(limit):
    sieve = bytearray([1]) * limit
    sieve[0] = sieve[1] = 0

    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            for multiple in range(p * p, limit, p):
                sieve[multiple] = 0

    return sum(i for i in range(2, limit) if sieve[i])

print(sum_primes(2_000_000))
