# leetcode-two-sum

- Source: `leetcode`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T04:00:01.648Z

---

## Turn 1

**User:**

Let's solve Leetcode #1, 'Two Sum'. Given a list of integers and a target, return the indices of the two numbers that add up to the target. Assume exactly one solution exists.

**Pair:**

Assistant: ## Two Sum – LeetCode #1

The optimal approach uses a **hash map** to find the complement in O(1) per lookup, giving us **O(n) time** overall.

### The Idea

For each number `x` at index `i`, we need to find a previous number equal to `target - x`. We store every number we've seen (mapped to its index) so we can check this in constant time.

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}  # value -> index

    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:
            return [seen[complement], i]
        seen[x] = i
```

### Walkthrough

```
nums = [2, 7, 11, 15], target = 9

i=0  x=2   complement=7   seen={}           → not found, store {2:0}
i=1  x=7   complement=2   seen={2:0}        → found! return [0, 1] ✓
```

### Complexity

| | Complexity |
|---|---|
| **Time** | O(n) — single pass |
| **Space** | O(n) — hash map stores up to n entries |

### Why not the naive approach?

The brute-force double loop (`for i ... for j ...`) is **O(n²)** — checking every pair. The hash map trades a little space to shave it down to a single linear pass, which matters a lot on large inputs.

### Edge cases handled
- **Duplicate values** (e.g. `[3, 3]`, target `6`) — works correctly because we check *before* inserting, so the same index is never reused.
- **Negative numbers** — works since we're just doing arithmetic and key lookups.

---

## Turn 2

**User:**

Great walkthrough! I follow the hash map approach — iterate once, check if complement exists, store as we go.

But before we code it, I want to understand the trade-offs. You mentioned the double-loop is O(n²). Are there any other practical approaches worth considering, or is the hash map the clear winner here? Should we see them side-by-side before I pick which one to code?

**Pair:**

Assistant: Good instinct to survey the landscape first. There are exactly **three practical approaches**, each with a real trade-off story:

---

## The Three Approaches

### 1. Brute Force — O(n²) time, O(1) space
```python
for i in range(len(nums)):
    for j in range(i + 1, len(nums)):
        if nums[i] + nums[j] == target:
            return [i, j]
```
Check every pair. Nothing extra stored.

---

### 2. Sort + Two Pointers — O(n log n) time, O(n) space
```python
sorted_nums = sorted(enumerate(nums), key=lambda x: x[1])
lo, hi = 0, len(sorted_nums) - 1
while lo < hi:
    s = sorted_nums[lo][1] + sorted_nums[hi][1]
    if s == target:   return [sorted_nums[lo][0], sorted_nums[hi][0]]
    elif s < target:  lo += 1
    else:             hi -= 1
```
Sort once, then squeeze inward from both ends. We must carry original indices along for the ride, hence the O(n) space.

---

### 3. Hash Map — O(n) time, O(n) space
```python
seen = {}
for i, x in enumerate(nums):
    if target - x in seen:
        return [seen[target - x], i]
    seen[x] = i
```
Single pass, complement lookup in O(1).

---

## Side-by-Side Comparison

| | Brute Force | Two Pointers | Hash Map |
|---|---|---|---|
| **Time** | O(n²) | O(n log n) | **O(n)** |
| **Space** | **O(1)** | O(n) | O(n) |
| **Passes** | 1 nested | 1 sort + 1 scan | **1** |
| **Modifies input?** | No | Yes (sort) | No |
| **Code simplicity** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |

---

## So — clear winner?

**Almost.** Here's the nuanced take:

- **Hash map wins on raw speed** and is the standard interview answer. It's also the simplest to read.
- **Two pointers wins on space** *only if* you could sort in-place — but since Two Sum requires returning *original indices*, you're forced to copy anyway, so the space advantage evaporates. It's really only compelling when you don't need original indices (a variant like "does any pair sum to target?").
- **Brute force is worth knowing** because it's the right call on very small inputs (n < ~10) where the overhead of hashing isn't worth it, or in memory-constrained embedded environments.

**For LeetCode #1 specifically: hash map is the clear winner.** O(n) time, clean code, no input mutation, handles all edge cases naturally.

Ready to code it up?

---

## Turn 3

**User:**

Absolutely. But let me present two concrete **coding options** before we write the actual code.

The question isn't really *which algorithm* anymore (hash map is clear)—it's *how to implement and structure it*. I want you to see the subtle trade-off:

---

**[A] Check-before-insert** (safer, more explicit)
```python
def twoSum(nums: list[int], target: int) -> list[int]:
    """Return indices of two numbers that sum to target."""
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:  # Check FIRST
            return [seen[complement], i]
        seen[num] = i  # Then store
    return []  # Guaranteed not needed, but makes intent clear
```

**Pro:** No edge-case surprises. We look for the *complement* before we add the current number, so we never accidentally reuse the same index even with duplicates.

---

**[B] Insert-then-check** (sleeker, but trap-prone)
```python
def twoSum(nums: list[int], target: int) -> list[int]:
    """Return indices of two numbers that sum to target."""
    seen = {}
    for i, num in enumerate(nums):
        seen[num] = i  # Store FIRST
        if target - num in seen:  # Then check
            return [seen[target - num], i]
    return []
