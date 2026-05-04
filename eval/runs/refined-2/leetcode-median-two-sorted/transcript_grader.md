# leetcode-median-two-sorted

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:23:43

## Initial prompt

Let's solve Leetcode #4, 'Median of Two Sorted Arrays'. Given two sorted arrays, return the median of the combined array. Aim for better than O(n+m).

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Tutor: Great problem. The key question is: what do we binary search *over*?

OPTIONS:
[A] Binary search the value
Binary search over the *value range* `[min, max]`. For each candidate midpoint, count how many elements across both arrays are ≤ it (using `bisect`), and use that count to home in on the median value.

[B] Binary search the partition
Binary search over a *split index* `i` in the smaller array. For each `i`, derive `j = half - i` in the larger array. Check whether the four boundary elements satisfy the "left ≤ right" condition, and adjust `i` accordingly.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach do you want to build on?

### Student

I think I'd like to go with **B** — binary search the partition.

I'm drawn to it because it feels like a more direct approach to the problem: we're literally trying to find where to "cut" the arrays so that the left half and right half are balanced. Option A (searching over values) seems like it would require extra bookkeeping to convert a value back into actual positions.

Can we start by walking through the logic? I want to understand:
- Why we binary search on the *smaller* array specifically
- How we derive `j = half - i`
- What the "left ≤ right" condition actually checks for

Once I understand those pieces, I think I can code it up.

---

## Turn 2

### Tutor

Tutor: Good instincts on all three. Let me walk through each.

---

**Why the smaller array?**

We binary search over `i ∈ [0, m]` — the number of elements we take from `nums1` into the left partition. Since `j = half - i`, if `m > n` it's possible to get `j < 0`. Always assigning `nums1` to the shorter array guarantees `j` stays in `[0, n]`. It also gives us the tightest bound: **O(log(min(m, n)))**.

---

**How `j = half - i` is derived**

We want the combined left partition to have exactly `half = (m + n + 1) // 2` elements. (The `+1` makes odd totals round up, which simplifies the median formula later.) We're drawing `i` elements from `nums1` and `j` from `nums2`:

```
i + j = half  →  j = half - i
```

So as we move `i` up or down in the binary search, `j` adjusts automatically.

---

**What "left ≤ right" actually checks**

After the cut:
```
nums1: [ ... nums1[i-1] | nums1[i] ... ]
nums2: [ ... nums2[j-1] | nums2[j] ... ]
```

