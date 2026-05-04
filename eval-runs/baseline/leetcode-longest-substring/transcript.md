# leetcode-longest-substring

- Source: `leetcode`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:26:00.658Z

---

## Turn 1

**User:**

Let's solve Leetcode #3, 'Longest Substring Without Repeating Characters'. Given a string, return the length of the longest substring with all distinct characters.

**Pair:**

Assistant: ## Sliding Window Approach

The key insight: maintain a window `[left, right]` of unique characters. When a duplicate is found, advance `left` past the previous occurrence.

**Complexity:** Time O(n) · Space O(min(n, alphabet))

```python
def length_of_longest_substring(s: str) -> int:
    char_index = {}  # char -> most recent index seen
    longest = 0
    left = 0

    for right, char in enumerate(s):
        # If char is in the window, shrink left past its last occurrence
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1

        char_index[char] = right
        longest = max(longest, right - left + 1)

    return longest
```

### Walkthrough — `"abcabcbb"`

| right | char | left | window    | longest |
|-------|------|------|-----------|---------|
| 0     | `a`  | 0    | `a`       | 1       |
| 1     | `b`  | 0    | `ab`      | 2       |
| 2     | `c`  | 0    | `abc`     | **3**   |
| 3     | `a`  | 1    | `bca`     | 3       |
| 4     | `b`  | 2    | `cab`     | 3       |
| 5     | `c`  | 3    | `abc`     | 3       |
| 6     | `b`  | 5    | `cb`      | 3       |
| 7     | `b`  | 7    | `b`       | 3       |

Result → **3** ✅

### Other test cases

```python
print(length_of_longest_substring("bbbbb"))   # 1  (all dupes)
print(length_of_longest_substring("pwwkew"))  # 3  ("wke")
print(length_of_longest_substring(""))        # 0  (empty)
print(length_of_longest_substring("abcdef"))  # 6  (all unique)
```

### Why not a Set?

A set works but requires potentially **many** `left` increments per step. The `char_index` dict lets us **jump `left` directly** to the right position in O(1), keeping the whole algorithm a true single pass.

---

## Turn 2 (final)

**User:**

Great! I've provided a complete solution above. Let me verify it's solid:

✅ **Algorithm**: Sliding window with character index map
✅ **Time complexity**: O(n) single pass
✅ **Space complexity**: O(min(n, alphabet))
✅ **Edge cases handled**: Empty string, all duplicates, all unique
✅ **Walkthrough**: Clear example showing the window movement
✅ **Test cases**: Multiple scenarios demonstrating correctness

The core insight is that `char_index` lets us jump the left pointer directly to skip past a duplicate—much cleaner than a set approach that would require multiple increments.

The solution is ready to submit!

<done/>

---

**Run end**: done after 1 turn (19s)
