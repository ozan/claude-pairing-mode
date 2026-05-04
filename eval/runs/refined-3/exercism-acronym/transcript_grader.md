# exercism-acronym

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:52:18

## Initial prompt

Exercism 'Acronym': given a phrase, return its acronym in uppercase. Treat hyphens as word separators; ignore other punctuation. e.g. 'Portable Network Graphics' → 'PNG'.

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Split on whitespace and hyphens
```diff
+++ acronym.py
@@ -0,0 +1,4 @@
+import re
+
+def abbreviate(words):
+    return ''.join(w[0].upper() for w in re.split(r'[\s-]+', words) if w)
```

[B] Find all letter runs
```diff
+++ acronym.py
@@ -0,0 +1,4 @@
+import re
+
+def abbreviate(words):
+    return ''.join(w[0] for w in re.findall(r'[a-zA-Z]+', words.replace('-', ' '))).upper()
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach would you go with?

### Student

I'd like to understand both options a bit better before choosing.

For **Option A**: It splits on whitespace and hyphens, then takes the first character of each non-empty word and uppercases it. That seems straightforward.

For **Option B**: It finds all letter runs (consecutive letters), but first replaces hyphens with spaces. Then it takes the first character of each found run and uppercases at the end.

I'm wondering — why does Option B replace the hyphen with a space before using `findall`? The `findall` already looks for letter runs with `[a-zA-Z]+`, so hyphens would naturally break those runs anyway. Wouldn't it work the same without that replacement?

Also, which one handles edge cases better? Like what if there are multiple hyphens in a row, or trailing punctuation?

---

## Turn 2

### Tutor

Tutor: You caught something real: **the `.replace('-', ' ')` in Option B is redundant.** `re.findall(r'[a-zA-Z]+', ...)` matches only letter characters, so hyphens already act as natural breaks — replacing them with spaces first changes nothing. It's harmless but unnecessary.

So the real difference between the two comes down to this edge case — consider a phrase like `"The Road _Not_ Taken"`:

| Approach | Token produced | `w[0]` | Result |
|---|---|---|---|
| **A** — `re.split(r'[\s-]+', ...)` | `'_Not_'` | `'_'` | ❌ wrong letter |
| **B** — `re.findall(r'[a-zA-Z]+', ...)` | `'Not'` | `'N'` | ✓ |

Option A splits on separators and takes the *first character of the token* — but if punctuation leads a token, that first character isn't a letter. Option B finds *letter sequences directly*, so it never picks up leading punctuation.

On your other questions:
- **Multiple hyphens in a row**: both handle it fine. Option A's `+` quantifier (`[\s-]+`) collapses consecutive separators. Option B just finds no letters in a run of hyphens.
- **Trailing punctuation**: Option A is fine here — `'word!'` splits to `'word!'`, and `w[0]` is `'w'`. The only problem is *leading* punctuation.

So Option B's `.replace` can be dropped entirely. Want to go with a cleaned-up version of B?

### Student

Yes, that makes sense! Option B is more robust because it's looking for actual letters rather than just taking the first character of whatever token results from splitting.

So the cleaned-up version of B would be:

```python
import re

def abbreviate(words):
    return ''.join(w[0] for w in re.findall(r'[a-zA-Z]+', words)).upper()
```

Just removing that redundant `.replace('-', ' ')` part. That way we're directly finding all letter sequences and grabbing the first letter of each one, which handles the leading punctuation edge case properly.

Should I test this against a few cases to make sure it works — like the basic 'Portable Network Graphics', the hyphenated case, and something with punctuation like "The Road _Not_ Taken"?

---

## Turn 3

### Tutor

Tutor: Exactly right. Let me write it and run those cases.

[Glob(acronym.py)]
  No files found

[Write(acronym.py)]
import re

def abbreviate(words):
    return ''.join(w[0] for w in re.findall(r'[a-zA-Z]+', words)).upper()

  File created successfully at: acronym.py

[Bash(python3 -c "
from acronym import abbreviate
cases = [
    ('Portable Network Graphics', 'PNG'),
    ('Liquid-crystal display', 'LCD'),
    ('The Road _Not_ Taken', 'TRNT'),
    (\"Halley's Comet\", 'HC'),
    ('Something - with a dash', 'SWAD'),
]
for phrase, expected in cases:
    result = abbreviate(phrase)
    status = '✓' if result == expected else f'✗ (got {result})'
    print(f'{status}  {phrase!r} → {result}')
"
)]
  ✓  'Portable Network Graphics' → PNG
  ✓  'Liquid-crystal display' → LCD
  ✓  'The Road _Not_ Taken' → TRNT
  ✗ (got HSC)  "Halley's Comet" → HSC
  ✓  'Something - with a dash' → SWAD

Tutor: One failure: `"Halley's Comet"` → `HSC` instead of `HC`. The apostrophe splits `Halley's` into two letter runs — `Halley` and `s` — so we get three initials instead of two.

