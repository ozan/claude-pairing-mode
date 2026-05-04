def trap(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0

    while left <= right:
        if left_max <= right_max:
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1

    return water


if __name__ == "__main__":
    cases = [
        ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),  # LC example 1
        ([4, 2, 0, 3, 2, 5],                          9),  # LC example 2
        ([3],                                          0),  # single bar
        ([3, 3],                                       0),  # two equal bars
        ([1, 0, 1],                                    1),  # simple valley
    ]
    for heights, expected in cases:
        result = trap(heights)
        status = "✓" if result == expected else "✗"
        print(f"{status} trap({heights}) = {result}  (expected {expected})")
