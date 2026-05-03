# leetcode-longest-substring

- Source: `leetcode`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T01:42:00.675Z

---

## Turn 1

**User:**

Let's solve Leetcode #3, 'Longest Substring Without Repeating Characters'. Given a string, return the length of the longest substring with all distinct characters.

**Pair:**

Assistant: Classic sliding window problem. Before we write any code, there's a key data structure decision at the heart of this — let me ask which approach you'd reach for.

Assistant: Looks like the options tool isn't available in this session — I'll just walk through the key decision with you directly.

**The core question:** what data structure tracks "what's in the current window"?

**Option A — `dict` mapping char → last-seen index.** When you hit a duplicate, jump `left` directly to `last_seen[char] + 1`. Single pass, no inner loop.

**Option B — `set` of chars in the window.** When you hit a duplicate, shrink from the left (`while ch in seen: seen.remove(s[left]); left += 1`). Still O(n) amortized, but has an inner while loop.

Both are O(n), but the dict approach is cleaner: no inner loop, `left` only ever moves forward in one place. Here's the full solution with the dict approach:

```python
def length_of_longest_substring(s: str) -> int:
    last_seen = {}
    left = 0
    best = 0

    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)

    return best
```

The subtle detail: `last_seen[ch] >= left`. Without that guard, a character seen *before* the current window could pull `left` backwards — e.g. `"abba"` would incorrectly shrink the window when we hit the second `a` after `left` has already passed it.

Want to trace through an example, or shall we go ahead and write this to a file with tests?

---

## Turn 2

**User:**

The explanation makes sense — the dict approach is cleaner since `left` only moves forward in one spot. The `>= left` guard is the key detail I might've forgotten; without it, we'd incorrectly jump left if we encounter a char we've seen before the *current* window started.

Let's write it out with tests so we can verify it works.

**Pair:**

Assistant: Good — you've got the intuition exactly right. Let me check if there's already a file for this.

[Glob(longest_substring*)]
  No files found

Assistant: Clean slate. Writing the solution + tests:

[Write(longest_substring.py)]
def length_of_longest_substring(s: str) -> int:
    last_seen = {}
    left = 0
    best = 0

    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)

    return best
… (25 more lines)

[Bash(python longest_substring.py)]
  error: Exit code 127

[Bash(python3 longest_substring.py)]
  All tests passed.

Assistant: All green. A few things worth noting about the test suite:

- **`test_guard_matters`** is the important one — it directly exercises the `>= left` guard. `"abba"`: when `right=3` (second `'a'`), `last_seen['a']=0` but `left=2`, so the guard fires and we correctly leave `left` at 2, giving window `"ba"` = length 2. Without the guard, `left` would snap back to 1, producing the wrong answer of 3.
- **`test_edge`** covers the empty string — make sure `best` initializes to 0, not 1.

The solution is O(n) time, O(min(n, |alphabet|)) space — the dict can't hold more entries than there are distinct characters in the input.

---

## Turn 3 (final)

**User:**

Perfect. The solution is solid, tests are passing, and you understand the key guard that makes it work. The dict approach is definitely cleaner than the set + shrink-from-left alternative, and you've got the sliding window pattern down for future problems.

<done/>

---

**Run end**: done after 2 turns (70s)
