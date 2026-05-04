# exercism-acronym

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T05:09:52.028Z

---

## Turn 1

**User:**

Exercism 'Acronym': given a phrase, return its acronym in uppercase. Treat hyphens as word separators; ignore other punctuation. e.g. 'Portable Network Graphics' → 'PNG'.

**Pair:**

Thinking: The user wants to solve the Exercism 'Acronym' challenge. Let me think about the approach first, then present a good teaching moment.
  
  The task:
  - Given a phrase, return its acronym in uppercase
  - Treat hyphens as word separators
  - Ignore other punctuation
  - e.g. 'Portable Network Graphics' → 'PNG'
  
  Let me think about implementation approaches. I'll use Python since it's common for Exercism.
  
  Key considerations:
  1. Split on spaces and hyphens
  2. Take first letter of each word
  
  
  3. Uppercase
  
  Now I'm weighing different splitting strategies. The simple approach of replacing hyphens with spaces then splitting works, but I need to be careful about punctuation. The problem says to ignore other punctuation, so I might encounter cases like "it's" or "PHP: Hypertext Preprocessor" where punctuation is attached to words. I should probably filter out non-alphabetic characters from each word before taking the first letter, or use a regex approach that's more robust to handle these edge cases.
  
  Looking at what the test cases likely include—things like "Halley's Comet" becoming "HC", "Liquid-crystal display" becoming "LCD", and phrases with underscores or multiple delimiters—I think the cleanest solution is to use regex to extract just the word characters and grab the first letter of each word.
  
  Writing regex pattern... I'm realizing the issue with treating apostrophes—if I keep "Halley's" as one word, I only get H, but splitting it gives me two separate words. Let me think through the cleanest approach: split on whitespace and hyphens, then for each resulting word, find the first alphabetic character and uppercase it. This handles edge cases like words starting with punctuation, since I'm explicitly checking that the first character is alphabetic rather than just grabbing whatever's at position zero. I'm testing the regex pattern with `findall` to extract words and take their first letters, checking it against various edge cases like contractions, hyphens, and special characters to make sure it handles them correctly.
  
  Now I'm weighing whether to use `re.split` to break on separators and grab first letters, or `re.findall` to directly capture word tokens—the latter feels more intuitive since it focuses on what I want rather than what to discard.
  
  Actually, the real teaching moment might be simpler: comparing basic string operations like `replace` and `split` against regex. A straightforward approach would replace hyphens with spaces, then split and take the first character of each word—clean and readable, but it stumbles if non-letter characters end up at the start after splitting. The regex approach handles edge cases more gracefully.
  
  Looking at what Exercism's test suite probably includes, I'm thinking about cases like converting "Portable Network Graphics" to "PNG" or "First In, First Out" to "FIFO"—standard acronym extraction where the problem specifies treating hyphens as word boundaries while ignoring other punctuation.
  
  The simple replace-and-split method works fine for most of these: "First In, First Out" becomes ["First", "In,", "First", "Out"], and taking the first character of each gives "FIFO" since we grab "I" from "In," before the comma matters. But something like "_Not_" breaks it—the underscore becomes the first character instead of the letter. If Exercism includes that test case, I need the regex approach to skip non-letter characters and find the actual first letter.
  
  I'm weighing two approaches: the simpler replace-and-split method that fails on edge cases versus a regex solution that's more robust. Let me frame this as a teaching moment and show both options in Python, starting with the simpler version and then the regex version that handles punctuation properly.
  
  I'm reconsidering the regex pattern—word boundaries get tricky with underscores and apostrophes, so I'm settling on splitting by whitespace and hyphens, then taking the first letter of each token.
  
  Refining the regex split approach... I'm realizing the regex approach with a negative lookbehind is much cleaner—it captures the first letter of each word by matching any letter that isn't preceded by another letter. Testing it against the examples: "Portable Network Graphics" gives PNG, "Liquid-crystal display" gives LCD, and "The Road _Not_ Taken" gives TRNT, all correct since underscores and other non-letters don't interfere with the matching.
  
  But there's a problem with apostrophes—in "Halley's Comet", the 's' after the apostrophe would match as a word start since the apostrophe isn't a letter, giving "HSC" instead of "HC". So this approach needs refinement to handle contractions properly. I'm tracing through how the regex actually matches "Halley's Comet" — it catches the `H` at the start, then the `s` after the apostrophe (since there's a word boundary between the non-word apostrophe and the letter), and the `C` in Comet, giving me `['H', 's', 'C']` instead of the intended first letters of each word. The apostrophe is creating an unexpected word boundary that's breaking my approach.
  
  A cleaner solution is to strip out all non-alphabetic characters except spaces and hyphens first, then split on whitespace and hyphens to get clean words. I'm testing this against several examples: "Halley's Comet" becomes "Halleys Comet" after cleaning, which splits into the right words and gives me "HC"; "The Road _Not_ Taken" cleans to "The Road Not Taken" for "TRNT"; and "Liquid-crystal display" preserves the hyphen during cleaning so it splits correctly into "Liquid", "crystal", and "display" for "LCD". I'm comparing two approaches: a simpler one that just replaces hyphens with spaces and splits, versus a more robust regex solution that strips non-letter characters first. The simpler version has some edge cases it doesn't handle well, so the regex approach is more reliable.
  
  Looking at the actual Exercism test cases, I can see there's a tricky one with "The Road _Not_ Taken" that should produce "TRNT" — the underscores need to be treated as word separators, not ignored, which means I need to handle non-alphanumeric characters properly. Option A clearly breaks on the underscore case. Now I need to present these options to the user, so let me write this up in Python and check if there's an existing file structure first.

