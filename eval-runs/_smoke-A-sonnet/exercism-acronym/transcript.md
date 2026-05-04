# exercism-acronym

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T02:29:20.981Z

---

## Turn 1

**User:**

Exercism 'Acronym': given a phrase, return its acronym in uppercase. Treat hyphens as word separators; ignore other punctuation. e.g. 'Portable Network Graphics' → 'PNG'.

**Pair:**

Thinking: The user wants to solve the Exercism 'Acronym' problem. Let me think about this and then propose options for the implementation approach.
  
  The task:
  - Given a phrase, return its acronym in uppercase
  - Treat hyphens as word separators
  - Ignore other punctuation
  - Example: 'Portable Network Graphics' → 'PNG'
  
  Let me think about the core implementation. The key decisions are:
  1. What language to use (user hasn't specified - I'll assume Python)
  2. How to split words (treating hyphens as separators along with spaces)
  
  
  3. How to handle punctuation
  
  I'm weighing two main approaches: splitting on whitespace and hyphens to get word boundaries, then taking the first letter of each word, versus using a regex to find sequences of letters. The first approach is cleaner for handling apostrophes within words like "GNU's" where the apostrophe shouldn't break the word.
  
  I'm settling on a function that splits on whitespace and hyphens, filters out empty strings, and takes the uppercase first letter of each resulting word. This naturally handles punctuation attached to words since we're only grabbing the first character anyway.
  
  Still exploring alternatives... The regex approach with `\b\w` is looking pretty solid—it catches the first character after word boundaries, which handles spaces, hyphens, and apostrophes correctly across all the test cases. Now I'm wondering if the split-based approach would be simpler or if this regex is already the cleanest solution. Let me think of a good teaching moment here. I'll present two approaches: using `re.findall(r'\b\w', phrase)` to directly capture word characters after boundaries, versus splitting on whitespace and hyphens then taking the first character. The split method has a subtle flaw—punctuation attached to words like "(GNU)" wouldn't be stripped, so you'd get '(' instead of 'G'. The regex approach handles this more elegantly by finding actual word characters at word boundaries. I'll go with the findall method as my primary suggestion since it's cleaner and more robust. A) and split second (as B). Wait no, I should randomize - let me put split as A and findall as B.
  
  Actually the instructions say to present in random order so user can't predict which is best. Let me put findall as A and split as B - so best_index = 0.
  
  Let me verify the split approach against typical Exercism test cases. "Liquid-crystal display" gives LCD, "Something - TBD" filters out empty strings to get ST, and "HyperText Markup Language" gives HML - all correct. For "Halley's Comet" both approaches extract HC properly. The split method works fine for standard cases, but the word boundary approach with `\b\w` is more idiomatic and handles edge cases better - like when punctuation precedes a word character, the word boundary regex correctly identifies the actual letter start while split might grab the punctuation itself. I'm writing out the solution with both approaches side by side, setting the findall method as the better option since it handles edge cases more gracefully.

Assistant: Before writing any code, let me ask about the core extraction strategy:

OPTIONS:
[A] Split then index
```diff
+++ acronym.py
@@ -0,0 +1,5 @@
+import re
+
+def abbreviate(words):
+    parts = re.split(r'[\s-]+', words)
+    return ''.join(p[0].upper() for p in parts if p)
```

[B] Find word-starts
```diff
+++ acronym.py
@@ -0,0 +1,4 @@
+import re
+
+def abbreviate(words):
+    return ''.join(re.findall(r'(?<![\w])\w', words)).upper()
```
Uses a lookbehind to find the first letter of every word, including after hyphens.

(Reply with A or B, or ask a follow-up question.)

Thinking: The tool isn't available. Let me just implement the solution directly.
  
  I'll go with the `re.findall(r'\b\w', phrase)` approach as it's the most robust. Let me first check if there's an existing file.

Assistant: Let me check for an existing file first, then I'll propose the two approaches inline.

[Glob(acronym.py)]
  No files found

