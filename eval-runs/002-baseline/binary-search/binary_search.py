def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def bisect_left(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def bisect_right(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def count(arr, target):
    return bisect_right(arr, target) - bisect_left(arr, target)


if __name__ == "__main__":
    arr = [1, 3, 5, 7, 9, 11, 13, 15]
    for t in [1, 7, 15, 4, 0, 16]:
        print(f"search({t}) -> {binary_search(arr, t)}")

    print()
    dups = [1, 2, 2, 2, 3, 5, 5, 8]
    print(f"arr = {dups}")
    for t in [2, 5, 4, 0, 9]:
        lo = bisect_left(dups, t)
        hi = bisect_right(dups, t)
        print(f"  t={t}: left={lo}  right={hi}  count={hi - lo}  slice={dups[lo:hi]}")
