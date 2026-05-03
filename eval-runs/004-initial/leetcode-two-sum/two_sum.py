def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i

if __name__ == "__main__":
    assert set(two_sum([2, 7, 11, 15], 9)) == {0, 1}
    assert set(two_sum([3, 2, 4], 6)) == {1, 2}
    assert set(two_sum([3, 3], 6)) == {0, 1}
    print("all tests passed")
