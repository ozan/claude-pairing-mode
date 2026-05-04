# leetcode-two-sum

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:23:43

## Initial prompt

Let's solve Leetcode #1, 'Two Sum'. Given a list of integers and a target, return the indices of the two numbers that add up to the target. Assume exactly one solution exists.

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Hash map, one pass
For each number, check if its complement (`target - num`) is already in a dict. If yes, return both indices. If no, store the current number and index.

```diff
+++ two_sum.py
@@ -0,0 +1,7 @@
+def two_sum(nums, target):
+    seen = {}
+    for i, num in enumerate(nums):
+        complement = target - num
+        if complement in seen:
+            return [seen[complement], i]
+        seen[num] = i
```

[B] Nested loops, brute force
Try every pair of indices and check if they sum to target. Simple and correct, no extra data structures needed.

```diff
+++ two_sum.py
@@ -0,0 +1,6 @@
+def two_sum(nums, target):
+    for i in range(len(nums)):
+        for j in range(i + 1, len(nums)):
+            if nums[i] + nums[j] == target:
+                return [i, j]
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach would you go with?

### Student

I think I'll go with **A** — the hash map approach.

Here's my reasoning: option B works, but it's O(n²) because we're checking every pair. Option A is O(n) since we only pass through the list once, and looking up or storing items in a dictionary is O(1) on average.

The hash map approach also makes sense conceptually — for each number, we're asking "have I already seen the number I need to reach the target?" That feels cleaner than brute force.

Let me make sure I understand the logic though: we store numbers we've *already seen* (with their indices) in the dict, then for each new number, we check if its complement exists in that dict. If it does, we return immediately. If not, we add the current number to the dict and keep going. That way we never pair a number with itself, right?

Should we test this with an example to make sure it works?

---

## Turn 2

### Tutor

Tutor: Exactly right — and that ordering (check *then* insert) is the key detail that silently handles the "no self-pairing" constraint. Good catch.

Let me write the file and run it.

[Write(two_sum.py)]
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i


# Tests
print(two_sum([2, 7, 11, 15], 9))   # expect [0, 1]
print(two_sum([3, 2, 4], 6))        # expect [1, 2]
… (2 more lines)
  File created successfully at: two_sum.py

[Bash(python two_sum.py)]
  [0, 1]
  [1, 2]
  [0, 1]

Tutor: All three pass. The third case — `[3, 3], target=6` — is the interesting one. Both values are identical, so a naive approach might accidentally map one over the other. This one works because we check *before* inserting: when we hit the second `3`, the first is already in `seen`, so we find it immediately.

One small thing worth thinking about — which of these captures the complexity correctly?

OPTIONS:
[A] O(n) time, O(n) space
One pass through the list → O(n) time. The `seen` dict can grow to hold all n elements → O(n) space.

[B] O(n) time, O(1) space
One pass through the list → O(n) time. Each dict operation is O(1), so space is O(1).

(Reply with A or B, or ask a follow-up question.)

Tutor: What's the space complexity of our solution?

### Student

It's **A** — O(n) time, O(n) space.

I think option B is a trap. Yeah, each individual dict operation is O(1), but the `seen` dict itself can grow to hold up to n elements in the worst case (if the answer is the last two numbers, we'd store almost everything before finding it). That dict is taking up space proportional to the input size, so the overall space complexity is O(n), not O(1).

O(1) space would mean the space we use doesn't grow with the input — like if we were just using a couple of variables. But we're building a whole dictionary here.

Does that make sense?

---

## Turn 3

### Tutor

Tutor: Spot on. O(1) *per operation* and O(1) *total space* are completely different things — that conflation trips people up constantly. You nailed it.

The solution is clean and correct. Worth knowing there's one alternative approach that comes up sometimes:

OPTIONS:
[A] Sort + two pointers
Sort the array, then walk pointers inward from both ends: if the sum is too big, move the right pointer left; too small, move the left pointer right. Runs in O(n log n) time, O(1) extra space (ignoring the sort's stack).

[B] Hash map stays better
The hash map solution is already O(n) time. Sorting to save space costs O(n log n) — a worse time bound — and sorting *destroys the original indices*, so you'd have to carry them along anyway, losing the space benefit too.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach do you think is stronger for this problem?

### Student

**B** — the hash map stays better.

You're right that sorting would destroy the indices, which is the whole point of the problem. We need to return the original indices, not the values themselves. So even if we sorted, we'd have to track which elements came from where, which adds complexity and loses the space savings.

And yeah, O(n log n) is strictly worse than O(n) for time. The hash map solution is already optimal on that front.

I think the sorting approach might be useful in *different* scenarios — like if the problem asked just "do these two numbers exist?" without caring about indices. But for Two Sum as stated, the hash map solution we have is the way to go.

We've got a working, efficient solution that passes all the test cases. I think we're done here.

<done/>

---

**Run end:** done after 3 turn(s) in 63.1s
