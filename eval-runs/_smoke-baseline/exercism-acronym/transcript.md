# exercism-acronym

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T00:15:01.737Z

---

## Turn 1

**User:**

Exercism 'Acronym': given a phrase, return its acronym in uppercase. Treat hyphens as word separators; ignore other punctuation. e.g. 'Portable Network Graphics' → 'PNG'.

**Pair:**

[Glob(**/*acronym*)]
  No files found

[Bash(ls)]
  (Bash completed with no output)

Assistant: No existing files — I'll write the solution from scratch. The logic: split on spaces and hyphens, take the first letter of each word, uppercase everything.

[Write(/acronym.py)]
import re

def abbreviate(words):
    return "".join(w[0].upper() for w in re.split(r"[\s\-]+", words) if w)


[Bash(pwd && ls ~)]
  /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-acronym-1p8J1a
  Applications
  Desktop
  dev
  Documents
  Downloads
  Library
  Movies
  Music
  Pictures
  Public

[Bash(ls /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-acronym-1p8J1a/)]
  (Bash completed with no output)

[Write(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-acronym-1p8J1a/acronym.py)]
import re

def abbreviate(words):
    return "".join(w[0].upper() for w in re.split(r"[\s\-]+", words) if w)


[Bash(python -c "
from acronym import abbreviate
tests = [
    ('Portable Network Graphics', 'PNG'),
    ('Ruby on Rails', 'ROR'),
    ('First In, First Out', 'FIFO'),
    ('GNU Image Manipulation Program', 'GIMP'),
    ('Complementary metal-oxide semiconductor', 'CMOS'),
    ('Rolling On The Floor Laughing So Hard', 'ROTFLSH'),
    ('Something - with - dashes', 'SWD'),
]
for phrase, expected in tests:
    result = abbreviate(phrase)
    status = '✓' if result == expected else f'✗ (got {result})'
    print(f'{status}  {phrase!r} → {expected}')
"
)]
  error: Exit code 127

[Bash(python3 -c "
from acronym import abbreviate
tests = [
    ('Portable Network Graphics', 'PNG'),
    ('Ruby on Rails', 'ROR'),
    ('First In, First Out', 'FIFO'),
    ('GNU Image Manipulation Program', 'GIMP'),
    ('Complementary metal-oxide semiconductor', 'CMOS'),
    ('Rolling On The Floor Laughing So Hard', 'ROTFLSH'),
    ('Something - with - dashes', 'SWD'),
]
for phrase, expected in tests:
    result = abbreviate(phrase)
    status = 'PASS' if result == expected else f'FAIL (got {result})'
    print(f'{status}  {phrase!r} -> {expected}')
" 2>&1
)]
  PASS  'Portable Network Graphics' -> PNG
  PASS  'Ruby on Rails' -> ROR
  PASS  'First In, First Out' -> FIFO
  PASS  'GNU Image Manipulation Program' -> GIMP
  PASS  'Complementary metal-oxide semiconductor' -> CMOS
  PASS  'Rolling On The Floor Laughing So Hard' -> ROTFLSH
  PASS  'Something - with - dashes' -> SWD

Assistant: All tests pass. Here's the solution:

```python
import re

def abbreviate(words):
    return "".join(w[0].upper() for w in re.split(r"[\s\-]+", words) if w)
```

**How it works:**

- `re.split(r"[\s\-]+", words)` — splits on any run of whitespace **or** hyphens, treating both as word separators (the `+` handles consecutive separators like `" - "`).
- `if w` — guards against empty strings from leading/trailing separators.
- `w[0].upper()` — takes the first character of each word and uppercases it.
- Other punctuation (commas, periods, etc.) is left attached to words and simply ignored since only the *first* character is taken.

---

## Turn 2 (final)

**User:**

Got it — that's elegant. The regex `[\s\-]+` covers both spaces and hyphens in one go, and the `if w` filter handles the empty strings edge case. The guard on `w[0]` is safe because we know each remaining element is non-empty.

All the test cases pass and the logic handles the punctuation requirement (ignore everything except word boundaries). I think we're done here.

<done/>

---

**Run end**: done after 1 turn (38s)
