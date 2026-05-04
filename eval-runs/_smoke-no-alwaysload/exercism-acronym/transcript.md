# exercism-acronym

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T04:53:03.786Z

---

## Turn 1

**User:**

Exercism 'Acronym': given a phrase, return its acronym in uppercase. Treat hyphens as word separators; ignore other punctuation. e.g. 'Portable Network Graphics' → 'PNG'.

**Pair:**

Thinking: The user wants to solve the Exercism 'Acronym' problem. Let me think about this:
  
  - Given a phrase, return its acronym in uppercase
  - Treat hyphens as word separators
  - Ignore other punctuation
  - e.g. 'Portable Network Graphics' → 'PNG'
  
  Let me start by thinking about the approach. I'll use Python. The key decisions:
  1. How to split the words (spaces and hyphens as separators)
  2. How to extract the first letter of each word
  
  Let me think about what makes a good question here. The main implementation decision is how to split/extract the first letters. 
  
  Option A: Use `re.split` to split on spaces and hyphens, then take the first character of each word.
  
  
  Option B: Use `re.findall` to directly find the first letter of each word (after word boundaries that include hyphens).
  
  I'm weighing the regex approaches here. I could split on whitespace and hyphens together, then grab the first letter from each resulting word, filtering out empty strings. Or I could use a pattern that directly captures the first letter of words, treating both spaces and hyphens as word boundaries.
  
  The split approach seems cleaner and more straightforward than trying to get the regex pattern right with word boundaries and hyphens. Let me think about what makes for a good question to ask about this problem.
  
  Looking at typical test cases, I need to handle apostrophes within words like "Halley's Comet" without splitting on them, while still splitting on whitespace and hyphens. The key is splitting on those delimiters specifically, then taking the first letter of each resulting word. I'm weighing the trade-offs between different approaches—splitting on delimiters and extracting the first character versus using `findall` to grab letters directly. The split-and-extract method feels cleaner to me, so I'm sketching out how that would work with a function that joins the uppercase first letters of each word. I'm weighing two approaches for this abbreviation function: splitting on whitespace and hyphens versus using a more complex regex pattern. The split approach feels cleaner and more straightforward—just break the input into words and grab the first letter of each, filtering out empty strings. The findall approach gets messier with edge cases around word boundaries, so I'm leaning toward the simpler solution. I'm leaning toward the pure string approach for its simplicity, though the regex version handles edge cases like consecutive separators and punctuation more robustly. I'll present both options and let them decide based on their preference for readability versus comprehensive edge case handling.
  
  Now I'm testing both approaches against various edge cases—spaces around hyphens, apostrophes in words, and other punctuation—to see where they might diverge in practice. I'm realizing that using `re.findall(r'[A-Za-z]+', ...)` to extract letter sequences is the cleanest solution—it naturally handles hyphens as word separators and strips underscores, so "e-mail" becomes "EM" and "_Not_" becomes just "N".
  
  But apostrophes are tricky: "Halley's Comet" would split into separate words, giving me "HSC" when I really want "HC" since the apostrophe should be treated as part of the word, not a separator. I need a pattern that keeps apostrophes within words while still extracting the first letter of each word unit.
  
  A pattern like `[A-Za-z][A-Za-z']*` would match words starting with a letter and allow apostrophes in the middle, so "Halley's" becomes one token starting with H. Let me test this against some cases: "Halley's" gives H, underscores like "_Not_" give N, and hyphenated words like "e-mail" split into E and M for "EM". This approach seems solid.
  
  Now I'm thinking through the distinction between two regex patterns—one that requires a letter at the start versus one that allows leading apostrophes, which could cause issues with contractions like "'Twas". Though looking at typical Exercism test cases, I'm recalling examples like "Portable Network Graphics" → "PNG" and "Ruby on Rails" → "ROR", which probably don't include those edge cases.
  
  Let me verify the regex approach against some actual test cases: "PHP: Hypertext Preprocessor" should yield "PHP" by extracting words that start with a letter, and "Halley's Comet" should give "HC" by handling the apostrophe within the word correctly. all the test cases correctly. Now I'm comparing two approaches for extracting acronyms: using regex to find words versus splitting on whitespace and hyphens. The first approach with `re.findall` is cleaner because it properly handles apostrophes and strips punctuation, while the split method leaves unwanted characters attached to words. I'm evaluating whether this comparison makes for a good teaching question.
  
  I think it does—the split approach has a subtle flaw with cases like `_Not_` that the findall method handles elegantly. I'll structure this as a foundational decision and present both complete implementations to show the difference clearly.
  
  Writing the implementations...

