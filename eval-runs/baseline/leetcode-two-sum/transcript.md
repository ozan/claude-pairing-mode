# leetcode-two-sum

- Source: `leetcode`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:26:00.651Z

---

## Turn 1

**User:**

Let's solve Leetcode #1, 'Two Sum'. Given a list of integers and a target, return the indices of the two numbers that add up to the target. Assume exactly one solution exists.

**Pair:**

Assistant: ## Two Sum — LeetCode #1

The optimal approach uses a **hash map** to store each number's index as we iterate. For every element, we check if its complement (`target - num`) already exists in the map — if so, we've found our pair!

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}  # maps value -> index

    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
```

### How it works

| Step | `i` | `num` | `complement` | `seen` |
|------|-----|-------|-------------|--------|
| 1 | 0 | 2 | 7 | `{2: 0}` |
| 2 | 1 | 7 | 2 | ✅ found! → `[0, 1]` |

*(example: `nums = [2, 7, 11, 15]`, `target = 9`)*

### Complexity

| | |
|---|---|
| **Time** | O(n) — single pass |
| **Space** | O(n) — hash map stores up to n elements |

### Why not the naïve O(n²) approach?
The brute-force solution checks every pair with two nested loops. The hash map trades **space for time** — instead of re-scanning the array for each element, we look up the complement in **O(1)** per step.

### Edge cases handled ✅
- **Same element used twice?** We only add `num` to `seen` *after* checking, so `seen[complement]` can never return the current index `i`.
- **Duplicate values?** Works fine — e.g. `[3, 3]` with `target = 6` returns `[0, 1]`.

---

## Turn 2

**User:**

I've given you the optimal solution, but let me present **two approaches** so you can see the trade-off:

---

## **Option A: Hash Map (Best)**  
✅ **One pass, fast lookups**

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
```

- **Time:** O(n)
- **Space:** O(n)
- **Key insight:** Store each number's index *before* checking; avoids using the same element twice.

---

## **Option B: Sorted Two-Pointer**  
⚠️ **Requires index mapping**

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    # Sort with original indices
    indexed = sorted(enumerate(nums), key=lambda x: x[1])
    
    left, right = 0, len(indexed) - 1
    while left < right:
        s = indexed[left][1] + indexed[right][1]
        if s == target:
            return sorted([indexed[left][0], indexed[right][0]])
        elif s < target:
            left += 1
        else:
            right -= 1
```

- **Time:** O(n log n) due to sorting
- **Space:** O(n) for the sorted copy
- **Trade-off:** Simpler two-pointer logic, but sorting adds complexity.

---

**Which approach appeals to you — A or B?** I'll code it up in a proper file once you pick.

**Pair:**

Assistant: **Option A, without question.** Here's why it wins on every axis:

### Head-to-Head

| | Option A (Hash Map) | Option B (Two-Pointer) |
|---|---|---|
| **Time** | O(n) | O(n log n) |
| **Space** | O(n) | O(n) |
| **Mutates input?** | No | No (uses a copy) |
| **Returns sorted indices?** | Naturally | Needs extra `sorted()` call |

Option B's space cost is *identical* to A, so you get **no space benefit** in exchange for the slower runtime. The two-pointer pattern shines on problems where the input is *already sorted* (e.g. LeetCode #167, Two Sum II) — here we're paying O(n log n) just to enable a technique we didn't need.

### One Small Correction in Option A's Note
> *"Store each number's index **before** checking"*

This is actually backwards — the code stores `seen[num] = i` **after** the complement check. That ordering is intentional and critical: it prevents returning `[i, i]` for an input like `[6], target=12`. Worth keeping the comment accurate.

### The Corrected, File-Ready Version

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}  # value -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i  # store AFTER checking to avoid reusing same index
```

Want me to write this to a file with test cases included?

---

## Turn 3 (final)

**User:**

Perfect! ✅ **All tests pass.** Here's what we've built:

## Summary

**File:** `two_sum.py`

The solution uses a **hash map** to solve Two Sum in **O(n) time** with a single pass:

1. **Iterate** through each number
2. **Check** if `target - num` already exists in our map
3. **Return** the pair immediately when found
4. **Store** the current number's index for future lookups

### Key Details

- **No index reuse:** We check *before* storing, so we never return `[i, i]`
- **Handles duplicates:** Works correctly for arrays like `[3, 3]`
- **Works with negatives:** No special cases needed

### Test Coverage

✓ Basic pair  
✓ Different target  
✓ Duplicate values  
✓ Negative numbers  
✓ Larger arrays  

The solution is optimal for this problem — any algorithm must visit every element at least once, so O(n) is the best we can achieve.

<done/>

---

**Run end**: done after 2 turns (69s)
