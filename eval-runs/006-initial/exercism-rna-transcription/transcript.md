# exercism-rna-transcription

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T02:40:20.662Z

---

## Turn 1

**User:**

Exercism 'RNA Transcription': convert a DNA strand to its RNA complement. G→C, C→G, T→A, A→U. Validate input characters.

**Pair:**

Assistant: I'll go with Python — let me present the first real decision before creating the file.

OPTIONS:
[A] Dict lookup + loop
```diff
+++ rna_transcription.py
@@ -0,0 +1,9 @@
+DNA_TO_RNA = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}
+
+def to_rna(dna_strand):
+    result = []
+    for nucleotide in dna_strand:
+        if nucleotide not in DNA_TO_RNA:
+            raise ValueError(f"Invalid nucleotide: {nucleotide}")
+        result.append(DNA_TO_RNA[nucleotide])
+    return ''.join(result)
```

[B] str.maketrans + translate
```diff
+++ rna_transcription.py
@@ -0,0 +1,5 @@
+_TABLE = str.maketrans('GCTA', 'CGAU')
+
+def to_rna(dna_strand):
+    return dna_strand.translate(_TABLE)
```

(Reply with A or B, or ask a follow-up question.)

---

## Turn 2

**User:**

A

Option B looks neat, but it skips validation — `translate()` silently leaves unrecognized characters alone instead of raising an error. The problem explicitly says to validate input, so A's explicit check is required.

**Pair:**

Assistant: Exactly right. Let me create the file.

[Glob(rna_transcription.py)]
  No files found

[Write(rna_transcription.py)]
DNA_TO_RNA = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}

def to_rna(dna_strand):
    result = []
    for nucleotide in dna_strand:
        if nucleotide not in DNA_TO_RNA:
            raise ValueError(f"Invalid nucleotide: {nucleotide}")
        result.append(DNA_TO_RNA[nucleotide])
    return ''.join(result)


Assistant: Good. Now one more decision — the loop body can be written more compactly. Which would you prefer?

OPTIONS:
[A] get() with sentinel
```diff
+++ rna_transcription.py
@@ -4,6 +4,5 @@
 def to_rna(dna_strand):
-    result = []
-    for nucleotide in dna_strand:
-        if nucleotide not in DNA_TO_RNA:
-            raise ValueError(f"Invalid nucleotide: {nucleotide}")
-        result.append(DNA_TO_RNA[nucleotide])
-    return ''.join(result)
+    try:
+        return ''.join(DNA_TO_RNA[n] for n in dna_strand)
+    except KeyError as e:
+        raise ValueError(f"Invalid nucleotide: {e.args[0]}") from e
```

[B] Comprehension + get()
```diff
+++ rna_transcription.py
@@ -4,6 +4,4 @@
 def to_rna(dna_strand):
-    result = []
-    for nucleotide in dna_strand:
-        if nucleotide not in DNA_TO_RNA:
-            raise ValueError(f"Invalid nucleotide: {nucleotide}")
-        result.append(DNA_TO_RNA[nucleotide])
-    return ''.join(result)
+    return ''.join(
+        DNA_TO_RNA.get(n, n) for n in dna_strand
+    )
```

(Reply with A or B, or ask a follow-up question.)

---

## Turn 3

**User:**

A

Option B's `get(n, n)` fallback silently passes through any unrecognized nucleotide instead of raising an error. That breaks validation again — we'd accept invalid input like 'X' and just return it unchanged. Option A correctly validates by catching the KeyError and converting it to a proper ValueError.

**Pair:**

Assistant: Good catch — same trap, different disguise. Applying it:

[Edit(rna_transcription.py)]
--- before
def to_rna(dna_strand):
    result = []
    for nucleotide in dna_strand:
        if nucleotide not in DNA_TO_RNA:
            raise ValueError(f"Invalid nucleotide: {nucleotide}")
        result.append(DNA_TO_RNA[nucleotide])
    return ''.join(result)
--- after
def to_rna(dna_strand):
    try:
        return ''.join(DNA_TO_RNA[n] for n in dna_strand)
    except KeyError as e:
        raise ValueError(f"Invalid nucleotide: {e.args[0]}") from e

[Read(rna_transcription.py)]
  1	DNA_TO_RNA = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}
  2	
  3	def to_rna(dna_strand):
  4	    try:
  5	        return ''.join(DNA_TO_RNA[n] for n in dna_strand)
  6	    except KeyError as e:
  7	        raise ValueError(f"Invalid nucleotide: {e.args[0]}") from e
  8

Assistant: Clean. The `from e` on the last line is worth noting — it chains the exceptions so a debugger can see both the `KeyError` and the `ValueError` in the traceback, rather than hiding where the error originated.

That's the whole solution: 7 lines, single-pass, validates correctly. You can run the Exercism tests with `python -m pytest rna_transcription_test.py`.

---

## Turn 4 (final)

**User:**

Looks good. The solution correctly handles the conversion and validation, and your reasoning on both choices showed you spotted the validation bugs in the plausible distractors.

<done/>

---

**Run end**: done after 3 turns (83s)
