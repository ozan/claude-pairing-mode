nums = range(1, 101)
sum_of_squares = sum(x**2 for x in nums)
square_of_sum  = sum(nums) ** 2
print(square_of_sum - sum_of_squares)
