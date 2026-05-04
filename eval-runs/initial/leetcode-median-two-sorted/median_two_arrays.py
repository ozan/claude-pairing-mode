from typing import List


def findMedianSortedArrays(nums1: List[int], nums2: List[int]) -> float:
    # Always binary search on the smaller array
    A, B = nums1, nums2
    if len(A) > len(B):
        A, B = B, A

    n, m = len(A), len(B)
    half = (n + m + 1) // 2  # size of the "left half"

    lo, hi = 0, n
    while lo <= hi:
        i = (lo + hi) // 2   # partition index in A
        j = half - i          # partition index in B (forced)

        # Sentinel values handle empty sub-partitions cleanly
        left_a  = A[i - 1] if i > 0 else float('-inf')
        left_b  = B[j - 1] if j > 0 else float('-inf')
        right_a = A[i]     if i < n else float('inf')
        right_b = B[j]     if j < m else float('inf')

        if left_a <= right_b and left_b <= right_a:
            # Valid partition found
            left_max  = max(left_a, left_b)
            right_min = min(right_a, right_b)
            if (n + m) % 2 == 1:
                return float(left_max)
            else:
                return (left_max + right_min) / 2.0
        elif left_a > right_b:
            hi = i - 1  # i is too large, move left
        else:
            lo = i + 1  # i is too small, move right

    raise ValueError("Input arrays are not sorted")


# --- tests ---
assert findMedianSortedArrays([1, 3], [2])       == 2.0
assert findMedianSortedArrays([1, 2], [3, 4])    == 2.5
assert findMedianSortedArrays([], [1])            == 1.0
assert findMedianSortedArrays([2], [])            == 2.0
assert findMedianSortedArrays([0, 0], [0, 0])    == 0.0
assert findMedianSortedArrays([1, 3], [2, 7])    == 2.5
print("All tests passed.")
