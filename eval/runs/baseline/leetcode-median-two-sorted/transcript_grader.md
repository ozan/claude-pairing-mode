# leetcode-median-two-sorted

- Condition: `baseline`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T20:50:27

## Initial prompt

Let's solve Leetcode #4, 'Median of Two Sorted Arrays'. Given two sorted arrays, return the median of the combined array. Aim for better than O(n+m).

---

## Turn 1

### Tutor

Tutor: ## Median of Two Sorted Arrays — O(log(min(m,n)))

The key insight is **binary search on partitions**, not on values. We find where to *cut* both arrays so the left halves and right halves are perfectly balanced and sorted across the cut.

### The Core Idea

Instead of merging, we find a **partition pair** `(i, j)` such that:

```
nums1: [ left1 | right1 ]   ← i elements on the left
nums2: [ left2 | right2 ]   ← j elements on the left

Valid when:  left1 ≤ right2  AND  left2 ≤ right1
```

We binary search only on the **smaller array** to find the valid partition. The other array's partition is fully determined: `j = half - i`.

```
Total left = (m + n + 1) / 2   ← guarantees left side has median
```

### Diagram

```
nums1 = [1, 3, 8]        nums2 = [2, 5, 6, 10]     total=7, half=4
          i=2                        j=2

LEFT  side: [1, 3]   [2, 5]   → 4 elements ✓
RIGHT side: [8]      [6, 10]

Check: left1(3) ≤ right2(6) ✓  and  left2(5) ≤ right1(8) ✓

Median = max(3, 5) = 5   (odd total → just the max of the left)
```

### Code

```python
def findMedianSortedArrays(nums1: list[int], nums2: list[int]) -> float:
    # Always binary search on the smaller array → O(log(min(m,n)))
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    half = (m + n + 1) // 2   # left side must have this many elements

    lo, hi = 0, m

    while lo <= hi:
        i = (lo + hi) // 2    # partition nums1: i elems on the left
        j = half - i          # partition nums2: j elems on the left (derived)

        # Use ±inf as sentinels for out-of-bounds edges
        left1  = nums1[i - 1] if i > 0 else float('-inf')
        right1 = nums1[i]     if i < m else float('inf')
        left2  = nums2[j - 1] if j > 0 else float('-inf')
        right2 = nums2[j]     if j < n else float('inf')

        if left1 <= right2 and left2 <= right1:
            # ✅ Perfect partition found
            max_left  = max(left1, left2)
            min_right = min(right1, right2)

            if (m + n) % 2 == 1:
                return float(max_left)              # odd: median is max of left
            else:
                return (max_left + min_right) / 2.0 # even: average the middle two

        elif left1 > right2:
            hi = i - 1   # nums1's left is too large → move partition left
        else:
            lo = i + 1   # nums2's left is too large → move partition right

    raise ValueError("Input arrays must be sorted")
```

### Traced Examples

| Input | Steps | Result |
|---|---|---|
| `[1,3]`, `[2]` | After swap: binary search on `[2]`. `i=1,j=1` → valid. Odd total. | `2.0` |
| `[1,2]`, `[3,4]` | `i=1` fails (3>2), `i=2,j=0` valid. Even total. | `2.5` |
| `[0,0]`, `[0,0]` | `i=1,j=1` valid immediately. | `0.0` |

### Complexity

| | |
|---|---|
| **Time** | O(log(min(m, n))) — binary search on the shorter array |
| **Space** | O(1) — no extra allocations |

### Why Not O(m+n)?

A naive merge costs O(m+n). The partition trick works because:
1. **We don't need the merged array** — only the value(s) at the median position.
2. **The partition is monotonic**: as `i` increases, `left1` increases and `right2` decreases, so binary search converges correctly.
3. **`j` is fully determined by `i`**, so we only search one dimension.

### Student

Thanks for walking through this! I can see the logic now — instead of merging arrays, we're cleverly using binary search to find where to split both arrays so the left and right sides are balanced.

Let me trace through the code with the first example to make sure I understand:

**Example: `nums1 = [1,3]`, `nums2 = [2]`**