Assistant: Let me check if you already have a file started:

[Glob(acronym.py)]
  No files found

Assistant: Fresh start. One key decision up front — how to tokenize the phrase. Here are two approaches:

OPTIONS:
[A] Split on delimiters
Treat spaces and hyphens as word separators, take the first character of each resulting token.

[B] Extract words directly
Use findall to pull out letter-sequences (treating apostrophes as intra-word), then take the first letter of each.

(Reply with A or B, or ask a follow-up question.)

Thinking: The tool isn't available. Let me just present both options in text format and ask the user to choose.

Assistant: The pairing tool isn't available right now, so let me just walk through it directly.

There are two natural approaches here — worth thinking about before writing code:

**Option A — Split on delimiters:**
```python
import re
def abbreviate(words):
    return ''.join(w[0].upper() for w in re.split(r'[\s-]+', words) if w)
```

**Option B — Extract words directly:**
```python
import re
def abbreviate(words):
    return ''.join(w[0].upper() for w in re.findall(r"[A-Za-z][A-Za-z']*", words))
```

Before I write it — which would you pick, and why? Consider the Exercism test case `"The Road _Not_ Taken"` → should give `"TRNT"`.

---

## Turn 2

**User:**

Okay, let me think through that test case:

With Option A (split on delimiters):
- `re.split(r'[\s-]+', "The Road _Not_ Taken")` gives me `['The', 'Road', '_Not_', 'Taken']`
- First character of each: `'T'`, `'R'`, `'_'`, `'T'`
- After uppercase: `'T'`, `'R'`, `'_'`, `'T'` → `"TR_T"` ❌

With Option B (extract words directly):
- `re.findall(r"[A-Za-z][A-Za-z']*", "The Road _Not_ Taken")` gives me `['The', 'Road', 'Not', 'Taken']`
- First character of each: `'T'`, `'R'`, `'N'`, `'T'` → `"TRNT"` ✓

Oh! Option A has that subtle bug — it splits but doesn't strip punctuation, so leading underscores get included. Option B avoids that by only matching letter sequences in the first place.

I'd go with **Option B**. It's cleaner because the regex pattern itself enforces "only letters and apostrophes," so punctuation just falls away naturally. Option A requires you to be aware that split doesn't remove punctuation attached to words.

Should I write it out and test it?

**Pair:**

Thinking: The user correctly identified the issue and wants to go with Option B. Let me write the file and then we can test it.

Assistant: Exactly right. The `findall` approach is doing one job — *define what a word is* — rather than two jobs (split, then hope the tokens are clean). Let me write it:

[Write(acronym.py)]
import re


def abbreviate(words):
    return ''.join(w[0].upper() for w in re.findall(r"[A-Za-z][A-Za-z']*", words))


Assistant: Let's run it against the key cases:

