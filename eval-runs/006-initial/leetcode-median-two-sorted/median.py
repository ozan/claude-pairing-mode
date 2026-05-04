def findMedianSortedArrays(nums1, nums2):
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1  # ensure nums1 is smaller

    m, n = len(nums1), len(nums2)
    lo, hi = 0, m

    while lo <= hi:
        i = (lo + hi) // 2
        j = (m + n + 1) // 2 - i

        # boundary values with sentinels
        nums1_left  = nums1[i-1] if i > 0 else float('-inf')
        nums1_right = nums1[i]   if i < m else float('inf')
        nums2_left  = nums2[j-1] if j > 0 else float('-inf')
        nums2_right = nums2[j]   if j < n else float('inf')

        if nums1_left <= nums2_right and nums2_left <= nums1_right:
            if (m + n) % 2 == 0:
                return (max(nums1_left, nums2_left) + min(nums1_right, nums2_right)) / 2
            else:
                return float(max(nums1_left, nums2_left))
        elif nums1_left > nums2_right:
            hi = i - 1
        else:
            lo = i + 1


# --- tests ---
cases = [
    ([1, 3],    [2],       2.0),
    ([1, 2],    [3, 4],    2.5),
    ([0, 0],    [0, 0],    0.0),
    ([],        [1],       1.0),
    ([2],       [],        2.0),
    ([1, 3],    [2, 7],    2.5),
    ([1,2,3,4], [5,6,7,8], 4.5),
]

for nums1, nums2, expected in cases:
    result = findMedianSortedArrays(nums1, nums2)
    status = "✓" if result == expected else "✗"
    print(f"{status}  nums1={nums1}, nums2={nums2}  → {result}  (expected {expected})")
