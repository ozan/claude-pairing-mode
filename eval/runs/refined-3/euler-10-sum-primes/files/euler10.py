def sieve(limit):
    is_prime = [True] * limit
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(limit**0.5) + 1):
        if is_prime[p]:
            for m in range(p*p, limit, p):
                is_prime[m] = False
    return sum(i for i, v in enumerate(is_prime) if v)

print(sieve(2_000_000))
