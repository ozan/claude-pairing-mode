# leetcode-two-sum

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:51:22

## Initial prompt

Let's solve Leetcode #1, 'Two Sum'. Given a list of integers and a target, return the indices of the two numbers that add up to the target. Assume exactly one solution exists.

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Hash map, one pass
For each number, check if its complement (`target - num`) is already in a dictionary. If so, return the pair of indices. Otherwise store `num → index` and continue.

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

[B] Nested loop, all pairs
Check every pair `(i, j)` until we find one that sums to the target.

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

Tutor: Which approach do you want to go with?

### Student

I think I'll go with **A** — the hash map approach.

I can see why it's more efficient (O(n) instead of O(n²)), and I want to understand how the dictionary lets us avoid checking all pairs. Let me make sure I follow the logic: we're building up a map of numbers we've seen as we go, and for each new number, we just check if its complement already exists in that map. That's clever because we only need one pass through the list.

Let me code this up and test it with a simple example to make sure I've got it right.

---

## Turn 2

### Tutor

Tutor: Exactly right — you've got the intuition nailed. Let me write the file.

[Write(two_sum.py)]
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i

  File created successfully at: two_sum.py

Tutor: Now — before we test, there's a subtle ordering question worth thinking about. Notice we check `seen` *before* inserting `num`. What happens if we flip that order?

OPTIONS:
[A] Insert then check
```diff
+++ two_sum.py
@@ -3,4 +3,4 @@
     for i, num in enumerate(nums):
         complement = target - num
+        seen[num] = i
         if complement in seen:
             return [seen[complement], i]
-        seen[num] = i
```

[B] Check then insert
```diff
+++ two_sum.py
@@ -3,4 +3,4 @@
     for i, num in enumerate(nums):
         complement = target - num
         if complement in seen:
             return [seen[complement], i]
         seen[num] = i
```
(unchanged — this is what we already have)

(Reply with A or B, or ask a follow-up question.)

Tutor: Which ordering is correct?

### Student

I think **B** is correct — check then insert, which is what we already have.

Here's my reasoning: if we insert `num` first (option A), then when we check for the complement, we might accidentally match the number against itself. For example, if `target = 4` and `nums = [2, 7, 11, 15]`, when we process the first `2`, we'd insert it into `seen`, then check if `complement = 4 - 2 = 2` exists. It would find itself and return `[0, 0]`, which is wrong — we need two *different* indices.

By checking first (option B), we only find the complement if we've actually seen it in a *previous* iteration, so we can't match a number with itself. That's the key.

---

## Turn 3

### Tutor

Tutor: Spot on. The `[2, 2]` / `target=4` case is exactly the one to stress-test this. Let's verify with a few cases:

[Bash(cd /Users/powerpraise/Desktop && python3 -c "
from two_sum import two_sum

cases = [
    ([2, 7, 11, 15], 9,  [0, 1]),  # basic
    ([3, 2, 4],      6,  [1, 2]),  # answer not at start
    ([3, 3],         6,  [0, 1]),  # duplicate values
    ([2, 2],         4,  [0, 1]),  # self-match trap
]
for nums, target, expected in cases:
    result = two_sum(nums, target)
    status = '✓' if result == expected else '✗'
    print(f'{status}  two_sum({nums}, {target}) = {result}  (expected {expected})')
"
)]
  error: Exit code 1

[Bash(python3 -c "
from two_sum import two_sum

cases = [
    ([2, 7, 11, 15], 9,  [0, 1]),  # basic
    ([3, 2, 4],      6,  [1, 2]),  # answer not at start
    ([3, 3],         6,  [0, 1]),  # duplicate values
    ([2, 2],         4,  [0, 1]),  # self-match trap
]
for nums, target, expected in cases:
    result = two_sum(nums, target)
    status = '✓' if result == expected else '✗'
    print(f'{status}  two_sum({nums}, {target}) = {result}  (expected {expected})')
"
)]
  ✓  two_sum([2, 7, 11, 15], 9) = [0, 1]  (expected [0, 1])
  ✓  two_sum([3, 2, 4], 6) = [1, 2]  (expected [1, 2])
  ✓  two_sum([3, 3], 6) = [0, 1]  (expected [0, 1])
  ✓  two_sum([2, 2], 4) = [0, 1]  (expected [0, 1])

Tutor: All green, including the self-match trap cases. The solution is clean and correct — O(n) time, O(n) space, handles duplicates, and the check-before-insert ordering guards against the subtle index reuse bug you identified.

Here's the final state of the file:

```python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
```

Seven lines. Hard to do better for this problem.

### Student

Perfect! Those test cases really solidify it — especially seeing the `[2, 2]` case pass. I can see now why the check-before-insert order is so critical; it's a subtle but essential guard.

I feel good about this solution. The logic is clean:
1. One pass through the list
2. For each number, compute what we'd need to reach the target
3. Check if we've already seen that complement
4. If yes, return the indices; if no, remember this number and move on

And the space/time tradeoff (O(n) space for O(n) time instead of O(1) space for O(n²) time) makes total sense for this problem.

<done/>

---

**Run end:** done after 3 turn(s) in 60.0s
