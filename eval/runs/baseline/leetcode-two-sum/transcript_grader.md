# leetcode-two-sum

- Condition: `baseline`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T20:49:47

## Initial prompt

Let's solve Leetcode #1, 'Two Sum'. Given a list of integers and a target, return the indices of the two numbers that add up to the target. Assume exactly one solution exists.

---

## Turn 1

### Tutor

Tutor: ## LeetCode #1 — Two Sum

### Approach: Hash Map (One Pass)

The key insight is: for each number `x`, we need `target - x`. Instead of checking all pairs (O(n²)), we store each number's index in a hash map as we go, so we can look up the complement in O(1).

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}  # Maps number -> index

    for i, num in enumerate(nums):
        complement = target - num

        if complement in seen:
            return [seen[complement], i]

        seen[num] = i
```

### Walkthrough

```
nums = [2, 7, 11, 15], target = 9

i=0, num=2  → complement=7  → not in seen → seen={2:0}
i=1, num=7  → complement=2  → 2 IS in seen → return [0, 1] ✅
```

### Complexity

| | Complexity |
|---|---|
| **Time** | O(n) — single pass through the array |
| **Space** | O(n) — hash map stores up to n elements |

This beats the naïve O(n²) brute-force approach of checking every pair.

### Test Cases

```python
assert two_sum([2, 7, 11, 15], 9)  == [0, 1]
assert two_sum([3, 2, 4],     6)   == [1, 2]
assert two_sum([3, 3],        6)   == [0, 1]
```

### Key Insight

By storing numbers we've **already seen**, we turn the inner loop into a single O(1) hash map lookup. Notice we only return `seen[complement]` **after** confirming it exists — this also naturally avoids using the same index twice (e.g. `[3]` with target `6` won't falsely match index 0 with itself).

### Student

Thanks for walking me through this! The hash map approach makes a lot of sense—I can see how it avoids the O(n²) brute force by trading space for speed.

One thing I want to make sure I understand: when we check `if complement in seen`, we're only looking at numbers we've *already processed*, right? So if the complement hasn't been seen yet, we just add the current number and move on. That's what prevents us from matching an element with itself—we haven't stored it yet.

Let me trace through the third test case to confirm I've got it:

```
nums = [3, 3], target = 6

i=0, num=3  → complement=3  → 3 not in seen yet → seen={3:0}
i=1, num=3  → complement=3  → 3 IS in seen (from i=0) → return [0, 1] ✅
```

So even though both elements are the same value, they have different indices, and we correctly return both indices. That makes sense!

I think I've got the logic down. Let me quickly code this up and test it locally to make sure it works:

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    
    for i, num in enumerate(nums):
        complement = target - num
        
        if complement in seen:
            return [seen[complement], i]
        
        seen[num] = i
```

This should handle all the test cases correctly. Is there anything else I should consider about this solution, or does this look good to submit?

---

## Turn 2

### Tutor

Tutor: Your trace is **exactly right**, and your understanding of *why* it works is spot on — the "add after checking" ordering is the elegant mechanism that prevents self-matching.

The solution is solid. A few quick things worth knowing before you submit:

### You're already covered ✅
- **Negative numbers** — work naturally since hash map keys can be any integer (e.g. `nums=[-1, 5], target=4` → returns `[0, 1]`)
- **Duplicate values** — handled correctly, as you traced
- **No fallback needed** — the problem guarantees exactly one solution, so the implicit `return None` at the end is never reached

### One subtle bonus property
Because you iterate **left to right**, `seen[complement]` is always the **earlier** index and `i` is always the **later** one. So your result is always index-sorted `[smaller, larger]` — not required by the problem, but a nice property.

### The one scenario this *would* break (not applicable here)
If the problem allowed **no solution**, you'd need to handle the case where the loop exhausts without returning. Since LeetCode #1 guarantees a solution, you're fine — but worth keeping in mind if you adapt this pattern elsewhere.

**Go ahead and submit** — this is the canonical optimal solution. 🚀

### Student

Got it! I really appreciate you pointing out those edge cases and the bonus property about the indices being naturally sorted. That's helpful context for when I adapt this pattern to similar problems later.

I feel confident about this solution now. The logic is clear, the complexity is optimal, and I understand *why* it works. Time to submit!

<done/>

---

**Run end:** done after 2 turn(s) in 29.3s
