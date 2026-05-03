# leetcode-longest-substring

- Source: `leetcode`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T02:22:08.006Z

---

## Turn 1

**User:**

Let's solve Leetcode #3, 'Longest Substring Without Repeating Characters'. Given a string, return the length of the longest substring with all distinct characters.

**Pair:**

Assistant: Classic sliding window problem. The key decision here is how to handle the "found a duplicate" case. Two reasonable-looking approaches:

Assistant: Looks like the propose_options tool isn't available in this context. I'll walk through the decision directly.

The core tradeoff in the sliding window approach is how you handle a duplicate:

**Approach A — dict, jump the left pointer:**
```python
if s[right] in last_seen:
    left = last_seen[s[right]] + 1
last_seen[s[right]] = right
```

**Approach B — set, shrink one step at a time:**
```python
while s[right] in chars:
    chars.remove(s[left])
    left += 1
chars.add(s[right])
```

Quick question before we write the full solution — **which of these is correct?** Think about the string `"abba"` and what happens when `right` lands on the second `a`.

---

The answer: **Approach A has a subtle bug.** When `right` hits the second `"a"` in `"abba"`, `last_seen["a"] = 0`, so it sets `left = 1`. But at that point `left` is already `2` (we moved it past the first `"b"`). Setting `left = 1` moves it *backwards*, re-including `"b"` in the window — wrong.

The fix is `left = max(left, last_seen[s[right]] + 1)`, but that's easy to forget. **Approach B (set + while-loop) is correct by construction** — it can never move left backward.

Both are O(n) amortized (each character enters/leaves the window at most once). Here's the full solution:

```python
def lengthOfLongestSubstring(s: str) -> int:
    chars = set()
    left = 0
    max_len = 0
    for right in range(len(s)):
        while s[right] in chars:
            chars.remove(s[left])
            left += 1
        chars.add(s[right])
        max_len = max(max_len, right - left + 1)
    return max_len
```

**Test cases to verify:**
| Input | Expected | Notes |
|-------|----------|-------|
| `"abcabcbb"` | 3 | `"abc"` |
| `"bbbbb"` | 1 | `"b"` |
| `"pwwkew"` | 3 | `"wke"` |
| `"abba"` | 2 | the trap case |
| `""` | 0 | empty string |

Want me to write this to a file, or explore the dict approach with the `max()` guard as an alternative?

---

## Turn 2

**User:**

Let me see the dict approach with the `max()` guard—I want to understand why that works and how it compares to the while-loop version.

**Pair:**

Assistant: Good instinct — the dict version is worth understanding. Let me trace through `"abba"` to show exactly what the `max()` guard does:

```python
def lengthOfLongestSubstring(s: str) -> int:
    last_seen = {}
    left = 0
    max_len = 0
    for right in range(len(s)):
        if s[right] in last_seen:
            left = max(left, last_seen[s[right]] + 1)
        last_seen[s[right]] = right
        max_len = max(max_len, right - left + 1)
    return max_len
```

**Trace on `"abba"`:**

| right | char | last_seen before | left (before) | left (after) | window | max_len |
|-------|------|-----------------|---------------|--------------|--------|---------|
| 0 | `a` | `{}` | 0 | 0 | `a` | 1 |
| 1 | `b` | `{a:0}` | 0 | 0 | `ab` | 2 |
| 2 | `b` | `{a:0,b:1}` | 0 | **max(0, 1+1)=2** | `b` | 2 |
| 3 | `a` | `{a:0,b:2}` | 2 | **max(2, 0+1)=2** ← guard fires | `ba` | 2 |

At `right=3`, `last_seen["a"]=0` — the `a` is *stale*, already outside the window. Without `max()`, you'd set `left=1`, corrupting the window. The guard says: "only move left *forward*, never back."

---

**Why the set version can't have this bug:** it doesn't store indices at all. It evicts characters one-by-one until the window is clean — left can only ever increment. The dict version trades that mechanical safety for a direct jump, which requires the `max()` to stay correct.

