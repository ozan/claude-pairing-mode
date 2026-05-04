def trap(height):
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0
    while left < right:
        if height[left] <= height[right]:
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1
    return water


# --- tests ---
assert trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6  # LC example 1
assert trap([4, 2, 0, 3, 2, 5])                    == 9  # LC example 2
assert trap([])                                     == 0  # empty
assert trap([3])                                    == 0  # single bar
assert trap([3, 0, 3])                              == 3  # simple valley
assert trap([1, 2, 3, 4, 5])                        == 0  # strictly increasing
print("All tests passed.")
