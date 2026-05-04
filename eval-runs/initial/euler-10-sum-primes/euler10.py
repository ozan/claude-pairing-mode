import timeit

def sieve_python_loop(n):
    """Original: list[bool] + Python for-loop."""
    if n <= 2:
        return 0
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(n**0.5) + 1):
        if is_prime[p]:
            for i in range(p*p, n, p):
                is_prime[i] = False
    return sum(i for i in range(n) if is_prime[i])

def sieve_list_slice(n):
    """list[bool] + C-level slice assignment."""
    if n <= 2:
        return 0
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(n**0.5) + 1):
        if is_prime[p]:
            is_prime[p*p::p] = [False] * len(is_prime[p*p::p])
    return sum(i for i in range(n) if is_prime[i])

def sieve_bytearray(n):
    """bytearray + C-level slice assignment."""
    if n <= 2:
        return 0
    is_prime = bytearray([1]) * n
    is_prime[0] = is_prime[1] = 0
    for p in range(2, int(n**0.5) + 1):
        if is_prime[p]:
            is_prime[p*p::p] = b'\x00' * len(is_prime[p*p::p])
    return sum(i for i, v in enumerate(is_prime) if v)

N = 2_000_000
assert sieve_python_loop(N) == sieve_list_slice(N) == sieve_bytearray(N) == 142913828922

for name, fn in [("python loop ", sieve_python_loop),
                 ("list + slice", sieve_list_slice),
                 ("bytearray   ", sieve_bytearray)]:
    t = timeit.timeit(lambda f=fn: f(N), number=5) / 5
    print(f"{name}  {t*1000:.1f} ms")