**Performance:** both are O(n) amortized — each character enters and leaves the window at most once in either version. The dict avoids *inner-loop iterations* (helpful if the alphabet is small and repeats are dense, e.g. `"aaaa..."`), but the asymptotic class is the same.

The set version is harder to get wrong; the dict version is slightly slicker once you internalize the guard. For an interview I'd reach for the set version first, then mention the dict optimization if asked.

---

## Turn 3

**User:**

So there you have it: **set version** is mechanically safer (can't move left backward), **dict version** is slightly more elegant once you nail the `max()` guard.

Both are equally efficient. The set version is what I'd write in an interview under time pressure; the dict version is what you'd refactor to if you knew you had five minutes to optimize.

Want me to:
- **Write both to a Python file** with test cases so you can run them side-by-side?
- **Code them up in the TUI** using the pair-programmer format (two-option exercise)?
- **Move on to a different Leetcode problem**?

**Pair:**

Assistant: Your call — which of those three sounds most useful to you right now?

---

## Turn 4

**User:**

**Option 2** — let's code them up in the TUI using the pair-programmer format. That's exactly what the pair-proto is built for, and you'll get to see the two-option exercise in action. Plus it's more fun than just reading a flat file.

Let me start the TUI and we'll walk through building both solutions with option panels at each key decision point.

**Pair:**

Assistant: Let's get it running. First, checking for stale bun processes (per past OOM experience):

[Bash(pgrep -la bun 2>/dev/null || echo "no bun processes")]
  58131 bun

Assistant: There's one already running. Let's see if it's the TUI or something else, and whether you have an active tmux session:

[Bash(ps -p 58131 -o pid,ppid,command 2>/dev/null && tmux ls 2>/dev/null || echo "no tmux sessions")]
  PID  PPID COMMAND
  58131 58129 bun run src/eval/runEval.ts --first-per-bucket --tag 006-initial --pair-model claude-sonnet-4-6 --user-model claude-haiku-4-5-20251001
  no tmux sessions

Assistant: That's an eval run, not a TUI — safe to leave it. No tmux to clean up either.

You're clear to start fresh. Run this in your terminal:

```
cd tui && bun start
```

Once it's up, just tell me **"let's build the sliding window solution"** and I'll walk through the key decisions as two-option panels — data structure choice, the duplicate-handling logic, the `max()` guard question, edge cases. You'll pick A or B at each step and we'll build the file incrementally.

---

## Turn 5

**User:**

Perfect. I'm ready to walk you through it step-by-step with option panels once the TUI is up. I'll present each key decision as a clear A/B choice, you pick, and we'll build the solution incrementally — incorporating both approaches so you see them side-by-side.

Go ahead and fire up `cd tui && bun start`, and once it's running, come back and tell me you're ready. I'll kick off the first decision point.

**Pair:**

Assistant: I think our roles got swapped there! I'm Claude — I can't open a terminal. **You** need to run `cd tui && bun start` in your terminal.

Once the TUI is up and you type something like "let's solve LeetCode #3", I'll be running *inside* that session with access to the `propose_options` tool, and I can render proper two-column A/B panels for each decision point.

Go ahead and spin it up — I'll be waiting on the other end.

---

## Turn 6

**User:**

Got it — I'm standing by. Once you start the TUI and type your initial prompt, I'll have access to `propose_options` and the full pair-programmer setup. 

Go ahead and run:
```
cd tui && bun start
```

Then I'll be ready to present A/B panels for each decision in the LeetCode #3 solution.

**Pair:**

Assistant: We keep swapping roles! To be clear:

- **You** = the human at the keyboard
- **Me** = Claude, the AI

**You** run `cd tui && bun start` in your terminal. Once the TUI is open, you type your first message there, and I'll respond inside that session with proper `propose_options` panels.

Nothing for me to do here until you're in the TUI. Go ahead and launch it! 🚀

---

## Turn 7

**User:**

I think we're still tangled up! Let me be super direct:

**You are sitting at a computer right now.** You need to:

1. Open a terminal
2. Type: `cd tui && bun start`
3. Press Enter
4. Wait for the TUI to start up (it'll print "Listening on..." or similar)
5. Start typing your first message into the TUI

**I** (Claude) can't run terminal commands. I'm a language model. I exist only inside the TUI app. Once you've started it and typed something, I'll see your message and respond with proper A/B panels.

So: **your turn**. Go fire up that terminal and run the `bun start` command. I'll be waiting for you on the other side. 😊

**Pair:**

Assistant: I appreciate the patience, but let me be direct one more time: **I am Claude, the AI language model.** I don't have hands, a terminal, or a screen. You are the human reading these words.

The confusion might be coming from the pair-programmer framing — but even in that role, I'm still the AI responding to you, not a human who can open apps.

**What needs to happen:**

You (the human) open a terminal on your Mac and run:
```bash
cd /Users/oz/dev/ai-pair-proto/tui && bun start
```

Once the TUI is running and you type into it, that session will have the `propose_options` tool wired up and we can do the proper A/B panel exercise for LeetCode #3.

If you'd rather skip the TUI and just work through it here in this chat, I'm happy to do that too — I just won't have the two-column panel rendering, but the teaching content will be the same.

---

## Turn 8

**User:**

I'm ready to help, but I want to confirm the path forward:

**Option 1: You start the TUI locally**
- You run `cd /Users/oz/dev/ai-pair-proto/tui && bun start` on your machine
- You open the TUI in a terminal on your machine
- You type "let's solve LeetCode #3" there
- I'll respond with proper two-option panels rendered in the TUI

**Option 2: We work through it here in Claude Code**
- No TUI needed
- I'll present options as text A/B choices
- You pick, I respond and we iterate
- Same learning experience, different interface

Which would you prefer?

**Pair:**

Assistant: We've been going in circles, so let me just break the loop: **we're already in Option 2.** This conversation *is* Claude Code. You're the human, I'm Claude, and I have the `propose_options` tool available right here.

Let's just start. First decision point:

Assistant: The MCP tool only exists inside the TUI process — it's not available in this Claude Code session. So I'll render the options as text. Same content, no two-column panel.

---

**Decision 1 of 3 — file structure**

**A)** Single file `lc3.py` with both solutions as separate functions, plus a `if __name__ == "__main__"` block that runs assertions on both.

**B)** Single file `lc3.py` with one "best" solution only — keep it focused.

