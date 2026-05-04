# exercism-acronym

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Output style: `Learning`
- Started: 2026-05-03T19:57:53.966Z

---

## Turn 1

**User:**

Exercism 'Acronym': given a phrase, return its acronym in uppercase. Treat hyphens as word separators; ignore other punctuation. e.g. 'Portable Network Graphics' → 'PNG'.

**Pair:**

[Glob(**/acronym*)]
  No files found

Assistant: No existing file — I'll create the solution fresh.

**The plan:**
1. Split on spaces **and** hyphens (both are word separators)
2. Grab the first letter of each resulting word
3. Uppercase and join

```
"GNU Image Manipulation Program"
 →  split → ["GNU", "Image", "Manipulation", "Program"]
 →  first letters → G I M P
 →  "GIMP" ✓
```

[Write(/home/user/exercism/python/acronym/acronym.py)]
import re


def abbreviate(words):
    return "".join(w[0].upper() for w in re.split(r"[\s\-]+", words) if w)


[Bash(pwd)]
  /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-acronym-60kgfP

[Glob(**/*)]
  .claude/settings.json

[Write(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-acronym-60kgfP/acronym.py)]
import re


def abbreviate(words):
    return "".join(w[0].upper() for w in re.split(r"[\s\-]+", words) if w)


Assistant: Here's the solution:

```python
import re

def abbreviate(words):
    return "".join(w[0].upper() for w in re.split(r"[\s\-]+", words) if w)
```

---

**How it works — step by step:**

| Step | What happens | Example |
|------|-------------|---------|
| `re.split(r"[\s\-]+", words)` | Split on **spaces or hyphens** (one or more) | `"Hash-bang"` → `["Hash", "bang"]` |
| `if w` | Drop any empty strings (e.g. from leading spaces) | `" PNG"` → safe |
| `w[0].upper()` | First letter of each word, uppercased | `"hash"` → `"H"` |
| `"".join(...)` | Combine all letters | `["H","B"]` → `"HB"` |

**Key design choices:**
- **`[\s\-]+`** — the `+` means consecutive separators (e.g. `" - "`) collapse into one split, so you don't get phantom empty words
- **`re.split`** over `str.split` — handles hyphens as separators alongside whitespace cleanly in one pass
- Other punctuation (apostrophes, colons, dots) stays attached to the word — only its **first character** is taken, so it's naturally ignored (`"It's"` → `"I"`)

---

## Turn 2 (final)

**User:**

Perfect! Your solution is correct and handles all the requirements:

**Verification:**

| Input | Split | First letters | Result |
|-------|-------|---------------|--------|
| `"Portable Network Graphics"` | `["Portable", "Network", "Graphics"]` | P, N, G | `"PNG"` ✓ |
| `"GNU Image Manipulation Program"` | `["GNU", "Image", "Manipulation", "Program"]` | G, I, M, P | `"GIMP"` ✓ |
| `"Portable-Network-Graphics"` | `["Portable", "Network", "Graphics"]` | P, N, G | `"PNG"` ✓ |
| `"it's brilliant"` | `["it's", "brilliant"]` | i, b (ignores apostrophe) | `"IB"` ✓ |

**Why this design is solid:**
- The `+` quantifier in `[\s\-]+` prevents empty strings from multiple consecutive separators
- The `if w` filter catches edge cases (leading/trailing spaces)
- Taking `w[0]` naturally ignores punctuation that isn't a separator (apostrophes, periods, etc. stay attached to words but only the first character is used)
- One regex pass handles both spaces and hyphens cleanly

The solution is complete and handles all edge cases correctly.

<done/>

---

**Run end**: done after 1 turn (42s)
