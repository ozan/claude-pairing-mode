# exercism-acronym

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:28:42.072Z

---

## Turn 1

**User:**

Exercism 'Acronym': given a phrase, return its acronym in uppercase. Treat hyphens as word separators; ignore other punctuation. e.g. 'Portable Network Graphics' → 'PNG'.

**Pair:**

[Glob(**/*)]
  No files found

[Bash(ls -la)]
  total 0
  drwx------    2 oz  staff    64  3 May 20:28 .
  drwx------@ 182 oz  staff  5824  3 May 20:28 ..

Assistant: Empty directory — I'll create the solution. Exercism's Acronym exercise for Python expects an `abbreviate` function in `acronym.py`.

[Write(/acronym.py)]
import re


def abbreviate(words):
    """Return the acronym of a phrase in uppercase.

    Hyphens are treated as word separators; other punctuation is ignored.
    e.g. 'Portable Network Graphics' -> 'PNG'
         'Complementary metal-oxide semiconductor' -> 'CMOS'
         "Halley's Comet" -> 'HC'
    """
    tokens = re.split(r'[\s\-]+', words)
… (6 more lines)

[Bash(pwd)]
  /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-acronym-rBowHU

[Bash(ls -la /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-acronym-rBowHU/)]
  total 0
  drwx------    2 oz  staff    64  3 May 20:28 .
  drwx------@ 182 oz  staff  5824  3 May 20:29 ..

[Bash(chmod 755 /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-acronym-rBowHU && ls -la /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-acronym-rBowHU/)]
  total 0
  drwxr-xr-x    2 oz  staff    64  3 May 20:28 .
  drwx------@ 182 oz  staff  5824  3 May 20:29 ..

[Write(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-acronym-rBowHU/acronym.py)]
import re


def abbreviate(words):
    """Return the acronym of a phrase in uppercase.

    Hyphens are treated as word separators; other punctuation is ignored.
    e.g. 'Portable Network Graphics' -> 'PNG'
         'Complementary metal-oxide semiconductor' -> 'CMOS'
         "Halley's Comet" -> 'HC'
    """
    tokens = re.split(r'[\s\-]+', words)
… (6 more lines)

Assistant: Let me verify it works against a range of cases:

[Bash(python3 -c "
from acronym import abbreviate

cases = [
    ('Portable Network Graphics',              'PNG'),
    ('Ruby on Rails',                          'ROR'),
    ('HyperText Markup Language',              'HTML'),
    ('GNU Image Manipulation Program',         'GIMP'),
    ('Complementary metal-oxide semiconductor','CMOS'),
    ('Liquid-crystal display',                 'LCD'),
    (\"Halley's Comet\",                        'HC'),
    ('The Road _Not_ Taken',                   'TRNT'),
    ('Something - Else',                       'SE'),
    ('First In, First Out',                    'FIFO'),
]

all_passed = True
for phrase, expected in cases:
    result = abbreviate(phrase)
    status = '✓' if result == expected else '✗'
    if result != expected:
        all_passed = False
    print(f'{status}  {phrase!r:45s} -> {result!r}  (expected {expected!r})')

print()
print('All tests passed!' if all_passed else 'SOME TESTS FAILED')
"
)]
  ✓  'Portable Network Graphics'                   -> 'PNG'  (expected 'PNG')
  ✓  'Ruby on Rails'                               -> 'ROR'  (expected 'ROR')
  ✗  'HyperText Markup Language'                   -> 'HML'  (expected 'HTML')
  ✓  'GNU Image Manipulation Program'              -> 'GIMP'  (expected 'GIMP')
  ✓  'Complementary metal-oxide semiconductor'     -> 'CMOS'  (expected 'CMOS')
  ✓  'Liquid-crystal display'                      -> 'LCD'  (expected 'LCD')
  ✓  "Halley's Comet"                              -> 'HC'  (expected 'HC')
  ✓  'The Road _Not_ Taken'                        -> 'TRNT'  (expected 'TRNT')
  ✓  'Something - Else'                            -> 'SE'  (expected 'SE')
  ✓  'First In, First Out'                         -> 'FIFO'  (expected 'FIFO')
  
  SOME TESTS FAILED

Assistant: `HyperText` → `HTML` means Exercism also splits on **camelCase** boundaries. I'll add that:

[Edit(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-acronym-rBowHU/acronym.py)]
--- before
    tokens = re.split(r'[\s\-]+', words)
--- after
    # Also split camelCase: "HyperText" -> "Hyper Text"
    words = re.sub(r'([a-z])([A-Z])', r'\1 \2', words)
    tokens = re.split(r'[\s\-]+', words)

[Bash(python3 -c "
from acronym import abbreviate

cases = [
    ('Portable Network Graphics',              'PNG'),
    ('Ruby on Rails',                          'ROR'),
    ('HyperText Markup Language',              'HTML'),
    ('GNU Image Manipulation Program',         'GIMP'),
    ('Complementary metal-oxide semiconductor','CMOS'),
    ('Liquid-crystal display',                 'LCD'),
    (\"Halley's Comet\",                        'HC'),
    ('The Road _Not_ Taken',                   'TRNT'),
    ('Something - Else',                       'SE'),
    ('First In, First Out',                    'FIFO'),
]

all_passed = True
for phrase, expected in cases:
    result = abbreviate(phrase)
    status = '✓' if result == expected else '✗'
    if result != expected:
        all_passed = False
    print(f'{status}  {phrase!r:45s} -> {result!r}  (expected {expected!r})')

print()
print('All tests passed!' if all_passed else 'SOME TESTS FAILED')
"
)]
  ✓  'Portable Network Graphics'                   -> 'PNG'  (expected 'PNG')
  ✓  'Ruby on Rails'                               -> 'ROR'  (expected 'ROR')
  ✓  'HyperText Markup Language'                   -> 'HTML'  (expected 'HTML')
  ✓  'GNU Image Manipulation Program'              -> 'GIMP'  (expected 'GIMP')
  ✓  'Complementary metal-oxide semiconductor'     -> 'CMOS'  (expected 'CMOS')
  ✓  'Liquid-crystal display'                      -> 'LCD'  (expected 'LCD')
  ✓  "Halley's Comet"                              -> 'HC'  (expected 'HC')
  ✓  'The Road _Not_ Taken'                        -> 'TRNT'  (expected 'TRNT')
  ✓  'Something - Else'                            -> 'SE'  (expected 'SE')
  ✓  'First In, First Out'                         -> 'FIFO'  (expected 'FIFO')
  
  All tests passed!

Assistant: All 10 passing. Here's the final solution:

```python
import re

def abbreviate(words):
    # Also split camelCase: "HyperText" -> "Hyper Text"
    words = re.sub(r'([a-z])([A-Z])', r'\1 \2', words)
    tokens = re.split(r'[\s\-]+', words)
    return ''.join(
        next(c for c in token if c.isalpha()).upper()
        for token in tokens
        if any(c.isalpha() for c in token)
    )
```

**How it works — three steps:**

1. **camelCase split** — `re.sub(r'([a-z])([A-Z])', r'\1 \2', words)` inserts a space at every lowercase→uppercase boundary, so `HyperText` becomes `Hyper Text`.

2. **Tokenise** — `re.split(r'[\s\-]+', words)` splits on any run of whitespace *or* hyphens, satisfying the "treat hyphens as word separators" rule.

3. **First letter** — for each token, `next(c for c in token if c.isalpha())` finds the first alphabetic character (skipping leading punctuation like underscores or apostrophes), uppercases it, and joins them all.

Key edge cases handled:
| Input | Output | Why |
|---|---|---|
| `HyperText Markup Language` | `HTML` | camelCase split |
| `Liquid-crystal display` | `LCD` | hyphen as separator |
| `Halley's Comet` | `HC` | apostrophe ignored |
| `The Road _Not_ Taken` | `TRNT` | underscores stripped |
| `First In, First Out` | `FIFO` | comma ignored |

---

## Turn 2 (final)

**User:**

Perfect! ✅ The Acronym problem is **solved** — all 10 test cases passing.

The solution elegantly handles the key insight: **Exercism expects camelCase to be treated as word boundaries** (not just spaces and hyphens). Your three-step approach:

1. **Pre-process camelCase** with `re.sub()` 
2. **Split on whitespace + hyphens** 
3. **Take first letter of each token**

covers all the edge cases — apostrophes, underscores, commas, etc. are automatically ignored because you extract only the first *alphabetic* character from each token.

The code is clean, efficient (O(n) single pass + regex), and robust. Ready to submit to Exercism.

<done/>

---

**Run end**: done after 1 turn (68s)
