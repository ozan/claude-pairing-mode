total = 0
sum_sq = 0
for i in range(1, 101):
    total += i
    sum_sq += i**2
print(total**2 - sum_sq)
