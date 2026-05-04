def sum_primes_below(n):
    # Sieve of Eratosthenes
    sieve = bytearray([1]) * n   # sieve[i] == 1 means i is (still) prime
    sieve[0] = sieve[1] = 0

    p = 2
    while p * p < n:
        if sieve[p]:
            # All multiples of p below p*p were already marked by smaller primes
            sieve[p * p :: p] = bytearray(len(sieve[p * p :: p]))
        p += 1

    return sum(i for i, is_prime in enumerate(sieve) if is_prime)


if __name__ == "__main__":
    result = sum_primes_below(2_000_000)
    print(result)
