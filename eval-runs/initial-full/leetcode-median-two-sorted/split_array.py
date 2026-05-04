def feasible(nums, k, limit):
    count, curr = 1, 0
    for x in nums:
        if curr + x > limit:
            count += 1
            curr = 0
        curr += x
    return count <= k


def splitArray(nums, k):
    lo, hi = max(nums), sum(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(nums, k, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
