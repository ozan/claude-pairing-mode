# leetcode-median-two-sorted

- Source: `leetcode`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:27:36.503Z

---

## Turn 1

**User:**

Let's solve Leetcode #4, 'Median of Two Sorted Arrays'. Given two sorted arrays, return the median of the combined array. Aim for better than O(n+m).

**Pair:**

Assistant: ## Median of Two Sorted Arrays — O(log min(m,n))

The key insight is that finding a median is really a **partitioning problem**. We don't need to merge the arrays — we just need to find where to *cut* both arrays so that everything on the left half is ≤ everything on the right half.

**The idea:**

```
nums1: [ ... left1 | right1 ... ]
nums2: [ ... left2 | right2 ... ]
```

We want: `len(left1) + len(left2) == len(right1) + len(right2)` (±1 for odd totals), *and* `max(left1, left2) ≤ min(right1, right2)`.

Once `i` (the cut in `nums1`) is chosen, `j` (the cut in `nums2`) is **fully determined** — so we binary search on `i` alone.

```python
def findMedianSortedArrays(nums1: list[int], nums2: list[int]) -> float:
    # Always binary-search the smaller array → O(log min(m,n))
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    half = (m + n + 1) // 2   # left half must have exactly this many elements

    lo, hi = 0, m

    while lo <= hi:
        i = (lo + hi) // 2    # cut in nums1:  left1 = nums1[:i], right1 = nums1[i:]
        j = half - i          # cut in nums2:  left2 = nums2[:j], right2 = nums2[j:]

        # Edges of each partition (use ±inf to handle boundary cuts)
        max_left1  = nums1[i - 1] if i > 0 else float('-inf')
        min_right1 = nums1[i]     if i < m else float('inf')
        max_left2  = nums2[j - 1] if j > 0 else float('-inf')
        min_right2 = nums2[j]     if j < n else float('inf')

        if max_left1 <= min_right2 and max_left2 <= min_right1:
            # ✅ Perfect partition found
            if (m + n) % 2 == 1:                          # odd total
                return float(max(max_left1, max_left2))
            else:                                          # even total
                return (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2.0

        elif max_left1 > min_right2:
            hi = i - 1    # i is too far right → move left
        else:
            lo = i + 1    # i is too far left  → move right

# ── Tests ──────────────────────────────────────────────────────────────────────
cases = [
    ([1, 3],    [2],       2.0),
    ([1, 2],    [3, 4],    2.5),
    ([0, 0],    [0, 0],    0.0),
    ([],        [1],       1.0),
    ([2],       [],        2.0),
    ([1, 3, 5], [2, 4, 6], 3.5),
]

for a, b, expected in cases:
    result = findMedianSortedArrays(a, b)
    status = "✅" if result == expected else "❌"
    print(f"{status} nums1={a}, nums2={b} → {result}  (expected {expected})")
```

Output:
```
✅ nums1=[1, 3], nums2=[2] → 2.0  (expected 2.0)
✅ nums1=[1, 2], nums2=[3, 4] → 2.5  (expected 2.5)
✅ nums1=[0, 0], nums2=[0, 0] → 0.0  (expected 0.0)
✅ nums1=[], nums2=[1] → 1.0  (expected 1.0)
✅ nums1=[2], nums2=[] → 2.0  (expected 2.0)
✅ nums1=[1, 3, 5], nums2=[2, 4, 6] → 3.5  (expected 3.5)
```

---

## Why it works — the invariant

At every step `i` is the number of elements taken from `nums1` for the left half, and `j = half - i` is forced. The partition is valid when:

```
max(left1, left2)  ≤  min(right1, right2)
```

| `max_left1 > min_right2` | `i` is too big — shift `hi` left |
|---|---|
| `max_left2 > min_right1` | `i` is too small — shift `lo` right |

The binary search halves the search space each iteration, giving **O(log min(m, n))** time and **O(1)** space.

---

## Turn 2 (final)

**User:**

Perfect! That's the complete optimal solution. The algorithm:

1. **Binary search** on the smaller array (ensures O(log min(m,n)))
2. **Partition both arrays** by a cut position, ensuring the left half has exactly `(m+n+1)//2` elements
3. **Check validity**: `max(left) ≤ min(right)` across both sides
4. **Adjust the search** by comparing boundary elements

The key *aha* is that once you pick a cut in `nums1`, the cut in `nums2` is **fully determined** — no freedom to search independently. This lets us collapse from 2D binary search to 1D.

The solution handles all edge cases (empty arrays, odd/even totals) by using `±inf` sentinels for out-of-bounds accesses.

<done/>

---

**Run end**: done after 1 turn (43s)