```

**Pro:** One fewer line; *looks* more concise.  
**Con:** **Trap!** On input `[3, 3]` with target `6`, we store `{3: 0}`, then check if `3` is in seen (it is!), and incorrectly return `[0, 0]`—reusing the same index. 🚨

---

Which feels right to you? **A** is the defensive, explicit choice; **B** is the risky shortcut that *almost* works but fails on duplicates. Pick one and let's code it.

**Pair:**

Assistant: **A, without hesitation.** And it's not really a close call — here's why the framing of "safer vs. sleeker" undersells it:

> **B isn't a stylistic trade-off. It's a bug.**

"Sleeker" implies it's a valid alternative with a minor downside. It isn't — it produces a wrong answer on valid input. `[0, 0]` for `[3, 3], target=6` violates the problem's constraint that the two indices must be *distinct*. That's a correctness failure, not a style preference.

The other thing worth naming: **A isn't actually less concise in any meaningful way.** It's the same loop, same number of operations — the only difference is *order of two lines*. There's no real trade to make here.

---

So here it is — clean, correct, final:

```python
def twoSum(nums: list[int], target: int) -> list[int]:
    """Return indices of the two numbers that sum to target."""
    seen = {}  # value → index

    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i

    return []  # unreachable given problem guarantees exactly one solution
```

A few deliberate choices worth noting:

- **`return []` kept** — not because it can execute, but because it signals to the reader (and type checker) that the function always returns a list. Dropping it returns `None` implicitly, which can cause subtle bugs downstream.
- **`complement` named explicitly** — `target - num` inline works, but naming it makes the intent self-documenting at a glance.
- **No `else` after the `if`** — the `return` already exits, so `seen[num] = i` only runs when no match was found. Cleaner than wrapping in `else`.

Want to trace through a few test cases to verify?

---

## Turn 4

**User:**

**A, definitely.** You're right — B isn't a trade-off, it's a bug. I can see it immediately on `[3, 3]` with target `6`: we'd store `{3: 0}`, then the check finds `3` in `seen` and returns `[0, 0]`, which reuses the same index and violates the constraint.

The key insight is that **checking before inserting guarantees we never match the current element against itself**, which is the whole point.

Your final implementation is clean. I like the explicit `complement` variable and the `return []` at the end — it clarifies intent even though it's unreachable.

Yes, let's trace through a couple of test cases. That'll cement the logic:

1. **`[2, 7, 11, 15]`, target `9`** — straightforward, should hit on second pass
2. **`[3, 3]`, target `6`** — the edge case that kills option B
3. **Negative numbers**, e.g. `[-3, 4, 3, 90]`, target `0`** — mix of signs

Go ahead and walk through one or two of these so I can see the algorithm live.

**Pair:**

Assistant: Let's run all three — they each illustrate something different.

---

### Test 1: `[2, 7, 11, 15]`, target `9`
*The happy path — complement found on the very next element.*

| i | num | complement | seen (before check) | result |
|---|-----|------------|----------------------|--------|
| 0 | 2 | 7 | `{}` | miss → store `{2:0}` |
| 1 | 7 | 2 | `{2:0}` | **hit!** → return `[0, 1]` ✓ |

Exits after 2 iterations. `nums[0] + nums[1] = 2 + 7 = 9`. ✅

---

### Test 2: `[3, 3]`, target `6`
*The duplicate edge case — this is where B breaks, A handles it cleanly.*

| i | num | complement | seen (before check) | result |
|---|-----|------------|----------------------|--------|
| 0 | 3 | 3 | `{}` | miss → store `{3:0}` |
| 1 | 3 | 3 | `{3:0}` | **hit!** → return `[0, 1]` ✓ |

The key moment: at `i=1`, complement `3` is in `seen`, but it maps to index `0` — a *different* element. We return `[0, 1]`, not `[0, 0]`. Check-before-insert is what makes this work. ✅

---

### Test 3: `[-3, 4, 3, 90]`, target `0`
*Negative numbers — the algorithm doesn't care, arithmetic is arithmetic.*

| i | num | complement | seen (before check) | result |
|---|-----|------------|----------------------|--------|
| 0 | -3 | 3 | `{}` | miss → store `{-3:0}` |
| 1 | 4 | -4 | `{-3:0}` | miss → store `{-3:0, 4:1}` |
| 2 | 3 | -3 | `{-3:0, 4:1}` | **hit!** → return `[0, 2]` ✓ |

`nums[0] + nums[2] = -3 + 3 = 0`. The `90` at index 3 is never even visited. ✅

---

### The pattern across all three

Every case follows the same rhythm:
```
complement found? → return immediately (early exit)
complement missing? → bank current number, move on
```

No special casing for negatives, duplicates, or early exits — the structure handles all of it uniformly. That's the mark of a clean algorithm.

---

## Turn 5

**User:**

Perfect — those traces seal it. The logic is bulletproof. Check-before-insert + single pass = guaranteed correctness, even on tricky edge cases like duplicates and negatives.

I'm convinced. Ready to actually write it now.

What's next — do you want me to create a new file with the solution, or should we sketch out two options for how to structure the code? (e.g., standalone function vs. class method, test layout, etc.)

**Pair:**

**Run end**: error after 5 turns — turn idle for 300s — likely SDK hang