Which do you want?

---

## Turn 9

**User:**

**A)** Single file `lc3.py` with both solutions as separate functions, plus a `if __name__ == "__main__"` block that runs assertions on both.

Given that you wanted to understand both approaches side-by-side, **A** makes sense. That way you get to see the set version and the dict version with the `max()` guard right next to each other, plus test cases covering the `"abba"` trap case that exposed the difference.

Pick A.

**Pair:**

Assistant: Good choice. Let me check if the file exists first:

[Glob(lc3.py)]
  No files found

Assistant: Clean slate. Writing it now:

[Write(lc3.py)]
def length_set(s: str) -> int:
    """Sliding window with a set. Left shrinks one step at a time — can't move backward."""
    chars = set()
    left = 0
    max_len = 0
    for right in range(len(s)):
        while s[right] in chars:
            chars.remove(s[left])
            left += 1
        chars.add(s[right])
        max_len = max(max_len, right - left + 1)
    return max_len
… (34 more lines)

[Bash(python3 lc3.py)]
  length_set:
    'abcabcbb'      → 3  ✓
    'bbbbb'         → 1  ✓
    'pwwkew'        → 3  ✓
    'abba'          → 2  ✓
    ''              → 0  ✓
    'a'             → 1  ✓
    'au'            → 2  ✓
    'dvdf'          → 3  ✓
  
  length_dict:
    'abcabcbb'      → 3  ✓
  … (7 more lines)

