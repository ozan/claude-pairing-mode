# exercism-pangram

- Source: `exercism`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:28:19.633Z

---

## Turn 1

**User:**

Exercism 'Pangram': write `is_pangram(text)` that returns True iff the input contains every letter of the alphabet at least once (case-insensitive).

**Pair:**

Assistant: ```python
def is_pangram(text: str) -> bool:
    return set("abcdefghijklmnopqrstuvwxyz").issubset(text.lower())
```

**How it works:**

1. `text.lower()` — normalises the input to lowercase so the check is case-insensitive.
2. `set("abcdefghijklmnopqrstuvwxyz")` — builds a set of all 26 letters.
3. `.issubset(...)` — returns `True` only if every letter in the alphabet appears at least once in the lowercased text (Python's `str` is iterable, so `set.issubset(str)` works directly).

**Quick mental tests:**

| Input | Result |
|---|---|
| `"The quick brown fox jumps over the lazy dog"` | `True` ✅ |
| `"Hello, World!"` | `False` ✅ |
| `""` | `False` ✅ |
| `"abcdefghijklmnopqrstuvwxyz"` | `True` ✅ |

An alternative one-liner using a generator expression, if you prefer it explicit:

```python
def is_pangram(text: str) -> bool:
    lowered = text.lower()
    return all(letter in lowered for letter in "abcdefghijklmnopqrstuvwxyz")
```

Both are O(n) in the length of the text. The `issubset` version is slightly more Pythonic.

---

## Turn 2 (final)

**User:**

That covers it! The solution is clean and efficient. Both approaches work—choose whichever feels more readable to you. The `issubset` version is more concise and idiomatic Python.

<done/>

---

**Run end**: done after 1 turn (13s)
