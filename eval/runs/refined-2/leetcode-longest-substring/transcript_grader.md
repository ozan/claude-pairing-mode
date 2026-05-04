# leetcode-longest-substring

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:23:43

## Initial prompt

Let's solve Leetcode #3, 'Longest Substring Without Repeating Characters'. Given a string, return the length of the longest substring with all distinct characters.

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Brute force all substrings
Check every possible substring with two nested loops. For each pair `(i, j)`, scan the characters between them to verify all are unique. O(n²) or O(n³) depending on the uniqueness check.

[B] Sliding window
Maintain a window `[left, right]` expanding right one char at a time. When a duplicate is found, shrink from the left until the window is valid again. O(n) time.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach would you take?

### Student

I think I'd go with **B** — the sliding window approach.

From what I understand, we'd expand the window by moving `right` forward, and whenever we encounter a character that's already in our current window, we'd move `left` forward until that duplicate is removed. That way we only scan the string once, which is much more efficient than checking every possible substring.

I'm a bit fuzzy on the implementation details though — like how do we efficiently track which characters are currently in the window? Should we use a set, or a HashMap with character counts, or something else?

---

## Turn 2

### Tutor

Tutor: Exactly right on the intuition. Now the key implementation question:

OPTIONS:
[A] Map of last-seen index
Store `char → last seen index`. On a duplicate, jump `left` directly to `last_seen[char] + 1` — no inner loop needed.

```diff
+++ solution.py
@@ -0,0 +1,8 @@
+def length_of_longest_substring(s: str) -> int:
+    seen = {}
+    left = 0
+    best = 0
+    for right, ch in enumerate(s):
+        if ch in seen:
+            left = seen[ch] + 1
+        seen[ch] = right
+        best = max(best, right - left + 1)
+    return best
```

[B] Set of window chars
Keep a set of characters currently in the window. On a duplicate, shrink left one step at a time until the duplicate is removed.

```diff
+++ solution.py
@@ -0,0 +1,10 @@
+def length_of_longest_substring(s: str) -> int:
+    seen = set()
+    left = 0
+    best = 0
+    for right, ch in enumerate(s):
+        while ch in seen:
+            seen.remove(s[left])
+            left += 1
+        seen.add(ch)
+        best = max(best, right - left + 1)
+    return best
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Both are valid sliding window implementations — which would you go with?

### Student

I think I'd go with **A** — the map of last-seen index.

It seems cleaner to me because we jump `left` directly to where we need it, rather than shrinking one character at a time in a while loop. Since we're storing the exact index where each character was last seen, we can just skip ahead in one operation. That feels more elegant and should be faster in practice too, even if both are O(n) overall.

Let me trace through an example to make sure I understand it: say we have `"abcabcbb"`. When we hit the second `'a'` at index 3, we look up `seen['a']` which is 0, so we jump `left` to `0 + 1 = 1`. The window is now `[1, 3]` containing `"bca"`, and we update `seen['a'] = 3`. That makes sense.

Should I code this up and test it on a few examples?

---

## Turn 3

### Tutor

Tutor: Good trace — your intuition is solid. Before we finalize, one question worth thinking through:

OPTIONS:
[A] Keep left = seen[ch] + 1
The current implementation as written — unconditionally set `left` to one past the last-seen index of the duplicate.

```diff
+++ solution.py
@@ -5,2 +5,2 @@
         if ch in seen:
-            left = seen[ch] + 1
+            left = seen[ch] + 1  # unchanged
```

[B] Clamp with max(left, ...)
Guard against moving `left` backwards if the duplicate was seen before the current window started.

```diff
+++ solution.py
@@ -5,2 +5,2 @@
         if ch in seen:
-            left = seen[ch] + 1
+            left = max(left, seen[ch] + 1)
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Try tracing `"abba"` through the current code — does anything go wrong?

### Student

Oh, good catch! Let me trace through `"abba"`:

- `right=0, ch='a'`: `seen = {'a': 0}`, `left=0`, `best=1`
- `right=1, ch='b'`: `seen = {'a': 0, 'b': 1}`, `left=0`, `best=2`
- `right=2, ch='b'`: `'b'` is in `seen`, so `left = seen['b'] + 1 = 1 + 1 = 2`. Then `seen = {'a': 0, 'b': 2}`, `left=2`, `best=2`
- `right=3, ch='a'`: `'a'` is in `seen`, so `left = seen['a'] + 1 = 0 + 1 = 1`. But wait — our window is already at `left=2`, and now we're moving it backwards to `left=1`?

That's wrong. The `'a'` at index 0 is already outside our current window, so we shouldn't move `left` backwards. We'd need **B** — `left = max(left, seen[ch] + 1)` — to keep `left` from going backwards and ensure we only ever shrink or maintain the window, never expand it leftward.

So the answer is **B**.

---

## Turn 4

### Tutor

Tutor: Exactly right — clean catch. The map remembers characters that have already left the window, so without `max()` you can get stale indices pulling `left` backward. Let me write the final solution:

[Write(solution.py)]
def length_of_longest_substring(s: str) -> int:
    seen = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in seen:
            left = max(left, seen[ch] + 1)
        seen[ch] = right
        best = max(best, right - left + 1)
    return best


… (13 more lines)
  File created successfully at: solution.py

[Bash(cd /Users/reza/src/lc3 && python solution.py)]
  error: Exit code 1

[Bash(python solution.py)]
  ✓ 'abcabcbb' → 3 (expected 3)
  ✓ 'bbbbb' → 1 (expected 1)
  ✓ 'pwwkew' → 3 (expected 3)
  ✓ 'abba' → 2 (expected 2)
  ✓ '' → 0 (expected 0)

Tutor: All passing. One last question worth thinking about:

OPTIONS:
[A] O(n) space overall
`seen` can grow proportionally to the input length — if all characters are unique, every character gets an entry, so space scales with `n`.

[B] O(1) space overall
`seen` is bounded by the size of the character set (e.g. 128 for ASCII, 26 for lowercase letters) — a fixed constant regardless of how long the input is.

(Reply with A or B, or ask a follow-up question.)

Tutor: What's the space complexity of this solution?

### Student

I'd say **B** — O(1) space overall.

Even though `seen` is a dictionary that can grow, it's fundamentally bounded by the alphabet size. We can never have more than 128 entries (for ASCII) or 26 (for lowercase letters), or whatever the character set is. That's a constant that doesn't depend on the input length `n`, so from a big-O perspective, it's O(1).

The test cases all pass, and I understand the logic now — the sliding window with the map of last-seen indices, guarded by `max(left, ...)` to prevent moving left backwards. This is a solid solution.

<done/>

---

**Run end:** done after 4 turn(s) in 82.9s