[Bash(python3 -c "
from acronym import abbreviate

cases = [
    ('Portable Network Graphics', 'PNG'),
    ('Ruby on Rails', 'ROR'),
    ('HyperText Markup Language', 'HTML'),
    ('Something - Component Software', 'SCS'),
    (\"Halley's Comet\", 'HC'),
    ('The Road _Not_ Taken', 'TRNT'),
    ('PHP: Hypertext Preprocessor', 'PHP'),
    ('Complementary metal-oxide semiconductor', 'CMOS'),
]

for phrase, expected in cases:
    got = abbreviate(phrase)
    status = '✓' if got == expected else f'✗ (got {got!r})'
    print(f'{status}  {phrase!r}')
"
)]
  ✓  'Portable Network Graphics'
  ✓  'Ruby on Rails'
  ✗ (got 'HML')  'HyperText Markup Language'
  ✓  'Something - Component Software'
  ✓  "Halley's Comet"
  ✓  'The Road _Not_ Taken'
  ✓  'PHP: Hypertext Preprocessor'
  ✓  'Complementary metal-oxide semiconductor'

Thinking: Interesting! "HyperText Markup Language" → expected "HTML" but we got "HML". 
  
  The issue is: "HyperText" - the regex `[A-Za-z][A-Za-z']*` matches "HyperText" as one token, so we take only 'H'. But the expected output is "HTML" where both 'H' (from Hyper) and 'T' (from Text) are included.
  
  Wait, actually - "HyperText" is one word. The expected acronym should be "HML" since it's three words: HyperText, Markup, Language. 
  
  But Exercism says "HTML"... So they must want me to split on camelCase boundaries too, treating "HyperText" as two separate words: "Hyper" and "Text". That means I need to detect capital letters mid-word and treat them as word boundaries. expects us to treat each capital letter start as a new word.
  
  So we need to handle CamelCase as well! Each capital letter that starts a new "word" within a token should be treated as a word boundary.
  
  Looking at the standard Exercism test cases, "HyperText Markup Language" should produce "HTML", which means capital letters within words do count as word boundaries. To handle this, I need to split on transitions from lowercase to uppercase letters within a word. I can use a regex substitution to insert spaces before capital letters that follow lowercase letters, then apply the standard word extraction logic.
  
  Modifying the regex approach... our findall approach.
  
  Another approach: use a more sophisticated regex in findall.
  
  Let me think about how to handle this as a teaching moment. The user just correctly identified the issue with Option A, and now we have a new bug to fix. This is a good opportunity to ask another question!
  
  The fix options:
  Option A: Pre-process to split CamelCase, then apply findall
  Option B: Use a more complex single regex
  
  Actually, let me think about this more carefully. The word "HyperText":
  - We want H from "Hyper" and T from "Text"
  - So we need to split "HyperText" into "Hyper" + "Text"
  
  The pre-processing approach would insert a space before capital letters that follow lowercase letters, converting "HyperText" to "Hyper Text", then extract the first letter of each word.
  
  A single-regex approach would be trickier—I'd need to match either the start of a word or a capital letter within a word, which gets complex. The pre-processing method is cleaner and more readable.
  
  Refining the solution... I'm testing the regex pattern mentally against "HyperText" and it correctly identifies 'H' at the start and 'T' where the camelCase boundary occurs. But this is getting complicated—I think the simpler two-step approach of preprocessing camelCase first, then using findall, is cleaner and easier to understand. Before I settle on a solution though, I should check what the actual Exercism test cases expect, particularly whether camelCase handling is even required.
  
  Looking at the test suite, I can see cases like "HyperText Markup Language" → "HTML", which confirms camelCase needs to be handled. So I have two viable approaches: either preprocess the string to insert spaces at camelCase boundaries before running the existing regex, or write a single regex that matches both word starts and camelCase transitions in one pass. I'm testing Option B against "Halley's Comet" and finding an issue—the apostrophe in the negated lookbehind means the `s` after the apostrophe won't match, which breaks the expected output. I'm leaning toward Option A for its clarity and separation of concerns, but let me test an edge case like "PHPHypertext" to see if the two approaches diverge. The regex pattern looks for a lowercase letter followed by an uppercase one, so in this string with consecutive capitals followed by a lowercase letter, it wouldn't actually trigger any substitutions—the boundary I'm looking for just isn't there. Both options produce the same result for 'PHPHypertext' and other test cases, so they're functionally equivalent. I'll go with Option A since it reads more clearly, then frame this as a comparison of stylistic alternatives.

Assistant: Seven pass, one fails. `"HyperText Markup Language"` → expected `"HTML"`, got `"HML"`. Makes sense — our regex sees `"HyperText"` as one token and only grabs `H`.

Exercism expects camelCase boundaries to count as word splits. Two ways to fix it — which do you think is cleaner?

**Option A — Pre-process, then reuse existing logic:**
```python
def abbreviate(words):
    words = re.sub(r'([a-z])([A-Z])', r'\1 \2', words)
    return ''.join(w[0].upper() for w in re.findall(r"[A-Za-z][A-Za-z']*", words))
```

**Option B — One regex that matches both word-starts and camelCase transitions:**
```python
def abbreviate(words):
    return ''.join(m.upper() for m in re.findall(r"(?<![A-Za-z'])[A-Za-z]|(?<=[a-z])[A-Z]", words))
```

Think about readability and how easy each is to modify if requirements change.

---

## Turn 3

**User:**

Option A, definitely. Let me think through why:

**Option A pros:**
- The `([a-z])([A-Z])` rule is immediately obvious — "insert a space before capitals that follow lowercase"
- I can test that regex independently: does it correctly convert `"HyperText"` to `"Hyper Text"`?
- The second step reuses the logic we already understand
- If requirements change (like "also split on underscores"), I just add another substitution line

**Option B cons:**
- That regex is a wall of symbols. `(?<![A-Za-z'])[A-Za-z]|(?<=[a-z])[A-Z]` — I'd need to spend time unpacking it every time I read the code
- If I'm debugging a failed test case, I can't easily test the camelCase part in isolation
- Adding new rules means rewriting the whole regex, not adding a line

It feels like the same lesson we learned earlier — define *what a word is* clearly, rather than encoding all the rules into one complex pattern. Here it's the same idea: normalize the input first (make it clean), then apply simple logic.

Should I apply Option A?

**Pair:**

Thinking: The user correctly identified Option A as the better choice, with good reasoning. Let me apply it.

Assistant: Exactly right — and that principle has a name: **normalize then process**. Transform the input into a canonical form first, then your extraction logic stays simple. It also means the two regex patterns each have one job and can be tested independently.

Applying it:

[Edit(acronym.py)]
--- before
def abbreviate(words):
    return ''.join(w[0].upper() for w in re.findall(r"[A-Za-z][A-Za-z']*", words))
--- after
def abbreviate(words):
    words = re.sub(r'([a-z])([A-Z])', r'\1 \2', words)
    return ''.join(w[0].upper() for w in re.findall(r"[A-Za-z][A-Za-z']*", words))

[Bash(python3 -c "
from acronym import abbreviate

cases = [
    ('Portable Network Graphics', 'PNG'),
    ('Ruby on Rails', 'ROR'),
    ('HyperText Markup Language', 'HTML'),
    ('Something - Component Software', 'SCS'),
    (\"Halley's Comet\", 'HC'),
    ('The Road _Not_ Taken', 'TRNT'),
    ('PHP: Hypertext Preprocessor', 'PHP'),
    ('Complementary metal-oxide semiconductor', 'CMOS'),
]

for phrase, expected in cases:
    got = abbreviate(phrase)
    status = '✓' if got == expected else f'✗ (got {got!r})'
    print(f'{status}  {phrase!r}')
"
)]
  ✓  'Portable Network Graphics'
  ✓  'Ruby on Rails'
  ✓  'HyperText Markup Language'
  ✓  'Something - Component Software'
  ✓  "Halley's Comet"
  ✓  'The Road _Not_ Taken'
  ✓  'PHP: Hypertext Preprocessor'
  ✓  'Complementary metal-oxide semiconductor'

Assistant: All green. Final solution is clean at 3 lines:

```python
import re

def abbreviate(words):
    words = re.sub(r'([a-z])([A-Z])', r'\1 \2', words)
    return ''.join(w[0].upper() for w in re.findall(r"[A-Za-z][A-Za-z']*", words))
```

Two regexes, each with a single responsibility — camelCase splitting is separate from word extraction. That's the whole trick.

---

## Turn 4 (final)

**User:**

Perfect! All tests pass. That's a solid solution.

I really liked how we approached this — we didn't just code blind. We started by thinking about what approach would be *clearer*, caught a subtle bug in the camelCase handling, then chose the simpler of two fixes based on readability and maintainability. That's exactly how I want to think about code decisions going forward.

The key takeaway: **normalize first, then process**. Makes everything downstream simpler and easier to test.

<done/>

---

**Run end**: done after 3 turns (167s)
