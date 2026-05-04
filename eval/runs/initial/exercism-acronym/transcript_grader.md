# exercism-acronym

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:01:26

## Initial prompt

Exercism 'Acronym': given a phrase, return its acronym in uppercase. Treat hyphens as word separators; ignore other punctuation. e.g. 'Portable Network Graphics' → 'PNG'.

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Tutor: Good — let's build this in Python. First design decision: how do we split the phrase into words?

OPTIONS:
[A] Regex split on separators
```diff
+++ acronym.py
@@ -0,0 +1,4 @@
+import re
+
+def abbreviate(words):
+    return ''.join(w[0].upper() for w in re.split(r'[\s-]+', words) if w)
```

[B] Replace then split
```diff
+++ acronym.py
@@ -0,0 +1,3 @@
+def abbreviate(words):
+    return ''.join(w[0].upper() for w in words.replace('-', ' ').split())
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach do you prefer?

### Student

I think I'd like to go with **B**.

Here's my reasoning: it's simpler and more readable. We don't need to import regex if we can solve it with basic string methods. The replace-then-split approach makes it clear in plain terms what we're doing — swap hyphens for spaces, then split on whitespace.

Option A works too, but regex feels like overkill for this problem. Plus, I want to make sure I understand the basic approach first before reaching for more advanced tools.

Should we go ahead and test option B with some examples?

---

## Turn 2

### Tutor

Tutor: Fair reasoning — and B is fine for simple cases. But before we commit, one heads-up: the Exercism suite includes this case:

> `"The Road _Not_ Taken"` → `"TRNT"`

With option B, splitting on spaces gives you `_Not_` as a token, so `w[0]` is `_`, not `N`. You'd get `TR_T` instead of `TRNT`.

Option A sidesteps this entirely by expanding the split pattern. You could also fix B by stripping leading punctuation from each token:

```python
w.lstrip("_'").upper()[0]
```

…but at that point you're patching edge cases one by one, which is exactly the regex trap in reverse. Your instinct to understand the simple approach first is solid — want to stick with B and handle the underscore case explicitly, or switch to A?

### Student

Ah, good catch! I see the issue now. You're right — if I stick with B and keep patching edge cases with `lstrip()`, I'll end up with a brittle solution that breaks as soon as we hit a punctuation mark we didn't anticipate.

Let me switch to **option A** with the regex split.

The regex pattern `r'[\s-]+'` splits on any whitespace *or* hyphens, which naturally handles underscores (and other punctuation) by treating them as part of the word — then taking the first character of each word gets us the right letter regardless of what punctuation is attached.

It feels cleaner than playing whack-a-mole with different punctuation characters. And now that I see why the regex approach is actually the right tool here, I'm comfortable with it.

Should we test option A against that test case and a few others to make sure it works?

---

## Turn 3

### Tutor

Tutor: One correction before we write: I spoke too fast earlier. `r'[\s-]+'` splits on whitespace and hyphens, but `_` isn't in that set — so `_Not_` is still a single token and `w[0]` is still `_`. Good news: the fix is trivial.

OPTIONS:
[A] Add underscore to split set
```diff
+++ acronym.py
@@ -0,0 +1,4 @@
+import re
+
+def abbreviate(words):
+    return ''.join(w[0].upper() for w in re.split(r'[\s\-_]+', words) if w)
```
Enumerate each separator character in the character class.

[B] Strip leading non-alpha chars
```diff
+++ acronym.py
@@ -0,0 +1,5 @@
+import re
+
+def abbreviate(words):
+    tokens = (re.sub(r'^[^a-zA-Z]+', '', w) for w in re.split(r'[\s-]+', words))
+    return ''.join(t[0].upper() for t in tokens if t)
```
Strip any leading non-letter characters from each token after splitting.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which do you prefer?

### Student

I'd go with **A**.

Option B is clever, but it adds another regex operation (`re.sub`) on top of the split, which feels like extra work. Plus, the logic is a bit harder to follow — I have to trace through the stripping step to understand what's happening.

Option A is direct: we're just adding `_` to the list of characters we split on. It's explicit about what counts as a word separator, and it's a one-line fix.

That said, I'm wondering: will option A handle *all* punctuation, or could we still run into cases where other characters (like apostrophes or parentheses) cause problems? Or is the intent that we only care about whitespace, hyphens, and underscores as separators?

---

## Turn 4

### Tutor

Tutor: Good instinct. The key insight: apostrophes appear *inside* words (`Halley's`), never at the start, so `w[0]` still lands on a letter — we're fine. Same for commas (`"First In, First Out"` → token `"In,"`, first char `I` ✓) and colons (`"PHP: Hypertext"` → token `"PHP:"`, first char `P` ✓).

The only danger is punctuation that *leads* a token — which only happens with underscores in the Exercism suite. We've handled that. Let's write it.

[Glob(acronym.py)]
  No files found

[Write(acronym.py)]
import re


def abbreviate(words):
    return ''.join(w[0].upper() for w in re.split(r'[\s\-_]+', words) if w)

  File created successfully at: acronym.py

Tutor: Let's verify against all the interesting cases:

[Bash(python3 -c "
from acronym import abbreviate

cases = [
    ('Portable Network Graphics',            'PNG'),
    ('Ruby on Rails',                         'ROR'),
    ('First In, First Out',                   'FIFO'),
    ('Complementary metal-oxide semiconductor','CMOS'),
    ('Liquid-crystal display',                'LCD'),
    ('Something - Interesting',              'SI'),
    (\"Halley's Comet\",                       'HC'),
    ('The Road _Not_ Taken',                  'TRNT'),
    ('PHP: Hypertext Preprocessor',           'PHP'),
]

for phrase, expected in cases:
    got = abbreviate(phrase)
    status = '✓' if got == expected else f'✗ (got {got})'
    print(f'{status}  {phrase!r}')
"
)]
  ✓  'Portable Network Graphics'
  ✓  'Ruby on Rails'
  ✓  'First In, First Out'
  ✓  'Complementary metal-oxide semiconductor'
  ✓  'Liquid-crystal display'
  ✓  'Something - Interesting'
  ✓  "Halley's Comet"
  ✓  'The Road _Not_ Taken'
  ✓  'PHP: Hypertext Preprocessor'

Tutor: All green. The final solution is clean:

```python
import re

def abbreviate(words):
    return ''.join(w[0].upper() for w in re.split(r'[\s\-_]+', words) if w)
```

Three moving parts:
- **`re.split(r'[\s\-_]+')`** — splits on runs of whitespace, hyphens, or underscores
- **`w[0].upper()`** — takes the first character (safe because leading non-alpha only happens with the separators we already split on)
- **`if w`** — guards against empty strings from leading/trailing separators

### Student

Perfect! That's really satisfying. I can see how the solution evolved: we started with a simple approach (option B), hit an edge case (underscores), and realized that a regex split was actually the cleaner path once we understood *why* — not because regex is always better, but because it directly solves the core problem (defining what counts as a word separator).

I also appreciate how the tutor walked me through the punctuation cases. It made me realize that most punctuation doesn't actually break the solution — only leading punctuation does, and we've explicitly handled that by adding underscores to the split pattern.

The final code is minimal and readable. The three moving parts you outlined make sense, and all nine test cases pass. I feel like I understand not just *what* the code does, but *why* each piece is there.

Thanks for working through this one — I'm confident in the solution now.

<done/>

---

**Run end:** done after 4 turn(s) in 114.1s
