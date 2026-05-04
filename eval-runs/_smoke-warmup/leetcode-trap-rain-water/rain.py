def trap(heights: list[int]) -> int:
    n = len(heights)
    if n < 3:
        return 0

    # max_left[i]  = tallest bar from index 0 .. i  (inclusive)
    max_left = [0] * n
    max_left[0] = heights[0]
    for i in range(1, n):
        max_left[i] = max(heights[i], max_left[i - 1])

    # max_right[i] = tallest bar from index i .. n-1 (inclusive)
    max_right = [0] * n
    max_right[n - 1] = heights[n - 1]
    for i in range(n - 2, -1, -1):
        max_right[i] = max(heights[i], max_right[i + 1])

    # water above bar i = min(left_wall, right_wall) - bar height
    total = 0
    for i in range(n):
        total += min(max_left[i], max_right[i]) - heights[i]

    return total


# ── tests ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cases = [
        ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),  # LC example 1
        ([4, 2, 0, 3, 2, 5],                   9),  # LC example 2
        ([3, 0, 3],                             3),  # single valley
        ([1, 2, 3],                             0),  # strictly increasing
        ([3, 2, 1],                             0),  # strictly decreasing
        ([],                                    0),  # empty
        ([5],                                   0),  # single bar
    ]
    for heights, expected in cases:
        result = trap(heights)
        status = "✓" if result == expected else f"✗ (got {result})"
        print(f"{status}  trap({heights}) = {expected}")
