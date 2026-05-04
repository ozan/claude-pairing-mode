# leetcode-longest-substring

- Condition: `learning`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:04:09

## Initial prompt

Let's solve Leetcode #3, 'Longest Substring Without Repeating Characters'. Given a string, return the length of the longest substring with all distinct characters.

---

## Turn 1

### Tutor

Tutor: ## Longest Substring Without Repeating Characters

### 🧠 Core Insight: Sliding Window

Imagine a window `[left, right]` sliding across the string. We **expand right** freely, but when we hit a **duplicate**, we **shrink from the left** — jumping past the previous occurrence of that character.

---

### Visualization

```
s = "a b c a b c b b"
      0 1 2 3 4 5 6 7

Step 1:  [a b c]      → len 3, no dupes
Step 2:   [b c a b]   → 'a' seen! jump left past old 'a' (idx 0) → left=1
Step 3:     [c a b c] → 'b' seen! jump left past old 'b' (idx 1) → left=2
...
```

---

### Solution

```python
def length_of_longest_substring(s: str) -> int:
    last_seen = {}   # char → most recent index
    left = 0
    max_len = 0

    for right, char in enumerate(s):
        # If char was seen AND is inside our current window
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1   # shrink: jump past the duplicate

        last_seen[char] = right          # update char's latest position
        max_len = max(max_len, right - left + 1)

    return max_len
```

---

### Walkthrough: `s = "abcabc"`

| right | char | left | window | max_len |
|-------|------|------|--------|---------|
| 0 | `a` | 0 | `"a"` | 1 |
| 1 | `b` | 0 | `"ab"` | 2 |
| 2 | `c` | 0 | `"abc"` | **3** |
| 3 | `a` | 1 | `"bca"` | 3 |
| 4 | `b` | 2 | `"cab"` | 3 |
| 5 | `c` | 3 | `"abc"` | 3 |

---

### Why `last_seen[char] >= left`?

This guards against a stale entry. Consider `"abba"`:
- At `right=3` (`'a'`), `last_seen['a'] = 0` — but `left` is already at `2`
- Without the check, `left` would wrongly jump *backward* to `1` ❌
- The check ensures we only react to duplicates **inside** our window ✅

---

### Complexity

| | |
|---|---|
| ⏱ **Time** | O(n) — each character visited once |
| 🗂 **Space** | O(min(n, σ)) — σ = alphabet size (26 for lowercase letters) |

### Student

Thanks for walking me through this! I understand the core idea—sliding window with a dictionary to track the most recent index of each character. Let me trace through the logic to make sure I've got it:

When we hit a duplicate character that's still in our current window, we jump `left` to skip past the old occurrence. The check `last_seen[char] >= left` is key—it makes sure we only shrink if the duplicate is actually *inside* our window, not from some old substring we've already moved past.

Let me test my understanding with a quick example in my head: `s = "au"`. 
- `right=0, char='a'`: `last_seen={'a': 0}`, `left=0`, `max_len=1`
- `right=1, char='u'`: `last_seen={'a': 0, 'u': 1}`, `left=0`, `max_len=2`
- Return `2` ✓

And one with a repeat: `s = "au au"` (ignoring the space, so really `"auau"`):
- `right=0, char='a'`: window `"a"`, `max_len=1`
- `right=1, char='u'`: window `"au"`, `max_len=2`
- `right=2, char='a'`: `'a'` was at index 0, which is `>= left (0)`, so `left = 0 + 1 = 1`. Window is now `"ua"`, `max_len=2`
- `right=3, char='u'`: `'u'` was at index 1, which is `>= left (1)`, so `left = 1 + 1 = 2`. Window is now `"au"`, `max_len=2`
- Return `2` ✓

That all clicks. The solution handles both non-repeating substrings and efficiently shrinks the window when duplicates appear. I feel confident in this approach now.

<done/>

---

**Run end:** done after 1 turn(s) in 22.2s
