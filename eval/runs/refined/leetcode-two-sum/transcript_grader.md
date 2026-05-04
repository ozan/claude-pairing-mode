# leetcode-two-sum

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:38:58

## Initial prompt

Let's solve Leetcode #1, 'Two Sum'. Given a list of integers and a target, return the indices of the two numbers that add up to the target. Assume exactly one solution exists.

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Tutor: Good starting point — let's think about the core algorithm first.

OPTIONS:
[A] Hash map, one pass
For each number, check if its complement (`target - num`) is already in a dict. If yes, return both indices. If no, store the current number and index.

```diff
+++ two_sum.py
@@ -0,0 +1,6 @@
+def two_sum(nums, target):
+    seen = {}
+    for i, num in enumerate(nums):
+        complement = target - num
+        if complement in seen:
+            return [seen[complement], i]
+        seen[num] = i
```

[B] Nested loops, brute force
Check every pair of indices `(i, j)` and return the first pair where the values sum to `target`.

```diff
+++ two_sum.py
@@ -0,0 +1,5 @@
+def two_sum(nums, target):
+    for i in range(len(nums)):
+        for j in range(i + 1, len(nums)):
+            if nums[i] + nums[j] == target:
+                return [i, j]
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach do you prefer — and can you guess what the time complexity difference is between them?

### Student

I'd like to go with **Option A** — the hash map approach.

My thinking: Option B would work, but it checks every pair, which feels inefficient. With the hash map, I only pass through the list once, so instead of comparing everything to everything, I'm just looking up whether each number's complement has already been seen.

For complexity: I'm guessing Option B is O(n²) because of the nested loops, and Option A should be O(n) since we're doing one pass and dictionary lookups are constant time?

Let me ask though — when we store `seen[num] = i`, are we storing the index of the *current* number? And then when we find a match, we return `[seen[complement], i]`, which gives us the index of the complement and the index of the current number. Is that right?

---

## Turn 2

### Tutor

Tutor: Exactly right on all counts. `seen[num] = i` maps the *value* to its index, so `seen[complement]` retrieves the index of the number we need. Your complexity analysis is spot on too.

Let me write the file, then there's one subtle ordering detail worth thinking about:

[Write(two_sum.py)]
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i

  File created successfully at: two_sum.py

Tutor: Now — notice we **check before storing**. Does that order matter?

OPTIONS:
[A] Order doesn't matter
Whether we check or store first, the dict will eventually contain all prior elements, and the lookup will find the right complement either way.

[B] Order matters — a subtle bug lurks
If we store *before* checking (swapping the two lines), a case like `nums = [4, 1, 3], target = 8` would cause the lookup for `4`'s complement (`4`) to find itself at index `0`, returning `[0, 0]` — the same index twice.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which do you think is true?

### Student

I think it's **Option B** — the order definitely matters.

If we stored before checking, then when we process a number, its own index would already be in the `seen` dict. So if we had a case where a number's complement equals itself (like when `target = 8` and we see `4`, since `8 - 4 = 4`), we'd incorrectly return `[0, 0]` instead of finding a *different* number that adds up.

By checking *first*, we ensure that when we find a complement, it's always from a *previous* element — never the current one. That way we're guaranteed to have two different indices.

Does that logic check out?

---

## Turn 3

### Tutor

Tutor: Spot on. The problem statement says "exactly one solution exists" but says nothing about the values — `[4, 4]` with `target=8` is totally valid input, and store-first would silently return a wrong answer. Check-first is the safe invariant: *only match against numbers you've already passed*.

Let's add tests. Given the edge case we just uncovered, which test suite do you think gives better coverage?

OPTIONS:
[A] Tests with edge case
```diff
+++ two_sum.py
@@ -8,0 +9,9 @@
+
+if __name__ == "__main__":
+    assert two_sum([2, 7, 11, 15], 9)  == [0, 1]
+    assert two_sum([3, 2, 4], 6)       == [1, 2]
+    assert two_sum([3, 3], 6)          == [0, 1]
+    assert two_sum([-1, -2, -3, -4], -6) == [1, 3]
+    print("all tests passed")
```

[B] Tests without edge case
```diff
+++ two_sum.py
@@ -8,0 +9,8 @@
+
+if __name__ == "__main__":
+    assert two_sum([2, 7, 11, 15], 9)  == [0, 1]
+    assert two_sum([3, 2, 4], 6)       == [1, 2]
+    assert two_sum([1, 5, 3, 9], 12)   == [1, 3]
+    print("all tests passed")
```

(Reply with A or B, or ask a follow-up question.)

### Student

Definitely **Option A** — it has the edge case test.

The `assert two_sum([3, 3], 6) == [0, 1]` test is exactly the scenario we just talked about. If someone accidentally swapped the check and store lines (or made that mistake in a similar implementation), this test would catch it immediately by failing. Without it, a bug like that could slip through.

Option B would pass even with the store-first mistake, so we'd have false confidence that the code is correct when it actually isn't.

Should we go ahead and add Option A's tests to the file?

---

## Turn 4

### Tutor

Tutor: Exactly — a test suite that doesn't catch a known bug class isn't really testing anything. Let's add them.

[Read(two_sum.py)]
  1	def two_sum(nums, target):
  2	    seen = {}
  3	    for i, num in enumerate(nums):
  4	        complement = target - num
  5	        if complement in seen:
  6	            return [seen[complement], i]
  7	        seen[num] = i
  8

[Edit(two_sum.py)]
--- before
        seen[num] = i

--- after
        seen[num] = i

if __name__ == "__main__":
    assert two_sum([2, 7, 11, 15], 9)    == [0, 1]
    assert two_sum([3, 2, 4], 6)         == [1, 2]
    assert two_sum([3, 3], 6)            == [0, 1]
    assert two_sum([-1, -2, -3, -4], -6) == [1, 3]
    print("all tests passed")

  The file two_sum.py has been updated successfully.

[Bash(python two_sum.py)]
  all tests passed

Tutor: All green. Here's what we landed on and why each decision mattered:

| Decision | Choice | Why |
|---|---|---|
| Algorithm | Hash map, one pass | O(n) vs O(n²) |
| Check vs store order | Check first | Prevents matching a number against itself |
| Test suite | Includes `[3, 3]` case | Catches the store-first bug; happy-path tests don't |

The general principle behind the last two points: **write tests that would fail if your code had the specific bug you just reasoned about.** A test that passes on both correct and buggy code isn't doing its job.

### Student

That's really helpful — thank you for walking through this systematically. I can see now how the order of operations wasn't just a detail, it was *the* critical detail that makes the algorithm correct. And the test case for `[3, 3]` is such a concrete way to verify it.

I especially appreciate the principle you called out: tests should actually catch bugs you've thought through, not just verify the happy path. That's something I'll keep in mind going forward.

The solution feels complete now — the code is correct, efficient, tested with edge cases in mind, and I understand *why* each part matters. I think we're done here.

<done/>

---

**Run end:** done after 4 turn(s) in 86.4s
