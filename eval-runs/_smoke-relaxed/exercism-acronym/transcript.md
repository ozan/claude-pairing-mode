# exercism-acronym

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T03:44:23.148Z

---

## Turn 1

**User:**

Exercism 'Acronym': given a phrase, return its acronym in uppercase. Treat hyphens as word separators; ignore other punctuation. e.g. 'Portable Network Graphics' → 'PNG'.

**Pair:**

Thinking: Let me build the Exercism 'Acronym' exercise. The task is to take a phrase and return its acronym in uppercase. Words can be separated by spaces or hyphens. Other punctuation should be ignored.
  
  Let me start by presenting a foundational decision about how to approach this - specifically around the regex/splitting approach.
  
  Let me think about the options:
  1. Split on spaces and hyphens, then take the first letter of each word
  2. Use regex to find all word-starting letters directly
  
  Option 1: `re.split(r'[\s-]+', phrase)` then take first char of each part
  Option 2: `re.findall(r"[a-zA-Z']+", phrase)` - but this doesn't treat hyphens as separators correctly... 
  
  Actually, splitting on whitespace and hyphens gives me the individual words, and I just need the first letter of each. Let me trace through some examples to verify this works: "Portable Network Graphics" splits into separate words and gives me P, N, G for "PNG". For "PHP: Hypertext Preprocessor", splitting on spaces leaves "PHP:" as one token, but taking the first letter still gives me P, which is correct. And "Complementary metal-oxide semiconductor" splits on both spaces and hyphens to give me the right letters.
  
  But wait, "HyperText Markup Language" is tricky—the standard expects "HTML", not just H, M, L. That suggests I need to handle camelCase words too, where capitals within a word might represent separate acronym letters. Let me check what the actual test cases expect to understand the pattern better. I'm reconsidering the approach—maybe I should use a regex pattern to capture uppercase letters followed by lowercase letters, or standalone uppercase letters, to properly handle camelCase words like "HyperText". Let me think through what the actual Exercism test cases are, since I'm not sure if "HyperText Markup Language" is even tested.
  
  Looking at the standard test cases, it seems like the focus is on simple phrases with spaces and hyphens, not camelCase splitting. So I'll go with a straightforward approach: replace hyphens with spaces, split on whitespace, strip non-alphabetic characters from each word, and take the first letter of what remains.
  
  The tricky part is handling edge cases like underscores—if I just split on spaces and hyphens, a word like "_Not_" would keep its leading underscore, which isn't alphabetic, so it would get skipped entirely. I need to make sure I'm checking if the first alphabetic character exists before taking it.
  
  Let me think through two cleaner approaches: either use a word boundary regex to grab the first letter of each word, or preprocess the string to remove non-alphanumeric characters before splitting. The word boundary approach with `\b[a-zA-Z]` should handle most cases, but I need to verify it works correctly with punctuation like colons and underscores. So the word boundary before 's' in "Halley's" means I'd incorrectly capture it as a separate word. I need a different approach—maybe removing non-apostrophe punctuation first, then splitting on spaces and hyphens to treat those as true word separators.
  
  Testing this logic through a few examples: "Halley's Comet" becomes "Halleys Comet" after stripping punctuation, giving me "HC". "PHP: Hypertext Preprocessor" cleans up nicely to "PHP". For "Something - or other", the regex handles multiple consecutive separators cleanly, skipping empty strings. And "The Road _Not_ Taken" strips the underscores to give me the right letters.
  
  I'm settling on the regex approach—cleaning out non-alphabetic characters except spaces and hyphens, then splitting on whitespace and hyphens together. This handles edge cases better than word boundaries. I'm settling on presenting two distinct approaches: the preprocessing method that strips punctuation first for robustness, versus the word boundary regex that's more elegant but stumbles on apostrophes. I'll lay out both options so the user can see the tradeoffs clearly.

Assistant: Quick setup first — let me check the directory.

[Bash(ls acronym* 2>/dev/null || echo "no files yet")]
  no files yet

Assistant: Clean slate. Before I write anything, a design question — what's the right core strategy here?

OPTIONS:
[A] Strip then split
```diff
+++ acronym.py
@@ -0,0 +1,5 @@
+import re
+
+def abbreviate(words):
+    cleaned = re.sub(r"[^a-zA-Z\s-]", "", words)
+    return ''.join(p[0] for p in re.split(r'[\s-]+', cleaned) if p).upper()
```