Within each array the order is already guaranteed (they're sorted). The only things that could be *wrong* are the two cross-comparisons:

| Condition | Meaning |
|---|---|
| `nums1[i-1] <= nums2[j]` | largest left-of-cut in nums1 ≤ smallest right-of-cut in nums2 |
| `nums2[j-1] <= nums1[i]` | largest left-of-cut in nums2 ≤ smallest right-of-cut in nums1 |

If `nums1[i-1] > nums2[j]`, `i` is too large — shift left. If `nums2[j-1] > nums1[i]`, `i` is too small — shift right. When both hold, you've found the partition.

---

Now, before we code this up — there's one implementation detail worth thinking about:

OPTIONS:
[A] Sentinels for boundaries
When `i = 0`, `nums1[i-1]` doesn't exist — treat it as `-inf`. When `i = m`, `nums1[i]` doesn't exist — treat it as `+inf`. Use `float('-inf')` / `float('inf')` so the comparisons just work without special cases.

[B] Explicit boundary checks
Guard every boundary access with `if i > 0` / `if i < m` checks, and skip the comparison (or treat it as automatically satisfied) when the index is out of range.

(Reply with A or B, or ask a follow-up question.)

Tutor: How do you want to handle the out-of-bounds cases at the edges of the partition?

### Student

I like **A** — sentinels for boundaries.

Using `float('-inf')` and `float('inf')` feels cleaner and more elegant. It lets the comparison logic stay uniform without littering the code with conditionals. If `i = 0`, then `nums1[i-1]` becomes `-inf`, and the check `nums1[i-1] <= nums2[j]` automatically passes (since `-inf` is less than everything). That's nice.

Option B with all the explicit guards would work, but it feels verbose and error-prone — easy to mess up a boundary check and introduce a bug.

Alright, I'm ready to code this up. Let me start writing the solution:

```python
def findMedianSortedArrays(nums1, nums2):
    # Ensure nums1 is the smaller array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    m, n = len(nums1), len(nums2)
    half = (m + n + 1) // 2
    
    left, right = 0, m
    
    while left <= right:
        i = (left + right) // 2
        j = half - i
        
        # Define sentinels
        left1 = float('-inf') if i == 0 else nums1[i - 1]
        right1 = float('inf') if i == m else nums1[i]
        left2 = float('-inf') if j == 0 else nums2[j - 1]
        right2 = float('inf') if j == n else nums2[j]
        
        # Check partition validity
        if left1 <= right2 and left2 <= right1:
            # Found the partition
            max_left = max(left1, left2)
            min_right = min(right1, right2)
            
            # Calculate median
            if (m + n) % 2 == 1:
                return float(max_left)
            else:
                return (max_left + min_right) / 2.0
        elif left1 > right2:
            # i is too large, go left
            right = i - 1
        else:
            # i is too small, go right
            left = i + 1
    
    return -1  # Should never reach here
```

Does this look right to you?

---

## Turn 3

### Tutor

Tutor: The logic is correct — clean implementation. Let me trace through a quick example to confirm:

`nums1 = [1,3]`, `nums2 = [2]` → after swap: `nums1=[2]`, `nums2=[1,3]`, `half=2`

- `i=0, j=2`: `left2=3 > right1=2` → `left=1`
- `i=1, j=1`: `left1=2, left2=1, right1=∞, right2=3` → both checks pass → `max_left=2`, odd total → return `2.0` ✓

One tiny note: `return -1` is unreachable — a valid partition is always guaranteed to exist. Worth replacing with `raise RuntimeError(...)` or just removing, so it doesn't look like a legitimate return path.

Now, one last question worth making sure is crisp in your head:

OPTIONS:
[A] O(log(m + n))
The binary search spans both arrays, so the search space is proportional to the total number of elements, giving O(log(m + n)).

[B] O(log(min(m, n)))
We only binary search over the *smaller* array's indices — a range of size `m` where `m ≤ n` — so the search space is bounded by the smaller array alone.

(Reply with A or B, or ask a follow-up question.)

Tutor: What's the time complexity of this solution?

### Student

It's **B** — O(log(min(m, n))).

We're binary searching over `i ∈ [0, m]` where `m` is the size of the smaller array. Even though we touch both arrays during each iteration (to compute the sentinel values and check the partition), the number of iterations is determined solely by how many times we can halve the range `[0, m]`, which is O(log(m)).

Since `m ≤ n`, that's O(log(min(m, n))).

That's the whole point of swapping to make `nums1` the smaller array — we get the tightest possible bound instead of O(log(m + n)).

---

Good catch on the unreachable `return -1`. Let me update that:

```python
def findMedianSortedArrays(nums1, nums2):
    # Ensure nums1 is the smaller array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    m, n = len(nums1), len(nums2)
    half = (m + n + 1) // 2
    
    left, right = 0, m
    
    while left <= right:
        i = (left + right) // 2
        j = half - i
        
        # Define sentinels
        left1 = float('-inf') if i == 0 else nums1[i - 1]
        right1 = float('inf') if i == m else nums1[i]
        left2 = float('-inf') if j == 0 else nums2[j - 1]
        right2 = float('inf') if j == n else nums2[j]
        
        # Check partition validity
        if left1 <= right2 and left2 <= right1:
            # Found the partition
            max_left = max(left1, left2)
            min_right = min(right1, right2)
            
            # Calculate median
            if (m + n) % 2 == 1:
                return float(max_left)
            else:
                return (max_left + min_right) / 2.0
        elif left1 > right2:
            # i is too large, go left
            right = i - 1
        else:
            # i is too small, go right
            left = i + 1
```

I feel good about this solution now. We've got O(log(min(m, n))) time complexity, which beats the O(m + n) naive approach, and the logic is clear. Thanks for walking through this!

<done/>

---

**Run end:** done after 3 turn(s) in 119.4s
