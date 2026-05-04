# exercism-acronym

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:38:51.990Z

---

## Turn 1

**User:**

Exercism 'Acronym': given a phrase, return its acronym in uppercase. Treat hyphens as word separators; ignore other punctuation. e.g. 'Portable Network Graphics' → 'PNG'.

**Pair:**

[Glob(acronym*)]
  No files found

Assistant: No file yet. Before writing anything, one key design question — which regex strategy handles all the edge cases correctly?

Assistant: Let me just walk through the approach. The tricky cases are:

- `"Halley's Comet"` → `"HC"` (apostrophe should not create a new "word")
- `"The Road _Not_ Taken"` → `"TRNT"` (underscores should be ignored)
- `"Something - Component"` → `"SC"` (hyphens *are* separators)

The cleanest strategy: **strip everything except letters, spaces, and hyphens first**, then split.

```python
import re

def abbreviate(words):
    cleaned = re.sub(r"[^a-zA-Z\s-]", "", words)
    return ''.join(p[0].upper() for p in re.split(r'[\s-]+', cleaned) if p)
```

A tempting alternative — `re.findall(r'[a-zA-Z]+', words)` — looks cleaner, but silently fails on `"Halley's Comet"`: the apostrophe splits `Halley's` into `['Halley', 's', 'Comet']`, producing `"HSC"` instead of `"HC"`.

The strip-first approach sidesteps that entirely — `'` is non-`[a-zA-Z\s-]` so it's removed, leaving `Halleys` as one token.

[Write(acronym.py)]
import re


def abbreviate(words):
    cleaned = re.sub(r"[^a-zA-Z\s-]", "", words)
    return ''.join(p[0].upper() for p in re.split(r'[\s-]+', cleaned) if p)


Assistant: Let's verify against the key cases:

[Bash(python3 -c "
from acronym import abbreviate
cases = [
    ('Portable Network Graphics', 'PNG'),
    ('Ruby on Rails', 'ROR'),
    ('HyperText Markup Language', 'HTML'),
    ('First In, First Out', 'FIFO'),
    ('Something - Component Software', 'SCS'),
    ('Halley\'s Comet', 'HC'),
    ('The Road _Not_ Taken', 'TRNT'),
    ('Complementary metal-oxide semiconductor', 'CMOS'),
]
for phrase, expected in cases:
    got = abbreviate(phrase)
    status = '✓' if got == expected else f'✗ got {got}'
    print(f'{status}  {phrase!r}')
"
)]
  ✓  'Portable Network Graphics'
  ✓  'Ruby on Rails'
  ✗ got HML  'HyperText Markup Language'
  ✓  'First In, First Out'
  ✓  'Something - Component Software'
  ✓  "Halley's Comet"
  ✓  'The Road _Not_ Taken'
  ✓  'Complementary metal-oxide semiconductor'

Assistant: One failure: `"HyperText Markup Language"`. Our code gives `HML` — just the first letter of each space-separated token. But Exercism expects `HTML`, meaning the camelCase boundary between `Hyper` and `Text` should also count as a word split.

The user's stated spec doesn't mention this, but it's part of the exercise. We need to split on capital letters within a word too. Quick fix:

[Read(/Users/oz/p/pair/acronym.py)]
  error: File does not exist. Note: your current working directory is /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-acronym-vPLR6Y.

[Read(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-acronym-vPLR6Y/acronym.py)]
  1	import re
  2	
  3	
  4	def abbreviate(words):
  5	    cleaned = re.sub(r"[^a-zA-Z\s-]", "", words)
  6	    return ''.join(p[0].upper() for p in re.split(r'[\s-]+', cleaned) if p)
  7

Assistant: The fix: insert spaces before any uppercase letter that follows a lowercase letter (camelCase boundary), before the existing cleanup:

[Edit(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-acronym-vPLR6Y/acronym.py)]
--- before
def abbreviate(words):
    cleaned = re.sub(r"[^a-zA-Z\s-]", "", words)
    return ''.join(p[0].upper() for p in re.split(r'[\s-]+', cleaned) if p)
--- after
def abbreviate(words):
    expanded = re.sub(r'([a-z])([A-Z])', r'\1 \2', words)
    cleaned = re.sub(r"[^a-zA-Z\s-]", "", expanded)
    return ''.join(p[0].upper() for p in re.split(r'[\s-]+', cleaned) if p)

[Bash(python3 -c "
from acronym import abbreviate
cases = [
    ('Portable Network Graphics', 'PNG'),
    ('Ruby on Rails', 'ROR'),
    ('HyperText Markup Language', 'HTML'),
    ('First In, First Out', 'FIFO'),
    ('Something - Component Software', 'SCS'),
    (\"Halley's Comet\", 'HC'),
    ('The Road _Not_ Taken', 'TRNT'),
    ('Complementary metal-oxide semiconductor', 'CMOS'),
]
for phrase, expected in cases:
    got = abbreviate(phrase)
    status = '✓' if got == expected else f'✗ got {got}'
    print(f'{status}  {phrase!r}')
"
)]
  ✓  'Portable Network Graphics'
  ✓  'Ruby on Rails'
  ✓  'HyperText Markup Language'
  ✓  'First In, First Out'
  ✓  'Something - Component Software'
  ✓  "Halley's Comet"
  ✓  'The Road _Not_ Taken'
  ✓  'Complementary metal-oxide semiconductor'

Assistant: All green. Here's the final solution:

```python
import re

def abbreviate(words):
    expanded = re.sub(r'([a-z])([A-Z])', r'\1 \2', words)  # camelCase → two words
    cleaned  = re.sub(r"[^a-zA-Z\s-]", "", expanded)       # drop other punctuation
    return ''.join(p[0].upper() for p in re.split(r'[\s-]+', cleaned) if p)
```

Three passes, each with a clear purpose:
1. **camelCase split** — `([a-z])([A-Z])` inserts a space at every lowercase→uppercase boundary
2. **punctuation strip** — keeps only letters, spaces, and hyphens
3. **split + initials** — splits on whitespace/hyphens, takes first letter of each token

Worth noting: the strip step (pass 2) is what saves `"Halley's Comet"` — the apostrophe is removed, leaving `Halleys` as one token → `H`, not `H` + `s`.

---

## Turn 2 (final)

**User:**

Looking at your transcript, you've already solved this beautifully! 

Your final solution handles all the edge cases elegantly:

```python
import re

def abbreviate(words):
    expanded = re.sub(r'([a-z])([A-Z])', r'\1 \2', words)  # camelCase → two words
    cleaned  = re.sub(r"[^a-zA-Z\s-]", "", expanded)       # drop other punctuation
    return ''.join(p[0].upper() for p in re.split(r'[\s-]+', cleaned) if p)
```

The key insight was recognizing that **camelCase boundaries** are implicit word separators — something the initial naive approach missed. Once you added that preprocessing step (inserting spaces at `[a-z][A-Z]` boundaries), everything fell into place:

1. **Expand camelCase**: `HyperText` → `Hyper Text` (ready for split)
2. **Strip non-word punctuation**: removes apostrophes, underscores, etc., but preserves hyphens as separators
3. **Split + initials**: take first letter of each resulting token

All eight test cases pass, including the tricky ones:
- `"Halley's Comet"` → apostrophe stripped → `HC` ✓
- `"HyperText Markup Language"` → camelCase handled → `HTML` ✓
- `"Complementary metal-oxide semiconductor"` → hyphens preserved → `CMOS` ✓

The three-pass design is clean and maintainable. Each regex has one job, making the code easy to reason about and debug.

<done/>

---

**Run end**: done after 1 turn (154s)