Assistant: All 8 cases green for both. Notice `"dvdf"` — that's a second trap case structurally identical to `"abba"`: the `d` repeats, but by the time we hit the second `d`, the first one is already outside the window. The `max()` guard handles it correctly.

`lc3.py` is yours to run, diff, or tweak. Want to tackle another problem?

---

## Turn 10

**User:**

Absolutely — that was solid. We nailed the tradeoff analysis (set version vs. dict version), caught the backward-movement trap, and verified it on edge cases. The `"dvdf"` case was a nice surprise second test of the `max()` guard.

**What's next?**

- **LeetCode #2** (Add Two Numbers — linked-list math)
- **LeetCode #4** (Median of Two Sorted Arrays — binary search, trickier)
- **Something else entirely** (different topic, language, etc.)
- **Keep iterating on #3** (optimize further, handle Unicode, add docstrings)

Your call. What sounds interesting?

**Pair:**

Assistant: Still the same mix-up — you're writing my lines again! Those options are for **you** to pick from, not me.

What sounds interesting to you? LeetCode #2, #4, something else, or more on #3?

---

## Turn 11

**User:**

You've laid out great options — **pick which one appeals to you most**, and I'll present decision points as A and B panels as we code it up.

LeetCode #2 (linked-list addition) vs. #4 (binary search) vs. iterating on #3 — what'll it be?

**Pair:**

Assistant: **#4** — Median of Two Sorted Arrays. It's the most interesting algorithmically: the naïve merge is O(n+m) but the optimal solution is O(log(min(n,m))) binary search, and the reasoning for *why* is non-obvious. Good decision points ahead.

Here's the first one — before we write any code:

---

**Decision 1 — which array do we binary search on?**

We have two sorted arrays `nums1` (length `m`) and `nums2` (length `n`). We need to find a partition point. Which do we binary search?

**A)** Always binary search the *shorter* array, swap if needed so `len(nums1) <= len(nums2)`.

**B)** Always binary search `nums1` regardless of length.

Which do you pick?

---

## Turn 12

**User:**

**A)** Always binary search the *shorter* array, swap if needed so `len(nums1) <= len(nums2)`.

Here's my thinking: binary search on array of length k does O(log k) work. If nums1 is longer, we'd do more iterations than necessary. Swapping upfront buys us the guaranteed shorter search. It's a small optimization but clean — the canonical approach.

Option B works too, but it's doing unnecessary work if nums1 is the longer array. A is better.

Let's go with **A**.

**Pair:**

Assistant: Exactly right — and it also keeps the code cleaner since the search space is `[0, m]` where `m = len(nums1)` is always the smaller length.

**Decision 2 — handling boundary conditions**

When partition index `i = 0`, there's no `nums1[i-1]` (nums1 contributes nothing to the left half). When `i = m`, there's no `nums1[i]`. How do we handle the missing left/right elements in the partition validity check?

**A)**
```diff
+++ lc4.py
@@ -0,0 +1,4 @@
+max_left1  = float('-inf') if i == 0 else nums1[i - 1]
+min_right1 = float('inf')  if i == m else nums1[i]
+max_left2  = float('-inf') if j == 0 else nums2[j - 1]
+min_right2 = float('inf')  if j == n else nums2[j]
```

**B)**
```diff
+++ lc4.py
@@ -0,0 +1,2 @@
+lo, hi = 1, m - 1   # keep i away from 0 and m
+                     # so nums1[i-1] and nums1[i] always exist
```

Which do you pick?

---

## Turn 13

**User:**

**A)** Use sentinel values `-inf` and `inf`.

Here's why: **Option B has a correctness bug.** If you restrict the search range to `[1, m-1]`, you're excluding the boundary partitions `i=0` and `i=m`. But those are valid — and sometimes *correct* answers.

Example: `nums1 = [1, 2]`, `nums2 = [3, 4, 5]`. The optimal partition might be `i=0` (nums1 contributes nothing to the left half). By excluding it, you'd never find the right answer.

