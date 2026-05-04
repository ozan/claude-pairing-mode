# exercism-acronym

- Condition: `baseline`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T20:51:02

## Initial prompt

Exercism 'Acronym': given a phrase, return its acronym in uppercase. Treat hyphens as word separators; ignore other punctuation. e.g. 'Portable Network Graphics' → 'PNG'.

---

## Turn 1

### Tutor

[Glob(**/*)]
  No files found

[Write(/home/user/acronym.py)]
import re


def abbreviate(words):
    """Return the acronym for the given phrase in uppercase.

    Hyphens are treated as word separators; all other punctuation is ignored.
    """
    tokens = re.split(r'[\s\-]+', words)
    result = []
    for token in tokens:
        for ch in token:
… (5 more lines)
  error: ENOTSUP: operation not supported on socket, mkdir '/home/user'

[Bash(pwd)]
  /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-m_dkcwue

[Write(/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-m_dkcwue/acronym.py)]
import re


def abbreviate(words):
    """Return the acronym for the given phrase in uppercase.

    Hyphens are treated as word separators; all other punctuation is ignored.
    """
    tokens = re.split(r'[\s\-]+', words)
    result = []
    for token in tokens:
        for ch in token:
… (5 more lines)
  File created successfully at: /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-m_dkcwue/acronym.py

Tutor: Let me verify the logic against the key cases:

[Bash(python3 -c "
from acronym import abbreviate

cases = [
    ('Portable Network Graphics',         'PNG'),
    ('HyperText Markup Language',         'HTML'),
    ('Ruby on Rails',                     'ROR'),
    ('First In, First Out',               'FIFO'),
    ('Something - Totally - Awful',       'STA'),  # hyphens as separators
    (\"It's a trap\",                       'IAT'),  # apostrophe ignored
    ('GNU Image Manipulation Program',    'GIMP'),
    ('Liquid-crystal display',            'LCD'),  # hyphen separator
    ('PHP: Hypertext Preprocessor',       'PHP'),  # colon ignored
]

all_pass = True
for phrase, expected in cases:
    got = abbreviate(phrase)
    status = '✓' if got == expected else '✗'
    if got != expected:
        all_pass = False
    print(f'{status}  {phrase!r:45s} → {got!r}  (expected {expected!r})')

print()
print('All tests passed!' if all_pass else 'SOME TESTS FAILED.')
"
)]
  ✓  'Portable Network Graphics'                   → 'PNG'  (expected 'PNG')
  ✗  'HyperText Markup Language'                   → 'HML'  (expected 'HTML')
  ✓  'Ruby on Rails'                               → 'ROR'  (expected 'ROR')
  ✓  'First In, First Out'                         → 'FIFO'  (expected 'FIFO')
  ✓  'Something - Totally - Awful'                 → 'STA'  (expected 'STA')
  ✓  "It's a trap"                                 → 'IAT'  (expected 'IAT')
  ✓  'GNU Image Manipulation Program'              → 'GIMP'  (expected 'GIMP')
  ✓  'Liquid-crystal display'                      → 'LCD'  (expected 'LCD')
  ✓  'PHP: Hypertext Preprocessor'                 → 'PHP'  (expected 'PHP')
  
  SOME TESTS FAILED.

Tutor: `HyperText` is expected to yield `H` + `T` (camelCase split). I need to handle that case:

[Edit(/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-m_dkcwue/acronym.py)]
--- before
import re


def abbreviate(words):
    """Return the acronym for the given phrase in uppercase.

    Hyphens are treated as word separators; all other punctuation is ignored.
    """
    tokens = re.split(r'[\s\-]+', words)
    result = []
    for token in tokens:
        for ch in token:
            if ch.isalpha():
                result.append(ch.upper())
                break
    return ''.join(result)
--- after
import re


def abbreviate(words):
    """Return the acronym for the given phrase in uppercase.

    Hyphens are treated as word separators; all other punctuation is ignored.
    CamelCase words (e.g. 'HyperText') are split at each lowercase→uppercase
    boundary so each component contributes a letter.
    """
    # Split camelCase: insert a space at every lowercase→uppercase boundary
    words = re.sub(r'([a-z])([A-Z])', r'\1 \2', words)
    # Now split on whitespace and hyphens
    tokens = re.split(r'[\s\-]+', words)
    result = []
    for token in tokens:
        for ch in token:
            if ch.isalpha():
                result.append(ch.upper())
                break
    return ''.join(result)
  The file /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-m_dkcwue/acronym.py has been updated successfully.

[Bash(python3 -c "
from acronym import abbreviate

cases = [
    ('Portable Network Graphics',         'PNG'),
    ('HyperText Markup Language',         'HTML'),   # camelCase split
    ('Ruby on Rails',                     'ROR'),
    ('First In, First Out',               'FIFO'),
    ('Something - Totally - Awful',       'STA'),    # hyphens as separators
    (\"It's a trap\",                       'IAT'),   # apostrophe ignored
    ('GNU Image Manipulation Program',    'GIMP'),   # all-caps word → first letter only
    ('Liquid-crystal display',            'LCD'),    # hyphen separator
    ('PHP: Hypertext Preprocessor',       'PHP'),    # colon ignored
    ('Complementary metal-oxide semiconductor', 'CMOS'),  # hyphen mid-phrase
    ('The Road _Not_ Taken',              'TRNT'),   # underscores (punctuation, ignored)
]

all_pass = True
for phrase, expected in cases:
    got = abbreviate(phrase)
    status = '✓' if got == expected else '✗'
    if got != expected:
        all_pass = False
    print(f'{status}  {phrase!r:50s} → {got!r}  (expected {expected!r})')

print()
print('All tests passed!' if all_pass else 'SOME TESTS FAILED.')
"
)]
  ✓  'Portable Network Graphics'                        → 'PNG'  (expected 'PNG')
  ✓  'HyperText Markup Language'                        → 'HTML'  (expected 'HTML')
  ✓  'Ruby on Rails'                                    → 'ROR'  (expected 'ROR')
  ✓  'First In, First Out'                              → 'FIFO'  (expected 'FIFO')
  ✓  'Something - Totally - Awful'                      → 'STA'  (expected 'STA')
  ✓  "It's a trap"                                      → 'IAT'  (expected 'IAT')
  ✓  'GNU Image Manipulation Program'                   → 'GIMP'  (expected 'GIMP')
  ✓  'Liquid-crystal display'                           → 'LCD'  (expected 'LCD')
  ✓  'PHP: Hypertext Preprocessor'                      → 'PHP'  (expected 'PHP')
  ✓  'Complementary metal-oxide semiconductor'          → 'CMOS'  (expected 'CMOS')
  ✓  'The Road _Not_ Taken'                             → 'TRNT'  (expected 'TRNT')
  
  … (1 more lines)

Tutor: All 11 cases pass. Here's the final solution:

```python
import re

def abbreviate(words):
    # Split camelCase: insert a space at every lowercase→uppercase boundary
    words = re.sub(r'([a-z])([A-Z])', r'\1 \2', words)
    # Now split on whitespace and hyphens
    tokens = re.split(r'[\s\-]+', words)
    result = []
    for token in tokens:
        for ch in token:
            if ch.isalpha():
                result.append(ch.upper())
                break
    return ''.join(result)
```

### How it works

| Step | What it does | Example |
|---|---|---|
| `re.sub(r'([a-z])([A-Z])', …)` | Insert a space at every lowercase→uppercase boundary to handle camelCase | `HyperText` → `Hyper Text` |
| `re.split(r'[\s\-]+', …)` | Split on any run of whitespace **or hyphens** (hyphens = word separators) | `Liquid-crystal` → `['Liquid', 'crystal']` |
| Inner `for ch in token` | Grab the **first alphabetic character** from each token, skipping leading punctuation | `"It's"` → `I` |
| `.upper()` | Ensure the final result is uppercase | always |

Key edge-case behaviours:
- **CamelCase** (`HyperText`) → each sub-word contributes a letter (`HT`)
- **All-caps** (`GNU`) → no lowercase→uppercase boundary, so treated as one word (`G`)
- **Hyphens** (`metal-oxide`) → word separator (`MO`)
- **Other punctuation** (`, : ' _`) → skipped; only the first *alpha* char of a token is taken

### Student

Thanks for walking me through this! I can see the solution now—I especially appreciate how you handled the camelCase split with that regex. That's a key insight I wouldn't have thought of at first.

Just to make sure I understand: the `re.sub(r'([a-z])([A-Z])', r'\1 \2', words)` line inserts a space whenever a lowercase letter is followed by an uppercase letter. That way `HyperText` becomes `Hyper Text`, and then the split handles it as two separate words. Is that right?

And the inner loop takes only the first alphabetic character from each token—so even if there's punctuation at the start like `"It's"`, we skip past the apostrophe and grab the `I`. That makes sense.

One last thing: why do we need `[\s\-]+` (with the `+`) instead of just `[\s\-]`? Is it to handle multiple consecutive separators, like in `Something - Totally` where there are spaces around the hyphen?

<done/>

---

**Run end:** done after 1 turn(s) in 78.9s
