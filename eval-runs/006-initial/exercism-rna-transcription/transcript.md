# exercism-rna-transcription

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T02:52:38.147Z

---

## Turn 1

**User:**

Exercism 'RNA Transcription': convert a DNA strand to its RNA complement. G→C, C→G, T→A, A→U. Validate input characters.

**Pair:**

Thinking: The user wants to solve the Exercism "RNA Transcription" problem. Let me start by checking if there's already a file for this exercise, then present a foundational decision to kick things off.
  
  Let me check the current directory first.

[Bash(ls)]
  (Bash completed with no output)

Assistant: Empty directory — let's start fresh. First decision: how should we handle invalid input characters?

OPTIONS:
[A] Raise ValueError
```diff
+++ rna_transcription.py
@@ -0,0 +1,7 @@
+def to_rna(dna_strand):
+    mapping = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}
+    result = []
+    for nucleotide in dna_strand:
+        if nucleotide not in mapping:
+            raise ValueError(f"Invalid nucleotide: {nucleotide}")
+        result.append(mapping[nucleotide])
+    return ''.join(result)
```

[B] Return None on bad input
```diff
+++ rna_transcription.py
@@ -0,0 +1,7 @@
+def to_rna(dna_strand):
+    mapping = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}
+    result = []
+    for nucleotide in dna_strand:
+        if nucleotide not in mapping:
+            return None
+        result.append(mapping[nucleotide])
+    return ''.join(result)
```

(Reply with A or B, or ask a follow-up question.)

Assistant: Which do you prefer — **A** or **B**?

---

## Turn 2

**User:**

I'll go with **A** — raising ValueError.

That matches what Exercism expects, and it's more Pythonic overall. When something is invalid, raising an exception is the standard way to signal the error rather than returning None, which would be ambiguous (the caller can't easily tell if None means "error happened" or "None was the actual result").

Let's apply A and move forward.

**Pair:**

Thinking: The user picked option A (raising ValueError), which is my preferred option. Let me write the file and then move to the next decision - maybe about using a more Pythonic approach like a dict comprehension or `str.translate`.

Assistant: Exactly right — `None` as a sentinel conflates "no result" with "invalid input", which is a common source of subtle bugs.

[Write(rna_transcription.py)]
def to_rna(dna_strand):
    mapping = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}
    result = []
    for nucleotide in dna_strand:
        if nucleotide not in mapping:
            raise ValueError(f"Invalid nucleotide: {nucleotide}")
        result.append(mapping[nucleotide])
    return ''.join(result)


Assistant: Now — the loop-and-append works, but Python has a more expressive way to build this. How would you rewrite the body?

OPTIONS:
[A] str.translate
```diff
+++ rna_transcription.py
@@ -1,7 +1,5 @@
 def to_rna(dna_strand):
-    mapping = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}
-    result = []
-    for nucleotide in dna_strand:
-        if nucleotide not in mapping:
-            raise ValueError(f"Invalid nucleotide: {nucleotide}")
-        result.append(mapping[nucleotide])
-    return ''.join(result)
+    if invalid := set(dna_strand) - set('GCTA'):
+        raise ValueError(f"Invalid nucleotide(s): {invalid}")
+    return dna_strand.translate(str.maketrans('GCTA', 'CGAU'))
```

[B] List comprehension + join
```diff
+++ rna_transcription.py
@@ -1,7 +1,5 @@
 def to_rna(dna_strand):
-    mapping = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}
-    result = []
-    for nucleotide in dna_strand:
-        if nucleotide not in mapping:
-            raise ValueError(f"Invalid nucleotide: {nucleotide}")
-        result.append(mapping[nucleotide])
-    return ''.join(result)
+    mapping = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}
+    if any(n not in mapping for n in dna_strand):
+        raise ValueError("Invalid nucleotide in strand")
+    return ''.join(mapping[n] for n in dna_strand)
```

(Reply with A or B, or ask a follow-up question.)

Assistant: **A** or **B**?

---

## Turn 3

**User:**

I'll choose **B** — list comprehension.

Option A is clever with the set difference and `str.translate()`, but it requires knowing the `str.maketrans()` API, and the walrus operator might be overkill here. Option B keeps the mapping visible and readable, which is better for learning. Yes, it iterates twice (once to check, once to build), but that's a small price for clarity — especially on an Exercism problem where understanding the logic matters more than micro-optimizing.

Let's apply B.

**Pair:**

Thinking: The user picked option B (list comprehension + join), which is my preferred option. Let me apply the edit and then we're basically done with this exercise.

Assistant: Well reasoned — double-iteration over a DNA strand is never going to matter, and keeping the `mapping` dict visible makes the logic self-documenting.

[Read(rna_transcription.py)]
  1	def to_rna(dna_strand):
  2	    mapping = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}
  3	    result = []
  4	    for nucleotide in dna_strand:
  5	        if nucleotide not in mapping:
  6	            raise ValueError(f"Invalid nucleotide: {nucleotide}")
  7	        result.append(mapping[nucleotide])
  8	    return ''.join(result)
  9

[Edit(rna_transcription.py)]
--- before
def to_rna(dna_strand):
    mapping = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}
    result = []
    for nucleotide in dna_strand:
        if nucleotide not in mapping:
            raise ValueError(f"Invalid nucleotide: {nucleotide}")
        result.append(mapping[nucleotide])
    return ''.join(result)
--- after
def to_rna(dna_strand):
    mapping = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}
    if any(n not in mapping for n in dna_strand):
        raise ValueError("Invalid nucleotide in strand")
    return ''.join(mapping[n] for n in dna_strand)

Assistant: Here's the final result:

```python
def to_rna(dna_strand):
    mapping = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}
    if any(n not in mapping for n in dna_strand):
        raise ValueError("Invalid nucleotide in strand")
    return ''.join(mapping[n] for n in dna_strand)
```

Clean and done. One small note: `any(... for n in dna_strand)` uses a **generator expression** (not a list comprehension) — it short-circuits on the first invalid character rather than scanning the whole strand. Worth knowing the difference: `[...]` always builds the full list; `(...)` inside `any`/`all`/`sum` is lazy and stops early.

---

## Turn 4 (final)

**User:**

Got it — that's a really useful distinction. Using a generator expression in `any()` means we bail out as soon as we hit an invalid character, which is more efficient than building a full list. Makes sense.

The solution looks solid. We've got:
- Correct transcription mapping
- Proper error handling that raises `ValueError` on invalid input
- Clean, readable code using idiomatic Python patterns

Thanks for walking through those choices with me!

<done/>

---

**Run end**: done after 3 turns (62s)
