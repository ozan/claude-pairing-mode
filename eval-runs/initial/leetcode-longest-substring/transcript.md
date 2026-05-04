# leetcode-longest-substring

- Source: `leetcode`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:37:27.561Z

---

## Turn 1

**User:**

Let's solve Leetcode #3, 'Longest Substring Without Repeating Characters'. Given a string, return the length of the longest substring with all distinct characters.

**Pair:**

Assistant: Classic sliding window problem. Both approaches below use that pattern — but one has a subtle bug. Which would you pick?

[Glob(solution.py)]
  No files found

Assistant: The core question: how do we handle tracking seen characters?

**Option A — Set, shrink left one step at a time:**
```diff
+++ solution.py
@@ -0,0 +1,10 @@
+def lengthOfLongestSubstring(s: str) -> int:
+    seen = set()
+    left = 0
+    max_len = 0
+    for right in range(len(s)):
+        while s[right] in seen:
+            seen.remove(s[left])
+            left += 1
+        seen.add(s[right])
+        max_len = max(max_len, right - left + 1)
+    return max_len
```

**Option B — Dict, jump left directly to skip past the duplicate:**
```diff
+++ solution.py
@@ -0,0 +1,10 @@
+def lengthOfLongestSubstring(s: str) -> int:
+    last_seen = {}
+    left = 0
+    max_len = 0
+    for right in range(len(s)):
+        if s[right] in last_seen:
+            left = last_seen[s[right]] + 1
+        last_seen[s[right]] = right
+        max_len = max(max_len, right - left + 1)
+    return max_len
```

Which do you prefer, and why?

---

## Turn 2

**User:**

I'd pick **Option A** — and I think Option B has a subtle bug.

Let me trace through an example that breaks Option B: `"abba"`

**Option A (Set):**
- `a`: window=[a], max=1
- `ab`: window=[a,b], max=2
- `abb`: duplicate 'b', shrink: remove 'a', then remove 'b', add new 'b' → window=[b], max=2
- `abba`: add 'a' → window=[b,a], max=2 ✓

**Option B (Dict):**
- `a`: last_seen={a:0}, left=0, max=1
- `ab`: last_seen={a:0,b:1}, left=0, max=2
- `abb`: 'b' at position 1, so left = 1+1 = 2 → window=[b], max=2 ✓
- `abba`: **'a' at position 0 is in last_seen**, so `left = 0+1 = 1`
  - **Window now spans indices 1→3: "bba"** — which has duplicate 'b'! 
  - max incorrectly becomes 3 ✗

The bug: when Option B jumps left, it doesn't check if that character was *already outside* the window. It can move `left` **backward**, re-admitting a duplicate we'd already removed.

**Option A avoids this** because the set contains *only* characters currently in the window. When we shrink, we remove characters; when we expand, we check what's actually in the set.

Should I write Option A to the file?

**Pair:**

Assistant: Exactly right — the fix for B is just `left = max(left, last_seen[s[right]] + 1)`, which prevents left from moving backward. But you correctly diagnosed *why* it breaks, which is the important part.

Let's write Option A:

[Write(solution.py)]
def lengthOfLongestSubstring(s: str) -> int:
    seen = set()
    left = 0
    max_len = 0
    for right in range(len(s)):
        while s[right] in seen:
            seen.remove(s[left])
            left += 1
        seen.add(s[right])
        max_len = max(max_len, right - left + 1)
    return max_len


Assistant: Good. Now a complexity question — what's the time complexity of Option A?

The `while` loop inside the `for` loop looks suspicious. Is this O(n²) in the worst case, or O(n)? Think about what bounds the total number of times `left` can move across the entire run of the algorithm.

---

## Turn 3 (final)

**User:**

Great question! At first glance, the nested while loop looks like it could be O(n²), but it's **actually O(n)**.

The key insight: **`left` only moves forward**. It never backtracks.

**Amortized analysis:**
- `right` iterates from 0 to n-1: **n steps**
- `left` starts at 0 and only increases: **at most n steps total** (across the entire algorithm, not per right iteration)
- Each character is added to `seen` once (when right passes it) and removed once (when left passes it)

So even though there's a nested while loop, the **total work** across all iterations is:
- O(n) iterations of the outer for loop
- O(n) total iterations of the while loop (summed across all outer loop runs)
- O(1) set operations (add, remove, membership check on average)

**Total: O(n) time, O(min(n, alphabet_size)) space**

The nested loop is a common pattern that *looks* suspicious but isn't — the trick is recognizing that the inner loop's iterations are "amortized" across the outer loop. Each index gets visited by `left` at most once, so there's no quadratic blowup.

This is why Option A is efficient despite the while loop — it's a textbook sliding window optimization.

<done/>

---

**Run end**: done after 2 turns (78s)
