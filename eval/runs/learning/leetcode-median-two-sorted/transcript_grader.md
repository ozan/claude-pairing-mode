# leetcode-median-two-sorted

- Condition: `learning`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:04:50

## Initial prompt

Let's solve Leetcode #4, 'Median of Two Sorted Arrays'. Given two sorted arrays, return the median of the combined array. Aim for better than O(n+m).

---

## Turn 1

### Tutor

Tutor: ## Median of Two Sorted Arrays — O(log min(m,n))

The key insight is that we don't need to *merge* the arrays — we need to **find the right partition point** using binary search.

---

### 🧠 Core Idea: Binary Search on the Partition

For the median to exist, we need to split **both** arrays such that:
1. The **left half** and **right half** have equal sizes (±1 for odd total)
2. Every element on the left ≤ every element on the right

```
nums1: [ ... L1 | R1 ... ]   ← partition at i
nums2: [ ... L2 | R2 ... ]   ← partition at j

Valid when: L1 ≤ R2  AND  L2 ≤ R1
```

Since `i + j` must equal `half = (m + n + 1) // 2`, **j is fully determined by i**. So we only binary search on one array — the shorter one.

---

### 📐 Partition Diagram

```
Total = 7 (odd) → half = 4 elements on the left

nums1:  1   3  |  8   9       (i = 2)
nums2:  2   4  |  6   7       (j = 2, since 4-2 = 2)
              ↑
         L1=3, R1=8
         L2=4, R2=6

Check: L1(3) ≤ R2(6) ✓  and  L2(4) ≤ R1(8) ✓
Median = max(L1, L2) = max(3,4) = 4
```

---

### ✅ Implementation

```python
def findMedianSortedArrays(nums1: list[int], nums2: list[int]) -> float:
    # Always binary search on the SMALLER array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    half = (m + n + 1) // 2   # left-half size (rounds up for odd totals)

    low, high = 0, m

    while low <= high:
        i = (low + high) // 2  # nums1 partition: 0..m elements on the left
        j = half - i           # nums2 partition: determined by i

        # Use ±∞ to handle edge partitions gracefully
        L1 = nums1[i - 1] if i > 0 else float('-inf')
        R1 = nums1[i]     if i < m else float('inf')
        L2 = nums2[j - 1] if j > 0 else float('-inf')
        R2 = nums2[j]     if j < n else float('inf')

        if L1 <= R2 and L2 <= R1:
            # ✅ Valid partition found
            max_left  = max(L1, L2)   # largest on the left
            min_right = min(R1, R2)   # smallest on the right

            if (m + n) % 2 == 1:
                return float(max_left)             # odd: median is max of left
            else:
                return (max_left + min_right) / 2  # even: average the midpoints

        elif L1 > R2:
            high = i - 1   # nums1's left is too big → shift partition left
        else:
            low = i + 1    # nums2's left is too big → shift partition right
```

---

### 🔍 Trace Through an Example

```
nums1 = [1, 3],  nums2 = [2, 4, 6]    (m=2, n=3, half=3)

Iter 1: i=1, j=2
  L1=1, R1=3,  L2=4, R2=6
  L2(4) > R1(3) → not valid → move right (low=2)

Iter 2: i=2, j=1
  L1=3, R1=∞,  L2=2, R2=4
  L1(3) ≤ R2(4) ✓  and  L2(2) ≤ R1(∞) ✓  → VALID

max_left=3, min_right=4
Total=5 (odd) → return 3.0  ✓  (merged: [1,2,3,4,6])
```

---

### 📊 Complexity

| | |
|---|---|
| **Time** | O(log min(m, n)) — binary search on the smaller array |
| **Space** | O(1) — no extra storage, just index arithmetic |

---

### 💡 Why This Works

The binary search **invariant** is: *"find `i` such that the partition is valid."* Because the arrays are sorted, if `L1 > R2` the partition is too far right — all positions further right will also fail, so we can safely eliminate half the search space each iteration.

### Student

Thanks for walking me through this! This is really elegant — I can see how the partition idea avoids merging entirely.

Let me make sure I understand the logic before I code it up:

1. We binary search on the **smaller** array to find partition index `i`
2. The partition on the second array `j` is automatically determined by `j = half - i`
3. We use infinity values for the edges so we don't have to special-case boundary checks
4. The validity check is: `L1 ≤ R2 AND L2 ≤ R1`
5. Once valid, the median comes from the max of the left elements (or the average of left/right boundaries if the total is even)