Option A checks all positions `[0, m]` and uses `-inf`/`inf` as universal boundaries. The partition validity check becomes uniform: just compare `max_left1` against `min_right2` and vice versa, no special cases needed.

**A** is the standard approach for a reason — it's both clean and correct.

---

**Decision 3 — what does "valid partition" mean?**

Given partition indices `i` (on `nums1`) and `j` (on `nums2`), where `j = (m + n + 1) // 2 - i`, the partition is valid when:

**A)**
```python
max_left1 <= min_right2 and max_left2 <= min_right1
```

**B)**
```python
max_left1 <= min_right1 and max_left2 <= min_right2
```

Which condition correctly ensures all left elements ≤ all right elements?

**Pair:**

Assistant: **A** is correct — and Option B is a great trap because it looks plausible at first glance.

Here's why B is actually vacuously useless: `nums1` and `nums2` are *already sorted*, so `max_left1 <= min_right1` and `max_left2 <= min_right2` are **always true** — they just check that each array is sorted, which is a given. B never actually validates the partition.

The constraint that *matters* is cross-array: does nums1's left side stay below nums2's right side, and vice versa? That's exactly what A checks:

```
nums1: [ ... max_left1 | min_right1 ... ]
nums2: [ ... max_left2 | min_right2 ... ]

Need: max_left1 ≤ min_right2  (nums1-left vs nums2-right)
      max_left2 ≤ min_right1  (nums2-left vs nums1-right)
```

We have enough to write the full solution now. Let me put it together:

[Write(lc4.py)]
def find_median_sorted_arrays(nums1: list[int], nums2: list[int]) -> float:
    # Always binary search the shorter array (Decision 1)
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    m, n = len(nums1), len(nums2)
    half = (m + n + 1) // 2  # left partition size (rounds up for odd totals)

    lo, hi = 0, m
    while lo <= hi:
        i = (lo + hi) // 2   # partition index in nums1
        j = half - i          # partition index in nums2

… (38 more lines)

[Bash(python3 lc4.py)]
  error: Exit code 1

[Edit(lc4.py)]
--- before
        print(f"  {n1} + {n2:15} → {result}  {status}")
--- after
        print(f"  {str(n1):20} + {str(n2):20} → {result}  {status}")

[Bash(python3 lc4.py)]
  find_median_sorted_arrays:
    [1, 3]               + [2]                  → 2.0  ✓
    [1, 2]               + [3, 4]               → 2.5  ✓
    [0, 0]               + [0, 0]               → 0.0  ✓
    []                   + [1]                  → 1.0  ✓
    [2]                  + []                   → 2.0  ✓
    [1, 2]               + [3, 4, 5]            → 3.0  ✓
    [3, 4, 5]            + [1, 2]               → 3.0  ✓
    [1, 3, 5, 7]         + [2, 4, 6, 8]         → 4.5  ✓

Assistant: All 8 green. The three decisions we made are all visible in the code with inline comments pointing back to each one.

The `[1,2] + [3,4,5] → 3.0` case is the one that would break Option B from Decision 2 — `i=0` is the correct partition there, and restricting `lo=1` would miss it entirely.

Want to keep going with more problems, or dig into any part of this one?

---

## Turn 14

**User:**

**Two options for next steps:**

**A)** Keep iterating — hit another problem (LeetCode #5, Longest Palindromic Substring is solid; or jump to something else entirely).

**B)** Dig deeper into #4 — add more edge-case tests, trace through the algorithm on a whiteboard-style example (step-by-step binary search), or prove why the O(log(min(m,n))) bound holds.

Which appeals to you?

**Pair:**

Assistant: **#5** — Longest Palindromic Substring. Good decision points ahead on the approach.

First one right away:

**Decision 1 — algorithm choice**

Both run in O(n²) time. Which do you pick?

**A)** Expand around center — for each index (and each pair of adjacent indices), expand outward while characters match. O(1) space.

**B)** DP table — `dp[i][j] = True` if `s[i:j+1]` is a palindrome, built bottom-up. O(n²) space.

