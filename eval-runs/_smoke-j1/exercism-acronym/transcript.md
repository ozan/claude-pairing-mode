# exercism-acronym

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T05:23:17.264Z

---

## Turn 1

**User:**

Exercism 'Acronym': given a phrase, return its acronym in uppercase. Treat hyphens as word separators; ignore other punctuation. e.g. 'Portable Network Graphics' → 'PNG'.

**Pair:**

Thinking: The user wants to solve the Exercism 'Acronym' challenge. Let me start by proposing a design decision for how to approach this problem.
  
  The core logic is: split the phrase into words (treating hyphens as word separators, ignoring other punctuation), then take the first letter of each word and uppercase it.
  
  Let me think about the implementation approach. I'll use Python since no language was specified.
  
  The key decision is how to split/extract the first letters. Two main approaches:
  
  1. Use `re.split` to split on whitespace and hyphens, then take first char of each word
  
  
  2. Use `re.findall` to find first letter of each word directly
  
  I'm comparing these two regex-based strategies. The split approach filters out empty strings after splitting, while the findall approach matches word patterns directly. Let me verify which handles edge cases better—particularly with apostrophes in contractions and how each deals with consecutive hyphens or punctuation. I see the issue now—the split approach handles contractions correctly, but the findall approach with just letters splits "Halley's" into separate tokens. Looking at likely test cases like "Halley's Comet" and "something - or - other", the regex pattern `[a-zA-Z]+` would incorrectly treat the 's' in "Halley's" as its own word, while splitting on whitespace and hyphens preserves the contraction intact. I'm comparing the two approaches by testing them against the examples. The split method cleanly separates words on whitespace and hyphens, handling edge cases like leading or trailing delimiters with the `if w` filter. The findall approach with word boundaries should also work, though I need to verify it correctly captures the first letter of each word when contractions are involved.
  
  Actually, the word boundary approach has a problem—`\b` matches between word and non-word characters, so with "Halley's", there's a boundary after the apostrophe before the 's', which would incorrectly capture that letter too, giving "HsC" instead of "HC". So the findall method is buggy with contractions.
  
  The better approach is to split on whitespace and hyphens, then grab the first character of each word. I should present both options—the correct split method and the flawed regex approach—as a nice gotcha about how `\b` behaves with apostrophes.

Assistant: Good problem. The crux is how you extract the first letter of each word, given hyphens are separators but apostrophes aren't. Which approach do you prefer?

OPTIONS:
[A] Split on whitespace/hyphens
```diff
+++ acronym.py
@@ -0,0 +1,5 @@
+import re
+
+def abbreviate(words):
+    parts = re.split(r'[\s-]+', words)
+    return ''.join(p[0].upper() for p in parts if p)
```

[B] Findall word-boundary letters
```diff
+++ acronym.py
@@ -0,0 +1,5 @@
+import re
+
+def abbreviate(words):
+    letters = re.findall(r'\b[a-zA-Z]', words.replace('-', ' '))
+    return ''.join(l.upper() for l in letters)
```

(Reply with A or B, or ask a follow-up question.)

Thinking: The tool isn't available. Let me just present the options to the user directly without using the tool.

Assistant: The tool isn't loading — I'll present options directly.

Two approaches to consider:

**Option A — Split on whitespace/hyphens**
```python
import re

def abbreviate(words):
    parts = re.split(r'[\s-]+', words)
    return ''.join(p[0].upper() for p in parts if p)
```

**Option B — `\b` word-boundary findall**
```python
import re

def abbreviate(words):
    letters = re.findall(r'\b[a-zA-Z]', words.replace('-', ' '))
    return ''.join(l.upper() for l in letters)
```

Which would you pick — and can you spot any issue with either one?

---

## Turn 2

**User:**

Hmm, let me trace through both with some examples...

**Option A** with "Halley's Comet":
- Split on `[\s-]+` gives `["Halley's", "Comet"]`
- Take first char of each: `'H'`, `'C'`
- Result: `"HC"` ✓

**Option B** with "Halley's Comet":
- Replace hyphens with spaces: `"Halley's Comet"` (no change)
- Use `\b[a-zA-Z]` — wait, `\b` is a word boundary. It matches between word and non-word characters, right? So the apostrophe creates a boundary...
- That would match: 'H' (before H), 'C' (before C), **and 's'** (after the apostrophe, which is not a word character)
- Result: `"HCS"` ✗

I think Option B is broken on contractions? The apostrophe isn't treated as part of the word, so `\b` sees it as a word boundary and captures the 's' separately.

I'd go with **Option A**. It cleanly splits on delimiters and the `if p` filter handles any empty strings from consecutive hyphens.

**Pair:**

Thinking: The user correctly identified the bug in Option B. They traced through the logic perfectly. Now I should affirm their analysis and create the file with Option A.

Assistant: Exactly right. `\b` is purely positional — it fires on any word/non-word transition, and `'` is non-word, so `Halley's` has *two* word starts. Option A sidesteps all of that by working with the separators we actually care about.

Let me write it out:

[Glob(acronym.py)]
  No files found

[Write(acronym.py)]
import re


def abbreviate(words):
    parts = re.split(r'[\s-]+', words)
    return ''.join(p[0].upper() for p in parts if p)


Assistant: Clean and done. A few cases worth mentally verifying:

| Input | Split result | Output |
|---|---|---|
| `"Portable Network Graphics"` | `["Portable","Network","Graphics"]` | `"PNG"` ✓ |
| `"Halley's Comet"` | `["Halley's","Comet"]` | `"HC"` ✓ |
| `"something-wrong"` | `["something","wrong"]` | `"SW"` ✓ |
| `"GNU Image Manipulation Program"` | `["GNU","Image","Manipulation","Program"]` | `"GIMP"` ✓ |
| `" - leading junk - "` | `["","leading","junk",""]` — `if p` drops empties | `"LJ"` ✓ |

The `if p` guard on the last case is the only real defensive touch needed. Want to run it against Exercism's test suite?

---

## Turn 3

**User:**

Yeah, definitely. Let me make sure it actually runs against the test suite. How do I verify that with Exercism?

**Pair:**

Thinking: The user wants to know how to run the Exercism test suite for this exercise. I should explain the typical Exercism workflow.

Assistant: Two ways, depending on how you're set up:

**If you've downloaded the exercise via the CLI:**
```bash
cd ~/exercism/python/acronym   # wherever you downloaded it
cp /path/to/acronym.py .       # or just work in that dir directly
python -m pytest acronym_test.py -v
```

**If you haven't downloaded it yet:**
```bash
exercism download --exercise=acronym --track=python
cd ~/exercism/python/acronym
# copy your acronym.py here, then:
python -m pytest acronym_test.py -v
```

**Once tests pass, submit:**
```bash
exercism submit acronym.py
```

The `-v` flag on pytest gives you the pass/fail per test case, which is handy for spotting which edge case trips you up if anything fails.

Do you have the exercise already downloaded, or do you need to set up the Exercism CLI first?

---

## Turn 4 (final)

**User:**

I've got it downloaded already. Let me run the tests now.

```bash
python -m pytest acronym_test.py -v
```

(Running...)

All tests pass! The edge cases all work — empty strings, leading/trailing hyphens, contractions, mixed case, everything. The solution handles it cleanly.

I'm satisfied with how we caught that `\b` gotcha with Option B. That was a good learning moment about word boundaries and punctuation. Thanks for walking through the logic carefully.

<done/>

---

**Run end**: done after 3 turns (80s)
