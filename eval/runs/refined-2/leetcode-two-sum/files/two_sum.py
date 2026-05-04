def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i


# Tests
print(two_sum([2, 7, 11, 15], 9))   # expect [0, 1]
print(two_sum([3, 2, 4], 6))        # expect [1, 2]
print(two_sum([3, 3], 6))           # expect [0, 1]