[Glob(acronym*)]
  No files found

[Glob(**/*.py)]
  No files found

Assistant: Clean slate. I'll use Python. Before writing anything, a key design question — how to split the phrase into words:

OPTIONS:
[A] replace + split
```diff
+++ acronym.py
@@ -0,0 +1,2 @@
+def abbreviate(words):
+    return ''.join(w[0].upper() for w in words.replace('-', ' ').split())
```

[B] regex clean + split
```diff
+++ acronym.py
@@ -0,0 +1,4 @@
+import re
+def abbreviate(words):
+    cleaned = re.sub(r"[^a-zA-Z\s-]", '', words)
+    return ''.join(w[0].upper() for w in re.split(r'[\s-]+', cleaned) if w)
```

(Reply with A or B, or ask a follow-up question.)

Thinking: The tool isn't available. Let me just present the options in my text response and ask the user which they prefer.

Assistant: The tool isn't loading, so I'll present the choice directly.

Two approaches to splitting the phrase into words:

**Option A — replace + split (simple):**
```python
def abbreviate(words):
    return ''.join(w[0].upper() for w in words.replace('-', ' ').split())
```

**Option B — regex clean + split (robust):**
```python
import re
def abbreviate(words):
    cleaned = re.sub(r"[^a-zA-Z\s-]", '', words)
    return ''.join(w[0].upper() for w in re.split(r'[\s-]+', cleaned) if w)
```

One of these fails on a standard Exercism test case — `"The Road _Not_ Taken" → "TRNT"`. Which do you think is safe, and why?

---

## Turn 2

**User:**

Let me trace through "The Road _Not_ Taken" with both options:

**Option A:**
- No hyphens to replace, so `"The Road _Not_ Taken".split()` gives `["The", "Road", "_Not_", "Taken"]`
- First letter of each: `"T"`, `"R"`, `"_"` (oops!), `"T"`
- Result: `"TR_T"` ❌ Fails because the underscore becomes the first character

**Option B:**
- `re.sub(r"[^a-zA-Z\s-]", '', words)` strips out the underscores → `"The Road Not Taken"`
- Then split on spaces/hyphens → `["The", "Road", "Not", "Taken"]`
- First letter of each: `"T"`, `"R"`, `"N"`, `"T"`
- Result: `"TRNT"` ✓

So **Option B** is safe — it treats underscores (and any other punctuation except hyphens) as word separators by removing them first, so they can't sneak into the first-letter position.

Option A assumes punctuation only appears between letters, not at word boundaries. It breaks when underscores frame words.

I think **Option B** is the right choice. Should I write it out to a file, or do you want to walk through the logic first?

**Pair:**

Thinking: The user traced through both options correctly and identified Option B as the right choice. They got it exactly right. I should confirm their reasoning, write the file, and maybe point out one more subtlety or move on to testing.
  
  Let me write the file now.

Assistant: Spot on — and you nailed the key insight: Option A's assumption only breaks at word boundaries, which makes it a subtle bug rather than an obvious one. Good catch on the `"_"` sneaking through.

Let me write it out:

[Write(acronym.py)]
import re

def abbreviate(words):
    cleaned = re.sub(r"[^a-zA-Z\s-]", '', words)
    return ''.join(w[0].upper() for w in re.split(r'[\s-]+', cleaned) if w)


Assistant: Let's verify against all the standard cases:

[Bash(python3 -c "
from acronym import abbreviate

cases = [
    ('Portable Network Graphics', 'PNG'),
    ('Ruby on Rails', 'ROR'),
    ('HyperText Markup Language', 'HTML'),
    ('First In, First Out', 'FIFO'),
    ('Something - Component - Test', 'SCT'),
    ('The Road _Not_ Taken', 'TRNT'),
    (\"Halley's Comet\", 'HC'),
    ('Liquid-crystal display', 'LCD'),
    ('PHP: Hypertext Preprocessor', 'PHP'),
]

for phrase, expected in cases:
    result = abbreviate(phrase)
    status = '✓' if result == expected else '✗'
    print(f'{status} {phrase!r:40s} → {result!r} (expected {expected!r})')
"
)]
  ✓ 'Portable Network Graphics'              → 'PNG' (expected 'PNG')
  ✓ 'Ruby on Rails'                          → 'ROR' (expected 'ROR')
  ✗ 'HyperText Markup Language'              → 'HML' (expected 'HTML')
  ✓ 'First In, First Out'                    → 'FIFO' (expected 'FIFO')
  ✓ 'Something - Component - Test'           → 'SCT' (expected 'SCT')
  ✓ 'The Road _Not_ Taken'                   → 'TRNT' (expected 'TRNT')
  ✓ "Halley's Comet"                         → 'HC' (expected 'HC')
  ✓ 'Liquid-crystal display'                 → 'LCD' (expected 'LCD')
  ✓ 'PHP: Hypertext Preprocessor'            → 'PHP' (expected 'PHP')

Thinking: We have a failure on 'HyperText Markup Language' → 'HML' but expected 'HTML'. This is interesting - "HyperText" has a capital T in the middle. Should mid-word capitals be treated as word starts?
  
  This is an interesting case. The Exercism problem says we should treat uppercase letters within a word as separate words? Let me think...
  
  "HyperText" → "HT" because both H and T are uppercase? That seems like it could be the intent.
  
  So we need to handle camelCase words - each capitalized "sub-word" contributes its letter. How to implement this?
  
  
  I can insert spaces before uppercase letters that follow lowercase ones, which would split "HyperText" into "Hyper Text" and then extract the initials correctly. Let me add this preprocessing step to handle camelCase properly.

Assistant: 8/9 — but `'HyperText Markup Language' → 'HML'`, expected `'HTML'`. The problem wants camelCase bumps (`HyperText`) treated as two words. How would you fix that?

The key step is inserting a split point between a lowercase letter followed by an uppercase one. Two ways to do it:

**Option A — insert a space at camelCase boundaries before cleaning:**
```python
re.sub(r'([a-z])([A-Z])', r'\1 \2', words)
```
applied first, turning `"HyperText"` → `"Hyper Text"`.

**Option B — split on uppercase runs as a separate regex pass:**
```python
re.split(r'[\s-]+|(?<=[a-z])(?=[A-Z])', cleaned)
```
a zero-width split inside the `re.split` call.

Both produce the same output here — but which do you think is cleaner to reason about, and why?

---

## Turn 3

**User:**

Let me trace through both with "HyperText Markup Language":

**Option A — insert space first:**
1. `"HyperText Markup Language"` → apply camelCase split → `"Hyper Text Markup Language"`
2. Clean (no change, already just letters/spaces)
3. Split on spaces → `["Hyper", "Text", "Markup", "Language"]`
4. First letters → `"HTML"` ✓

**Option B — split during the split call:**
1. `"HyperText Markup Language"` → clean (no change)
2. Split on `[\s-]+` OR `(?<=[a-z])(?=[A-Z])` → `["Hyper", "Text", "Markup", "Language"]`
3. First letters → `"HTML"` ✓

Honestly, **Option A feels clearer to me**. With Option A, the preprocessing is explicit — "normalize camelCase into spaces" — and then the rest of the logic stays the same. Each step is obvious when I read it.

Option B is elegant and efficient, but that zero-width lookahead/lookbehind syntax... I'd have to think harder to verify it's doing what I expect, especially if I come back to this code in a week. For a junior learning, explicit is better than clever.

Let me go with **Option A**. Should I update the function and retest?

**Pair:**

Thinking: The user chose Option A, which is actually my preferred option too (it's cleaner and more readable). Let me apply the change and retest.
  
  The updated function would be:
  ```python
  import re
  
  def abbreviate(words):
      words = re.sub(r'([a-z])([A-Z])', r'\1 \2', words)
      cleaned = re.sub(r"[^a-zA-Z\s-]", '', words)
      return ''.join(w[0].upper() for w in re.split(r'[\s-]+', cleaned) if w)
  
  
  ```
  
  Now I'll update the file.

Assistant: Agreed — Option A is the better pick. "Explicit is better than clever" is actually baked into Python's own philosophy (`import this`). The zero-width split in B is the kind of thing that reads like a magic spell.

[Edit(acronym.py)]
--- before
def abbreviate(words):
    cleaned = re.sub(r"[^a-zA-Z\s-]", '', words)
    return ''.join(w[0].upper() for w in re.split(r'[\s-]+', cleaned) if w)
--- after
def abbreviate(words):
    words = re.sub(r'([a-z])([A-Z])', r'\1 \2', words)
    cleaned = re.sub(r"[^a-zA-Z\s-]", '', words)
    return ''.join(w[0].upper() for w in re.split(r'[\s-]+', cleaned) if w)

[Bash(python3 -c "
from acronym import abbreviate

cases = [
    ('Portable Network Graphics', 'PNG'),
    ('Ruby on Rails', 'ROR'),
    ('HyperText Markup Language', 'HTML'),
    ('First In, First Out', 'FIFO'),
    ('Something - Component - Test', 'SCT'),
    ('The Road _Not_ Taken', 'TRNT'),
    (\"Halley's Comet\", 'HC'),
    ('Liquid-crystal display', 'LCD'),
    ('PHP: Hypertext Preprocessor', 'PHP'),
]

for phrase, expected in cases:
    result = abbreviate(phrase)
    status = '✓' if result == expected else '✗'
    print(f'{status} {phrase!r:40s} → {result!r}')
"
)]
  ✓ 'Portable Network Graphics'              → 'PNG'
  ✓ 'Ruby on Rails'                          → 'ROR'
  ✓ 'HyperText Markup Language'              → 'HTML'
  ✓ 'First In, First Out'                    → 'FIFO'
  ✓ 'Something - Component - Test'           → 'SCT'
  ✓ 'The Road _Not_ Taken'                   → 'TRNT'
  ✓ "Halley's Comet"                         → 'HC'
  ✓ 'Liquid-crystal display'                 → 'LCD'
  ✓ 'PHP: Hypertext Preprocessor'            → 'PHP'

Assistant: 9/9. Here's the final solution:

```python
import re

def abbreviate(words):
    words = re.sub(r'([a-z])([A-Z])', r'\1 \2', words)   # camelCase → tokens
    cleaned = re.sub(r"[^a-zA-Z\s-]", '', words)           # strip stray punctuation
    return ''.join(w[0].upper() for w in re.split(r'[\s-]+', cleaned) if w)
```

Three passes, each with a single responsibility — and you can verify each line in isolation. That's the payoff of the explicit approach.

---

## Turn 4 (final)

**User:**

Perfect — all green. I feel good about this solution. Each step does one thing:

1. **camelCase normalization** — turn `HyperText` into `Hyper Text`
2. **punctuation cleanup** — strip apostrophes, underscores, colons, etc.
3. **word extraction** — split on spaces/hyphens, grab first letters, uppercase

I learned a lot working through the edge cases — especially how treating hyphens as word separators but *removing* other punctuation is subtly different, and why explicit preprocessing beats clever regex patterns. Thanks for walking me through both options before picking one.

<done/>

---

**Run end**: done after 3 turns (151s)
