n = 100
total = sum(range(1, n+1))
sum_sq = sum(i*i for i in range(1, n+1))
print(total**2 - sum_sq)
