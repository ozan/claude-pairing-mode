# leetcode-two-sum

- Source: `leetcode`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T08:56:47.125Z

---

## Turn 1

**User:**

Let's solve Leetcode #1, 'Two Sum'. Given a list of integers and a target, return the indices of the two numbers that add up to the target. Assume exactly one solution exists.

**Pair:**

Assistant: Good classic problem. There are a few ways to approach this — let me ask before we write any code:

OPTIONS:
[A] Sort + Two Pointers
Sort the array, then use two pointers (lo, hi) converging inward. O(n log n) time, O(1) extra space.

[B] Hash Map
Single pass: for each number, check if its complement already exists in a hash map. O(n) time, O(n) space.

(Reply with A or B, or ask a follow-up question.)

Assistant: Which approach would you go with?

---

## Turn 2

**User:**

I'd pick **B - Hash Map**.

The two-pointer approach would give us better space, but sorting loses the original indices — we'd have to track them separately or search backwards to find positions, which defeats the purpose. The hash map approach is cleaner here: O(n) time, we naturally preserve indices, and we only need one pass. For this problem, the time win over sorting is worth the extra space.

Let's go with B.

**Pair:**

Assistant: Exactly right. Now one implementation subtlety worth considering:

OPTIONS:
[A] Two-pass
```diff
+++ two_sum.py
@@ -0,0 +1,7 @@
+def two_sum(nums, target):
+    seen = {}
+    for i, n in enumerate(nums):
+        seen[n] = i  # build full map first
+    for i, n in enumerate(nums):
+        comp = target - n
+        if comp in seen and seen[comp] != i:
+            return [i, seen[comp]]
```

[B] Single-pass
```diff
+++ two_sum.py
@@ -0,0 +1,6 @@
+def two_sum(nums, target):
+    seen = {}
+    for i, n in enumerate(nums):
+        comp = target - n
+        if comp in seen:
+            return [seen[comp], i]
+        seen[n] = i
```

(Reply with A or B, or ask a follow-up question.)

Assistant: Which would you go with?

---

## Turn 3

**User:**

**B - Single-pass**.

The single-pass approach is cleaner here. By checking for the complement *before* inserting the current number, we naturally avoid using the same index twice — we don't need the `seen[comp] != i` guard. And since the problem guarantees exactly one solution, we can return immediately, which is more efficient than a second full pass.

It's the more idiomatic way to write this.

Let's go with B.

**Pair:**

Assistant: Spot on. Let's write it.

[Glob(two_sum.py)]
  No files found

[Write(two_sum.py)]
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, n in enumerate(nums):
        comp = target - n
        if comp in seen:
            return [seen[comp], i]
        seen[n] = i


if __name__ == "__main__":
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum([3, 2, 4], 6) == [1, 2]
… (3 more lines)

[Bash(python two_sum.py)]
  error: Exit code 127

[Bash(python3 two_sum.py)]
  All tests passed.

Assistant: All tests pass — including the `[3, 3]` duplicate case that would've tripped up the two-pass approach without the guard.

Summary of what we built:
- **O(n) time, O(n) space**
- Single pass — check complement first, insert after, so no element ever matches itself
- Early return on first hit (guaranteed by problem constraints)

Clean and done.

---

## Turn 4 (final)

**User:**

Looks good — solid work. You made thoughtful calls at each decision point (hash map for time + index preservation, single-pass to avoid the guard), and the implementation is clean. Edge cases covered, tests passing.

<done/>

---

**Run end**: done after 3 turns (93s)
