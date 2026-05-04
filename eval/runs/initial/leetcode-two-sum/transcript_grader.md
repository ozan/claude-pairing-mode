# leetcode-two-sum

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T20:59:17

## Initial prompt

Let's solve Leetcode #1, 'Two Sum'. Given a list of integers and a target, return the indices of the two numbers that add up to the target. Assume exactly one solution exists.

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Tutor: Good, let's start with the core algorithmic approach. Two options:

OPTIONS:
[A] Nested loop search
For each element `i`, scan every `j > i` to find a pair that sums to target.
```diff
+++ two_sum.py
@@ -0,0 +1,5 @@
+def two_sum(nums, target):
+    for i in range(len(nums)):
+        for j in range(i + 1, len(nums)):
+            if nums[i] + nums[j] == target:
+                return [i, j]
```

[B] Hash map one-pass
Track seen values in a dict as you go: for each number, check if its complement is already stored.
```diff
+++ two_sum.py
@@ -0,0 +1,6 @@
+def two_sum(nums, target):
+    seen = {}
+    for i, n in enumerate(nums):
+        complement = target - n
+        if complement in seen:
+            return [seen[complement], i]
+        seen[n] = i
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach would you go with?

### Student

I think I'd like to understand the tradeoffs a bit better before choosing.

Option A looks simpler to understand at first glance — just brute force checking all pairs. But I'm guessing it's slower for large lists because of the nested loops, right? That would be O(n²)?

Option B uses a hash map, which I think would be O(n) time since we only loop through once, but I'm less familiar with how that complement logic works. Can you walk me through why checking `target - n` in the dictionary tells us we found a valid pair? I want to make sure I understand the logic before we go with it.

---

## Turn 2

### Tutor

Tutor: You've got the complexity analysis exactly right — A is O(n²), B is O(n).

Here's the intuition for the complement logic. Say `nums = [2, 7, 11, 15]` and `target = 9`.

We need two numbers `a + b == target`. If we're looking at `a`, then the number we *need* is `b = target - a`. That's the complement.

So as we walk the list, we ask: **"Have I already seen the number that would pair with me?"**

Tracing through:
- `i=0, n=2`: complement is `9-2=7`. Is `7` in `seen`? No. Store `seen[2]=0`.
- `i=1, n=7`: complement is `9-7=2`. Is `2` in `seen`? **Yes, at index 0!** Return `[0, 1]`. ✓

The key insight is that we only need one pass because we're recording *past* elements as we go. By the time we reach the second number of a valid pair, the first is already in the dict.

**On the tradeoffs:**

| | Time | Space |
|---|---|---|
| Nested loops | O(n²) | O(1) |
| Hash map | O(n) | O(n) |

Option A uses no extra memory, which sounds appealing — but for n=10,000 elements, that's 100 million comparisons vs 10,000 lookups. The space cost of a dict is almost never the bottleneck in practice.

Want to go with B?

### Student

That makes total sense now — thanks for walking through the trace! I see it: we're building up a "seen" dictionary as we go, so by the time we hit the complement, it's already recorded from a previous iteration. That's elegant.

Yeah, I'm convinced on the tradeoffs. O(n) is way better than O(n²) for any reasonably sized input, and the O(n) extra space is a fair tradeoff. 

Let's go with **Option B**. Before we finalize though — does the code handle edge cases okay? Like, what if someone passes in `[3, 3]` with `target = 6`? Would the hash map solution accidentally use the same index twice?

---

## Turn 3

### Tutor

Tutor: Great catch — this is worth tracing carefully. Let's check `nums = [3, 3]`, `target = 6`:

- `i=0, n=3`: complement is `3`. Is `3` in `seen`? **No** (dict is empty). Store `seen[3] = 0`.
- `i=1, n=3`: complement is `3`. Is `3` in `seen`? **Yes, at index 0**. Return `[0, 1]`. ✓

It handles it correctly — and the reason *why* is subtle and worth noting. The order of operations inside the loop is:

1. **Check** if complement is in `seen`
2. **Then** add current element to `seen`

If those were reversed (add first, then check), `i=0` would store `seen[3]=0` and then immediately find it as its own complement — returning `[0, 0]`, which is wrong. The check-before-insert order is what prevents an index from matching itself.

Let's write the file:

[Write(two_sum.py)]
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        complement = target - n
        if complement in seen:
            return [seen[complement], i]
        seen[n] = i

  File created successfully at: two_sum.py

Tutor: Clean and done. Want to add some test cases to verify, or explore anything else about the solution?

### Student

Actually, I think we're good! The solution is solid and I understand the logic now — especially why the check-before-insert order matters for edge cases like `[3, 3]`. That was a great detail to catch.

Let me just mentally run through one more quick example to feel confident: `nums = [3, 2, 4]`, `target = 6`:
- `i=0, n=3`: complement = 3, not in seen. Store `seen[3]=0`.
- `i=1, n=2`: complement = 4, not in seen. Store `seen[2]=1`.
- `i=2, n=4`: complement = 2, **is in seen at index 1**. Return `[1, 2]`. ✓

Yep, that works. I feel solid on this problem now.

<done/>

---

**Run end:** done after 3 turn(s) in 41.5s
