# leetcode-two-sum

- Source: `leetcode`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T02:20:01.090Z

---

## Turn 1

**User:**

Let's solve Leetcode #1, 'Two Sum'. Given a list of integers and a target, return the indices of the two numbers that add up to the target. Assume exactly one solution exists.

**Pair:**

Assistant: Classic. Before we write a line — what's your instinct on the core approach?

OPTIONS:
[A] Nested loops
```diff
+++ two_sum.py
@@ -0,0 +1,6 @@
+def two_sum(nums: list[int], target: int) -> list[int]:
+    for i in range(len(nums)):
+        for j in range(i + 1, len(nums)):
+            if nums[i] + nums[j] == target:
+                return [i, j]
```

[B] Hash map
```diff
+++ two_sum.py
@@ -0,0 +1,7 @@
+def two_sum(nums: list[int], target: int) -> list[int]:
+    seen: dict[int, int] = {}
+    for i, num in enumerate(nums):
+        complement = target - num
+        if complement in seen:
+            return [seen[complement], i]
+        seen[num] = i
```

(Reply with A or B, or ask a follow-up question.)

Assistant: Which approach — **A** (nested loops) or **B** (hash map)?

---

## Turn 2

**User:**

B

The hash map approach is more efficient — O(n) vs O(n²) — and it's the standard pattern for this problem. The complement trick is clean: as we iterate, we check if we've already seen the value that would pair with the current number.

**Pair:**

Assistant: Exactly right. Let me write that out.

[Glob(two_sum.py)]
  No files found

[Write(two_sum.py)]
def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i


Assistant: One detail worth noticing: we check `seen` *before* inserting `num`. That means a number can never match itself — so `two_sum([3, 5], 6)` won't falsely return `[0, 0]` even though `3 + 3 == 6`.

Want to add some tests?

---

## Turn 3

**User:**

Yeah, definitely. Let's test the happy path, edge cases, and make sure that self-match thing actually works.

**Pair:**

Assistant: Good call. Before I write them all out — one question about the self-match case specifically:

OPTIONS:
[A] Test [3, 5], target=6
```diff
+++ test_two_sum.py
@@ -0,0 +1,3 @@
+# self-match guard
+assert two_sum([3, 5], 6) is None
```
No valid pair sums to 6 (only one 3), so the result should be None.

[B] Test [3, 3], target=6
```diff
+++ test_two_sum.py
@@ -0,0 +1,3 @@
+# self-match guard
+assert two_sum([3, 3], 6) == [0, 1]
```
Two distinct 3s — a valid pair, but only if we don't match index 0 with itself.

(Reply with A or B, or ask a follow-up question.)

Assistant: Which is the sharper test for the self-match guard — **A** (`[3, 5]`) or **B** (`[3, 3]`)?

---

## Turn 4

**User:**

B

Option A doesn't really test the guard — `[3, 5]` has no valid pair at all, so it doesn't exercise the scenario we're checking for. Option B is the real test: it has two *distinct* 3s that should validly pair together, which directly verifies that the algorithm matches different *indices* of the same value, not an index with itself.

**Pair:**

Assistant: Exactly. Now let me put together the full suite.

[Glob(test_two_sum.py)]
  No files found

[Write(test_two_sum.py)]
from two_sum import two_sum


def test_happy_path():
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]


def test_answer_not_at_start():
    assert two_sum([3, 2, 4], 6) == [1, 2]


def test_self_match_guard():
… (11 more lines)

[Bash(cd /Users/oz/dev/ai-pair-proto && python -m pytest test_two_sum.py -v 2>&1)]
  error: Exit code 127

[Bash(cd /Users/oz/dev/ai-pair-proto && python3 -m pytest test_two_sum.py -v 2>&1)]
  error: Exit code 4

[Bash(python3 -m pytest /Users/oz/dev/ai-pair-proto/test_two_sum.py -v 2>&1)]
  error: Exit code 4

[Bash(pwd && ls *.py 2>&1)]
  /Users/oz/dev/ai-pair-proto/eval-runs/006-initial/leetcode-two-sum
  test_two_sum.py
  two_sum.py

[Bash(python3 -m pytest test_two_sum.py -v 2>&1)]
  ============================= test session starts ==============================
  platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0 -- /Library/Developer/CommandLineTools/usr/bin/python3
  cachedir: .pytest_cache
  rootdir: /Users/oz/dev/ai-pair-proto/eval-runs/006-initial/leetcode-two-sum
  collecting ... collected 5 items
  
  test_two_sum.py::test_happy_path PASSED                                  [ 20%]
  test_two_sum.py::test_answer_not_at_start PASSED                         [ 40%]
  test_two_sum.py::test_self_match_guard PASSED                            [ 60%]
  test_two_sum.py::test_negative_numbers PASSED                            [ 80%]
  test_two_sum.py::test_mixed_signs PASSED                                 [100%]
  
  … (1 more lines)

Assistant: 5/5. The `test_self_match_guard` case is the one that would've caught a "insert-before-check" bug — the others are just good hygiene (negatives, answer buried mid-array, mixed signs). We're done unless you want to push further.

---

## Turn 5 (final)

**User:**

Looks good. The solution is clean, efficient, well-tested, and we understand the key design decision. Nothing left to push on.

<done/>

---

**Run end**: done after 4 turns (127s)
