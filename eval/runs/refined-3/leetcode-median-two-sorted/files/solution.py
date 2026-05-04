def findMedianSortedArrays(nums1, nums2):
    # Ensure nums1 is the shorter array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    n, m = len(nums1), len(nums2)
    left, right = 0, n

    while left <= right:
        i = (left + right) // 2
        j = (n + m + 1) // 2 - i

        # Sentinel approach for boundary reads
        max_left1  = nums1[i - 1] if i > 0 else float('-inf')
        min_right1 = nums1[i]     if i < n else float('inf')
        max_left2  = nums2[j - 1] if j > 0 else float('-inf')
        min_right2 = nums2[j]     if j < m else float('inf')

        if max_left1 <= min_right2 and max_left2 <= min_right1:
            # Found the partition — compute the median
            if (n + m) % 2 == 1:
                return max(max_left1, max_left2)
            else:
                return (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2
        elif max_left1 > min_right2:
            right = i - 1   # i is too large, move left
        else:
            left = i + 1    # i is too small, move right

    return -1  # unreachable for valid input
