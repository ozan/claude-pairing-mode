# exercism-acronym

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T03:54:55.477Z

---

## Turn 1

**User:**

Exercism 'Acronym': given a phrase, return its acronym in uppercase. Treat hyphens as word separators; ignore other punctuation. e.g. 'Portable Network Graphics' → 'PNG'.

**Pair:**

Thinking: The user wants to solve the Exercism 'Acronym' problem. Let me start building this with them. I'll use the teaching approach - propose options for the key implementation decision.
  
  The core question is: how to split/tokenize the phrase to extract first letters?
  
  Key considerations:
  - Split on whitespace and hyphens
  - Ignore other punctuation (apostrophes, etc.)
  - Take first letter of each word
  - Uppercase result
  
  The main interesting decision is how to handle the splitting/regex approach vs a manual approach.
  
  Let me think about good options to present:
  
  Option A: Use `re.findall` to extract word-starting letters directly
  
  
  Option B: Split on whitespace and hyphens, then grab the first character of each resulting word
  
  I'm weighing the regex approaches - specifically whether `\b` word boundaries work reliably with hyphens, or if I should explicitly split on `[\s-]+` and then process each token.
  
  Let me trace through "Halley's Comet" to see where each method breaks down. The apostrophe creates a word boundary issue since it's not a word character, so `\b[a-zA-Z]` would incorrectly capture the 's' after the apostrophe. Splitting on whitespace and hyphens avoids this problem entirely because "Halley's" stays intact as a single token.
  
  I'm also considering a negative lookbehind approach with `(?<![a-zA-Z])[a-zA-Z]` to match letters not preceded by other letters, which would correctly skip the 's' since it follows an apostrophe rather than a space.
  
  Actually, a cleaner regex would be `(?:^|[\s-])([a-zA-Z])` to explicitly match letters that come after the start of the string or whitespace/hyphens—this handles contractions properly without edge cases.
  
  I think the split approach is clearest: splitting on whitespace and hyphens, then taking the first character of each part. The regex with word boundaries looks elegant but fails silently on contractions like "Halley's Comet", which is worth highlighting as a teaching moment.
  
  Let me present both options to show the tradeoff between simplicity and the subtle bug that word boundaries introduce.

Assistant: Good problem — the interesting bit is the tokenization. Before writing any code, let me ask the key question:

OPTIONS:
[A] Split, then slice
```diff
+++ acronym.py
@@ -0,0 +1,5 @@
+import re
+
+def abbreviate(words):
+    parts = re.split(r'[\s-]+', words)
+    return ''.join(p[0] for p in parts if p).upper()
```

[B] Word-boundary findall
```diff
+++ acronym.py
@@ -0,0 +1,5 @@
+import re
+
+def abbreviate(words):
+    return ''.join(re.findall(r'\b[a-zA-Z]', words)).upper()
```

(Reply with A or B, or ask a follow-up question.)

Thinking: The tool isn't available. Let me just present the options in text form and ask the user which they prefer.

Assistant: The tool isn't loading, so I'll just lay out the two approaches directly:

**Option A — Split, then slice:**
```python
import re

def abbreviate(words):
    parts = re.split(r'[\s-]+', words)
    return ''.join(p[0] for p in parts if p).upper()
```

**Option B — Word-boundary `findall`:**
```python
import re

def abbreviate(words):
    return ''.join(re.findall(r'\b[a-zA-Z]', words)).upper()
```

Which would you go with — and why? One of these has a subtle failure case worth knowing about.

---

## Turn 2

**User:**

Hmm, I'm leaning toward **A** — the split approach feels more explicit about what we're separating on. 

But I'm not immediately seeing the failure in B. Is it the apostrophe issue? Like if we had "Halley's Comet", the `\b` matches *both* the boundary before 'H' *and* the boundary after the apostrophe (before 's'), so we'd accidentally grab the 's' too and get "HSC" instead of "HC"?

With A, since we're only splitting on whitespace and hyphens, "Halley's" stays as one token, we take the 'H', and the apostrophe never gets a chance to create a false boundary.

Is that the gotcha you were hinting at?

**Pair:**

Thinking: The user correctly identified the gotcha. Let me confirm and proceed with writing the file.

Assistant: Exactly right. `\b` is purely about the word-char / non-word-char boundary — it has no notion of "is this punctuation *inside* a word or *between* words". The apostrophe in `Halley's` looks like an internal separator to the regex engine, so you get a bonus boundary before the `s`.

Your intuition about A is spot on: by only splitting on explicit separators (spaces and hyphens), intra-word punctuation is never given a chance to carve out a new token.

Let me write the file:

[Bash(ls acronym.py 2>/dev/null && echo exists || echo missing)]
  missing

[Write(acronym.py)]
import re


def abbreviate(words):
    parts = re.split(r'[\s-]+', words)
    return ''.join(p[0] for p in parts if p).upper()


Assistant: Quick sanity check:

[Bash(python3 -c "
from acronym import abbreviate
cases = [
    ('Portable Network Graphics', 'PNG'),
    ('Ruby on Rails', 'ROR'),
    ('First In, First Out', 'FIFO'),
    ('GNU Image Manipulation Program', 'GIMP'),
    ('Complementary metal-oxide semiconductor', 'CMOS'),
    (\"Halley's Comet\", 'HC'),
]
for phrase, expected in cases:
    got = abbreviate(phrase)
    status = '✓' if got == expected else f'✗ (got {got})'
    print(f'{status}  {phrase!r} → {got}')
"
)]
  ✓  'Portable Network Graphics' → PNG
  ✓  'Ruby on Rails' → ROR
  ✓  'First In, First Out' → FIFO
  ✓  'GNU Image Manipulation Program' → GIMP
  ✓  'Complementary metal-oxide semiconductor' → CMOS
  ✓  "Halley's Comet" → HC

Assistant: All green, including the apostrophe case. The solution is five lines and the regex is doing one focused job — splitting on separators — rather than trying to describe what a "word start" looks like.

---

## Turn 3 (final)

**User:**

Perfect — that makes sense. I can see why word boundaries would be tempting for elegance, but you're right that the regex is cleaner when it's just doing one job: splitting on our known separators (spaces and hyphens). Everything else falls naturally out of that.

Thanks for walking me through the gotcha; that's a good lesson about edge cases with punctuation and regex boundaries.

<done/>

---

**Run end**: done after 2 turns (67s)
