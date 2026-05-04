# leetcode-group-anagrams

- Condition: `learning`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:04:09

## Initial prompt

Let's solve Leetcode #49, 'Group Anagrams'. Given a list of strings, group strings that are anagrams of each other into sub-lists.

---

## Turn 1

### Tutor

Tutor: ## Group Anagrams — LeetCode #49

### 🔑 Core Insight

Two strings are anagrams **if and only if their sorted characters are identical**.

```
"eat" → sorted → "aet"  ┐
"tea" → sorted → "aet"  ┼─ same key → same group
"ate" → sorted → "aet"  ┘

"tan" → sorted → "ant"  ┐
"nat" → sorted → "ant"  ┘─ same key → same group
```

So the plan: use a **hash map** keyed by the sorted string.

---

### Solution 1 — Sort as Key `O(n · k log k)`

```python
from collections import defaultdict

def groupAnagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)

    for word in strs:
        key = tuple(sorted(word))   # e.g. "eat" → ('a','e','t')
        groups[key].append(word)

    return list(groups.values())

# --- Example ---
print(groupAnagrams(["eat","tea","tan","ate","nat","bat"]))
# [['eat','tea','ate'], ['tan','nat'], ['bat']]
```

**Walk-through on `"eat"`:**
1. `sorted("eat")` → `['a','e','t']`
2. `tuple(...)` → `('a','e','t')` → used as dict key
3. Append `"eat"` to `groups[('a','e','t')]`

---

### Solution 2 — Frequency Count as Key `O(n · k)` ⚡ faster

Instead of sorting, count the 26 letter frequencies — this avoids the `log k` sort cost.

```python
from collections import defaultdict

def groupAnagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)

    for word in strs:
        # Build a count of each letter a–z
        count = [0] * 26
        for ch in word:
            count[ord(ch) - ord('a')] += 1

        key = tuple(count)   # e.g. "eat" → (1,0,0,0,1,0,...,1,0,0)
        groups[key].append(word)

    return list(groups.values())
```

---

### Complexity Comparison

| Approach | Time | Space |
|---|---|---|
| Sort as key | `O(n · k log k)` | `O(n · k)` |
| Frequency count as key | `O(n · k)` | `O(n · k)` |

> `n` = number of strings, `k` = max string length

---

### 💡 Key Takeaways

1. **Canonical form trick** — transform each element into a *normalized key* so equivalent items map to the same bucket. Sorting and frequency counts are two classic normalizations.
2. **`defaultdict(list)`** — avoids the `if key not in d` boilerplate; new keys auto-initialize to `[]`.
3. The frequency-count approach is preferred when strings are long, since it's linear in `k` rather than `k log k`.

### Student

Thanks for walking me through this! I can see how the core insight makes sense — finding a canonical form that's identical for all anagrams, then grouping by that form.

I have a couple of quick questions before I try coding it myself:

1. In Solution 1, why do we convert the sorted list to a `tuple`? Can't we just use the sorted list directly as a dictionary key?

2. For Solution 2 with the frequency count — I understand we're building a list of 26 zeros and incrementing the right position for each character. But I'm a bit unclear: when we do `tuple(count)`, we're converting the entire frequency array into a tuple, right? So `"eat"` and `"tea"` would both produce the same 26-element tuple as the key?

I think I'm ready to try implementing one of these approaches myself now. Should I start with Solution 1 (the sorting approach) since it's more straightforward, or would you recommend jumping to Solution 2?

---

## Turn 2

### Tutor

Tutor: Great questions — both get at important Python fundamentals.

---

**Q1: Why `tuple` and not a `list` as the key?**

Python requires dictionary keys to be **hashable** (immutable). Lists are mutable, so Python refuses to hash them:

```python
d = {}
d[['a','e','t']] = "test"   # ❌ TypeError: unhashable type: 'list'
d[('a','e','t')] = "test"   # ✅ tuples are immutable → hashable
```

The rule of thumb: if you need a sequence as a dict key, wrap it in `tuple()`.

---

**Q2: Yes, your understanding is exactly right.**

