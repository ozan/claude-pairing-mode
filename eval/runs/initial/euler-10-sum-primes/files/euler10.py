LIMIT = 2_000_000
sieve = bytearray([1]) * LIMIT
sieve[0] = sieve[1] = 0

for p in range(2, int(LIMIT**0.5) + 1):
    if sieve[p]:
        sieve[p*p::p] = bytearray(len(sieve[p*p::p]))

print(sum(i for i, v in enumerate(sieve) if v))
