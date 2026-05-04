# ours-word-counter

- Source: `ours`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Output style: `Learning`
- Started: 2026-05-03T20:00:54.949Z

---

## Turn 1

**User:**

Let's write a Python function that takes a block of text and returns a dictionary mapping each word (lowercased) to its frequency. Strip punctuation.

**Pair:**

Assistant: ```python
import re
from collections import Counter

def word_frequency(text: str) -> dict[str, int]:
    words = re.findall(r"[a-z]+", text.lower())
    return dict(Counter(words))
```

**How it works, step by step:**

1. **`text.lower()`** — converts everything to lowercase so `"The"` and `"the"` count as the same word.

2. **`re.findall(r"[a-z]+"`, ...)`** — extracts sequences of letters only, which implicitly strips all punctuation and numbers. No manual `.replace()` needed.

3. **`Counter(words)`** — tallies occurrences in one pass; it's a subclass of `dict`, so wrapping it in `dict()` gives you a plain dictionary.

---

**Quick demo:**

```python
text = "To be, or not to be — that is the question!"

print(word_frequency(text))
# {'to': 2, 'be': 2, 'or': 1, 'not': 1, 'that': 1, 'is': 1, 'the': 1, 'question': 1}
```

---

**Key design choices worth knowing:**

| Choice | Why |
|---|---|
| `re.findall` over `.split()` | `.split()` leaves punctuation glued to words (`"be,"`) |
| `Counter` over a manual loop | It's O(n) and part of the stdlib — no reason to reinvent it |
| `dict[str, int]` type hint | Makes the return type explicit for editors/type checkers |

If you also want to **exclude common filler words** (stop words like `"the"`, `"is"`, `"to"`), that's a natural next extension — just shout!

---

## Turn 2 (final)

**User:**

Perfect! I've provided you with a complete, working solution. The function:

✅ Takes a block of text  
✅ Returns a `dict[str, int]`  
✅ Maps each word lowercased to its frequency  
✅ Strips all punctuation  

The code is production-ready, uses stdlib tools efficiently (`re` + `Counter`), and the example shows it handles real text like Shakespeare correctly.

If you want to **test it**, you can drop that into a Python file and run:

```python
text = "To be, or not to be — that is the question!"
print(word_frequency(text))
```

Or if you'd like to **extend it** (e.g., filter out stop words, handle contractions, return sorted results), I'm here. Otherwise, this solves the original ask!

<done/>

---

**Run end**: done after 1 turn (19s)
