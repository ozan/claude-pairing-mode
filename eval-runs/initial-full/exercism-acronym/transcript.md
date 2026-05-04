# exercism-acronym

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T05:45:50.064Z

---

## Turn 1

**User:**

Exercism 'Acronym': given a phrase, return its acronym in uppercase. Treat hyphens as word separators; ignore other punctuation. e.g. 'Portable Network Graphics' → 'PNG'.

**Pair:**

Assistant: Nice, clean little problem. I'll use Python. Let me check if anything's already there.

[Glob(acronym*)]
  No files found

Assistant: Fresh start. The core question here is how to extract the first letter of each word — there are two natural regex approaches worth comparing:

Assistant: The `propose_options` tool isn't loading, so I'll lay them out manually. Which approach would you pick for extracting the leading letter of each word?

**Option A** — find letters at word boundaries:
```python
import re
def abbreviate(phrase):
    return ''.join(re.findall(r'\b[a-zA-Z]', phrase)).upper()
```

**Option B** — split on separators, take first char:
```python
import re
def abbreviate(phrase):
    return ''.join(w[0] for w in re.split(r'[\s-]+', phrase) if w).upper()
```

Both are short. Which do you prefer — and why?

---

## Turn 2

**User:**

I'd pick **Option B**.

Here's my reasoning: Option A's `\b` word boundary will match at *any* transition between word and non-word characters — including apostrophes. So a phrase like "You Can't Encrypt Everything" would incorrectly pull out both 'C' and 't' from "Can't" (boundary before the 't' after the apostrophe). The problem says to "ignore other punctuation", which means apostrophes and similar should *not* create new word boundaries.

Option B is explicit: it splits only on spaces and hyphens as separators, leaving other punctuation to be silently dropped when we take `w[0]`. The `if w` guard handles consecutive separators cleanly too.

Option B is more robust. Let's go with that.

**Pair:**

Assistant: Exactly right — that's the key insight. `\b` is deceptively attractive but it's really "any non-word/word transition", not "start of a word". Your apostrophe example nails it.

Let's build the file:

[Write(acronym.py)]
import re


def abbreviate(phrase):
    return ''.join(w[0] for w in re.split(r'[\s-]+', phrase) if w).upper()


Assistant: Let's verify it against a few cases:

[Bash(python3 -c "
from acronym import abbreviate
cases = [
    ('Portable Network Graphics', 'PNG'),
    ('GNU Image Manipulation Program', 'GIMP'),
    ('Halley\'s Comet', 'HC'),
    ('The Road _Not_ Taken', 'TRNT'),
    ('Something - Useful', 'SU'),
    ('You Can\'t Encrypt Everything', 'YCEE'),
]
for phrase, expected in cases:
    result = abbreviate(phrase)
    status = '✓' if result == expected else f'✗ (got {result})'
    print(f'{status}  {phrase!r} → {result}')
"
)]
  ✓  'Portable Network Graphics' → PNG
  ✓  'GNU Image Manipulation Program' → GIMP
  ✓  "Halley's Comet" → HC
  ✗ (got TR_T)  'The Road _Not_ Taken' → TR_T
  ✓  'Something - Useful' → SU
  ✓  "You Can't Encrypt Everything" → YCEE

Assistant: One edge case fails: `_Not_` — the split gives us the token `_Not_`, and `w[0]` grabs `_` instead of `N`. The "ignore other punctuation" rule means we need the **first alphabetic character** in each token, not just the first character.

[Edit(acronym.py)]
--- before
def abbreviate(phrase):
    return ''.join(w[0] for w in re.split(r'[\s-]+', phrase) if w).upper()
--- after
def abbreviate(phrase):
    return ''.join(
        m.group() for part in re.split(r'[\s-]+', phrase)
        if (m := re.search(r'[a-zA-Z]', part))
    ).upper()

[Bash(python3 -c "
from acronym import abbreviate
cases = [
    ('Portable Network Graphics', 'PNG'),
    ('GNU Image Manipulation Program', 'GIMP'),
    ('Halley\'s Comet', 'HC'),
    ('The Road _Not_ Taken', 'TRNT'),
    ('Something - Useful', 'SU'),
    ('You Can\'t Encrypt Everything', 'YCEE'),
]
for phrase, expected in cases:
    result = abbreviate(phrase)
    status = '✓' if result == expected else f'✗ (got {result})'
    print(f'{status}  {phrase!r} → {result}')
"
)]
  ✓  'Portable Network Graphics' → PNG
  ✓  'GNU Image Manipulation Program' → GIMP
  ✓  "Halley's Comet" → HC
  ✓  'The Road _Not_ Taken' → TRNT
  ✓  'Something - Useful' → SU
  ✓  "You Can't Encrypt Everything" → YCEE

Assistant: All green. Final solution:

```python
import re

def abbreviate(phrase):
    return ''.join(
        m.group() for part in re.split(r'[\s-]+', phrase)
        if (m := re.search(r'[a-zA-Z]', part))
    ).upper()
```

The logic in three steps:
1. **Split** on spaces/hyphens — the only true word separators
2. **Find the first letter** in each token (skips leading `_`, digits, etc.)
3. **Join and uppercase**

The walrus operator (`:=`) keeps it tidy — it assigns *and* tests in one expression, avoiding a separate `re.search` call for filtering and another for extracting. Worth knowing that pattern: `if (m := expr)` is idiomatic Python for "compute, assign, and skip if falsy."

---

## Turn 3 (final)

**User:**

Spot on. I followed your logic perfectly — the walrus operator pattern is clean, and splitting only on the specified separators (spaces and hyphens) while hunting for the first letter in each fragment is exactly what the problem asks for. The test cases confirm it handles all the edge cases: apostrophes, underscores, consecutive separators, hyphens mid-phrase.

This is ready.

<done/>

---

**Run end**: done after 2 turns (91s)
