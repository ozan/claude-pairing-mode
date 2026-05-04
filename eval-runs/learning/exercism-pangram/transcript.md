# exercism-pangram

- Source: `exercism`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Output style: `Learning`
- Started: 2026-05-03T19:57:33.023Z

---

## Turn 1

**User:**

Exercism 'Pangram': write `is_pangram(text)` that returns True iff the input contains every letter of the alphabet at least once (case-insensitive).

**Pair:**

Assistant: ```python
def is_pangram(text):
    return set("abcdefghijklmnopqrstuvwxyz").issubset(text.lower())
```

**How it works:**

- `text.lower()` — normalise to lowercase so `A` and `a` both count
- `set(...)` on a string gives you its unique characters
- `.issubset(text.lower())` — checks that every letter in the 26-letter set appears somewhere in the text

**Why `issubset` over alternatives:**

| approach | what it does |
|---|---|
| `set(alphabet) <= set(text.lower())` | same logic, `<=` is the subset operator |
| `all(c in text.lower() for c in alphabet)` | short-circuits early, but loops explicitly |
| `len(set(text.lower()) & set(alphabet)) == 26` | intersection count — works but more steps |

`issubset` is the most *self-documenting* choice — the intent is literally "is this set a subset of that string's characters?"

**Quick sanity checks:**
```python
is_pangram("The quick brown fox jumps over the lazy dog")  # True  ✓
is_pangram("Hello, World!")                                # False ✓ (missing many letters)
is_pangram("")                                             # False ✓
```

---

## Turn 2 (final)

**User:**

Perfect! You've nailed this one. The solution is clean, correct, and well-explained.

Just to verify the logic once more:

```python
is_pangram("The quick brown fox jumps over the lazy dog")  # True
```

- `text.lower()` → `"the quick brown fox jumps over the lazy dog"`
- `set("abcdefghijklmnopqrstuvwxyz")` → all 26 letters
- `.issubset(...)` → checks: are all 26 letters present in the text's characters?
- Yes → returns `True` ✓

The `issubset` approach is particularly nice because:
1. It's readable — the intent is immediately clear
2. It's efficient — set operations are O(n), not O(26n) with repeated `in` checks
3. It handles all the edge cases naturally (empty string, already-lowercase, numbers/symbols ignored)

<done/>

---

**Run end**: done after 1 turn (21s)
