def feasible(piles, h, k):
    return sum((p + k - 1) // k for p in piles) <= h


def minEatingSpeed(piles, h):
    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(piles, h, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