[B] Word-boundary extraction
```diff
+++ acronym.py
@@ -0,0 +1,4 @@
+import re
+
+def abbreviate(words):
+    return ''.join(re.findall(r'\b[a-zA-Z]', words)).upper()
```

(Reply with A or B, or ask a follow-up question.)

Thinking: The tool isn't available. Let me just present the options in text format and ask the user to choose.

Assistant: Two approaches to consider — which do you prefer?

---

**Option A — Strip then split**
```diff
+++ acronym.py
@@ -0,0 +1,5 @@
+import re
+
+def abbreviate(words):
+    cleaned = re.sub(r"[^a-zA-Z\s-]", "", words)
+    return ''.join(p[0] for p in re.split(r'[\s-]+', cleaned) if p).upper()
```

**Option B — Word-boundary extraction**
```diff
+++ acronym.py
@@ -0,0 +1,4 @@
+import re
+
+def abbreviate(words):
+    return ''.join(re.findall(r'\b[a-zA-Z]', words)).upper()
```

---

Option B is appealingly short — but think carefully about what `\b` does at an apostrophe. What happens with `"Halley's Comet"`?

---

## Turn 2

**User:**

Ah, good catch! With Option B and `"Halley's Comet"`:

The apostrophe isn't a word character, so `\b` sees it as a boundary. That means `\b[a-zA-Z]` would match:
- **H** (start of "Halley")
- **s** (after the apostrophe, treated as a new word start)
- **C** (start of "Comet")

So we'd get **"HSC"** instead of the correct **"HC"**. That's the subtle flaw.

Option A avoids this by stripping the apostrophe entirely first — "Halley's Comet" becomes "Halleys Comet", splits cleanly into ["Halleys", "Comet"], and gives us "HC".

**I'd go with Option A.** It's more robust to punctuation quirks, and hyphens/spaces are already treated as real word separators instead of accidental boundaries.

**Pair:**

Thinking: The user correctly identified the flaw in Option B and chose Option A. Let me write the file now.

Assistant: Exactly right — nice analysis. Let's write it.

[Write(acronym.py)]
import re


def abbreviate(words):
    cleaned = re.sub(r"[^a-zA-Z\s-]", "", words)
    return ''.join(p[0] for p in re.split(r'[\s-]+', cleaned) if p).upper()


Assistant: Let's verify against the key cases:

[Bash(python3 -c "
from acronym import abbreviate

cases = [
    ('Portable Network Graphics', 'PNG'),
    ('Ruby on Rails', 'ROR'),
    ('PHP: Hypertext Preprocessor', 'PHP'),
    ('Complementary metal-oxide semiconductor', 'CMOS'),
    (\"Halley's Comet\", 'HC'),
    ('The Road _Not_ Taken', 'TRNT'),
    ('Something - or other', 'SOO'),
]

for phrase, expected in cases:
    result = abbreviate(phrase)
    status = '✓' if result == expected else f'✗ (got {result})'
    print(f'{status}  {phrase!r} → {expected}')
"
)]
  ✓  'Portable Network Graphics' → PNG
  ✓  'Ruby on Rails' → ROR
  ✓  'PHP: Hypertext Preprocessor' → PHP
  ✓  'Complementary metal-oxide semiconductor' → CMOS
  ✓  "Halley's Comet" → HC
  ✓  'The Road _Not_ Taken' → TRNT
  ✓  'Something - or other' → SOO

Assistant: All passing. A few things worth noting about why this holds up:

- **`PHP:`** — the colon gets stripped, leaving `PHP` as a single token → `P` ✓  
- **`_Not_`** — underscores stripped, becomes `Not` ✓  
- **`metal-oxide`** — hyphen is kept as a separator in the `re.sub` pattern (`[^a-zA-Z\s-]`), so `re.split` then breaks on it → two tokens ✓  
- **`" - "`** — the `if p` guard drops any empty strings that appear from splitting on consecutive separators ✓

---

## Turn 3 (final)

**User:**

Perfect — that covers all the edge cases cleanly. The `if p` guard is especially nice for handling things like `" - "` where we'd otherwise get empty strings after splitting.

I feel confident in this solution. It's straightforward, handles punctuation robustly by stripping it upfront, and treats hyphens and spaces consistently as word separators. The tests confirm it works across the scenarios that matter.

<done/>

---

**Run end**: done after 2 turns (144s)
