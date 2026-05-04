from typing import List


def findMedianSortedArrays(nums1: List[int], nums2: List[int]) -> float:
    # Always binary search on the smaller array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    half = (m + n + 1) // 2

    lo, hi = 0, m
    while lo <= hi:
        i = (lo + hi) // 2   # cut in nums1: i elements on the left
        j = half - i          # cut in nums2: j elements on the left

        nums1_left  = float('-inf') if i == 0 else nums1[i - 1]
        nums1_right = float('inf')  if i == m else nums1[i]
        nums2_left  = float('-inf') if j == 0 else nums2[j - 1]
        nums2_right = float('inf')  if j == n else nums2[j]

        if nums1_left <= nums2_right and nums2_left <= nums1_right:
            # --- correct partition found ---
            max_left = max(nums1_left, nums2_left)
            if (m + n) % 2 == 1:
                return float(max_left)
            return (max_left + min(nums1_right, nums2_right)) / 2.0
        elif nums1_left > nums2_right:
            hi = i - 1   # i too large, move left
        else:
            lo = i + 1   # i too small, move right

    return 0.0
