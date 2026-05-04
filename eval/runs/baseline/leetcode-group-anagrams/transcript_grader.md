# leetcode-group-anagrams

- Condition: `baseline`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T20:49:47

## Initial prompt

Let's solve Leetcode #49, 'Group Anagrams'. Given a list of strings, group strings that are anagrams of each other into sub-lists.

---

## Turn 1

### Tutor

Tutor: ## LeetCode #49 — Group Anagrams

### Key Insight

Two strings are anagrams **if and only if their sorted characters are identical**.

Use that sorted string as a **hash map key**, and bucket the original strings under it.

---

### Solution

```python
from collections import defaultdict

def groupAnagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)

    for s in strs:
        key = tuple(sorted(s))   # e.g. "eat" → ('a','e','t')
        groups[key].append(s)

    return list(groups.values())
```

---

### Walkthrough

```
Input: ["eat","tea","tan","ate","nat","bat"]

  "eat" → sorted → ('a','e','t')  →  { ('a','e','t'): ["eat"] }
  "tea" → sorted → ('a','e','t')  →  { ('a','e','t'): ["eat","tea"] }
  "tan" → sorted → ('a','n','t')  →  { ..., ('a','n','t'): ["tan"] }
  "ate" → sorted → ('a','e','t')  →  { ('a','e','t'): ["eat","tea","ate"] }
  "nat" → sorted → ('a','n','t')  →  { ..., ('a','n','t'): ["tan","nat"] }
  "bat" → sorted → ('a','b','t')  →  { ..., ('a','b','t'): ["bat"] }

Output: [["eat","tea","ate"], ["tan","nat"], ["bat"]]
```

---

### Complexity

| | |
|---|---|
| **Time** | O(n · k log k) — sorting each of the `n` strings of max length `k` |
| **Space** | O(n · k) — storing all strings in the hash map |

---

### Bonus: O(n·k) Approach via Character Frequency

If you want to avoid the `log k` sort cost, use a **character count tuple** as the key instead:

```python
def groupAnagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)

    for s in strs:
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1
        groups[tuple(count)].append(s)   # e.g. "eat" → (1,0,0,1,1,0,...,0)

    return list(groups.values())
```

This replaces the O(k log k) sort with a O(k) linear scan — a win when strings are very long, but practically negligible for typical inputs.

### Student

Thanks for walking through this! I think I understand the core idea now—using sorted characters as a key is clever because anagrams will always produce the same sorted form.

Let me make sure I've got it: when we sort "eat", "tea", and "ate", they all become `('a','e','t')`, so they all hash to the same bucket in our dictionary. That groups them together automatically. Got it.

I have a couple of quick questions before I feel confident:

1. **Why use `tuple(sorted(s))` instead of just `''.join(sorted(s))`?** I know both work as dictionary keys, but is there a reason to prefer one over the other here?

2. **In the bonus O(n·k) approach**, we're building a list of 26 counts and converting it to a tuple. Does that tuple get recreated fresh every time we loop, or does Python cache it somehow? I'm just curious if we're "wasting" work by making so many tuples.

3. One more thing—if the input list is empty, does this return an empty list? I want to make sure there are no edge cases I'm missing.

---

## Turn 2

### Tutor

Tutor: Great questions — each one touches a real nuance worth understanding.

---

### 1. `tuple(sorted(s))` vs `''.join(sorted(s))`

Both are valid dictionary keys, and honestly **`''.join(sorted(s))` is the better choice here**. A joined string like `"aet"` is:

- ✅ More **readable** — it looks like a word, which matches the mental model
- ✅ More **memory-efficient** — a `str` is a flat array of characters; a `tuple` holds individual object references (more overhead per element)

```python
key = ''.join(sorted(s))   # "aet"   ← prefer this
key = tuple(sorted(s))     # ('a','e','t')
```

`tuple` would only have a real advantage if the elements weren't strings — e.g., if you were keying on a mix of types. For this problem, the joined string is cleaner. I should have written it that way in the first place!

---

### 2. Does Python cache those 26-count tuples?

**No — a fresh tuple is allocated every loop iteration.** Python has no general tuple-caching mechanism. Each call to `tuple(count)` allocates a new object.

However, this is **not wasted work** for two reasons:

1. The tuple is **26 elements long always** — it's O(1) to create, regardless of the input string length. It doesn't grow with `k`.
2. Python *does* cache small integers (typically -5 to 256), so the *integers inside* the tuple (like `0`, `1`, `2`...) are reused from a pool — only the tuple *container* is newly allocated.

So the cost is one pointer-array allocation of fixed size 26, every iteration. That's genuinely cheap and doesn't affect the O(n·k) complexity.

---

### 3. Edge cases — does empty input work?

Yes, cleanly:

```python
groupAnagrams([])   # → []
```
The `for` loop never runs, `groups` stays empty, `list({}.values())` returns `[]`. ✅

A few other edge cases that also work correctly:

```python
groupAnagrams([""])        # → [[""]]   — empty string maps to key "" or ()
groupAnagrams(["", ""])    # → [["", ""]]  — two empty strings are anagrams of each other
groupAnagrams(["a"])       # → [["a"]]
```

The only real "gotcha" the problem constraints rule out is `None` values in the list — but LeetCode guarantees all elements are strings, so you're safe.

---

### Summary

| Question | Takeaway |
|---|---|
| `tuple` vs `join` | Prefer `''.join(sorted(s))` — more readable, less memory |
| Tuple caching | No caching, but creation is O(1) so it doesn't matter |
| Empty input | Returns `[]` correctly; empty strings also handled gracefully |

### Student

Ah, that makes sense! Thanks for the clarity on all three points.

I think the one thing that will stick with me is preferring `''.join(sorted(s))` over `tuple(sorted(s))` — I can see now that a string key is just cleaner and lighter. I'll remember that for similar problems.

And knowing that tuple creation is O(1) and doesn't scale with string length is reassuring; I was worried we were doing something inefficient in the bonus approach, but it sounds like it's genuinely solid.

Let me write out a clean final solution using what we discussed, just to lock it in:

```python
from collections import defaultdict

def groupAnagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    
    for s in strs:
        key = ''.join(sorted(s))  # sorted chars as string key
        groups[key].append(s)
    
    return list(groups.values())
```

That's straightforward and handles all the edge cases we talked about. I feel good about this solution now — the logic is clear, the complexity is solid, and I understand *why* each choice was made.

<done/>

---

**Run end:** done after 2 turn(s) in 49.0s
