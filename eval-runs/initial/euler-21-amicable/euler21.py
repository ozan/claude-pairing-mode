import math

def d(n):
    """Sum of proper divisors of n, in O(sqrt(n))."""
    if n <= 1:
        return 0
    s = 1  # 1 is always a proper divisor for n > 1
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            s += i
            if i * i != n:       # avoid double-counting perfect-square roots
                s += n // i
    return s

total = 0
for a in range(2, 10_000):
    b = d(a)
    if b != a and d(b) == a:    # amicable: d(a)=b, d(b)=a, a≠b
        total += a

print(total)
