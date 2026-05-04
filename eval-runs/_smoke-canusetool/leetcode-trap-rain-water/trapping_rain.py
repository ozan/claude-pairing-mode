def trap(heights: list[int]) -> int:
    n = len(heights)
    if n < 3:
        return 0

    # left_max[i] = tallest bar from index 0 to i (inclusive)
    left_max = [0] * n
    left_max[0] = heights[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], heights[i])

    # right_max[i] = tallest bar from index i to n-1 (inclusive)
    right_max = [0] * n
    right_max[-1] = heights[-1]
    for i in range(n - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], heights[i])

    # water at i is bounded by the shorter wall, minus the bar itself
    water = 0
    for i in range(n):
        water += max(0, min(left_max[i], right_max[i]) - heights[i])

    return water


if __name__ == "__main__":
    cases = [
        ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),  # LC example 1
        ([4, 2, 0, 3, 2, 5],                           9),  # LC example 2
        ([3],                                           0),  # single bar
        ([3, 3],                                        0),  # no gap
        ([0, 0, 0],                                     0),  # all flat
    ]
    for heights, expected in cases:
        result = trap(heights)
        status = "✓" if result == expected else f"✗ (expected {expected})"
        print(f"trap({heights}) = {result}  {status}")
