# exercism-acronym

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Output style: `Learning`
- Started: 2026-05-04T00:15:05.373Z

---

## Turn 1

**User:**

Exercism 'Acronym': given a phrase, return its acronym in uppercase. Treat hyphens as word separators; ignore other punctuation. e.g. 'Portable Network Graphics' → 'PNG'.

**Pair:**

[Glob(**/*acronym*)]
  No files found

Assistant: No existing files — let me write the solution from scratch.

**The plan:**
- Split on **spaces and hyphens** (both are word separators)
- Strip other punctuation so it doesn't sneak into the first letter
- Grab the **first character** of each remaining word, uppercase it, join

[Write(/home/user/exercism/acronym/acronym.py)]
import re

def abbreviate(words):
    tokens = re.split(r'[\s\-]+', words)          # split on spaces & hyphens
    return ''.join(
        token.lstrip("'").upper()[0]              # strip leading apostrophes, take first letter
        for token in tokens
        if token                                  # skip empty strings from edge-case splits
    )


[Bash(pwd)]
  /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-acronym-yaJMpE

[Glob(**/*)]
  .claude/settings.json

[Write(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-acronym-yaJMpE/acronym.py)]
import re

def abbreviate(words):
    tokens = re.split(r'[\s\-]+', words)          # split on spaces & hyphens
    return ''.join(
        token.lstrip("'").upper()[0]              # strip leading apostrophes, take first letter
        for token in tokens
        if token                                  # skip empty strings from edge-case splits
    )


Assistant: Let me verify it against the examples:

[Bash(python3 - <<'EOF'
from acronym import abbreviate

tests = [
    ("Portable Network Graphics",           "PNG"),
    ("Ruby on Rails",                       "ROR"),
    ("HyperText Markup Language",           "HTML"),
    ("PHP: Hypertext Preprocessor",         "PHP"),   # colon ignored
    ("Something - Useful",                  "SU"),    # hyphen as separator
    ("Complementary metal-oxide semiconductor", "CMOS"),
    ("The Road _Not_ Taken",                "TRNT"),  # underscores ignored
]

for phrase, expected in tests:
    result = abbreviate(phrase)
    status = "✓" if result == expected else f"✗  (got {result!r})"
    print(f"{status}  {phrase!r} → {result}")
EOF
)]
  ✓  'Portable Network Graphics' → PNG
  ✓  'Ruby on Rails' → ROR
  ✗  (got 'HML')  'HyperText Markup Language' → HML
  ✓  'PHP: Hypertext Preprocessor' → PHP
  ✓  'Something - Useful' → SU
  ✓  'Complementary metal-oxide semiconductor' → CMOS
  ✗  (got 'TR_T')  'The Road _Not_ Taken' → TR_T

Assistant: Two bugs to fix:
1. **`HyperText` → `HT`**: need to detect **camelCase boundaries** (uppercase after lowercase)
2. **`_Not_` → `N`**: need to strip **all leading/trailing non-alpha** chars, not just apostrophes

[Edit(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-acronym-yaJMpE/acronym.py)]
--- before
import re

def abbreviate(words):
    tokens = re.split(r'[\s\-]+', words)          # split on spaces & hyphens
    return ''.join(
        token.lstrip("'").upper()[0]              # strip leading apostrophes, take first letter
        for token in tokens
        if token                                  # skip empty strings from edge-case splits
    )
--- after
import re

def abbreviate(words):
    result = []
    for token in re.split(r'[\s\-]+', words):           # spaces & hyphens are separators
        token = re.sub(r'^[^a-zA-Z]+|[^a-zA-Z]+$', '', token)  # strip leading/trailing punctuation
        if not token:
            continue
        result.append(token[0])                          # first letter of token
        for i in range(1, len(token)):                   # camelCase: uppercase after lowercase
            if token[i].isupper() and token[i - 1].islower():
                result.append(token[i])
    return ''.join(result).upper()

[Bash(python3 - <<'EOF'
from acronym import abbreviate

tests = [
    ("Portable Network Graphics",               "PNG"),
    ("Ruby on Rails",                           "ROR"),
    ("HyperText Markup Language",               "HTML"),   # camelCase
    ("PHP: Hypertext Preprocessor",             "PHP"),   # colon ignored
    ("Something - Useful",                      "SU"),    # hyphen as separator
    ("Complementary metal-oxide semiconductor", "CMOS"),  # hyphen mid-phrase
    ("The Road _Not_ Taken",                    "TRNT"),  # underscores stripped
    ("Halley's Comet",                          "HC"),    # apostrophe ignored
    ("It's a trap",                             "IAT"),   # mid-word apostrophe
]

all_pass = True
for phrase, expected in tests:
    result = abbreviate(phrase)
    ok = result == expected
    if not ok:
        all_pass = False
    print(f"{'✓' if ok else '✗'} {phrase!r:45} → {result}  (expected {expected})")

print("\nAll tests passed!" if all_pass else "\nSome tests FAILED.")
EOF
)]
  ✓ 'Portable Network Graphics'                   → PNG  (expected PNG)
  ✓ 'Ruby on Rails'                               → ROR  (expected ROR)
  ✓ 'HyperText Markup Language'                   → HTML  (expected HTML)
  ✓ 'PHP: Hypertext Preprocessor'                 → PHP  (expected PHP)
  ✓ 'Something - Useful'                          → SU  (expected SU)
  ✓ 'Complementary metal-oxide semiconductor'     → CMOS  (expected CMOS)
  ✓ 'The Road _Not_ Taken'                        → TRNT  (expected TRNT)
  ✓ "Halley's Comet"                              → HC  (expected HC)
  ✓ "It's a trap"                                 → IAT  (expected IAT)
  
  All tests passed!

Assistant: All 9 pass. Here's the final solution with the key ideas explained:

```python
import re

def abbreviate(words):
    result = []
    for token in re.split(r'[\s\-]+', words):           # spaces & hyphens are separators
        token = re.sub(r'^[^a-zA-Z]+|[^a-zA-Z]+$', '', token)  # strip leading/trailing punctuation
        if not token:
            continue
        result.append(token[0])                          # first letter of token
        for i in range(1, len(token)):                   # camelCase: uppercase after lowercase
            if token[i].isupper() and token[i - 1].islower():
                result.append(token[i])
    return ''.join(result).upper()
```

**Three key decisions:**

| Rule | Example | How it's handled |
|---|---|---|
| Spaces *and* hyphens split words | `metal-oxide` → `M`,`O` | `re.split(r'[\s\-]+', ...)` |
| Other punctuation is ignored | `_Not_`, `PHP:`, `Halley's` | Strip non-alpha from token edges with `re.sub` |
| camelCase counts as two words | `HyperText` → `H`,`T` | Extra loop: uppercase after lowercase = new word start |

The final `.upper()` ensures the result is always uppercase regardless of source casing.

---

## Turn 2 (final)

**User:**

Perfect! That makes total sense. I wasn't thinking about camelCase as word boundaries — that's a really clean way to handle it. And stripping punctuation from both edges before processing is way more robust than just checking for apostrophes.

I appreciate the breakdown in the table; it really clarifies the three layers of the problem. Looks like this solution is solid and ready to go.

<done/>

---

**Run end**: done after 1 turn (84s)
