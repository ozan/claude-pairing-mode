def trap(height: list[int]) -> int:
    n = len(height)
    if n == 0:
        return 0

    left_max = [0] * n
    right_max = [0] * n

    # Pass 1: fill left_max
    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], height[i])

    # Pass 2: fill right_max
    right_max[n - 1] = height[n - 1]
    for i in range(n - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], height[i])

    # Pass 3: accumulate water
    total = 0
    for i in range(n):
        total += min(left_max[i], right_max[i]) - height[i]

    return total


def trap_two_pointer(height: list[int]) -> int:
    lo, hi = 0, len(height) - 1
    left_max, right_max = 0, 0
    water = 0

    while lo <= hi:
        if left_max < right_max:
            left_max = max(left_max, height[lo])
            water += left_max - height[lo]
            lo += 1
        else:
            right_max = max(right_max, height[hi])
            water += right_max - height[hi]
            hi -= 1

    return water


# --- tests ---
cases = [
    ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),
    ([4, 2, 0, 3, 2, 5], 9),
    ([], 0),
    ([3], 0),
    ([3, 3], 0),
]
for height, expected in cases:
    assert trap(height) == expected, f"trap({height}) failed"
    assert trap_two_pointer(height) == expected, f"trap_two_pointer({height}) failed"
print("All tests passed — both implementations agree.")
