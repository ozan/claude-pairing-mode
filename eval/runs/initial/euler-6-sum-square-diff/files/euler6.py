n = 100
sum_of_sq = sum(i*i for i in range(1, n+1))
sq_of_sum = sum(range(1, n+1)) ** 2
print(sq_of_sum - sum_of_sq)
