a, b = 2, 8
total = 0
while a <= 4_000_000:
    total += a
    a, b = b, 4*b + a
print(total)