Both `"eat"` and `"tea"` produce the **same** 26-element tuple:

```
index:  0  1  2  3  4  ...  19  ...
letter: a  b  c  d  e  ...   t  ...

"eat"  → [1, 0, 0, 0, 1, ..., 1, ...]  → tuple → same key ✅
"tea"  → [1, 0, 0, 0, 1, ..., 1, ...]  → tuple → same key ✅
```

Same letters, same counts, same tuple — that's the whole trick.

---

**Which to start with?**

👉 **Start with Solution 1.** The sorting approach lets you focus on the *grouping logic* without the extra bookkeeping of 26-element arrays. Once Solution 1 clicks, Solution 2 is just swapping out one line (the key-building step). Master the pattern first, then optimize.

Give it a go — feel free to paste your attempt here!

### Student

Okay, that makes total sense — thanks for clarifying the hashability thing. I'm going to code up Solution 1 now.

Here's my attempt:

```python
from collections import defaultdict

def groupAnagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    
    for word in strs:
        key = tuple(sorted(word))
        groups[key].append(word)
    
    return list(groups.values())
```

Let me test it mentally on the example:
- `"eat"` → sorted → `['a','e','t']` → tuple → `('a','e','t')` → add to `groups[('a','e','t')]`
- `"tea"` → sorted → `['a','e','t']` → same key, so both go in the same list
- `"bat"` → sorted → `['a','b','t']` → different key, different group

Then `groups.values()` gives us all the grouped lists, and we convert to a regular list to return.

Does this look right? Should I test it out on the actual example `["eat","tea","tan","ate","nat","bat"]`?

---

## Turn 3

### Tutor

Tutor: Your solution is **correct** — and your mental trace is spot-on. 🎉

Yes, run it on the full example to confirm. Here's the complete trace so you can check your output:

```
"eat" → ('a','e','t') → groups: {('a','e','t'): ['eat']}
"tea" → ('a','e','t') → groups: {('a','e','t'): ['eat','tea']}
"tan" → ('a','n','t') → groups: {('a','e','t'): ['eat','tea'], ('a','n','t'): ['tan']}
"ate" → ('a','e','t') → groups: {('a','e','t'): ['eat','tea','ate'], ...}
"nat" → ('a','n','t') → groups: {..., ('a','n','t'): ['tan','nat']}
"bat" → ('a','b','t') → groups: {..., ('a','b','t'): ['bat']}
```

**Final output:**
```python
[['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
```

---

**Your code hits every mark:**

| Requirement | ✅ |
|---|---|
| Uses `defaultdict` to avoid key-init boilerplate | ✓ |
| Sorts each word to build a canonical key | ✓ |
| Wraps in `tuple()` for hashability | ✓ |
| Returns `list(groups.values())` | ✓ |

---

**When you're ready for a next step**, try implementing Solution 2 (frequency count) — the structure is identical, you're just replacing these two lines:

```python
# swap this...
key = tuple(sorted(word))

# ...for this (fill in the blanks)
count = [0] * 26
for ch in word:
    count[___________] += 1
key = tuple(count)
```

### Student

Perfect! I'm confident in Solution 1 now. Let me try filling in Solution 2 quickly:

```python
from collections import defaultdict

def groupAnagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    
    for word in strs:
        count = [0] * 26
        for ch in word:
            count[ord(ch) - ord('a')] += 1
        
        key = tuple(count)
        groups[key].append(word)
    
    return list(groups.values())
```

I'm using `ord(ch) - ord('a')` to convert each character to its position (0–25) in the alphabet. So `'a'` → `0`, `'e'` → `4`, `'t'` → `19`, etc.

For `"eat"`:
- `'e'` → index 4 → `count[4] += 1`
- `'a'` → index 0 → `count[0] += 1`
- `'t'` → index 19 → `count[19] += 1`

And `"tea"` would build the exact same `count` array, so same key. That should work!

Both solutions should produce the same output. I feel good about understanding the problem now — the key insight is picking the right canonical form (sorted string or frequency count) as your grouping key.

<done/>

---

**Run end:** done after 3 turn(s) in 50.9s
