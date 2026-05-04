# exercism-acronym

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T03:51:40.399Z

---

## Turn 1

**User:**

Exercism 'Acronym': given a phrase, return its acronym in uppercase. Treat hyphens as word separators; ignore other punctuation. e.g. 'Portable Network Graphics' → 'PNG'.

**Pair:**

Thinking: The user wants to solve the Exercism 'Acronym' problem. Let me think about the approach:
  
  - Split on spaces and hyphens
  - Take the first letter of each word
  - Uppercase all letters
  - Ignore other punctuation
  
  Let me start by proposing the core approach for splitting/parsing, as that's the interesting design decision here.
  
  The key question is: how do we handle the word splitting? We could:
  1. Use `re.split(r'[\s\-]+', phrase)` to split on whitespace and hyphens
  2. Use `re.findall(r"[a-zA-Z']+", phrase)` to find word-like tokens, then take first letters
  
  
  I'm weighing two regex approaches: splitting on whitespace and hyphens versus finding all letter sequences. The split method would capture words cleanly but needs filtering for empty strings, while findall naturally extracts just the words we care about and automatically handles hyphens as word separators.
  
  The tricky case is contractions like "it's" - findall with just letters would split this into "it" and "s" as separate matches, which would incorrectly give us two initials instead of one. I should check what the actual test cases expect, since the problem might not even include contractions, but if it does, I'd need to handle them specially. I'm comparing two regex approaches for extracting acronyms: splitting on whitespace and hyphens versus finding all letter sequences. The split method handles contractions correctly—"Halley's Comet" becomes "HC"—while the findall approach incorrectly splits on the apostrophe to produce "HSC". This is a good teaching moment to show why the split approach is superior, and I'll present both options as a pairing question before implementing the solution in Python.

Assistant: Nice and clean problem. The core design question is how we extract the "first letters" — let me ask before we write a line.

OPTIONS:
[A] findall words
```diff
+++ acronym.py
@@ -0,0 +1,4 @@
+import re
+
+def abbreviate(words):
+    return ''.join(m[0].upper() for m in re.findall(r'[a-zA-Z]+', words))
```

[B] split on separators
```diff
+++ acronym.py
@@ -0,0 +1,4 @@
+import re
+
+def abbreviate(words):
+    return ''.join(w[0].upper() for w in re.split(r'[\s\-]+', words) if w)
```

(Reply with A or B, or ask a follow-up question.)

Thinking: The tool isn't available directly. Let me try searching for it.

Thinking: The tool isn't available. Let me just present the options as text then.
  
  Actually, I'll just present the options as text, since the mcp tool isn't available. Let me do it inline.
  
  The core design question is: split on separators vs. findall letter sequences. I'll explain both approaches and ask the user to pick.

Assistant: The tool isn't loading, so I'll present the options directly.

**Two approaches to extracting first letters:**

---

**Option A — `re.findall`**
```python
import re
def abbreviate(words):
    return ''.join(m[0].upper() for m in re.findall(r'[a-zA-Z]+', words))
```

**Option B — `re.split` on separators**
```python
import re
def abbreviate(words):
    return ''.join(w[0].upper() for w in re.split(r'[\s\-]+', words) if w)
```

---

Which would you go with, and why?

---

## Turn 2

**User:**

I think I'd go with **Option B**.

Here's my reasoning: the problem says to treat hyphens as word separators but ignore *other* punctuation. So if we have something like "Halley's Comet", Option A would find `['Halley', 's', 'Comet']` and give us "HSC" — that's wrong because the apostrophe shouldn't split a word.

Option B splits only on spaces and hyphens, so "Halley's Comet" stays as `["Halley's", "Comet"]`, and we take the first letter of each: "HC". That respects the punctuation rules correctly.

The `if w` filter is also smart — it handles edge cases like double spaces or trailing hyphens that might leave empty strings in the split result.

Should I write out a test case first to make sure I'm thinking about this right, or go ahead and implement B?

**Pair:**

Thinking: The user picked my preferred option (B) and gave excellent reasoning. They even caught the `if w` detail. I should affirm their choice, maybe add a small note, and then help them implement it. They're asking whether to write tests first or implement directly - I'll let them decide but lean toward implementing since Exercism usually provides tests. Let me check if there's already an acronym.py file.

Assistant: Exactly right — you caught the key failure mode and the reason for `if w`. Good instincts.

Exercism ships its own test suite, so you don't need to hand-write cases unless you want to think through edge cases first. I'd just implement and run the tests — they'll surface anything surprising. Let me write the file:

[Glob(acronym.py)]
  No files found

[Write(acronym.py)]
import re


def abbreviate(words):
    return ''.join(w[0].upper() for w in re.split(r'[\s\-]+', words) if w)


Assistant: Done. Run it with:

```
pytest acronym_test.py
```

One thing worth knowing: `\-` inside a character class is fine, but conventionally you'd write the hyphen at the start or end (`[-\s]` or `[\s-]`) to make it unambiguously literal rather than a range marker. Both work here since `\-` is an escaped hyphen, but it's a habit worth forming for readability.

Let me know what the test output looks like.

---

## Turn 3

**User:**

Got it, thanks for the tip on hyphen placement — I'll remember that convention.

Let me run the tests:

```
pytest acronym_test.py
```

Nice! All tests pass. Let me spot-check a couple of the cases that were probably in there:

- `'Portable Network Graphics'` → splits on space → `['Portable', 'Network', 'Graphics']` → takes first letters, uppers them → `'PNG'` ✓
- `'First-class functions'` → splits on hyphen and space → `['First', 'class', 'functions']` → `'FCF'` ✓
- `'Halley\'s Comet'` → splits only on space → `['Halley\'s', 'Comet']` → `'HC'` ✓ (the apostrophe stays inside the word, so we don't split on it)

That last one is exactly what we talked about — if we'd used Option A, we'd have gotten 'HSC' by mistake. The test suite definitely caught that.

Is there anything else to think about with this solution, or are we done?

**Pair:**

Thinking: The user has passed all tests and understands the solution well. They're asking if there's anything else to think about. Let me think about potential edge cases or improvements:
  
  1. The solution is clean and correct.
  2. One thing worth mentioning: what about words that start with numbers? Like "MP3 player" - probably not tested but worth thinking about.
  3. What about the `re.split` behavior with a leading separator? e.g., `" PNG"` - would give `['', 'PNG']` - the `if w` handles this.
  4. Performance: for this problem, completely irrelevant.
  5. The solution is already quite idiomatic Python.
  
  
  6. I think we're genuinely done here - the solution is clean, correct, and passes all tests. I could mention edge cases with numbers or the `re.compile` pattern, but that feels like padding. I'll wrap this up with a brief confirmation and maybe one small observation worth noting.

Assistant: You're done — the solution is clean and correct.

One small thing worth filing away: `re.split` on a pattern that matches at the *start* of the string produces a leading empty string (e.g. `re.split(r'[\s-]+', ' PNG')` → `['', 'PNG']`). Your `if w` guard already handles that, which is exactly why it's there. It's a subtle but common `re.split` gotcha.

Nothing else to change here. Solid work.

---

## Turn 4 (final)

**User:**

Thanks for that — I'll remember that about `re.split`. Good to know the `if w` is doing double duty: filtering out empty strings *and* handling the leading-separator edge case. That's the kind of detail that bites you later if you don't understand it.

I feel confident with this solution now. Acronym is solved.

<done/>

---

**Run end**: done after 3 turns (75s)
