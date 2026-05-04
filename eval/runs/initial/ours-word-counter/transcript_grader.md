# ours-word-counter

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:04:35

## Initial prompt

Let's write a Python function that takes a block of text and returns a dictionary mapping each word (lowercased) to its frequency. Strip punctuation.

---

## Turn 1

### Tutor

Tutor: Good task for a clean teaching moment. Before I write anything, quick question on the counting approach:

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Use collections.Counter
```diff
+++ word_freq.py
@@ -0,0 +1,7 @@
+import re
+from collections import Counter
+
+def word_frequency(text):
+    words = re.findall(r'[a-z]+', text.lower())
+    return dict(Counter(words))
```

[B] Manual dict accumulation
```diff
+++ word_freq.py
@@ -0,0 +1,8 @@
+import re
+
+def word_frequency(text):
+    words = re.findall(r'[a-z]+', text.lower())
+    freq = {}
+    for word in words:
+        freq[word] = freq.get(word, 0) + 1
+    return freq
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach do you prefer?

### Student

I think I'll go with **B** — the manual dict accumulation approach.

I want to understand how the counting actually works rather than just delegating it to Counter. Plus, the `freq.get(word, 0) + 1` pattern feels like something I should be comfortable with. It'll help me see exactly what's happening at each step.

---

## Turn 2

### Tutor

Tutor: Totally fair — `dict.get(key, default)` is a pattern that shows up constantly in Python, worth having in muscle memory.

One thing worth knowing: `Counter` isn't magic — it's essentially this same loop under the hood, just wrapped up. And if you later need "top 10 words", `Counter.most_common(10)` saves you a sort. But starting from first principles is a solid call.

Let me write the file:

[Write(word_freq.py)]
import re


def word_frequency(text):
    words = re.findall(r'[a-z]+', text.lower())
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq

  File created successfully at: word_freq.py

Tutor: A couple of notes on what's already here:

- **`re.findall(r'[a-z]+')`** extracts runs of letters only — punctuation and digits are simply never captured. This means `"don't"` → `["don", "t"]` and `"hello-world"` → `["hello", "world"]`. A simpler `str.translate` + `split` approach would instead fuse `"hello-world"` into `"helloworld"`, which is worse.
- **`freq.get(word, 0) + 1`** — on the first sight of a word, `.get` returns `0`, so you store `1`. On every subsequent hit you increment. No `if key in dict` check needed.

Want to add a quick `if __name__ == "__main__"` smoke test, or move on to something like handling edge cases (empty string, numbers, mixed unicode)?

### Student

Let me add a quick smoke test first — I want to see it actually work before we think about edge cases.

```python
if __name__ == "__main__":
    text = "Hello, world! Hello everyone."
    result = word_frequency(text)
    print(result)
```

What should I expect to see when I run this?

---

## Turn 3

### Tutor

Tutor: You'll get:

```
{'hello': 2, 'world': 1, 'everyone': 1}
```

Tracing through: `"Hello, world! Hello everyone."` → lowercased → regex pulls out `["hello", "world", "hello", "everyone"]` (commas, `!`, `.` are never captured) → loop counts them up.

Let me add the test block:

[Edit(word_freq.py)]
--- before
import re


def word_frequency(text):
    words = re.findall(r'[a-z]+', text.lower())
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq
--- after
import re


def word_frequency(text):
    words = re.findall(r'[a-z]+', text.lower())
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq


if __name__ == "__main__":
    text = "Hello, world! Hello everyone."
    result = word_frequency(text)
    print(result)
  The file word_freq.py has been updated successfully.

[Bash(python word_freq.py)]
  {'hello': 2, 'world': 1, 'everyone': 1}

Tutor: Exactly as predicted. Works correctly.

Ready to think about edge cases? The interesting ones are: empty string, text that's *all* punctuation/numbers, and unicode (e.g. `"café"`). Want to tackle those next?

### Student

Actually, I think we're good for now. The function works as specified — it takes a block of text, lowercases it, strips punctuation, and counts word frequencies. The smoke test confirms it's doing exactly what we asked.

Edge cases are interesting, but they're a separate problem. For the one I was given, this solution is solid.

<done/>

---

**Run end:** done after 3 turn(s) in 60.2s
