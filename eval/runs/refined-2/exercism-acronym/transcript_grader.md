# exercism-acronym

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:24:40

## Initial prompt

Exercism 'Acronym': given a phrase, return its acronym in uppercase. Treat hyphens as word separators; ignore other punctuation. e.g. 'Portable Network Graphics' → 'PNG'.

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Tutor: The core decision here is how to tokenize the phrase before grabbing initials. Two natural approaches:

OPTIONS:
[A] Split on separators
```diff
+++ acronym.py
@@ -0,0 +1,5 @@
+import re
+
+def abbreviate(words):
+    parts = re.split(r'[\s-]+', words)
+    return ''.join(p[0] for p in parts if p).upper()
```

[B] Find all alpha sequences
```diff
+++ acronym.py
@@ -0,0 +1,5 @@
+import re
+
+def abbreviate(words):
+    words_list = re.findall(r'[a-zA-Z]+', words)
+    return ''.join(w[0] for w in words_list).upper()
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach would you go with?

### Student

I think I'll go with **B**.

My reasoning: option A splits on separators, which means it could leave empty strings in the list if there are consecutive separators or leading/trailing whitespace. Even though there's an `if p` guard to filter those out, option B feels more direct — it just finds all the word-like sequences (letters only) and grabs the first letter from each one.

Plus, option B naturally handles the "ignore other punctuation" requirement without me having to think about which characters are separators and which aren't. If it's not a letter, `findall` won't include it in a word.

Does that logic make sense?

---

## Turn 2

### Tutor

Tutor: Your reasoning about punctuation and empty strings is sound — but there's a case where B breaks that's worth thinking through.

Consider **"Halley's Comet"**. Option B finds all `[a-zA-Z]+` sequences:
```
["Halley", "s", "Comet"]
```
So it produces `"HSC"` instead of `"HC"`. The apostrophe splits a contraction into two "words," and `s` sneaks in as an initial.

Option A keeps `"Halley's"` as one token (nothing to split on), takes `'H'`, and gives `"HC"`.

Your intuition that "if it's not a letter, ignore it" is appealing — but the problem is punctuation *inside* a word vs. *between* words. Apostrophes are intra-word; hyphens and spaces are inter-word. B treats them the same.

The `if p` guard in A is genuinely trivial — `re.split` on a clean input rarely produces empty strings, and when it does (e.g. leading spaces), the guard handles it in one character. That's not really a cost.

Want to switch to A, or would you like to dig into this more?

### Student

Ah, that's a really good catch. I see it now — I was conflating two different things. An apostrophe *inside* a word like "Halley's" shouldn't be a word boundary, but my approach treated it like one. Option A doesn't have that problem because it only splits on hyphens and whitespace, so "Halley's" stays together and gives us just the 'H'.

Yeah, I want to switch to **A**. 

The `if p` guard makes sense now too — it's not defensive over-engineering, it's just handling the edge case cleanly if consecutive separators or weird whitespace do create empty strings. One condition, problem solved.

So we're using:
```python
import re

def abbreviate(words):
    parts = re.split(r'[\s-]+', words)
    return ''.join(p[0] for p in parts if p).upper()
```

Should we test this against a few cases to make sure it works — like the "Halley's Comet" example, and maybe "Portable Network Graphics" from the original spec?

---

## Turn 3

### Tutor

Tutor: Let's write it and run some cases right away.

[Glob(acronym.py)]
  No files found

[Write(acronym.py)]
import re


def abbreviate(words):
    parts = re.split(r'[\s-]+', words)
    return ''.join(p[0] for p in parts if p).upper()

  File created successfully at: acronym.py

[Bash(python3 -c "
from acronym import abbreviate

cases = [
    ('Portable Network Graphics', 'PNG'),
    ('Ruby on Rails', 'ROR'),
    ('Complementary metal-oxide semiconductor', 'CMOS'),
    (\"Halley's Comet\", 'HC'),
    ('The Road _Not_ Taken', 'TRNT'),
    ('Something - Component', 'SC'),
]

for phrase, expected in cases:
    result = abbreviate(phrase)
    status = '✓' if result == expected else '✗'
    print(f'{status}  {phrase!r:45} → {result!r}  (expected {expected!r})')
"
)]
  ✓  'Portable Network Graphics'                   → 'PNG'  (expected 'PNG')
  ✓  'Ruby on Rails'                               → 'ROR'  (expected 'ROR')
  ✓  'Complementary metal-oxide semiconductor'     → 'CMOS'  (expected 'CMOS')
  ✓  "Halley's Comet"                              → 'HC'  (expected 'HC')
  ✗  'The Road _Not_ Taken'                        → 'TR_T'  (expected 'TRNT')
  ✓  'Something - Component'                       → 'SC'  (expected 'SC')

Tutor: Four pass, one fail — `_Not_` trips us up because `p[0]` grabs `_` instead of `N`. We need to reach past leading non-alpha characters. Two ways to fix it:

OPTIONS:
[A] Skip to first alpha char
```diff
+++ acronym.py
@@ -4,2 +4,3 @@
-    parts = re.split(r'[\s-]+', words)
-    return ''.join(p[0] for p in parts if p).upper()
+    parts = re.split(r'[\s-]+', words)
+    return ''.join(next(c for c in p if c.isalpha())
+                   for p in parts if any(c.isalpha() for c in p)).upper()
```

[B] Capture via regex group
```diff
+++ acronym.py
@@ -4,2 +4,2 @@
-    parts = re.split(r'[\s-]+', words)
-    return ''.join(p[0] for p in parts if p).upper()
+    return ''.join(re.findall(r'(?:^|[\s-])[^a-zA-Z]*([a-zA-Z])', words)).upper()
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which do you prefer?