After swap (since len(nums1) > len(nums2)), we have:
- `nums1 = [2]`, `nums2 = [1,3]`
- `m=1, n=2, half = (1+2+1)//2 = 2`
- `lo=0, hi=1`

**First iteration:** `i = 0`
- `j = 2 - 0 = 2`
- `left1 = -inf`, `right1 = 2`
- `left2 = 3`, `right2 = inf`
- Check: `-inf ≤ inf` ✓ but `3 ≤ 2` ✗
- Since `left2 > right1`, we need to move right: `lo = 1`

**Second iteration:** `i = 1`
- `j = 2 - 1 = 1`
- `left1 = 2`, `right1 = inf`
- `left2 = 1`, `right2 = 3`
- Check: `2 ≤ 3` ✓ and `1 ≤ inf` ✓
- Total length is 3 (odd), so median = `max(2, 1) = 2.0` ✓

Got it! One quick question though — in the code, when we set `lo = i + 1` (when `left2 > right1`), we're saying nums2's left side is too large. But intuitively, wouldn't we want to *increase* the partition on nums1 to get more elements on its left? Or does increasing `i` on nums1 automatically shrink the partition on nums2?

Oh wait — yes! If `i` goes up, then `j = half - i` goes *down*, so nums2's partition moves left. That makes sense now. Just wanted to confirm I'm reading the logic correctly before I test the code myself.

---

## Turn 2

### Tutor

Tutor: You've got it exactly right! And you actually answered your own question perfectly — that's the elegant core of the whole algorithm.

The relationship `j = half - i` is the key constraint that ties everything together:

```
i ↑  →  j ↓  (nums2's left partition shrinks)
i ↓  →  j ↑  (nums2's left partition grows)
```

So the two "move" cases map directly to which side is too greedy:

```python
elif left1 > right2:
    hi = i - 1   # nums1 took too much → give some back to nums2

else:  # left2 > right1
    lo = i + 1   # nums2 took too much → take more from nums1 (shrinks nums2's share)
```

The total `i + j == half` is an **invariant** — it never changes. We're not searching for a *value*, we're searching for the right *distribution* of elements between the two arrays, with the total always fixed. Binary search works because that distribution is monotonic: pushing `i` right always makes `left1` larger and `left2` smaller (since fewer elements come from `nums2`), so there's exactly one valid crossing point.

Your trace was spot-on. Go ahead and run it — it should behave exactly as you worked through it!

### Student

Perfect, that makes it crystal clear now. The invariant `i + j == half` being constant is what I was missing — it's not two independent searches, it's one search with a constraint that automatically determines the other partition.

Let me test the code with a couple of examples to make sure it works:

```python
def findMedianSortedArrays(nums1: list[int], nums2: list[int]) -> float:
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    half = (m + n + 1) // 2

    lo, hi = 0, m

    while lo <= hi:
        i = (lo + hi) // 2
        j = half - i

        left1  = nums1[i - 1] if i > 0 else float('-inf')
        right1 = nums1[i]     if i < m else float('inf')
        left2  = nums2[j - 1] if j > 0 else float('-inf')
        right2 = nums2[j]     if j < n else float('inf')

        if left1 <= right2 and left2 <= right1:
            max_left  = max(left1, left2)
            min_right = min(right1, right2)

            if (m + n) % 2 == 1:
                return float(max_left)
            else:
                return (max_left + min_right) / 2.0

        elif left1 > right2:
            hi = i - 1
        else:
            lo = i + 1

    raise ValueError("Input arrays must be sorted")

# Test
print(findMedianSortedArrays([1, 3], [2]))           # Expected: 2.0
print(findMedianSortedArrays([1, 2], [3, 4]))        # Expected: 2.5
print(findMedianSortedArrays([0, 0], [0, 0]))        # Expected: 0.0
print(findMedianSortedArrays([], [1]))               # Expected: 1.0
print(findMedianSortedArrays([2], []))               # Expected: 2.0
```

All of these should pass — the logic holds up, the boundary handling with sentinels prevents index errors, and the binary search correctly narrows in on the valid partition. I feel confident in this solution now.

<done/>

---

**Run end:** done after 2 turn(s) in 54.0s
