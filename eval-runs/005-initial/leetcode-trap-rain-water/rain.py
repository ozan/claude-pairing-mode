def trap(height: list[int]) -> int:
    if not height:
        return 0
    lo, hi = 0, len(height) - 1
    max_left, max_right = height[lo], height[hi]
    water = 0

    while lo < hi:
        if max_left <= max_right:
            lo += 1
            max_left = max(max_left, height[lo])
            water += max_left - height[lo]
        else:
            hi -= 1
            max_right = max(max_right, height[hi])
            water += max_right - height[hi]

    return water


if __name__ == "__main__":
    cases = [
        ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),
        ([4, 2, 0, 3, 2, 5], 9),
        ([3], 0),
        ([], 0),
        ([1, 1], 0),
    ]
    for height, expected in cases:
        result = trap(height)
        status = "✓" if result == expected else f"✗ (expected {expected})"
        print(f"trap({height}) = {result}  {status}")