### Student

I need to think through these carefully.

Option A: We split as before, then for each part, we skip non-alpha characters until we find an alpha one. The nested generator is a bit dense, but the logic is clear — "find the first alphabetic character in each part."

Option B: We use a single regex with a capture group. The pattern says "at a word boundary (start or after space/hyphen), skip any non-alpha characters, then capture the first alpha character." It's more compact, but the regex itself is harder for me to parse.

Honestly, I think I prefer **A**. Even though it's more verbose, I can follow the logic step-by-step: split, then for each part that has at least one letter, grab the first letter. The `if any(c.isalpha() for c in p)` guards against empty strings and parts with no letters, which feels safer.

Option B is clever, but I'd have to stare at that regex pattern for a minute to convince myself it handles all the cases right. For a problem like this, I'd rather have code that's easier to reason about than code that's compact.

Want to test A?

---

## Turn 4

### Tutor

Tutor: Agreed — and good instinct to trust readability over cleverness. Let's apply it and verify.

[Edit(acronym.py)]
--- before
    parts = re.split(r'[\s-]+', words)
    return ''.join(p[0] for p in parts if p).upper()
--- after
    parts = re.split(r'[\s-]+', words)
    return ''.join(next(c for c in p if c.isalpha())
                   for p in parts if any(c.isalpha() for c in p)).upper()
  The file acronym.py has been updated successfully.

[Bash(python3 -c "
from acronym import abbreviate

cases = [
    ('Portable Network Graphics', 'PNG'),
    ('Ruby on Rails', 'ROR'),
    ('Complementary metal-oxide semiconductor', 'CMOS'),
    (\"Halley's Comet\", 'HC'),
    ('The Road _Not_ Taken', 'TRNT'),
    ('Something - Component', 'SC'),
]

for phrase, expected in cases:
    result = abbreviate(phrase)
    status = '✓' if result == expected else '✗'
    print(f'{status}  {phrase!r:45} → {result!r}  (expected {expected!r})')
"
)]
  ✓  'Portable Network Graphics'                   → 'PNG'  (expected 'PNG')
  ✓  'Ruby on Rails'                               → 'ROR'  (expected 'ROR')
  ✓  'Complementary metal-oxide semiconductor'     → 'CMOS'  (expected 'CMOS')
  ✓  "Halley's Comet"                              → 'HC'  (expected 'HC')
  ✓  'The Road _Not_ Taken'                        → 'TRNT'  (expected 'TRNT')
  ✓  'Something - Component'                       → 'SC'  (expected 'SC')

Tutor: All six pass. Here's where we landed:

```python
import re

def abbreviate(words):
    parts = re.split(r'[\s-]+', words)
    return ''.join(next(c for c in p if c.isalpha())
                   for p in parts if any(c.isalpha() for c in p)).upper()
```

The two key decisions that shaped it:
1. **Split on separators** (not findall alpha runs) — so `"Halley's"` stays one token
2. **First alpha char per token** (not `p[0]`) — so `"_Not_"` gives `N`, not `_`

### Student

Perfect — all tests pass. I feel good about how we got here.

Looking back at the journey: we started with option B (findall), which seemed elegant until we hit the apostrophe case. That forced us to think carefully about what punctuation actually means in the problem — intra-word vs. inter-word separators. Switching to option A (split on separators) fixed that. Then the underscores showed us we needed one more refinement: skipping to the first alphabetic character instead of just grabbing `p[0]`.

Each failure taught us something concrete about the problem, and each fix was a small, readable change. I like that approach way better than trying to guess the perfect solution upfront.

The code is clear too: split on spaces and hyphens, filter to parts that have at least one letter, grab the first letter from each, uppercase it all. Done.

<done/>

---

**Run end:** done after 4 turn(s) in 134.8s
