# exercism-acronym

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T04:19:01.623Z

---

## Turn 1

**User:**

Exercism 'Acronym': given a phrase, return its acronym in uppercase. Treat hyphens as word separators; ignore other punctuation. e.g. 'Portable Network Graphics' → 'PNG'.

**Pair:**

Thinking: The user wants to solve the Exercism 'Acronym' problem. Let me start by thinking about the approach.
  
  The task is:
  - Given a phrase, return its acronym in uppercase
  - Treat hyphens as word separators
  - Ignore other punctuation
  - e.g. 'Portable Network Graphics' → 'PNG'
  
  Let me think about how to approach this. The key decisions are:
  1. What language to use (the user didn't specify - I'll assume Python)
  2. How to split the words - this is the interesting design question
  
  The core approach:
  - Split on spaces and hyphens
  
  
  - Take the first letter of each word
  - Uppercase them
  - Join
  
  For splitting, I could use regex to handle spaces and hyphens together, or normalize hyphens to spaces first and then split. The regex approach is more explicit, but chaining string operations is simpler. The trickier part is handling punctuation within words—I need to think about whether to strip punctuation from each word or just take the first character as-is.
  
  Looking at typical test cases, words like "Halley's" should still contribute their first letter "H", and underscores or dashes between words shouldn't create empty entries. So after splitting on spaces and hyphens, I need to find the first actual letter in each word, not just grab the first character, since some words might start with punctuation.
  
  The straightforward approach is to split on whitespace and hyphens using regex, then take the first character of each non-empty word and uppercase it. This handles most cases cleanly, though the real subtlety is whether to use regex splitting or normalize the string first—both work, but they handle edge cases like consecutive spaces slightly differently.
  
  The more interesting teaching angle is how to extract the actual first *letter* from each word, since simple indexing like `word[0]` fails when words are prefixed with punctuation like apostrophes or underscores. That's where you'd need to either filter for alphabetic characters or use pattern matching to find the first letter, which is a more nuanced problem than the initial split. I need to reconsider the approach here. The key insight is splitting on whitespace and hyphens, then taking the first letter from each resulting token. When I split "Something - with - dashes" on those delimiters, I get the right tokens and can uppercase the first character of each, but I need to handle edge cases like punctuation or empty strings. I'm weighing two main strategies: using `re.split()` to break the phrase apart and filter for valid words, or using `re.findall()` with a word boundary pattern to grab initial letters directly.
  
  Testing the regex approach with word boundaries...
  
  Actually, I'm realizing the `\b` method has a real problem with contractions—something like "Halley's Comet" would incorrectly treat the apostrophe as a word boundary and grab the 's', giving "HSC" instead of "HC". That's a subtle but important bug that makes it a good teaching moment.
  
  The cleaner approach is splitting on whitespace and hyphens, then taking the first letter of each resulting word. Let me verify how that handles edge cases like multiple consecutive dashes. I've already laid out the two regex approaches, so now I'm moving forward with writing the actual solution. I'll create the Python file and use the tool to present both splitting strategies as design options.

Assistant: Classic string-processing puzzle. The interesting design question is in *how* you extract the first letters — let me show you two approaches before writing any code.

OPTIONS:
[A] Split then index
```diff
+++ acronym.py
@@ -0,0 +1,5 @@
+import re
+
+def abbreviate(phrase):
+    words = re.split(r'[\s-]+', phrase)
+    return ''.join(w[0] for w in words if w).upper()
```

[B] Findall word-boundary
```diff
+++ acronym.py
@@ -0,0 +1,4 @@
+import re
+
+def abbreviate(phrase):
+    return ''.join(re.findall(r'\b[a-zA-Z]', phrase)).upper()
```

(Reply with A or B, or ask a follow-up question.)

Thinking: The tool isn't available. Let me just present the options as text and ask the user to choose.

Assistant: Let me present two approaches — which do you think handles all edge cases correctly?

