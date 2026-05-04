# leetcode-longest-substring

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:38:58

## Initial prompt

Let's solve Leetcode #3, 'Longest Substring Without Repeating Characters'. Given a string, return the length of the longest substring with all distinct characters.

---

## Turn 1

### Tutor

Tutor: Good problem — classic sliding window. Before writing any code, the key decision is how to track which characters are in the current window.

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Set + shrink step-by-step
Use a `set` to track characters in the window. When a duplicate is found, advance the left pointer one step at a time, removing characters, until the duplicate is gone.

[B] Dict storing last index
Use a `dict` mapping each character to its last-seen index. When a duplicate is found, jump the left pointer directly past the previous occurrence — no inner loop needed.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach do you want to use?

### Student

I think I'll go with **[B]** — the dict storing last index.

I like that it jumps the left pointer directly instead of sliding one character at a time. It feels more efficient, and I want to understand how to use that last-seen index to skip ahead.

Can we start coding it up?

---

## Turn 2

### Tutor

Tutor: Good pick. The crux of the dict approach is one line — how you update `left` when you hit a duplicate. Let me ask about that before we write anything:

When `s[right]` was seen before, which update is correct?

OPTIONS:
[A] Jump left directly
```diff
+++ solution.py
@@ -0,0 +1,10 @@
+def length_of_longest_substring(s: str) -> int:
+    last_seen = {}
+    left = 0
+    best = 0
+    for right, c in enumerate(s):
+        if c in last_seen:
+            left = last_seen[c] + 1
+        last_seen[c] = right
+        best = max(best, right - left + 1)
+    return best
```

[B] Clamp with max()
```diff
+++ solution.py
@@ -0,0 +1,10 @@
+def length_of_longest_substring(s: str) -> int:
+    last_seen = {}
+    left = 0
+    best = 0
+    for right, c in enumerate(s):
+        if c in last_seen:
+            left = max(left, last_seen[c] + 1)
+        last_seen[c] = right
+        best = max(best, right - left + 1)
+    return best
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Both look almost identical — which one is correct?

### Student

Hmm, let me think through this. The difference is whether we just assign `left = last_seen[c] + 1` or use `max(left, last_seen[c] + 1)`.

I think it's **[B]** with the `max()`. 

My reasoning: if we've already moved `left` forward past a duplicate, we don't want to move it *backwards* when we encounter a character whose last occurrence was further back. The `max()` ensures `left` only moves forward (or stays put), never goes backward.

For example, in a string like "abba", when we see the second 'a', we'd set `left` to skip past the first 'a'. We shouldn't let `left` jump backward just because we later see 'b' again.

Is that right?

---

## Turn 3

### Tutor

Tutor: Exactly right — and you even picked the exact example that breaks Option A. `"abba"` is the canonical gotcha for this problem.

The dict is never cleaned up, so stale entries for characters outside the window stick around. `max()` is the guard that makes the left pointer a ratchet — it only ever moves forward.

Let me write the file:

[Write(solution.py)]
def length_of_longest_substring(s: str) -> int:
    last_seen = {}
    left = 0
    best = 0
    for right, c in enumerate(s):
        if c in last_seen:
            left = max(left, last_seen[c] + 1)
        last_seen[c] = right
        best = max(best, right - left + 1)
    return best

  File created successfully at: solution.py

Tutor: Let's verify it on a few cases:

[Bash(python3 -c "
from solution import length_of_longest_substring as f
cases = [('abcabcbb', 3), ('bbbbb', 1), ('pwwkew', 3), ('abba', 2), ('', 0), ('a', 1)]
for s, expected in cases:
    result = f(s)
    status = '✓' if result == expected else '✗'
    print(f'{status}  f({s!r:12}) = {result}  (expected {expected})')
"
)]
  ✓  f('abcabcbb'  ) = 3  (expected 3)
  ✓  f('bbbbb'     ) = 1  (expected 1)
  ✓  f('pwwkew'    ) = 3  (expected 3)
  ✓  f('abba'      ) = 2  (expected 2)
  ✓  f(''          ) = 0  (expected 0)
  ✓  f('a'         ) = 1  (expected 1)

Tutor: All passing, including `"abba"`. 

Quick complexity recap:
- **Time: O(n)** — `right` visits each character once, and `left` only moves forward, so the total work across all iterations is O(n).
- **Space: O(min(n, α))** — the dict holds at most one entry per unique character, bounded by the alphabet size α (26 for lowercase letters, 128 for ASCII).

One thing worth noting: we never delete stale entries from `last_seen`, and the `max()` is what makes that safe. It's a nice example of a correctness invariant doing double duty as a performance trick — no cleanup needed.

### Student

That makes sense! I really appreciate how you walked through the `"abba"` example — seeing why option A breaks there made it click for me. The `max()` guard is elegant; it prevents `left` from moving backward and handles the stale dictionary entries automatically.

I'm satisfied with the solution. It passes all the test cases, the logic is clear, and I understand the time and space complexity. The sliding window approach with the dictionary is a solid pattern to remember for this class of problems.

Thanks for the pair session!

<done/>

---

**Run end:** done after 3 turn(s) in 55.0s