We need to treat apostrophes as part of a word. Two ways to patch the pattern:

OPTIONS:
[A] Allow apostrophes mid-word
```diff
+++ acronym.py
@@ -3,2 +3,2 @@
-    return ''.join(w[0] for w in re.findall(r'[a-zA-Z]+', words)).upper()
+    return ''.join(w[0] for w in re.findall(r"[a-zA-Z]+(?:'[a-zA-Z]+)*", words)).upper()
```
Matches letter runs optionally followed by `'`+letters, so `Halley's` is one token. A leading apostrophe (e.g. `'word`) can never match since the pattern must start with `[a-zA-Z]+`.

[B] Include apostrophe in character class
```diff
+++ acronym.py
@@ -3,2 +3,2 @@
-    return ''.join(w[0] for w in re.findall(r'[a-zA-Z]+', words)).upper()
+    return ''.join(w[0] for w in re.findall(r"[a-zA-Z][a-zA-Z']*", words)).upper()
```
Uses `[a-zA-Z][a-zA-Z']*` — must start with a letter, then allows letters or apostrophes. `Halley's` matches whole; leading apostrophes are skipped.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which option do you prefer — A or B?

### Student

I think I prefer **Option B**.

Option A is more explicit about the structure — it says "letters, optionally followed by apostrophe-then-more-letters" — which accurately describes contractions like `Halley's`. But Option B is simpler and more flexible.

With Option B, `[a-zA-Z][a-zA-Z']*` means "start with a letter, then any mix of letters and apostrophes." It's shorter and handles the same cases. And I like that it naturally rejects leading apostrophes — if the input is `'word`, the pattern just won't match the leading `'`, it'll match `word`. That feels safe.

Let me see if it handles the test cases:

```python
import re

def abbreviate(words):
    return ''.join(w[0] for w in re.findall(r"[a-zA-Z][a-zA-Z']*", words)).upper()
```

Should I run the tests again to confirm this fixes the `Halley's Comet` case?

---

## Turn 4

### Tutor

Tutor: Fair reasoning — B is more concise and safe enough here. My slight preference for A is that `[a-zA-Z']*` technically matches tokens like `word'''` (trailing apostrophes), but since we only ever use `w[0]` it makes no practical difference. Let's apply it and verify.

[Edit(acronym.py)]
--- before
    return ''.join(w[0] for w in re.findall(r'[a-zA-Z]+', words)).upper()
--- after
    return ''.join(w[0] for w in re.findall(r"[a-zA-Z][a-zA-Z']*", words)).upper()
  The file acronym.py has been updated successfully.

[Bash(python3 -c "
from acronym import abbreviate
cases = [
    ('Portable Network Graphics', 'PNG'),
    ('Liquid-crystal display', 'LCD'),
    ('The Road _Not_ Taken', 'TRNT'),
    (\"Halley's Comet\", 'HC'),
    ('Something - with a dash', 'SWAD'),
    ('GNU Image Manipulation Program', 'GIMP'),
    ('Complementary metal-oxide semiconductor', 'CMOS'),
]
for phrase, expected in cases:
    result = abbreviate(phrase)
    status = '✓' if result == expected else f'✗ (expected {expected})'
    print(f'{status}  {phrase!r} → {result}')
"
)]
  ✓  'Portable Network Graphics' → PNG
  ✓  'Liquid-crystal display' → LCD
  ✓  'The Road _Not_ Taken' → TRNT
  ✓  "Halley's Comet" → HC
  ✓  'Something - with a dash' → SWAD
  ✓  'GNU Image Manipulation Program' → GIMP
  ✓  'Complementary metal-oxide semiconductor' → CMOS

Tutor: All green. Here's the final solution:

```python
import re

def abbreviate(words):
    return ''.join(w[0] for w in re.findall(r"[a-zA-Z][a-zA-Z']*", words)).upper()
```

The key insight you landed on: rather than *splitting* on separators and taking whatever character comes next, *find the things you actually want* (letter-led tokens). It's a useful instinct — regex `findall` is often cleaner than `split` when the "good" parts are easier to describe than the "bad" separators.

### Student

Perfect! That all makes sense. I appreciate how the solution evolved:

1. We started with the basic approach of splitting on separators, which seemed straightforward but had the edge case with leading punctuation.
2. Switching to `findall` to directly capture letter sequences was much more robust.
3. Then handling contractions by allowing apostrophes within words while still requiring a leading letter.

The final pattern `[a-zA-Z][a-zA-Z']*` is clean and handles all the test cases — including the tricky ones like `"Halley's Comet"` and `"The Road _Not_ Taken"`.

And yeah, that's a good lesson: when you have natural "good" parts to match, describing those directly with `findall` is often simpler and more reliable than trying to split on all the possible separators. Thanks for walking through this!

<done/>

---

**Run end:** done after 4 turn(s) in 123.5s
