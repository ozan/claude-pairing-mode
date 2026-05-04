# leetcode-two-sum

- Source: `leetcode`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Output style: `Learning`
- Started: 2026-05-03T19:55:55.989Z

---

## Turn 1

**User:**

Let's solve Leetcode #1, 'Two Sum'. Given a list of integers and a target, return the indices of the two numbers that add up to the target. Assume exactly one solution exists.

**Pair:**

Assistant: ## LeetCode #1 — Two Sum

### 🧠 The Key Insight

For every number `x`, you're looking for exactly one partner: `target - x`. Instead of checking every pair (slow), **remember what you've seen** as you go.

---

### Brute Force First (to build intuition)

Check every pair — O(n²) time:

```python
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
```

This works, but scanning the whole array for a partner on every step is wasteful.

---

### Optimal: Hash Map — O(n) time, O(n) space

The idea: as you walk through the array, **store each number's index in a map**. Before storing, check if the number's *complement* is already there.

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}  # value → index

    for i, num in enumerate(nums):
        complement = target - num

        if complement in seen:          # ✅ partner found!
            return [seen[complement], i]

        seen[num] = i                   # 📝 remember for later
```

---

### Walkthrough: `nums = [2, 7, 11, 15]`, `target = 9`

| Step | `num` | `complement` | `seen` before check | Result |
|------|-------|--------------|----------------------|--------|
| i=0 | 2 | 7 | `{}` | miss → store `{2:0}` |
| i=1 | 7 | 2 | `{2:0}` | **hit!** → return `[0, 1]` |

---

### Why this works

You only need **one pass** because:
- If `a + b = target`, when you reach `b`, `a` is already in the map (or vice versa).
- A dict lookup is O(1), so the whole loop is O(n).

| | Brute Force | Hash Map |
|---|---|---|
| Time | O(n²) | **O(n)** |
| Space | O(1) | O(n) |

The classic **time/space tradeoff** — you spend a little memory to save a lot of time. 🎯

---

## Turn 2

**User:**

Great! You've got the explanation. Now let's actually implement it. Here are two ways forward:

---

## **Option A: You code it first (learning-focused)**
I'll hold the answer. You write the function from the walkthrough above — hash map approach. Once you paste it, I'll review it, catch any edge cases, and we'll test it together.

**Why pick this**: You'll solidify the logic by typing it out and fixing any gaps yourself.

---

## **Option B: I code it, you make the choices (guided implementation)**
I write the solution with inline comments, then we:
1. Test it with provided examples
2. Trace through the algorithm step-by-step
3. Discuss why it's O(n) vs. O(n²)

**Why pick this**: Faster to a working solution, good for seeing production-level style.

---

Which would you prefer? **A** or **B**?

(Also: what language — Python, JavaScript, or something else?)

**Pair:**

Assistant: Great framing! Since you're presenting both options, let's go with **Option B in Python** — it builds directly on the walkthrough we just did, and we can move fast.

---

## Implementation

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}  # maps value → index

    for i, num in enumerate(nums):
        complement = target - num   # what we need to find

        if complement in seen:
            return [seen[complement], i]  # found the pair!

        seen[num] = i  # haven't found it yet — store for later

    # Problem guarantees a solution, so we never reach here
```

---

## Test Cases

```python
print(two_sum([2, 7, 11, 15], 9))   # → [0, 1]  (2 + 7)
print(two_sum([3, 2, 4], 6))        # → [1, 2]  (2 + 4)
print(two_sum([3, 3], 6))           # → [0, 1]  (3 + 3) — duplicate values!
```

The third case is the interesting one — duplicates work correctly because we **check before we store**, so a number can't match itself.

---

## Why O(n) and not O(n²)?

| Operation | Cost | How many times? |
|---|---|---|
| `complement in seen` | O(1) — hash lookup | n times |
| `seen[num] = i` | O(1) — hash insert | n times |
| **Total** | **O(n)** | |

The brute force runs a nested loop: for each of n elements, it scans up to n others → **n × n = O(n²)**. The hash map eliminates the inner scan entirely.

---

**Want to go deeper?** A few natural next steps:
- 🔁 What if you needed **all** pairs (not just one)?
- 📦 What if the array were **sorted** — could you do O(1) space? *(Two Pointers)*
- 🔢 What if you needed **three** numbers? *(3Sum — LC #15)*

---

## Turn 3 (final)

**User:**

Perfect! Let me create this solution and verify it works with your test cases.✅ **All tests pass!** Great — the solution is solid.

---

## Step-by-Step Trace: `[2, 7, 11, 15]`, target `9`

Let me walk through the algorithm to solidify how it works:

| Iteration | `i` | `num` | `complement` (9 - num) | `seen` before check | Complement in map? | Action |
|-----------|-----|-------|------------------------|----------------------|-----------|---------|
| 1 | 0 | 2 | 7 | `{}` | ❌ No | Store: `{2: 0}` |
| 2 | 1 | 7 | 2 | `{2: 0}` | ✅ **Yes!** | Return `[seen[2], 1]` = `[0, 1]` ✓ |

**The aha moment**: At step 2, we find that `2` is already in the map from step 1. So `7 + 2 = 9` ✓

---

## Key insight I appreciate

The "check before you store" order is crucial:
- If we stored first, then checked, a duplicate like `[3, 3]` would match itself (wrong!)
- Checking first means: *"Is my complement already here from an earlier step?"*
- If yes → return. If no → store and move on.

---

## One follow-up: Two Pointers (if the array is sorted)

If the input **was pre-sorted**, you could use **zero extra space**:

```python
def two_sum_sorted(nums: list[int], target: int) -> list[int]:
    left, right = 0, len(nums) - 1
    
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return [left, right]
        elif total < target:
            left += 1  # need a bigger number
        else:
            right -= 1  # need a smaller number
```

But **the LeetCode problem gives an unsorted array**, so the hash map is the right choice here. The two-pointer trick trades a sorted input for O(1) space.

---

**Now I understand the tradeoff:** hash map is best for unsorted arrays (O(n) time, can't do better without sorting first). Pretty clean! 🎯

<done/>

---

**Run end**: done after 2 turns (67s)
