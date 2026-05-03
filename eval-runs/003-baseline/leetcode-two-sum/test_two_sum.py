import pytest
from two_sum import two_sum

@pytest.mark.parametrize("nums,target,expected", [
    ([2, 7, 11, 15], 9, [0, 1]),
    ([3, 3], 6, [0, 1]),
    ([3, 2, 4], 6, [1, 2]),
    ([-1, -2, -3, 5, 10], 7, [2, 4]),
])
def test_two_sum(nums, target, expected):
    result = two_sum(nums, target)
    assert result == expected
    # Verify the values at those indices actually sum to target
    assert nums[result[0]] + nums[result[1]] == target

def test_no_solution():
    with pytest.raises(ValueError):
        two_sum([1, 2, 3], 10)
