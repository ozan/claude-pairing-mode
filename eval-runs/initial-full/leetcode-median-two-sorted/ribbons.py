def feasible(ribbons, m, k):
    return sum(r // k for r in ribbons) >= m


def maxLength(ribbons, m):
    lo, hi = 1, max(ribbons) + 1  # hi is first infeasible candidate
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(ribbons, m, mid):
            lo = mid + 1   # search right for larger valid k
        else:
            hi = mid       # mid might be leftmost infeasible
    return lo - 1          # leftmost infeasible - 1 = rightmost feasible
