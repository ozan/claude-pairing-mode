# leetcode-longest-substring

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:51:22

## Initial prompt

Let's solve Leetcode #3, 'Longest Substring Without Repeating Characters'. Given a string, return the length of the longest substring with all distinct characters.

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Sliding window + set
Keep a `set` of characters in the current window. When a duplicate is found, remove from the left until it's gone, then expand right. O(n) time, but left pointer may advance many steps per right step.

[B] Sliding window + index map
Store `last_seen[char] = index` in a dict. When a duplicate is found, jump the left pointer directly to `last_seen[char] + 1` — no inner loop needed. O(n) time, each character visited once.

(Reply with A or B, or ask a follow-up question.)

Tutor: Both approaches use a sliding window, but they differ in how they handle a duplicate:

**Which would you go with?**

### Student

I think I'll go with **B** — the sliding window with an index map.

My reasoning: option A requires an inner loop to remove characters from the left one at a time, which feels less efficient even though both are O(n). Option B lets us jump the left pointer directly to where we need it, which should be faster in practice and cleaner to understand. Plus, storing the last seen index of each character feels like a natural way to "remember" where we've been.

Let me start coding that approach.

---

## Turn 2

### Tutor

Tutor: Exactly right — and your intuition about "remembering where we've been" is the key insight. Before we write the file, here's the one subtle decision in this implementation:

OPTIONS:
[A] Jump with max guard
```diff
+++ solution.py
@@ -0,0 +1,3 @@
+        if char in last_seen:
+            left = max(left, last_seen[char] + 1)
+        last_seen[char] = right
```

[B] Jump directly
```diff
+++ solution.py
@@ -0,0 +1,3 @@
+        if char in last_seen:
+            left = last_seen[char] + 1
+        last_seen[char] = right
```

(Reply with A or B, or ask a follow-up question.)

Tutor: How should we update `left` when we encounter a character we've seen before?

### Student

I'll go with **A** — the jump with `max` guard.

Here's my thinking: if we use option B and jump `left` directly to `last_seen[char] + 1`, we could accidentally move the left pointer *backwards*. That would happen if we encounter a duplicate character that we saw a while ago, but we've already advanced past it with a more recent duplicate. The `max()` ensures we only move left forward (or keep it in place), never backward. That way we maintain a valid window.

Let me write out the full solution with that logic.

---

## Turn 3

### Tutor

Tutor: Spot on. Let me write the full solution now.

[Write(solution.py)]
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last_seen = {}
        left = 0
        best = 0
        for right, char in enumerate(s):
            if char in last_seen:
                left = max(left, last_seen[char] + 1)
            last_seen[char] = right
            best = max(best, right - left + 1)
        return best

  File created successfully at: solution.py

Tutor: Clean and correct. One refinement worth considering:

OPTIONS:
[A] Keep the dict
Works for any Unicode string, no assumptions about character range. Dict lookup is O(1) amortized but has hashing overhead and potential cache misses.

[B] Swap to a fixed array
```diff
+++ solution.py
@@ -2,2 +2,2 @@
-        last_seen = {}
+        last_seen = [-1] * 128  # ASCII
```
Index directly by `ord(char)` — no hashing, better cache locality, faster in practice for ASCII inputs.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which would you go with?

### Student

I'll stick with **A** — keep the dict.

Here's why: the problem doesn't specify that the input is limited to ASCII, and using a dict makes the solution more general and robust. It works for any Unicode string without modification. Yes, there's some hashing overhead compared to a fixed array, but that's a micro-optimization. The code is already O(n) and clean.

For a coding interview or real-world code, I'd rather have a solution that's correct for all inputs and easy to understand than squeeze out a bit of speed on a specific character set. If performance profiling later showed the dict was a bottleneck, *then* I could optimize to an array — but I wouldn't premature-optimize for ASCII.

Let me test this solution with a few examples to make sure it works.

---

## Turn 4

### Tutor

Tutor: Exactly — profile before optimizing. Let's run through a few cases, including `"abba"` which specifically exercises the `max()` guard we chose:

[Bash(cd /tmp && python3 -c "
import sys
sys.path.insert(0, '.')

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last_seen = {}
        left = 0
        best = 0
        for right, char in enumerate(s):
            if char in last_seen:
                left = max(left, last_seen[char] + 1)
            last_seen[char] = right
            best = max(best, right - left + 1)
        return best

sol = Solution()
cases = [
    ('abcabcbb', 3),
    ('bbbbb',    1),
    ('pwwkew',   3),
    ('',         0),
    ('abba',     2),
]
for s, expected in cases:
    result = sol.lengthOfLongestSubstring(s)
    status = '✓' if result == expected else '✗'
    print(f'{status}  {repr(s):<14} → {result}  (expected {expected})')
"
)]
  ✓  'abcabcbb'     → 3  (expected 3)
  ✓  'bbbbb'        → 1  (expected 1)
  ✓  'pwwkew'       → 3  (expected 3)
  ✓  ''             → 0  (expected 0)
  ✓  'abba'         → 2  (expected 2)
  Shell cwd was reset to /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-7x5ch1lg

Tutor: All green, including `"abba"` — the case that would have failed without the `max()` guard.

**Summary of what we built:**
- Sliding window with a `last_seen` dict mapping `char → last index`
- Left pointer jumps directly on duplicate: `left = max(left, last_seen[char] + 1)`
- `max()` prevents the pointer from going backwards when a stale entry is in the map
- O(n) time, O(k) space where k is the size of the character set

The solution is on LeetCode's faster end — each character is touched exactly once.

### Student

Perfect! I'm satisfied with this solution. The code is clean, correct, and efficient. I learned a lot here:

1. **Why sliding window with index map is better than a set** — jumping directly is faster than removing characters one at a time.

2. **Why the `max()` guard matters** — without it, we'd move the left pointer backwards on stale duplicates, breaking the window invariant. The `"abba"` case proved that.

3. **When to optimize and when not to** — the dict is the right choice for clarity and generality; premature optimization to an array would be overkill.

The solution handles edge cases well (empty string, all repeats, all unique) and runs in O(n) time with O(k) space. I'm ready to move on.

<done/>

---

**Run end:** done after 4 turn(s) in 75.2s
