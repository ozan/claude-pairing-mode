# leetcode-group-anagrams

- Source: `leetcode`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:26:34.323Z

---

## Turn 1

**User:**

Let's solve Leetcode #49, 'Group Anagrams'. Given a list of strings, group strings that are anagrams of each other into sub-lists.

**Pair:**

Assistant: ## LeetCode #49 — Group Anagrams

### Core Insight

Two strings are anagrams if and only if they have the **same sorted characters**. So we can use the sorted string as a canonical key in a hash map — all anagrams map to the same key and get bucketed together.

### Solution 1: Sorted-Key (Simple & Pythonic)

```python
from collections import defaultdict

def groupAnagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)

    for word in strs:
        key = tuple(sorted(word))   # "eat" → ('a','e','t')
        groups[key].append(word)

    return list(groups.values())
```

**Walkthrough with `["eat","tea","tan","ate","nat","bat"]`:**

| Word  | Key (sorted) | Bucket        |
|-------|--------------|---------------|
| "eat" | `('a','e','t')` | ["eat"]    |
| "tea" | `('a','e','t')` | ["eat","tea"] |
| "tan" | `('a','n','t')` | ["tan"]    |
| "ate" | `('a','e','t')` | ["eat","tea","ate"] |
| "nat" | `('a','n','t')` | ["tan","nat"] |
| "bat" | `('a','b','t')` | ["bat"]    |

**Output:** `[["eat","tea","ate"], ["tan","nat"], ["bat"]]`

---

### Solution 2: Character-Count Key (Optimal — avoids sorting)

```python
from collections import defaultdict

def groupAnagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)

    for word in strs:
        # Count of each letter a-z as a 26-element tuple
        count = [0] * 26
        for ch in word:
            count[ord(ch) - ord('a')] += 1

        groups[tuple(count)].append(word)

    return list(groups.values())
```

---

### Complexity Comparison

| Approach | Time | Space |
|---|---|---|
| Sorted key | **O(N · K log K)** | O(N · K) |
| Count key | **O(N · K)** | O(N · K) |

*N = number of words, K = max word length*

---

### Which to use?

- **Interview / clarity** → Solution 1 (fewer lines, immediately readable)
- **Performance-critical / long strings** → Solution 2 (linear in input size, no sorting overhead)

The sorted-key version is the standard interview answer — it's concise and the intent is obvious at a glance.

---

## Turn 2

**User:**

I've given you two solid solutions above! Now, let me frame this as a **meaningful choice** for the pair-programming workflow:

---

## Two Approaches — Which Would You Prefer?

### **Option A: Sorted-Key (Best for interviews & readability)**
```diff
+from collections import defaultdict
+
+def groupAnagrams(strs: list[str]) -> list[list[str]]:
+    groups = defaultdict(list)
+    for word in strs:
+        key = tuple(sorted(word))
+        groups[key].append(word)
+    return list(groups.values())
```

✅ **Why this is great:**
- Dead simple — one line of actual logic (`sorted()`)
- O(N · K log K) is fast enough for 99% of cases
- Immediately obvious what's happening

---

### **Option B: Character-Count Key (Best for performance)**
```diff
+from collections import defaultdict
+
+def groupAnagrams(strs: list[str]) -> list[list[str]]:
+    groups = defaultdict(list)
+    for word in strs:
+        count = [0] * 26
+        for ch in word:
+            count[ord(ch) - ord('a')] += 1
+        groups[tuple(count)].append(word)
+    return list(groups.values())
```

✅ **Why this is great:**
- True O(N · K) — avoids sorting overhead
- Better for very long strings (e.g., 1000+ chars each)
- Shows deeper understanding of character frequency

---

**Which approach resonates with you?** (Or would you like me to code something else?)

If you want me to write this into a real file and test it, just say **A** or **B** — I'll create a solution file with test cases!

**Pair:**

Assistant: **A** — sorted-key is the right default. It's instantly readable, the performance trade-off only matters at extreme scale, and clarity wins in almost every real codebase. Let me write it out with tests:

[Bash(pwd)]
  /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-leetcode-group-anagrams-PETesY

[Write(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-leetcode-group-anagrams-PETesY/group_anagrams.py)]
from collections import defaultdict


def groupAnagrams(strs: list[str]) -> list[list[str]]:
    """
    Group strings that are anagrams of each other.

    Strategy: sorted characters form a canonical key — all anagrams
    share the same key and get collected into the same bucket.

    Time:  O(N * K log K)  — N words, K = max word length
    Space: O(N * K)        — storing all words in the hash map
… (86 more lines)

[Bash(python group_anagrams.py)]
  error: Exit code 127

[Bash(python3 group_anagrams.py)]
  PASS  test_leetcode_example
    PASS  test_single_empty_string
    PASS  test_multiple_empty_strings
    PASS  test_all_unique
    PASS  test_all_same_anagram
    PASS  test_single_character_words
    PASS  test_single_word
    PASS  test_mixed_lengths
  
  8 tests passed.

Assistant: All 8 tests pass. Here's what the test suite covers:

| Test | What it guards against |
|---|---|
| `test_leetcode_example` | The canonical happy path |
| `test_single/multiple_empty_strings` | Empty string edge case — `""` must group with `""` |
| `test_all_unique` | No false positives — distinct words stay separate |
| `test_all_same_anagram` | Everything collapses into one group correctly |
| `test_single_character_words` | Duplicates in input are grouped, not deduplicated |
| `test_single_word` | Minimal input doesn't crash |
| `test_mixed_lengths` | Words of different lengths are never anagrams (implicit via key) |

The `sorted_groups()` helper is worth noting — since the problem says order doesn't matter, we canonicalize both the expected and actual results before comparing, so the assertions don't depend on insertion order.

---

## Turn 3 (final)

**User:**

Perfect! The solution is complete. Here's the summary:

## ✅ Group Anagrams — Solved

**Choice**: Option A (Sorted-Key)
- **File**: `group_anagrams.py`
- **Tests**: 8/8 passing
- **Complexity**: O(N · K log K) time, O(N · K) space

The implementation groups anagrams by using the sorted characters as a canonical key, which is:
- ✨ Immediately readable
- 🚀 Fast enough for real problems
- 🛡️ Well-tested across edge cases (empties, duplicates, single words, mixed lengths)

The logic is bulletproof: if two words are anagrams, `sorted(word1) == sorted(word2)`, so they hash to the same bucket and get grouped together automatically.

<done/>

---

**Run end**: done after 2 turns (76s)