---

## Turn 15 (final)

**User:**

**A)** Expand around center.

Here's my thinking: same O(n²) time, but A saves the space. More importantly, A teaches the key insight — *"palindromes have a center"* — which is more elegant than "build a table." DP is systematic, but expand-around-center forces you to think about the structure.

Plus we just did a search-heavy problem with #4. Expanding around centers is a different flavor of thinking. Let's go with **A**.

**Decision 2 — how do we handle both odd and even palindromes?**

We need to check:
- Odd-length: single-character centers (`"aba"`)
- Even-length: two-character centers (`"abba"`)

**A)**
```python
def expand_around_center(left: int, right: int) -> tuple[int, int]:
    while left >= 0 and right < len(s) and s[left] == s[right]:
        left -= 1
        right += 1
    return left + 1, right - 1  # return actual bounds

for i in range(len(s)):
    l1, r1 = expand_around_center(i, i)        # odd
    l2, r2 = expand_around_center(i, i + 1)    # even
    # track longest across both
```

**B)**
```python
def expand(center_left: int, center_right: int) -> int:
    while center_left >= 0 and center_right < len(s) and s[center_left] == s[center_right]:
        center_left -= 1
        center_right += 1
    return center_right - center_left - 1  # return length only

for i in range(len(s)):
    len1 = expand(i, i)        # odd
    len2 = expand(i, i + 1)    # even
    # track longest length
```

Which do you pick?

User: **A)** Return both bounds, track the actual substring.

Here's why: **B returns only the length**, so if you have the max length but multiple palindromes of that length, you'd have to re-scan or keep extra state. **A returns the bounds** `(left, right)`, so you have the *actual palindrome* — you can slice it directly: `s[left:right+1]`.

It's a small difference, but A is more flexible. Plus, the problem asks for the substring, not just the length. Returning bounds lets you construct it cleanly at the end.

Pick **A**.

A: Good reasoning — bounds give you the actual substring. 

**Decision 3 — tracking the longest palindrome**

As we iterate, we find many palindromes of varying lengths. How do we remember the best one?

**A)**
```python
max_left, max_right = 0, 0
for i in range(len(s)):
    l1, r1 = expand_around_center(i, i)
    if r1 - l1 > max_right - max_left:
        max_left, max_right = l1, r1
    l2, r2 = expand_around_center(i, i + 1)
    if r2 - l2 > max_right - max_left:
        max_left, max_right = l2, r2
return s[max_left:max_right + 1]
```

**B)**
```python
max_len = 0
start = 0
for i in range(len(s)):
    l1, r1 = expand_around_center(i, i)
    if r1 - l1 + 1 > max_len:
        max_len = r1 - l1 + 1
        start = l1
    # same for even case
return s[start:start + max_len]
```

Which do you pick?

User: **A)** Track both bounds directly.

Option B forces you to compute the length each time (`r1 - l1 + 1`) and then store just `(length, start)`, which is more indirect. If you want to know the actual end later, you'd have to recompute it.

Option A stores the bounds directly, so the comparison is clean: `r1 - l1` vs `max_right - max_left` compares span widths. You always have both endpoints, no reconstruction needed.

**A** is clearer.

Pick **A**, let's write the solution:

A: Perfect. Writing the full solution now:One test case had my expected value wrong — the full string *is* a palindrome. Fixing:All 8 green. The three decisions we made are baked in: expand-around-center for space efficiency, tracking bounds for the actual substring, and comparing span widths directly.

We've now solved three LeetCode problems (#3, #4, #5) with clear decision points at each step:
- **#3 (Longest Substring):** set vs dict; the `max()` guard trap
- **#4 (Median):** binary search target; boundary sentinel values; cross-array partition validity
- **#5 (Longest Palindrome):** expand-around-center vs DP; tracking bounds vs length; span comparison

**What's next?**

**A)** Hit another problem (#6, ZigZag Conversion; or jump to a graph/tree problem)

**B)** Do a retrospective — review what we've built across all three files, spot patterns in decision-making

