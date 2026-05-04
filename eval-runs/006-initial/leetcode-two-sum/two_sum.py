def two_sum(nums, target):
    seen = {}
    for i, val in enumerate(nums):
        comp = target - val
        if comp in seen:
            return [seen[comp], i]
        seen[val] = i


if __name__ == "__main__":
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum([3, 2, 4], 6) == [1, 2]
    assert two_sum([3, 3], 6) == [0, 1]
    print("All tests passed.")
