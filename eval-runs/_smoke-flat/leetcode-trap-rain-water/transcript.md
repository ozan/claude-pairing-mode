# leetcode-trap-rain-water

- Source: `leetcode`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T05:03:47.689Z

---

## Turn 1

**User:**

Let's solve Leetcode #42, 'Trapping Rain Water'. Given a list of non-negative integers representing bar heights, compute how much rainwater would be trapped between the bars.

**Pair:**

Thinking: Let me think about this problem and then present a good teaching moment about the approach.
  
  Trapping Rain Water - LeetCode #42
  
  The problem: Given an array of non-negative integers representing elevation heights, compute how much water can be trapped after it rains.
  
  Key insight: For each position i, the water trapped = min(max_left[i], max_right[i]) - height[i]
  
  There are several approaches:
  1. **Brute force** O(n²) - for each position, scan left and right to find max heights
  2. **Dynamic programming with prefix/suffix arrays** O(n) time, O(n) space - precompute max_left and max_right arrays
  
  
  3. **Two pointers** O(n) time, O(1) space - the most elegant solution
  
  I want to start with a foundational question about the core insight: whether water at position i equals min(max_left, max_right) - height[i] or max(max_left, max_right) - height[i], then build toward the two-pointer optimization afterward.

Assistant: Good problem — it has a clean insight at its core. Let me start with the key question before we write any code.

Thinking: Now let me propose the first teaching question about the core formula for water at each position.

OPTIONS:
[A] Use min of both maxes
Water at position `i` = `min(left_max, right_max) - height[i]`. Water is bounded by the *shorter* wall — the taller side can't help if the other side is lower.

[B] Use max of both maxes
Water at position `i` = `max(left_max, right_max) - height[i]`. The highest surrounding wall determines the potential water level.

(Reply with A or B, or ask a follow-up question.)

Assistant: For each bar, how much water sits on top of it?

---

## Turn 2

**User:**

I think it's [A] — the water level at each position is capped by the *lower* of the two surrounding maxima. 

Let me think through a concrete example: if I have bars like `[3, 0, 2, 0, 4]`, the bar at index 1 (height 0) has a max height of 3 to its left and 4 to its right. The water fills up to the level of the lower wall, which is 3. So water trapped = 3 - 0 = 3. If I used the max (4), that would overflow immediately over the 3-bar on the left.

So it's **[A]**: the water is trapped up to `min(left_max, right_max)`, and we subtract the bar height to get the water volume at that spot.

**Pair:**

Thinking: The user correctly picked option A and explained it perfectly. Now let me move on to the next teaching moment: the implementation approach. I'll propose between:
  
  1. The DP/prefix-suffix array approach: O(n) time, O(n) space - precompute max_left and max_right arrays
  2. The two-pointer approach: O(n) time, O(1) space
  
  This is a great teaching moment because the two-pointer approach is elegant and O(1) space, but the reasoning for why it works is subtle. Let me present these as options.
  
  Actually, let me think about the order of teaching. I should probably:
  1. First establish the formula (done ✓)
  
  
  2. Then maybe ask about naive vs DP approach
  3. Then ask about DP vs two-pointer
  
  Or I could skip straight to asking about DP vs two-pointer since the user seems knowledgeable. I think presenting DP vs two-pointer is the right move—the DP approach is straightforward with O(n) space, while the two-pointer approach achieves O(1) space but requires understanding why it works. That's the subtle insight worth exploring.
  
  Writing both implementations... Finishing the two-pointer solution...
  
  The two-pointer approach uses constant space instead of the O(n) arrays needed for the dynamic programming version, so I'll show both as trade-off options.

Assistant: Exactly right — water leaks over the lower wall, so `min` is the bound. Great intuition.

Now, the straightforward implementation precomputes `left_max` and `right_max` arrays and then does one pass. But there's a smarter approach. Which would you prefer to build?

OPTIONS:
[A] Two pointers O(1) space
```diff
+++ trap.py
@@ -0,0 +1,13 @@
+def trap(height):
+    left, right = 0, len(height) - 1
+    left_max = right_max = 0
+    water = 0
+    while left < right:
+        if height[left] < height[right]:
+            left_max = max(left_max, height[left])
+            water += left_max - height[left]
+            left += 1
+        else:
+            right_max = max(right_max, height[right])
+            water += right_max - height[right]
+            right -= 1
+    return water
```

