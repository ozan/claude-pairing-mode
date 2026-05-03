def find_median_sorted_arrays(nums1: list[int], nums2: list[int]) -> float:
    # Always binary search the shorter array (Decision 1)
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    m, n = len(nums1), len(nums2)
    half = (m + n + 1) // 2  # left partition size (rounds up for odd totals)

    lo, hi = 0, m
    while lo <= hi:
        i = (lo + hi) // 2   # partition index in nums1
        j = half - i          # partition index in nums2

        # Sentinel values handle i=0, i=m, j=0, j=n (Decision 2)
        max_left1  = float('-inf') if i == 0 else nums1[i - 1]
        min_right1 = float('inf')  if i == m else nums1[i]
        max_left2  = float('-inf') if j == 0 else nums2[j - 1]
        min_right2 = float('inf')  if j == n else nums2[j]

        # Valid partition: cross-array constraint (Decision 3)
        if max_left1 <= min_right2 and max_left2 <= min_right1:
            if (m + n) % 2 == 1:
                return float(max(max_left1, max_left2))
            else:
                return (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2
        elif max_left1 > min_right2:
            hi = i - 1  # i too far right, move left
        else:
            lo = i + 1  # i too far left, move right

    raise ValueError("Input arrays are not sorted")


if __name__ == "__main__":
    cases = [
        ([1, 3],       [2],          2.0),   # odd total
        ([1, 2],       [3, 4],       2.5),   # even total
        ([0, 0],       [0, 0],       0.0),   # all zeros
        ([],           [1],          1.0),   # empty nums1
        ([2],          [],           2.0),   # empty nums2
        ([1, 2],       [3, 4, 5],    3.0),   # i=0 boundary (nums1 all-left)
        ([3, 4, 5],    [1, 2],       3.0),   # same after swap
        ([1, 3, 5, 7], [2, 4, 6, 8], 4.5),  # interleaved even
    ]

    print("find_median_sorted_arrays:")
    for n1, n2, expected in cases:
        result = find_median_sorted_arrays(n1, n2)
        status = "✓" if result == expected else f"✗ (got {result})"
        print(f"  {str(n1):20} + {str(n2):20} → {result}  {status}")
