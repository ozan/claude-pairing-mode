def trap(height: list[int]) -> int:
    """O(n) time, O(n) space — precompute left/right max arrays."""
    n = len(height)
    if n < 3:
        return 0

    # left_max[i] = tallest bar in height[0..i]
    left_max = [0] * n
    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], height[i])

    # right_max[i] = tallest bar in height[i..n-1]
    right_max = [0] * n
    right_max[-1] = height[-1]
    for i in range(n - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], height[i])

    # water at i is bounded by the shorter of the two tallest bars
    water = 0
    for i in range(n):
        water += min(left_max[i], right_max[i]) - height[i]

    return water


def trap_two_pointer(height: list[int]) -> int:
    """O(n) time, O(1) space — collapse the max arrays into two running vars.

    Invariant: process whichever side has the smaller running max.
    We know that side's constraint exactly; the other side is >= it,
    so min(...) resolves to the side we're on.
    """
    if len(height) < 3:
        return 0

    lo, hi = 0, len(height) - 1
    left_max = right_max = 0
    water = 0

    while lo < hi:
        left_max  = max(left_max,  height[lo])
        right_max = max(right_max, height[hi])

        if left_max <= right_max:
            water += left_max - height[lo]   # left side is the constraint
            lo += 1
        else:
            water += right_max - height[hi]  # right side is the constraint
            hi -= 1

    return water


# ── quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cases = [
        ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),  # LC example 1
        ([4, 2, 0, 3, 2, 5],                   9),  # LC example 2
        ([3],                                  0),  # single bar
        ([],                                   0),  # empty
        ([3, 0, 3],                             3),  # simple valley
    ]
    for heights, expected in cases:
        r1 = trap(heights)
        r2 = trap_two_pointer(heights)
        s1 = "✓" if r1 == expected else f"✗ (got {r1})"
        s2 = "✓" if r2 == expected else f"✗ (got {r2})"
        print(f"trap({heights}): dp={r1} {s1}  two_ptr={r2} {s2}")