[B] Prefix/suffix arrays O(n) space
```diff
+++ trap.py
@@ -0,0 +1,13 @@
+def trap(height):
+    n = len(height)
+    left_max  = [0] * n
+    right_max = [0] * n
+    left_max[0] = height[0]
+    for i in range(1, n):
+        left_max[i] = max(left_max[i-1], height[i])
+    right_max[-1] = height[-1]
+    for i in range(n-2, -1, -1):
+        right_max[i] = max(right_max[i+1], height[i])
+    return sum(min(left_max[i], right_max[i]) - height[i]
+               for i in range(n))
```

(Reply with A or B, or ask a follow-up question.)

Assistant: Both are O(n) time — but they differ in space. Which do you pick?

---

## Turn 3

**User:**

I'll go with **[A]** — the O(1) space is a big win, and both hit O(n) time anyway.

But I want to make sure I understand the logic: when we're at the left pointer and `height[left] < height[right]`, why can we safely say the water at `left` is just `left_max - height[left]`? We haven't scanned all the way to the right yet. Doesn't the right side matter?

**Pair:**

Thinking: The user picked the right answer and is asking a great follow-up question about the correctness of the two-pointer approach. Let me explain this clearly.
  
  The key insight is:
  
  When `height[left] < height[right]`, we know that:
  1. `right_max >= height[right]` (because right_max is the max seen so far from the right, and height[right] is the current right pointer value)
  2. `height[right] > height[left]`
  3. Therefore `right_max >= height[right] > height[left]`
  
  So `min(left_max, right_max) = left_max` — the right side doesn't matter because we KNOW it's taller than the left side. The water is fully determined by left_max.
   
  The water trapped at position `left` is `min(left_max, right_max) - height[left]`. Since we've established that `right_max > height[left]`, the limiting factor is always `left_max`, regardless of whether `left_max` is greater than or less than `right_max`. This is why we can safely compute the water level using only `left_max` without needing to know the exact value of `right_max`. So when `height[left] < height[right]`, I know that `true_right_max` is at least `height[right]`, which is greater than `height[left]`. This means `true_right_max > height[left]` for sure. In Case 1, if `left_max` doesn't exceed `true_right_max`, then the water trapped is simply `left_max - height[left]`, which I can calculate immediately. But in Case 2, where `left_max` is actually larger than `true_right_max`, I'd need to know the exact value of `true_right_max` to compute the water level — except wait, can that scenario even occur when `height[left] < height[right]`? If the max from the left side up to position `left` is greater than the max from `left` onward, that would mean...
  
  Actually, I think the real insight here is that when `height[left] < height[right]`, there's guaranteed to be a taller bar somewhere to the right of `left`, so the water at position `left` is constrained by what's on the left side, not the right. left `]`, which contradicts `left_max > right_max`. So this case is impossible, and we can safely use `left_max - height[left]` without worrying about the right side.
  
  Let me verify this with a concrete example to make sure the logic holds. At index 1, I process the final right position with height 0, adding 4 more units of water before the pointers meet. Now I'm verifying this result using the prefix/suffix maximum approach—computing the left and right maximums for each position, then calculating trapped water as the minimum of those two minus the bar height at each index, which confirms the total of 11 units. Continuing through the algorithm with this new example, I'm processing the left pointer since the left height is smaller, updating left_max and moving inward. Let me trace through to see if I can finally construct a case where left_max exceeds the true right_max while processing from the left side. I'm testing a different array to see if I can construct a case where the accumulated right_max is less than the true right_max when we need to process the left side. Let me trace through this example with heights [3, 0, 1, 0, 2] to verify the algorithm handles it correctly. = max(2, 0) = 2
    water += 2 - 0 = 2
    right = 2
  
  left=0, right=2, height[left]=3, height[right]=1.
  height[left]=3 >= height[right]=1, process right:
    right_max = max(2, 1) = 2
    water += 2 - 1 = 1
    right = 1
  
  left=0, right=1, height[left]=3, height[right]=0.
  height[left]=3 >= height[right]=0, process right:
    right_max = max(2, 0) = 2
    water += 2 - 0 = 2
    right = 0
  
  Done. Water = 5.
  
  Verify: heights=[3,0,1,0,2]
  left_max=[3,3,3,3,3], right_max=[3,2,2,2,2]
  min=[3,2,2,2,2], water=[0,2,1,2,0]=5 ✓
  
  Now I'm testing a different case with [1, 3, 0, 2] to see how the algorithm handles processing from the left side. When I process index 2 with height 0 from the left while right_max is 2, I need to trace through the steps carefully to understand the behavior.
  
  Continuing with [2, 3, 0, 1, 4], I'm working through the two-pointer approach step by step to verify the water calculation. I'm verifying the calculation worked correctly with that example, then moving on to construct a different scenario where the left_max exceeds the true right_max to test Case 2 of the algorithm. Let me work through heights = [5, 2, 0, 1, 3] and trace what the actual maximum values are from each position onward. Water totals to 6, which I can verify by computing the left and right maximums at each position and confirming the trapped water calculation. Now I'm trying to understand why I can't construct a Case 2 scenario—it seems like when processing from the left, the left_max needs to be less than or equal to the true right_max for the algorithm to work correctly, and I'm exploring what conditions would violate that assumption. I'm trying to construct a case where this algorithm would overcount by using the left_max instead of the true_right_max. I need h[left] < h[right] so we process from the left side, but also need left_max to exceed the actual maximum of all remaining heights to the right. Let me trace through a specific example to see if this scenario actually occurs. Now I'm testing this with a different array where the heights are [0, 4, 0, 2, 3]. Using the two-pointer approach, I process from the outside in—when the left height is smaller, I advance left and accumulate water based on the left maximum, and when the right is smaller or equal, I advance right and use the right maximum. Working through the iterations, I'm tracking how much water gets trapped at each position as the pointers converge.
  
  The final water trapped is 4, which I can verify by checking that at each position, the water level equals the minimum of the left and right maximums minus the bar height. Now I'm thinking about why Case 2 (where we'd need to process right but left_max exceeds true_right_max) can't actually occur. The key insight is that when we process left because h[left] < h[right], the left_max at that point must be less than or equal to the true right maximum from that position onward, because left_max only accumulates from the left side inward while the true right maximum is computed from the entire right portion. I'm working through the two cases: when left_max is less than or equal to true_right_max, the water trapped matches our formula, but when left_max exceeds true_right_max, I need to verify the algorithm never actually reaches that state. The key is that when we process from the left with h[left] < h[right], we're guaranteed certain constraints that prevent left_max from ever exceeding the true maximum on the right side. I'm trying to prove that when we process from the left and find h[left] < h[right], the left_max we've accumulated is guaranteed to be less than or equal to the true maximum to the right. The key insight is that if there were a taller bar somewhere in the left portion, we would have already processed it and moved the left pointer past it, so it couldn't still be constraining the current position. The key insight is that when `h[left] < h[right]`, we're guaranteed the true maximum height to the right of the current position is at least as large as `left_max`, so we can safely calculate the water trapped at `left` using `left_max` as the limiting factor without needing to know what's actually to the right. or [left..n-1] depending on definition).
  
  These can be compared independently. There's no reason why max(heights[0..left]) <= max(heights[left+1..n-1]).
  
  So I think the correct answer is: the algorithm is NOT just "left_max determines water at left when h[left] < h[right]."
  
  Actually, let me re-examine. The key insight is:
  
  When `h[left] < h[right]`:
  - `right_max` in our running variable >= `h[right]` > `h[left]`
  - If `left_max` (running) <= `right_max` (running): water at left = left_max - h[left] ✓
  - If `left_max` (running) > `right_max` (running): This means left_max > right_max >= h[right] > h[left]. But `right_max` is the max seen from the right side so far. The actual maximum from right to n-1 might be larger than what we've scanned yet.
  
  The water trapped at position `left` really depends on the true global left_max (which we have: max from 0 to left) and the true global right_max (max from left+1 to n-1, which we haven't fully computed). Let me reconsider the standard proof: when h[left] < h[right], the water at `left` should equal `left_max - height[left]`, meaning `left_max` is the limiting factor. The reasoning is that the true right_max from the unscanned portion must be at least h[right], which is already greater than h[left], so it can't be the constraint. Continuing with the next test case, I process position 2 from the right since the left height exceeds the right, accumulating 1 unit of water there. Then I verify the result matches the expected water distribution. Moving to another example with heights [0, 3, 0, 2], I start the two-pointer traversal again, processing from the left when the left height is smaller, then switching to process from the right when the left becomes taller.
  
  Now I'm trying to understand why Case 2 (where left_max exceeds the true global right maximum when h[left] < h[right]) seems impossible to construct. The key insight is that if left_max is greater than the true maximum on the right side of the array, then the tallest bar overall must be in the left portion. The algorithm tracks right_max as it scans from the right, but this only represents the maximum seen so far from that direction, not necessarily the global maximum for the entire right section.
  
  Let me verify the invariants more carefully: at any point, left_max correctly represents max(heights[0..left]) and right_max represents max(heights[right..n-1]) since we've already processed all positions from right onwards to the end. This means both pointers maintain accurate maximum values for their respective scanned regions, which constrains what failure cases are actually possible. I need to reconsider how right_max is being tracked as the right pointer moves leftward. Since right_max gets updated to include each new position as we move left, when the right pointer is at position r, right_max correctly represents max(heights[r..n-1]). For any position left, the true right maximum should be max(heights[left+1..n-1]), which can be decomposed into the max of the range between left and right, plus the max from right onward—and since right_max already captures that rightmost portion, I can use it directly when left+1 <= right. If left_max > h[right], then some earlier position had a height greater than h[right], but since h[left] < h[right] and left_max >= h[left], I need to think through whether this case even matters for the algorithm's correctness.
  
  Let me trace through a concrete example: heights = [5, 1, 0, 2]. Starting with left=0, right=3, since h[left] >= h[right], I process from the right side. As I move right inward, I track right_max and accumulate water at each step, eventually getting a total of 3 units trapped.
  
  Now testing with [3, 5, 1, 0, 2] to see how the algorithm handles a taller bar appearing on the right side mid-traversal. Now I'm testing this with heights [3, 5, 1, 2] using the two-pointer approach—processing from the right side first since the left element is taller than the right, then continuing inward until the pointers meet. The final water trapped is 1, which checks out against the min and max arrays.
  
  But I'm realizing something about Case 2: when we process left because h[left] < h[right], we know h[right] is greater than h[left], and since right is somewhere to the right of left, the true maximum to the right of left must be at least h[right]. However, that doesn't guarantee the true right maximum is greater than or equal to left_max—left_max could actually be larger than what we'll encounter on the right side. So why does the algorithm still work?
  
  The key insight is that right_max in the algorithm tracks the maximum from the current right pointer onward, which might underestimate the true maximum between left and right if there are taller bars we haven't scanned yet. But when h[left] < h[right], we can safely use left_max as the binding constraint because we know h[right] > h[left], guaranteeing that the true right maximum is at least h[right], and if left_max ≤ right_max, then left_max is definitely the limiting factor for water at position left. I'm going in circles here—let me think through the actual proof more carefully. The two-pointer approach maintains exact left and right maximums at the current pointers, and the key insight is that when we process from the side with the smaller height, we can guarantee the water level is determined by that side's maximum, since the opposite side must have an equal or greater maximum (otherwise we'd be processing from that side instead). water[left] = left_max - h[left] is only valid if left_max is guaranteed to be the minimum of the two maximum values on either side of left. The algorithm works because when h[left] < h[right], we know left_max ≤ right_max—meaning the global maximum isn't confined to just the left portion—so left_max becomes the binding constraint for water trapped at that position. but the global maximum could actually be somewhere in the middle rather than at the current boundary. Let me trace through a concrete example: heights = [3, 10, 0, 1, 0, 2]. If L[left] (the max from start to left) is greater than R[left] (the max from left to end), that means the tallest bar in the entire array must be somewhere before the current left position, since the global max appears in both ranges.
  
  Now I'm working through what happens when we've already passed that tallest bar—say it was at position k. After left moves past k, left_max gets locked at that tall value, but h[left] could be quite small. If h[right] is also small but still larger than h[left], we'd keep advancing left, yet left_max would exceed R[left], which contradicts the condition we're trying to prove. Let me test this with heights = [0, 5, 0, 2, 0, 3].
  
  At position 2, the right maximum is 3 and the left maximum is 5, so water trapped is min(5, 3) - 0 = 3. Tracing through the two-pointer algorithm: starting with left at 0 and right at 5, since h[0] < h[5], we process from the left, advancing left to 1. Now h[1] = 5 ≥ h[5] = 3, so we switch to processing from the right, advancing right to 4. At this point h[1] ≥ h[4], so we continue right, and the algorithm correctly accumulates the water at position 4.
  
  Continuing the trace: at position 3, we process from the right with right_max = 3, adding 1 unit of water. At position 2, we again process from the right, adding 3 units. The final total is 7 units of water, which matches the verification using the left_max and right_max arrays.
  
  The key insight is that when L[i] > R[i], position i gets processed from the right side of the two-pointer algorithm, not the left. This happens because the global maximum lies on the left side, so the algorithm naturally advances the right pointer inward until it reaches position i. The invariant that makes this work is that we can safely compute water at a position based on whichever side has the smaller maximum, since the larger maximum on the opposite side guarantees the water level. I'm questioning whether the condition h[left] < h[right] actually guarantees the invariant left_max <= right_max, since they're tracking different things. Let me think about when this algorithm would actually fail—it would only break if we process left with h[left] < h[right] but the true water level is less than what we calculate, which would mean the global right maximum is smaller than the left maximum, a contradiction that can't happen given how we're moving the pointers.
  
  When the global maximum appears at position g in the left region, once the left pointer reaches it, h[left] equals the global max and will always be >= h[right], so we'll only process from the right side afterward, ensuring we never incorrectly compute water for positions we haven't fully evaluated. position). Unless left has moved past g.
  
  Wait, when left moves past g (i.e., left > g), left_max remains global_max (since it's a running max). And now h[left] could be small. If h[right] > h[left] for the current right, we'd process from left.
  
  At this point: L[left] = left_max = global_max. And R[left] = max(heights[left..n-1]).
  
  Since global_max is at position g < left, it's NOT in [left..n-1]. So R[left] = max(heights[left..n-1]) < global_max = left_max.
  
  This is Case 2! L[left] > R[left]!
  
  But... does h[left] < h[right] actually occur in this case?
  
  After left has passed position g (global max), right_max has been accumulating from the right. Let me trace through a concrete example to see when this scenario actually plays out. With heights = [0, 5, 0, 2, 0, 3], I can walk through the loop step by step: starting with left=0 and right=5, I process left since h[0] < h[5], then advance left to 1. Now h[1]=5 >= h[5]=3, so I process right and move right to 4. Continuing this way shows how position 2 gets processed from the right side.
  
  The key realization is that once left reaches the global maximum, it stays there (or moves past it), and all remaining positions get processed from the right since the global max is always >= any remaining right values. Similarly, once right hits the global max, everything else processes from the left.
  
  When we process from the left (h[left] < h[right]), the global maximum hasn't been reached yet by the left pointer, so it must be at or to the right of the current position. This guarantees that the maximum to the right of left is at least as large as the maximum to the left, making L[left] the limiting factor and giving us the correct answer. I see the issue now—when the left pointer reaches the position holding the global maximum, the algorithm must process from the right side instead, which prevents the left pointer from advancing past that point. So if left_max exceeds the true right maximum, the left pointer gets stuck at the global max position and can't move further. The key insight is that the left pointer can never advance past the global maximum height—if it did, we'd have h[left] >= h[right], which contradicts our processing condition. So whenever we're at a position where h[left] < h[right], the tallest bar must be somewhere to the right of left, which means left_max is guaranteed to be the limiting factor for water trapped at that position.

Assistant: Great question — this is the subtle part. The right side *does* matter conceptually, but the algorithm guarantees you'll never need it.

Here's the key: **the left pointer can never advance past the global maximum.** When the left pointer sits on the tallest bar in the array, `h[left] >= h[right]` for *any* right pointer position — so we always process from the right instead. The left pointer stays put.

That means when `h[left] < h[right]` and we *are* about to process from the left, we know the global max hasn't been passed yet — it must be somewhere to the **right** of `left`. Therefore:

```
true_right_max ≥ global_max ≥ left_max
```

So `left_max` is guaranteed to be the smaller (binding) wall, and `left_max - height[left]` is exactly right — no information about what's between the two pointers is needed.

The symmetric argument holds for the right side: when `h[right] <= h[left]`, the global max must lie to the left, making `right_max` the binding constraint.

Neat, right? The two pointers work because each side only "claims" a position when it's safe to do so. Let's write the file now:

[Bash(ls trap.py 2>/dev/null && echo "exists" || echo "not found")]
  not found

[Write(trap.py)]
def trap(height):
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0
    while left < right:
        if height[left] < height[right]:
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:
            right_max = max(right_max, height[right])
            water += right_max - height[right]
… (3 more lines)

Assistant: Now let me add tests to verify:

OPTIONS:
[A] Edge cases plus assert
```diff
+++ trap.py
@@ -11,0 +12,9 @@

+if __name__ == "__main__":
+    assert trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
+    assert trap([4, 2, 0, 3, 2, 5]) == 9
+    assert trap([3, 0, 2, 0, 4]) == 7
+    assert trap([]) == 0
+    assert trap([5]) == 0
+    assert trap([5, 5]) == 0
+    print("all tests passed")
```

[B] Use unittest.TestCase
```diff
+++ trap.py
@@ -11,0 +12,14 @@

+import unittest
+
+class TestTrap(unittest.TestCase):
+    def test_examples(self):
+        self.assertEqual(trap([0,1,0,2,1,0,1,3,2,1,2,1]), 6)
+        self.assertEqual(trap([4,2,0,3,2,5]), 9)
+        self.assertEqual(trap([3,0,2,0,4]), 7)
+    def test_edge(self):
+        self.assertEqual(trap([]), 0)
+        self.assertEqual(trap([5]), 0)
+        self.assertEqual(trap([5, 5]), 0)
+
+if __name__ == "__main__":
+    unittest.main()
```

(Reply with A or B, or ask a follow-up question.)

Assistant: How should we test it?

---

## Turn 4

**User:**

I'll go with **[A]** — the assert statements are simpler and give us immediate feedback. For a single function like this, we don't need the overhead of unittest.

Let me run it to verify the implementation works:

[Run(python trap.py)]

**Pair:**

Thinking: The user wants to run the tests. Let me first apply the edit to add the test cases, then run the file.

Assistant: Let me add those tests first, then run:

[Edit(trap.py)]
--- before
    return water
--- after
    return water

if __name__ == "__main__":
    assert trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert trap([4, 2, 0, 3, 2, 5]) == 9
    assert trap([3, 0, 2, 0, 4]) == 7
    assert trap([]) == 0
    assert trap([5]) == 0
    assert trap([5, 5]) == 0
    print("all tests passed")

[Bash(python trap.py)]
  error: Exit code 127

[Bash(python3 trap.py)]
  all tests passed

Assistant: All green. Here's the final file:

[Read(trap.py)]
  1	def trap(height):
  2	    left, right = 0, len(height) - 1
  3	    left_max = right_max = 0
  4	    water = 0
  5	    while left < right:
  6	        if height[left] < height[right]:
  7	            left_max = max(left_max, height[left])
  8	            water += left_max - height[left]
  9	            left += 1
  10	        else:
  11	            right_max = max(right_max, height[right])
  12	            water += right_max - height[right]
  … (12 more lines)

Assistant: Clean solution. To recap what we built and why it works:

- **Formula**: water at `i` = `min(left_max, right_max) - height[i]` — bounded by the *shorter* wall
- **Two-pointer trick**: avoids storing O(n) prefix/suffix arrays by processing from whichever side has the smaller current bar
- **Correctness guarantee**: the left pointer can never advance past the global maximum (since `h[left] >= h[right]` there always), so whenever we process from the left, the global max is to the right — ensuring `right_max_global >= left_max`, making `left_max` the safe binding constraint

**O(n) time, O(1) space** — optimal on both axes.

---

## Turn 5 (final)

**User:**

Perfect — that all makes sense now. The key insight I'm taking away is that the two-pointer approach **guarantees safety** by never letting us process a position until we're certain which constraint (left or right maximum) is actually binding. By always processing from the side with the smaller bar, we ensure we never pass the global maximum on the side we're scanning, which means the opposite side's maximum is always at least as large — making the current side's maximum the definite constraint.

This is a much more elegant solution than precomputing the full prefix/suffix arrays, and the O(1) space is a nice bonus. Thanks for walking through the subtle part — that was the trickiest bit to understand.

<done/>

---

**Run end**: done after 4 turns (292s)
