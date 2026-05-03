def two_sum(nums: list[int], target: int) -> list[int]:
    """
    Find two distinct indices of numbers that sum to target.
    Time: O(n), Space: O(n).
    """
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    raise ValueError("No solution")
