# leetcode-longest-substring

- Condition: `baseline`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T20:49:47

## Initial prompt

Let's solve Leetcode #3, 'Longest Substring Without Repeating Characters'. Given a string, return the length of the longest substring with all distinct characters.

---

## Turn 1

### Tutor

Tutor: ## LeetCode #3 — Longest Substring Without Repeating Characters

The optimal approach is a **Sliding Window** with a hash map to track the last seen index of each character, letting us jump the left pointer forward in O(1) instead of crawling one step at a time.

### Intuition

Maintain a window `[left, right]` that always contains unique characters. When `s[right]` collides with a character already inside the window, jump `left` past that character's previous position — no need to shrink one-by-one.

```
s = "a b c a b c b b"
      ↑       ↑
    left     right   → window = "abca" ← collision on 'a'!
      
              ↑ ↑
            left right  → jump left past previous 'a', window = "bca"
```

### Solution

```python
def lengthOfLongestSubstring(s: str) -> int:
    last_seen = {}   # char → most recent index seen
    left = 0
    max_len = 0

    for right, char in enumerate(s):
        # If char is inside the current window, shrink from the left
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1

        last_seen[char] = right
        max_len = max(max_len, right - left + 1)

    return max_len
```

### Walkthrough — `"abcabcbb"`

| `right` | `char` | `last_seen` | `left` | window | `max_len` |
|---------|--------|-------------|--------|--------|-----------|
| 0 | `a` | `{a:0}` | 0 | `"a"` | 1 |
| 1 | `b` | `{a:0,b:1}` | 0 | `"ab"` | 2 |
| 2 | `c` | `{a:0,b:1,c:2}` | 0 | `"abc"` | 3 |
| 3 | `a` | `{a:3,b:1,c:2}` | **1** | `"bca"` | 3 |
| 4 | `b` | `{a:3,b:4,c:2}` | **2** | `"cab"` | 3 |
| 5 | `c` | `{a:3,b:4,c:5}` | **3** | `"abc"` | 3 |
| 6 | `b` | `{a:3,b:6,c:5}` | **5** | `"cb"` | 3 |
| 7 | `b` | `{a:3,b:7,c:5}` | **7** | `"b"` | **3** ✅ |

### Complexity

| | |
|---|---|
| **Time** | **O(n)** — single pass, each character visited once |
| **Space** | **O(min(n, m))** — map holds at most `m` unique chars (e.g. 128 for ASCII) |

### Key Guard: `last_seen[char] >= left`

This check is critical. Without it, stale entries from *before* the current window could incorrectly push `left` backwards. For example:

```
s = "abba"
         ↑ right='a', last_seen['a']=0, but left=2
         Without the guard: left would jump to 1 ← WRONG (moves backward!)
         With the guard:    0 < left(2), so we skip → correct
```

### Student

Thanks for walking me through this! The sliding window approach with the hash map makes sense — I like how we can jump `left` forward in O(1) instead of slowly incrementing it.

I have a question about that key guard `last_seen[char] >= left`. Let me make sure I understand it:

If we see a character that's *already in our map*, we only move `left` forward if that character's last seen index is **within** the current window (i.e., at or after `left`). If the character was seen *before* the window started, we ignore it and don't move `left` at all — that makes sense because it's not actually a duplicate inside our window.

In your `"abba"` example, when we hit the second `'a'` at index 3, `last_seen['a']` is 0 but `left` is already 2, so 0 is not >= 2. We skip the update, and `left` stays at 2. Got it.

Let me test this logic on a quick example myself:

For `s = "au"`:
- right=0, char='a': last_seen={'a':0}, left=0, window="a", max_len=1
- right=1, char='u': last_seen={'a':0,'u':1}, left=0, window="au", max_len=2

And for `s = "dvdf"`:
- right=0, char='d': last_seen={'d':0}, left=0, max_len=1
- right=1, char='v': last_seen={'d':0,'v':1}, left=0, max_len=2
- right=2, char='d': 'd' is in map, 0 >= 0 ✓, so left=1, max_len=2
- right=3, char='f': last_seen={'d':2,'v':1,'f':3}, left=1, window="vdf", max_len=3 ✓

That looks right! I think I've got it now. One more thing — should I implement and test this on a few more cases to feel confident, or does this understanding feel solid enough?

---

## Turn 2

### Tutor

Tutor: Your understanding is spot-on — both walkthroughs are exactly right, and the fact that you caught the `"dvdf"` case yourself is a great sign. That's actually one of the trickier examples because it exercises the guard precisely (a character collides mid-window, then the window slides and a new collision would be stale).

Your understanding is solid. But if you want to feel *confident* rather than just correct, here are the three edge cases worth running through mentally — not because your logic is shaky, but because interviewers love them:

| Input | Expected | Why it's interesting |
|---|---|---|
| `""` | `0` | Empty string — loop never runs, returns initial `max_len=0` ✅ |
| `"bbbbb"` | `1` | All same character — `left` chases `right` the whole way |
| `"pwwkew"` | `3` | `"wke"` not `"kew"` — tests that you're maximizing, not just returning the final window |

The `"bbbbb"` one is the most instructive: trace through it and you'll see `left` always equals `right`, so the window is always size 1. It confirms the guard works in the degenerate case too.

Beyond that, I'd say: **implement it once from scratch without looking at the solution.** The real test of understanding isn't tracing existing code — it's whether you can reconstruct the two key decisions independently:

1. *What do I store in the map?* (last-seen index, not just presence)
2. *When do I update `left`?* (only when the collision is inside the window)

If you can write it clean from memory, you've got it.

### Student

You're right — let me actually code this up from scratch without looking back at the solution.

```python
def lengthOfLongestSubstring(s: str) -> int:
    char_index = {}
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        char = s[right]
        
        # If char was seen and is in the current window, move left past it
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1
        
        # Update the last seen index of this character
        char_index[char] = right
        
        # Track the longest substring
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

Let me mentally trace through `"bbbbb"`:
- right=0, char='b': char_index={'b':0}, left=0, max_length=1
- right=1, char='b': 'b' in map, 0 >= 0 ✓, left=1, char_index={'b':1}, max_length=max(1, 1-1+1)=1
- right=2, char='b': 'b' in map, 1 >= 1 ✓, left=2, char_index={'b':2}, max_length=1
- right=3, char='b': 'b' in map, 2 >= 2 ✓, left=3, char_index={'b':3}, max_length=1
- right=4, char='b': 'b' in map, 3 >= 3 ✓, left=4, char_index={'b':4}, max_length=1

Returns 1 ✓

And `"pwwkew"`:
- right=0, 'p': char_index={'p':0}, left=0, max_length=1
- right=1, 'w': char_index={'p':0,'w':1}, left=0, max_length=2
- right=2, 'w': 'w' in map, 1 >= 0 ✓, left=2, char_index={'p':0,'w':2}, max_length=2
- right=3, 'k': char_index={'p':0,'w':2,'k':3}, left=2, max_length=max(2, 3-2+1)=2
- right=4, 'e': char_index={'p':0,'w':2,'k':3,'e':4}, left=2, max_length=max(2, 4-2+1)=3
- right=5, 'w': 'w' in map, 2 >= 2 ✓, left=3, char_index={'p':0,'w':5,'k':3,'e':4}, max_length=max(3, 5-3+1)=3

Returns 3 ✓

Got it! The two key decisions are crystal clear now:
1. Store the *index*, not just presence — so we know where to jump `left` to
2. Only move `left` if the collision is actually in the current window

I feel confident about this solution now.

<done/>

---

**Run end:** done after 2 turn(s) in 40.5s