One thing I want to clarify before implementing: when we do `half = (m + n + 1) // 2`, I see that rounds up for odd totals. Why `+ 1` specifically? Is that to ensure the left half is always at least as big as the right half?

And then when I calculate the median at the end, if the total is odd, I return just `max_left` — that makes sense because the left half has one more element. But if it's even, I average `max_left` and `min_right`, which are the two "middle" elements. Got it.

Let me code this up and test it on a few examples:

```python
def findMedianSortedArrays(nums1: list[int], nums2: list[int]) -> float:
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    m, n = len(nums1), len(nums2)
    half = (m + n + 1) // 2
    
    low, high = 0, m
    
    while low <= high:
        i = (low + high) // 2
        j = half - i
        
        L1 = nums1[i - 1] if i > 0 else float('-inf')
        R1 = nums1[i] if i < m else float('inf')
        L2 = nums2[j - 1] if j > 0 else float('-inf')
        R2 = nums2[j] if j < n else float('inf')
        
        if L1 <= R2 and L2 <= R1:
            max_left = max(L1, L2)
            min_right = min(R1, R2)
            
            if (m + n) % 2 == 1:
                return float(max_left)
            else:
                return (max_left + min_right) / 2
        
        elif L1 > R2:
            high = i - 1
        else:
            low = i + 1
    
    return -1  # shouldn't reach here with valid input
```

Let me trace through your example to verify: `nums1 = [1, 3], nums2 = [2, 4, 6]`

- `m=2, n=3, half=3`
- Iteration 1: `i=1, j=2` → `L1=1, R1=3, L2=4, R2=6` → `L2 > R1` so `low=2`
- Iteration 2: `i=2, j=1` → `L1=3, R1=∞, L2=2, R2=4` → valid! `max_left=3, min_right=4` → total is 5 (odd) → return `3.0` ✓

That matches! Does my implementation look correct?

---

## Turn 2

### Tutor

Tutor: Your implementation is correct — and your trace matches perfectly. ✓

---

### The `+ 1` question — great instinct

Your interpretation is exactly right. The `+1` **biases the left half to win the tie** when the total is odd:

```
Total = 5:  (5 + 1) // 2 = 3  → left gets 3,  right gets 2
Total = 6:  (6 + 1) // 2 = 3  → left gets 3,  right gets 3
```

Without the `+1`, odd totals would give left 2 and right 3 — the median would then sit at `min_right` instead of `max_left`. Either convention works, but `+1` lets you **always use `max_left` for odd totals**, which keeps the final return logic clean. Consistency is the point.

---

### A few more test cases worth running

```python
# Edge: one empty array
findMedianSortedArrays([], [1, 2, 3])        # → 2.0

# Edge: single elements
findMedianSortedArrays([1], [2])             # → 1.5

# Edge: all of nums1 < all of nums2 (no interleaving)
findMedianSortedArrays([1, 2], [3, 4])       # → 2.5

# Edge: duplicate values
findMedianSortedArrays([1, 1], [1, 1])       # → 1.0
```

These stress the **boundary partitions** — where `i=0` or `i=m` — which is exactly where the ±∞ sentinels earn their keep. If those pass, you can trust the implementation.

---

### One small note on the fallthrough

```python
return -1  # shouldn't reach here with valid input
```

This is fine for LeetCode. In production you'd raise a `ValueError` to make the contract explicit — valid sorted input always finds a partition, so reaching here signals a bug or bad input.

Your understanding is solid. The code is ready to submit.

### Student

Perfect, thanks for clarifying the `+1` logic — that makes total sense now. The idea of biasing the left half to win the tie keeps the median calculation consistent and clean.

I ran through those edge cases in my head:
- Empty array: infinity sentinels handle it gracefully
- Single elements: partition finds the midpoint between them
- No interleaving: partition ends up with all of nums1 on the left, all of nums2 on the right (or vice versa)
- Duplicates: the validity check still works because `≤` handles equality

I feel confident about this solution. The binary search on the partition is much cleverer than I expected — instead of thinking "merge and find the middle," thinking "find the right split point" cuts the complexity down to O(log min(m,n)). 

One more quick sanity check: I want to make sure the loop always terminates. Since we're binary searching on a bounded range `[0, m]` and we either adjust `low` or `high` each iteration (or find the answer), we'll definitely hit a valid partition or exhaust the range. Given that valid input always has a solution, we should always find it before `low > high`. Makes sense.

I'm ready to submit this. Thanks for walking through the intuition and catching my understanding along the way!

<done/>

---

**Run end:** done after 2 turn(s) in 74.9s