**Option A — Split then index:**
```python
import re

def abbreviate(phrase):
    words = re.split(r'[\s-]+', phrase)
    return ''.join(w[0] for w in words if w).upper()
```

**Option B — `\b` word-boundary findall:**
```python
import re

def abbreviate(phrase):
    return ''.join(re.findall(r'\b[a-zA-Z]', phrase)).upper()
```

Both look clean. Which would you pick, and why?

---

## Turn 2

**User:**

I'm leaning toward **Option A**, but let me think through a tricky case.

If the input is "Halley's Comet", we'd want "HC", right? 

With Option A:
- `re.split(r'[\s-]+', "Halley's Comet")` → `["Halley's", "Comet"]`
- First chars: `"H"`, `"C"` → `"HC"` ✓

With Option B:
- `re.findall(r'\b[a-zA-Z]', "Halley's Comet")`
- The `\b` matches a word boundary, so it'd match: H (start of Halley's), then... wouldn't the apostrophe create another boundary, making `\b[a-zA-Z]` match the 's' too?
- That'd give `"HSC"` ✗

So Option B would treat contractions wrong. Option A splits on spaces and hyphens only, which feels safer. Should I go with **A**?

**Pair:**

Thinking: The user correctly identified the issue with Option B. They chose Option A, which is my preferred option. I should express brief agreement and apply the changes by creating the file.

Assistant: Exactly right — `'` is a non-word character, so `\b` fires before the `s`, giving the spurious match. You nailed it.

Let me write the file:

[Bash(ls acronym.py 2>/dev/null || echo "not found")]
  not found

[Write(acronym.py)]
import re


def abbreviate(phrase):
    words = re.split(r'[\s-]+', phrase)
    return ''.join(w[0] for w in words if w).upper()


Assistant: Let's verify against the spec cases:

[Bash(python3 -c "
from acronym import abbreviate
cases = [
    ('Portable Network Graphics', 'PNG'),
    ('GNU Image Manipulation Program', 'GIMP'),
    ('Halley\'s Comet', 'HC'),
    ('The Road _Not_ Taken', 'TRNT'),
    ('Something - with - dashes', 'SWD'),
    ('PHP: Hypertext Preprocessor', 'PHP'),
]
for phrase, expected in cases:
    got = abbreviate(phrase)
    status = '✓' if got == expected else f'✗ (got {got})'
    print(f'{status}  {phrase!r} → {got}')
"
)]
  ✓  'Portable Network Graphics' → PNG
  ✓  'GNU Image Manipulation Program' → GIMP
  ✓  "Halley's Comet" → HC
  ✗ (got TR_T)  'The Road _Not_ Taken' → TR_T
  ✓  'Something - with - dashes' → SWD
  ✓  'PHP: Hypertext Preprocessor' → PHP

Thinking: There's a failing case: `'The Road _Not_ Taken'` → `TR_T` but expected `TRNT`. The issue is that `_Not_` gets split into a single token `_Not_`, and then `w[0]` is `_`, not `N`.
  
  So we need to handle the case where a token starts with non-letter characters. We need to take the first *letter* of each word, not the first character.
  
  The fix: instead of `w[0]`, use `re.search(r'[a-zA-Z]', w).group()` or similar to get the first letter.
  
  
  I'm considering whether this is actually a standard Exercism test case or something the user added, but either way the fix is clear—I need to extract the first alphabetic character from each token rather than just the first character, and I'm weighing between a pythonic approach like iterating through characters with `isalpha()` versus using regex. I'm considering a few ways to fix this: either extract the first alphabetic character from each token using a generator expression, strip leading non-letter punctuation before indexing, or use regex to filter tokens that contain letters. I think presenting two clean options would make for a good teaching moment here.

Assistant: One failure: `_Not_` is a token after splitting, and `w[0]` gives `_` instead of `N`. We need the first *letter* of each token, not the first character. Two ways to fix that:

