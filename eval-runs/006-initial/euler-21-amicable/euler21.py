def d(n):
    if n == 1:
        return 0
    total = 1  # 1 always divides n (for n > 1)
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            total += i
            if i != n // i:
                total += n // i
    return total


amicable = set()
for a in range(2, 10000):
    b = d(a)
    if b != a and b < 10000 and d(b) == a:
        amicable.add(a)
        amicable.add(b)

print(sum(amicable))
