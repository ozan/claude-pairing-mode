# exercism-acronym

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T04:13:24.234Z

---

## Turn 1

**User:**

Exercism 'Acronym': given a phrase, return its acronym in uppercase. Treat hyphens as word separators; ignore other punctuation. e.g. 'Portable Network Graphics' → 'PNG'.

**Pair:**

Thinking: Let me build this Exercism 'Acronym' exercise with the user, using the pair programming approach. I'll start with a foundational decision about how to approach the solution.
  
  Let me think about the core approach:
  1. Split on whitespace and hyphens
  2. Take first letter of each word
  3. Uppercase
  
  The interesting design question here is how to handle the splitting/extraction. Two approaches:
  1. `re.split(r'[\s-]+', phrase)` - split on whitespace and hyphens
  2. `re.findall(r"[a-zA-Z']+", phrase)` - find word-like tokens (but this treats hyphens as separators naturally since hyphens aren't included)
     
  Now I'm thinking through the edge cases more carefully. The key insight is that hyphens are word separators, but apostrophes within words should be preserved—so "Halley's Comet" becomes "HC", not treating the apostrophe as a break. Looking at typical Exercism test cases like "HyperText Markup Language" → "HTML" and "GNU Image Manipulation Program" → "GIMP", the pattern is straightforward: extract the first letter of each word, where words are separated by spaces and hyphens.
  
  The approach is to split on whitespace or hyphens using a regex pattern, then take the first character of each resulting token and uppercase it. For something like "Something - with - dashes", splitting on spaces and hyphens gives individual words, yielding "SWD". And "Complementary metal-oxide semiconductor" splits into four tokens, giving "CMOS". I should also handle leading or trailing punctuation that might create empty tokens after splitting.
  
  I'm considering two approaches: one that splits on spaces and hyphens directly, and another using `findall` to extract letter sequences. The first approach is better because it preserves tokens like "Halley's" as a single unit, correctly producing "HC" for "Halley's Comet" rather than incorrectly splitting it into "HS".
  
  Writing the abbreviation function...

Assistant: Good Exercism puzzle. The core question is how to tokenize the phrase before grabbing initials — let me make that the first decision.

OPTIONS:
[A] Find letter-runs
```diff
+++ acronym.py
@@ -0,0 +1,4 @@
+import re
+
+def abbreviate(words):
+    return ''.join(w[0].upper() for w in re.findall(r'[a-zA-Z]+', words))
```

[B] Split on delimiters
```diff
+++ acronym.py
@@ -0,0 +1,4 @@
+import re
+
+def abbreviate(words):
+    return ''.join(w[0].upper() for w in re.split(r'[\s\-]+', words) if w)
```

(Reply with A or B, or ask a follow-up question.)

Assistant: The pairing tool isn't available in this session — I'll just ask directly.

Here's the core design question: which tokenization strategy should we use?

**Option A — find letter-runs:**
```python
re.findall(r'[a-zA-Z]+', words)
```

**Option B — split on delimiters:**
```python
re.split(r'[\s\-]+', words)
```

Both look reasonable. Which would you pick, and why? Think about a phrase like `"Halley's Comet"`.

---

## Turn 2

**User:**

Ah, good question. Let me trace through "Halley's Comet":

**Option A** (`findall` letters):
- Finds: `['Halley', 's', 'Comet']`
- Takes first letters: `'H'`, `'S'`, `'C'` → `'HSC'` ❌

That's wrong — the apostrophe splits the word, so we'd treat the `'s` as its own token.

**Option B** (`split` on spaces and hyphens):
- Splits on `\s\-`: `["Halley's", "Comet"]`
- Takes first letters: `'H'`, `'C'` → `'HC'` ✓

Option B preserves apostrophes inside words, which is what we want. I'll go with **B**.

**Pair:**

Thinking: The user correctly identified the issue and chose Option B. Let me create the file with that implementation.

Assistant: Exactly right. Apostrophes are "other punctuation" — they belong inside the word, not between words. Option A treats every non-letter as a separator, which is too aggressive.

[Bash(ls acronym.py 2>/dev/null && echo exists || echo missing)]
  missing

[Write(acronym.py)]
import re


def abbreviate(words):
    return ''.join(w[0].upper() for w in re.split(r'[\s\-]+', words) if w)


Assistant: Let's verify it against the key cases:

[Bash(python3 - <<'EOF'
from acronym import abbreviate

cases = [
    ("Portable Network Graphics",        "PNG"),
    ("HyperText Markup Language",        "HTML"),
    ("Complementary metal-oxide semiconductor", "CMOS"),
    ("Halley's Comet",                   "HC"),
    ("The Road _Not_ Taken",             "TRNT"),
    ("Something - with - dashes",        "SWD"),
]

for phrase, expected in cases:
    got = abbreviate(phrase)
    status = "✓" if got == expected else f"✗ (got {got!r})"
    print(f"{status}  {phrase!r} → {expected}")
EOF
)]
  ✓  'Portable Network Graphics' → PNG
  ✗ (got 'HML')  'HyperText Markup Language' → HTML
  ✓  'Complementary metal-oxide semiconductor' → CMOS
  ✓  "Halley's Comet" → HC
  ✗ (got 'TR_T')  'The Road _Not_ Taken' → TRNT
  ✓  'Something - with - dashes' → SWD

Thinking: Two failures:
  1. "HyperText Markup Language" → "HML" instead of "HTML". The issue is that "HyperText" is one word but should contribute "H" AND "T"? Wait, no. "HyperText" → "H" is the first letter, so the result would be "HML" not "HTML". But Exercism expects "HTML" from "HyperText Markup Language".
  
  Hmm, this is a case where CamelCase words should be split too. So "HyperText" → ["Hyper", "Text"] → "HT".
  
  
  Actually, the Exercism tests confirm it—I need to split on camelCase boundaries too, treating each capital letter as the start of a new word.
  
  2. "The Road _Not_ Taken" → "TR_T" because the underscore handling is off. When I split on whitespace and hyphens, `_Not_` stays intact since underscores aren't in the split pattern, so I'm taking the first letter of that whole string instead of recognizing the underscores as word boundaries.
  
  The real issue is I need to handle both camelCase splitting and stripping non-alphabetic characters from token edges. For camelCase like "HyperText", I need to extract H and T as separate tokens. For "_Not_", I need to skip past the leading underscore and grab N. A regex pattern that captures uppercase letters and their following lowercase sequences, plus standalone uppercase runs, should handle the camelCase splitting cleanly. The regex approach with `[a-zA-Z']+` actually handles most cases well—it correctly processes "Halley's Comet" and underscores—but CamelCase still needs special handling since "HyperText" would only give "H" instead of "HT". I could either insert spaces before uppercase letters that follow lowercase ones, or use a more sophisticated pattern like `[A-Z]?[a-z']+|[A-Z]+` to capture word boundaries within camelCase strings.
  
  Writing the abbreviation function... Looking at the test cases, I can see the pattern now—I need to handle CamelCase words like "HyperText" by extracting uppercase letters, treat underscores and hyphens as word separators, and ignore punctuation like colons and commas. The tricky part is distinguishing between cases where punctuation should be ignored versus where it marks a word boundary. I'm working through the tokenization approach now. When I split "PHP: Hypertext Preprocessor" on whitespace and hyphens, I get the tokens with the colon attached to "PHP", but taking the first character gives me "P" from "PHP:" which is correct. For "HyperText Markup Language", splitting on spaces gives me three words, but I'm getting "HML" instead of "HTML" — I need to handle CamelCase so "HyperText" contributes both its capital letters. And for cases like "_Not_", the leading underscore is being picked up as the first character when I should be stripping non-alphabetic characters first.
  
  I'm trying a regex-based approach that inserts spaces at camelCase boundaries, then extracts all alphabetic sequences and takes the first character of each one.
  
  Let me trace through some test cases to verify this works: "HyperText Markup Language" becomes "HTML", "Halley's Comet" gives "HC", underscores get stripped leaving just "N" for "_Not_", and "Complementary metal-oxide semiconductor" produces "CMOS". Testing a few more edge cases with dashes...
  
  The pattern is clear now—inserting spaces at camelCase boundaries, then extracting words with a character class that includes apostrophes, works reliably. I initially thought Option A was flawed for apostrophes, but actually including the apostrophe directly in the character class `[a-zA-Z']+` handles it perfectly, so that approach was correct all along. So `findall` with the apostrophe pattern actually handles the underscore case fine—it just extracts "Not" from "_Not_" since underscores aren't in the character class. The real problem is just CamelCase, which I can fix by inserting spaces before capital letters that follow lowercase letters, then running the same `findall` approach.

Assistant: Two failures worth understanding:

1. **`"HyperText"`** → our split gives one token `["HyperText"]`, first char `"H"` — but Exercism expects `"HT"` (CamelCase counts as two words)
2. **`"_Not_"`** → split gives `["_Not_"]`, first char `"_"` instead of `"N"`

Both are tokenization problems. Here's a design question — how should we fix it?

Assistant: The `mcp__pairing__propose_options` tool isn't available, so I'll lay out the options directly.

**Option A — pre-process CamelCase with a sub, then findall:**
```python
def abbreviate(words):
    expanded = re.sub(r'([a-z])([A-Z])', r'\1 \2', words)
    return ''.join(w[0].upper() for w in re.findall(r"[a-zA-Z']+", expanded))
```

**Option B — split on more delimiters (add `_`, strip leading non-alpha):**
```python
def abbreviate(words):
    tokens = re.split(r'[\s\-_]+', words)
    return ''.join(re.search(r'[a-zA-Z]', w).group().upper() for w in tokens if re.search(r'[a-zA-Z]', w))
```

Option B adds underscore splitting and finds the first alpha char per token — but it still won't handle `"HyperText"` since that's one token with no delimiter. Option A handles both problems: the `sub` inserts a space at camelCase transitions, and `findall` with `[a-zA-Z']+` naturally skips leading underscores/punctuation.

Which do you prefer?

---

## Turn 3

**User:**

Let me trace through "HyperText Markup Language" for both:

**Option A:**
- `sub` inserts space: `"Hyper Text Markup Language"`
- `findall`: `["Hyper", "Text", "Markup", "Language"]`
- First letters: `H`, `T`, `M`, `L` → `"HTML"` ✓

**Option B:**
- Split on spaces/hyphens/underscores: `["HyperText", "Markup", "Language"]`
- First alpha in each: `H`, `M`, `L` → `"HML"` ✗ (still breaks on CamelCase)

Option B still doesn't handle it because "HyperText" is a single token with no delimiter inside it. Option A solves both problems at once by preprocessing the camelCase boundaries.

I'll go with **Option A**.

**Pair:**

Thinking: The user correctly identified that Option A is better. Let me apply the change to the file.

Assistant: Exactly — the `sub` is doing the heavy lifting by normalizing CamelCase *before* tokenizing, so `findall` doesn't need to know anything about it. Clean separation of concerns.

[Edit(acronym.py)]
--- before
def abbreviate(words):
    return ''.join(w[0].upper() for w in re.split(r'[\s\-]+', words) if w)
--- after
def abbreviate(words):
    expanded = re.sub(r'([a-z])([A-Z])', r'\1 \2', words)
    return ''.join(w[0].upper() for w in re.findall(r"[a-zA-Z']+", expanded))

[Bash(python3 - <<'EOF'
from acronym import abbreviate

cases = [
    ("Portable Network Graphics",             "PNG"),
    ("HyperText Markup Language",             "HTML"),
    ("Complementary metal-oxide semiconductor","CMOS"),
    ("Halley's Comet",                         "HC"),
    ("The Road _Not_ Taken",                   "TRNT"),
    ("Something - with - dashes",              "SWD"),
    ("PHP: Hypertext Preprocessor",            "PHP"),
    ("First In, First Out",                    "FIFO"),
    ("Liquid-crystal display",                 "LCD"),
    ("Rolling On The Floor Laughing So Hard",  "ROTFLSH"),
]

for phrase, expected in cases:
    got = abbreviate(phrase)
    status = "✓" if got == expected else f"✗ (got {got!r})"
    print(f"{status}  {phrase!r} → {expected}")
EOF
)]
  ✓  'Portable Network Graphics' → PNG
  ✓  'HyperText Markup Language' → HTML
  ✓  'Complementary metal-oxide semiconductor' → CMOS
  ✓  "Halley's Comet" → HC
  ✓  'The Road _Not_ Taken' → TRNT
  ✓  'Something - with - dashes' → SWD
  ✓  'PHP: Hypertext Preprocessor' → PHP
  ✓  'First In, First Out' → FIFO
  ✓  'Liquid-crystal display' → LCD
  ✓  'Rolling On The Floor Laughing So Hard' → ROTFLSH

Assistant: All green. Here's the final solution:

```python
import re

def abbreviate(words):
    expanded = re.sub(r'([a-z])([A-Z])', r'\1 \2', words)
    return ''.join(w[0].upper() for w in re.findall(r"[a-zA-Z']+", expanded))
```

Two-step pipeline:
1. **Normalize** — insert spaces at `lowercase→Uppercase` boundaries so CamelCase becomes separate words
2. **Extract** — `findall` with `[a-zA-Z']+` grabs clean word tokens, incidentally skipping underscores, commas, colons, and any other leading/trailing punctuation

---

## Turn 4 (final)

**User:**

Perfect. That's elegant — the regex sub does all the camelCase normalization work, then `findall` handles everything else naturally. I can see how the two-step approach is cleaner than trying to bake everything into one pattern.

Thanks for working through this with me. The key insight was recognizing that Option A solved *both* problems (CamelCase and punctuation) with a simple preprocessing step, while Option B only partially addressed them.

<done/>

---

**Run end**: done after 3 turns (121s)