OPTIONS:
[A] next() with isalpha
```diff
+++ acronym.py
@@ -4,2 +4,2 @@
-    return ''.join(w[0] for w in words if w).upper()
+    return ''.join(next(c for c in w if c.isalpha()) for w in words if any(c.isalpha() for c in w)).upper()
```

[B] re.search per token
```diff
+++ acronym.py
@@ -4,2 +4,3 @@
-    return ''.join(w[0] for w in words if w).upper()
+    firsts = (re.search(r'[a-zA-Z]', w) for w in words)
+    return ''.join(m.group() for m in firsts if m).upper()
```

(Reply with A or B, or ask a follow-up question.)

Thinking: The tool is not available. Let me just present the options as text.

Assistant: The tool isn't loading, so I'll present the options directly — which do you prefer?

**Option A — `next()` with `isalpha`:**
```python
return ''.join(next(c for c in w if c.isalpha()) for w in words if any(c.isalpha() for c in w)).upper()
```

**Option B — `re.search` per token:**
```python
firsts = (re.search(r'[a-zA-Z]', w) for w in words)
return ''.join(m.group() for m in firsts if m).upper()
```

Both fix the `_Not_` case. One thing worth noticing: Option A traverses each token *twice* — once for `any()` and once for `next()`. Which would you pick?

---

## Turn 3

**User:**

I'd pick **Option B**. You already pointed out that Option A traverses each token twice — once for `any()` to check if there are letters, then again for `next()` to find the first one. That feels wasteful.

Option B scans each token once with `re.search()`, and since `re.search()` returns either a match object or `None`, the `if m` check is clean. Plus it's easier to read as a sequence of steps:
1. Find the first letter in each token
2. Keep only the non-None results
3. Extract and uppercase

Let me apply that fix.

**Pair:**

Thinking: The user picked Option B, which is my preference. Let me apply the change with Edit.

Assistant: Spot on. Let's apply it:

[Edit(acronym.py)]
--- before
    return ''.join(w[0] for w in words if w).upper()
--- after
    firsts = (re.search(r'[a-zA-Z]', w) for w in words)
    return ''.join(m.group() for m in firsts if m).upper()

[Bash(python3 -c "
from acronym import abbreviate
cases = [
    ('Portable Network Graphics', 'PNG'),
    ('GNU Image Manipulation Program', 'GIMP'),
    (\"Halley's Comet\", 'HC'),
    ('The Road _Not_ Taken', 'TRNT'),
    ('Something - with - dashes', 'SWD'),
    ('PHP: Hypertext Preprocessor', 'PHP'),
]
for phrase, expected in cases:
    got = abbreviate(phrase)
    status = '✓' if got == expected else f'✗ (got {got})'
    print(f'{status}  {phrase!r} → {got}')
"
)]
  ✓  'Portable Network Graphics' → PNG
  ✓  'GNU Image Manipulation Program' → GIMP
  ✓  "Halley's Comet" → HC
  ✓  'The Road _Not_ Taken' → TRNT
  ✓  'Something - with - dashes' → SWD
  ✓  'PHP: Hypertext Preprocessor' → PHP

Assistant: All green. Final solution:

```python
import re

def abbreviate(phrase):
    words = re.split(r'[\s-]+', phrase)
    firsts = (re.search(r'[a-zA-Z]', w) for w in words)
    return ''.join(m.group() for m in firsts if m).upper()
```

The two-step design is worth remembering as a pattern: **split on separators, then extract the meaningful character from each token**. Trying to do both at once (like the `\b` approach) tends to break on edge cases where "word boundary" and "separator" don't perfectly align.

---

## Turn 4 (final)

**User:**

Got it. That pattern makes a lot of sense — separating the concerns of "how do I identify words?" from "how do I extract the key character?" keeps each part simple and testable. I was initially drawn to the fancy one-liner with `\b`, but seeing how it breaks on contractions was a good reminder that regex word boundaries aren't the same as linguistic word separators.

Thanks for walking through this. The solution feels solid now.

<done/>

---

**Run end**: done after 3 turns (160s)