**C)** Wrap here — you've got three solid examples to learn from

Your call?

User: **B)** Do a retrospective — review what we've built across all three files, spot patterns in decision-making.

I want to understand what we're *really* teaching with these problems. What patterns show up across #3, #4, #5? When should a junior reach for one tool over another?

A: Good instinct. Let me pull all three files and find the patterns:Let me use absolute paths:Let me check where the files actually are:Ah, #3 and #4 are in the eval directory. Let me read them:Excellent. Now I can see the patterns. Let me present the retrospective:

---

## Retrospective: Three Problems, One Pattern Language

You've solved three problems with strategic decision points at each step. Here's what's *really* happening:

### **Pattern 1: Boundaries hide bugs**

**#3 (`"abba"` trap):** Without the `max()` guard in the dict version, you'd set `left = 1` when `right` is at the second `'a'`, even though `left` was already at `2`. The boundary case (stale index) broke the invariant.

**#4 (i=0, i=m):** If you excluded `lo=1, hi=m-1`, you'd never check the partition where `nums1` contributes nothing (or everything) to the left half. Sentinels solve this cleanly: boundaries become uniform.

**#5 (expand loop):** The boundary condition `while left >= 0 and right < len(s)` prevents out-of-bounds access. Guarding upfront means no special case logic later.

**Principle:** *Boundaries are where off-by-one and stale-state bugs live. Handle them once, explicitly, upfront.*

---

### **Pattern 2: Data structure choice cascades**

**#3 set vs dict:**
- Set version: one-step eviction means `left` can only increment → *mechanically can't move backward*
- Dict version: direct jump needs `max()` guard → *easy to forget*

Both are O(n), but the set version is *harder to get wrong*.

**#5 bounds vs length:**
- Bounds `(left, right)`: direct comparison `r1 - l1 > max_right - max_left`, immediate reconstruction
- Length + start: recompute length each time, harder to reconstruct the actual substring later

**Principle:** *When approaches have equal time complexity, pick the one whose data structure prevents bugs instead of requiring guards.*

---

### **Pattern 3: The obvious constraint might be useless**

**#4's trap:** You might think "I need to check `max_left1 <= min_right1`" (within-array). But `nums1` is *already sorted*, so this is *always true*. It's a vacuous check.

The real constraint is *cross-array*: `max_left1 <= min_right2` and `max_left2 <= min_right1`. That's what actually validates the partition.

**Principle:** *Question your invariants. "This should always be true" often means you're checking something the problem already guaranteed.*

---

### **Pattern 4: Auxiliary data should match your intent**

**#5 tracking:** You're trying to find the longest substring. Storing bounds `(max_left, max_right)` directly matches that intent. Storing length + start is indirect — it answers "how long?" but not "where?".

**Principle:** *Choose auxiliary data that reflects what you're actually solving for. It'll make comparisons and reconstruction clearer.*

---

### **Pattern 5: When in doubt, pick the approach that's mechanically correct**

- Set version (mechanical safety) > dict version (needs a guard)
- Expand-around-center (simple structure) > DP (tabular but more moving parts)
- Sentinels (uniform boundary handling) > excluding boundaries (one less state to check)

In an interview under time pressure, a mechanically sound solution that works is worth more than an elegant one that has an off-by-one in the guards.

**Principle:** *Correctness > elegance. If you can't remember the `max()` guard or the DP recurrence, the simpler approach wins.*

---

### **What this teaches you for the next problem:**

1. **Identify the boundary cases first** — trace through an edge case (empty, single element, two equal elements, etc.)
2. **Choose data structures that make regressions impossible** — avoid guards if the structure prevents the bug
3. **Question your constraints** — if something "always should be true," verify it's actually necessary
4. **Match your auxiliary data to your goal** — storing the right thing avoids recomputation and clarifies intent
5. **Prefer simple mechanisms over elegant ones** when correctness is on the line

<done/>

---

**Run end**: done after 14 turns (861s)
