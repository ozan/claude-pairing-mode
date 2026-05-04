# leetcode-two-sum

- Source: `leetcode`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:37:27.557Z

---

## Turn 1

**User:**

Let's solve Leetcode #1, 'Two Sum'. Given a list of integers and a target, return the indices of the two numbers that add up to the target. Assume exactly one solution exists.

**Pair:**

Assistant: Classic. Before we write any code, let's nail the approach — this is worth thinking about carefully.

OPTIONS:
[A] Nested loop
For each element, scan every other element to find a pair that sums to target. Simple and correct.

```diff
+++ two_sum.py
@@ -0,0 +1,6 @@
+def two_sum(nums, target):
+    for i in range(len(nums)):
+        for j in range(i + 1, len(nums)):
+            if nums[i] + nums[j] == target:
+                return [i, j]
```

[B] Hash map (one pass)
Track each number's index in a dict. For each element, check if its complement already exists.

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

(Reply with A or B, or ask a follow-up question.)

Assistant: Which approach do you want to go with?

---

## Turn 2

**User:**

I'd go with **B** — the hash map approach.

Here's my reasoning: We're solving a classic interview problem, and this is a great moment to learn the *pattern*. Option A works, but it's O(n²), which means the solution degrades with larger inputs. Option B is O(n) and teaches a powerful technique: using a hash map to trade a bit of space for a major speed win. This "complement lookup" pattern shows up everywhere in real problems.

Plus, Option B is still readable and not more complex — it's a cleaner win.

Let's go with **B**.

**Pair:**

Assistant: Exactly right — and you nailed the framing: it's not just faster, it's a *reusable pattern*. Complement lookup via hash map shows up in Two Sum variants, subarray problems, anagram checks, and more.

[Write(two_sum.py)]
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i


Assistant: Let's add a few tests to verify correctness. One thing worth thinking about: how should we handle the test for `[3, 3]` with target `6` — where both numbers are the same value? The one-pass approach handles this correctly because we only add to `seen` *after* checking, so we never match an index with itself.

OPTIONS:
[A] assert statements
```diff
+++ two_sum.py
@@ -7,0 +8,7 @@
+
+if __name__ == "__main__":
+    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
+    assert two_sum([3, 2, 4], 6) == [1, 2]
+    assert two_sum([3, 3], 6) == [0, 1]
+    print("All tests passed.")
```

[B] unittest.TestCase
```diff
+++ two_sum.py
@@ -7,0 +8,13 @@
+
+import unittest
+
+class TestTwoSum(unittest.TestCase):
+    def test_basic(self):
+        self.assertEqual(two_sum([2, 7, 11, 15], 9), [0, 1])
+    def test_middle(self):
+        self.assertEqual(two_sum([3, 2, 4], 6), [1, 2])
+    def test_duplicate(self):
+        self.assertEqual(two_sum([3, 3], 6), [0, 1])
+
+if __name__ == "__main__":
+    unittest.main()
```

(Reply with A or B, or ask a follow-up question.)

Assistant: Which style for the tests?

---

## Turn 3 (final)

**User:**

I'd go with **A** — the simple assert statements.

Here's why: For a Leetcode problem at this scale, assert statements are perfect. They're lightweight, direct, and mirror how most people validate solutions in interviews or quick coding sessions. unittest.TestCase is great for larger projects with dozens of tests that need discovery and reporting, but it adds ceremony we don't need here.

Plus, asserts keep the file focused on the core logic — the solution stays in the spotlight, tests are just a quick sanity check below it.

**A** it is.

[Update(two_sum.py)]
```diff
+++ two_sum.py
@@ -7,0 +8,7 @@
+
+if __name__ == "__main__":
+    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
+    assert two_sum([3, 2, 4], 6) == [1, 2]
+    assert two_sum([3, 3], 6) == [0, 1]
+    print("All tests passed.")
```

Done. Let's verify it works:

```bash
python two_sum.py
```

Should print `All tests passed.` ✓

The solution is solid: O(n) time, O(n) space, handles edge cases (duplicates, any ordering), and demonstrates the complement-lookup pattern. You'll see this exact technique in interview follow-ups too — "what if you wanted to find three numbers?" or "find all pairs that sum to target?" The hash map approach scales well to those variants.

<done/>

---

**Run end**: done after 2 turns (52s)
