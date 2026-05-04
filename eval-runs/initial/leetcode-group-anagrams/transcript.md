# leetcode-group-anagrams

- Source: `leetcode`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:37:27.562Z

---

## Turn 1

**User:**

Let's solve Leetcode #49, 'Group Anagrams'. Given a list of strings, group strings that are anagrams of each other into sub-lists.

**Pair:**

Assistant: Good problem. The structure is straightforward — a hashmap from "canonical form" → list of strings. The interesting decision is how you compute that canonical form (i.e., the key). Let me pose that as a question:

[Glob(group_anagrams.py)]
  No files found

Assistant: Which key generation approach do you want to use?

**Option A — Sort the string:**
```diff
+++ group_anagrams.py
@@ -0,0 +1,8 @@
+from collections import defaultdict
+
+def groupAnagrams(strs):
+    groups = defaultdict(list)
+    for s in strs:
+        key = tuple(sorted(s))
+        groups[key].append(s)
+    return list(groups.values())
```

**Option B — Character frequency tuple:**
```diff
+++ group_anagrams.py
@@ -0,0 +1,9 @@
+from collections import defaultdict, Counter
+
+def groupAnagrams(strs):
+    groups = defaultdict(list)
+    for s in strs:
+        count = Counter(s)
+        key = tuple(count.get(c, 0) for c in 'abcdefghijklmnopqrstuvwxyz')
+        groups[key].append(s)
+    return list(groups.values())
```

Which is asymptotically faster — A or B?

---

## Turn 2

**User:**

**Option B is asymptotically faster.**

Here's why:

- **Option A (sorting)**: For each string of length k, sorting is O(k log k). For n strings: **O(n · k log k)**

- **Option B (character frequency)**: For each string of length k, Counter is O(k), then we iterate 26 letters (constant): O(1). For n strings: **O(n · k)**

So B drops the log k factor. It wins on asymptotic complexity.

**But there's a tradeoff:**
- Option A is simpler, more readable, and works with *any* characters
- Option B assumes lowercase English letters only (or you'd need to adapt it)
- For typical LeetCode constraints (short strings), the log k overhead is small in practice

For a real interview, I'd probably lean toward **Option A** — it's cleaner and the asymptotic advantage of B doesn't matter much in practice. But B is the "correct" answer if you're optimizing theoretically.

Which way would you like to go?

**Pair:**

Assistant: Exactly right on all counts. Option A is my preference too — it's the move in an interview. The log k factor is irrelevant when k is "length of an English word," and the generality is a real bonus (Unicode strings, mixed case, etc.).

Let's write it:

[Write(group_anagrams.py)]
from collections import defaultdict


def groupAnagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))
        groups[key].append(s)
    return list(groups.values())


if __name__ == "__main__":
… (12 more lines)

[Bash(python group_anagrams.py)]
  error: Exit code 127

[Bash(python3 group_anagrams.py)]
  All tests passed.

Assistant: All green. A few things worth noting about this solution:

- **`defaultdict(list)`** saves the `if key not in groups` guard — a small but clean habit.
- **`tuple(sorted(s))`** — we need a tuple (not a list) because dict keys must be hashable, and lists aren't.
- The test comparison uses `frozenset` to avoid caring about output ordering, which the problem doesn't guarantee.

**Complexity summary:**
| | Time | Space |
|---|---|---|
| Overall | O(n · k log k) | O(n · k) |

Space is O(n·k) because we're storing all the strings plus their keys. Worth mentioning in an interview.

---

## Turn 3 (final)

**User:**

Perfect! The solution is solid and we've covered the key trade-offs.

One last bit of learning: the reason we use a **dict/defaultdict here** rather than, say, sorting the input and grouping consecutive runs is that we'd then need a second pass to return the grouped lists in the right structure. The single-pass hash approach is both faster and cleaner.

If you ever see this problem in an interview, you can now confidently explain why you picked the sort-based key (simplicity + generality beat a theoretical log k savings), and you can walk through the space/time complexity without hesitation.

<done/>

---

**Run end**: done after 2 turns (65s)