Assistant: Two ways to pull out the first letter of each word:

**A — split then index**
```python
parts = re.split(r'[\s-]+', words)
return ''.join(p[0].upper() for p in parts if p)
```

**B — find word-starts directly**
```python
return ''.join(re.findall(r'\b\w', words)).upper()
```

Worth thinking about: what does each do with input like `"(Portable) Network Graphics"`? Which handles leading punctuation on a word better?

I'd go with **B** — `\b\w` matches the first word-character after any word boundary (space, hyphen, `(`, etc.), so it never accidentally picks up a punctuation char as the "first letter". The split approach can grab `(` as `p[0]` if punctuation is attached to the front of a token.

Shall I go with B?

---

## Turn 2

**User:**

Yeah, B makes sense. I can see how `\b\w` directly grabs the first *letter* at each word boundary, whereas splitting might leave punctuation stuck to the front of a part. Even if the test cases don't explicitly check `"(Portable) Network Graphics"`, it's cleaner to handle that right.

Let me go with **B** — write it out and test it against the examples.

**Pair:**

Thinking: The user wants to go with option B. Let me write the file and then test it.

[Write(acronym.py)]
import re


def abbreviate(words):
    return ''.join(re.findall(r'\b\w', words)).upper()


[Bash(python3 -c "
from acronym import abbreviate

cases = [
    ('Portable Network Graphics', 'PNG'),
    ('Ruby on Rails', 'ROR'),
    ('First In First Out', 'FIFO'),
    ('GNU Image Manipulation Program', 'GIMP'),
    ('Liquid-crystal display', 'LCD'),
    ('Something - TBD', 'STBD'),
    (\"GNU's Not Unix\", 'GNU'),
]

for phrase, expected in cases:
    got = abbreviate(phrase)
    status = '✓' if got == expected else f'✗ (got {got})'
    print(f'{status}  {phrase!r} → {got}')
"
)]
  ✓  'Portable Network Graphics' → PNG
  ✓  'Ruby on Rails' → ROR
  ✓  'First In First Out' → FIFO
  ✓  'GNU Image Manipulation Program' → GIMP
  ✓  'Liquid-crystal display' → LCD
  ✗ (got ST)  'Something - TBD' → ST
  ✗ (got GSNU)  "GNU's Not Unix" → GSNU

Thinking: Two failures:
  1. `'Something - TBD'` → got `ST` instead of `STBD`. Wait, `STBD`? Actually "Something - TBD" should be "STB"... wait. "Something", "-", "TBD". The expected should be `STB`... hmm. Actually let me reconsider. 
  
  Wait, "Something - TBD" - I put the expected as 'STBD' but T-B-D are separate letters? No wait, "TBD" is a single word, so the acronym should be S (Something) + T (TBD) = "ST". So my expected value was wrong! Let me reconsider.
  
  
  Actually, I see the issue now—my expected value was incorrect. The words are "Something" and "TBD", giving first letters S and T, which correctly produces "ST".
  
  2. `"GNU's Not Unix"` → got `GSNU` instead of `GNU`. The apostrophe in "GNU's" breaks the word boundary, so the regex picks up `G`, then `s` (after the apostrophe creates a word boundary), then `N`, then `U`. This is a real edge case where contractions get split incorrectly.
  
  The Exercism test expects "GNU" (G from GNU's, N from Not, U from Unix), so I need to handle apostrophes differently. I could normalize the input first by replacing hyphens with spaces and stripping out punctuation while preserving apostrophes within words, then extract the first letter of each space-separated word. Alternatively, I could use a negative lookbehind that excludes both letters and apostrophes to prevent matching letters that follow apostrophes. Removing apostrophes and other non-alphanumeric characters through preprocessing would let me use the simpler `\b\w` pattern reliably. I'm defining a function that strips out everything except letters, spaces, and hyphens, then extracts the first letter of each word and converts it to uppercase. and T → "ST"). But wait, maybe underscores count as word boundaries too? Let me think about what makes sense for an acronym generator—typically you'd want the first letter of each word, where words are separated by spaces, hyphens, or underscores. The real issue is that the apostrophe creates a word boundary where `\b` matches, splitting "GNU's" incorrectly. I can fix this by stripping out non-alphabetic characters (except spaces and hyphens) before applying the regex, which ensures the apostrophe doesn't interfere with word boundary detection.
  
  Actually, there's a cleaner single-step regex that matches letters following either the string start, a space, or a hyphen, with optional punctuation in between. This naturally handles cases like "GNU's Not Unix" by only capturing the G, N, and U—the 's' gets skipped because there's no space or hyphen before it.
  
  I'll explain why the word boundary approach fails with apostrophes and then present this regex solution as the fix.

Assistant: Two issues to unpack:

1. `'Something - TBD'` → `"ST"` is actually **correct** — "TBD" is one word, so only `T` is taken. My expected value was wrong.

2. `"GNU's Not Unix"` → `"GSNU"` is a real bug. The apostrophe in `GNU's` is not a `\w` character, so `\b` fires *between* `'` and `s`, treating the `s` as a new word-start.

The fix: strip everything that isn't a letter, space, or hyphen *before* running `findall`, so apostrophes (and similar punctuation) disappear and no false boundaries appear:

[Read(acronym.py)]
  1	import re
  2	
  3	
  4	def abbreviate(words):
  5	    return ''.join(re.findall(r'\b\w', words)).upper()
  6

[Edit(acronym.py)]
--- before
def abbreviate(words):
    return ''.join(re.findall(r'\b\w', words)).upper()
--- after
def abbreviate(words):
    cleaned = re.sub(r"[^a-zA-Z\s-]", "", words)
    return ''.join(re.findall(r'\b\w', cleaned)).upper()

[Bash(python3 -c "
from acronym import abbreviate

cases = [
    ('Portable Network Graphics', 'PNG'),
    ('Ruby on Rails', 'ROR'),
    ('First In First Out', 'FIFO'),
    ('GNU Image Manipulation Program', 'GIMP'),
    ('Liquid-crystal display', 'LCD'),
    ('Something - TBD', 'ST'),
    (\"GNU's Not Unix\", 'GNU'),
    ('(Portable) Network Graphics', 'PNG'),
]

for phrase, expected in cases:
    got = abbreviate(phrase)
    status = '✓' if got == expected else f'✗ (got {got})'
    print(f'{status}  {phrase!r} → {got}')
"
)]
  ✓  'Portable Network Graphics' → PNG
  ✓  'Ruby on Rails' → ROR
  ✓  'First In First Out' → FIFO
  ✓  'GNU Image Manipulation Program' → GIMP
  ✓  'Liquid-crystal display' → LCD
  ✓  'Something - TBD' → ST
  ✓  "GNU's Not Unix" → GNU
  ✓  '(Portable) Network Graphics' → PNG

Assistant: All green. Final solution:

```python
import re

def abbreviate(words):
    cleaned = re.sub(r"[^a-zA-Z\s-]", "", words)
    return ''.join(re.findall(r'\b\w', cleaned)).upper()
```

The key insight: `\b` is purely structural — it fires at *any* transition between `\w` and `\W`, regardless of meaning. Apostrophes are `\W`, so they silently create a boundary mid-word. The `re.sub` pre-pass removes that ambiguity by erasing everything that isn't a letter, space, or hyphen before the pattern ever runs.

---

## Turn 3 (final)

**User:**

Perfect — that makes sense. I was misunderstanding how `\b` works. It's not "smart" about meaning; it just fires at any transition between word and non-word characters, so an apostrophe immediately creates a boundary. Stripping out the punctuation upfront is elegant because it removes the trap entirely.

The solution handles all the cases now, including the contractions and punctuation edge cases. Thanks for walking me through the regex pitfall and the cleanup step — that's a useful pattern to remember.

<done/>

---

**Run end**: done after 2 turns (144s)
