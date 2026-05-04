total = 0
a, b = 2, 8          # first two even Fibonacci numbers
while a <= 4_000_000:
    total += a
    a, b = b, 4*b + a

print(total)
