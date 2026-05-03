# exercism-rna-transcription

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T01:48:06.930Z

---

## Turn 1

**User:**

Exercism 'RNA Transcription': convert a DNA strand to its RNA complement. G→C, C→G, T→A, A→U. Validate input characters.

**Pair:**

[Glob(rna_transcription.py)]
  No files found

Assistant: Core design question first — how to drive the character substitution:

OPTIONS:
[A] str.translate
```diff
+++ rna_transcription.py
@@ -0,0 +1,3 @@
+def to_rna(dna_strand: str) -> str:
+    return dna_strand.translate(
+        str.maketrans("GCTA", "CGAU"))
```

[B] dict + join
```diff
+++ rna_transcription.py
@@ -0,0 +1,4 @@
+MAP = {"G": "C", "C": "G", "T": "A", "A": "U"}
+
+def to_rna(dna_strand: str) -> str:
+    return "".join(MAP[c] for c in dna_strand)
```

(Reply with A or B, or ask a follow-up question.)

Assistant: Which approach do you prefer for the core translation?

---

## Turn 2

**User:**

I'll pick **B**.

While `str.translate` is more concise, the dict approach better handles the validation requirement. The dict lookup will raise a `KeyError` if we encounter invalid characters, which gives us a natural validation point. Plus, the mapping is explicit and readable.

**Pair:**

Assistant: Exactly right — and you spotted the key subtlety: `str.translate` is one of those "looks obviously correct" choices that quietly swallows invalid input.

The `KeyError` gives us a hook, but Exercism expects a `ValueError`. Let me write the base and then ask how to handle that conversion.

[Write(rna_transcription.py)]
MAP = {"G": "C", "C": "G", "T": "A", "A": "U"}

def to_rna(dna_strand: str) -> str:
    return "".join(MAP[c] for c in dna_strand)


Assistant: Now — `MAP[c]` raises `KeyError` on bad input, but callers expect `ValueError`. How should we surface that?

OPTIONS:
[A] try/except in the loop
```diff
+++ rna_transcription.py
@@ -3,2 +3,6 @@
-def to_rna(dna_strand: str) -> str:
-    return "".join(MAP[c] for c in dna_strand)
+def to_rna(dna_strand: str) -> str:
+    try:
+        return "".join(MAP[c] for c in dna_strand)
+    except KeyError as e:
+        raise ValueError(f"invalid nucleotide: {e}") from e
```

[B] pre-validate with a set check
```diff
+++ rna_transcription.py
@@ -3,2 +3,6 @@
-def to_rna(dna_strand: str) -> str:
-    return "".join(MAP[c] for c in dna_strand)
+def to_rna(dna_strand: str) -> str:
+    invalid = set(dna_strand) - MAP.keys()
+    if invalid:
+        raise ValueError(f"invalid nucleotide(s): {invalid}")
+    return "".join(MAP[c] for c in dna_strand)
```

(Reply with A or B, or ask a follow-up question.)

Assistant: A or B?

---

## Turn 3

**User:**

I'll pick **A**.

Option A stays lean and idiomatic — try/except around the core logic, catch the `KeyError` on the first bad character, convert to `ValueError`. It's the natural Python pattern: "code that might fail, convert the exception if needed."

Option B pre-validates with a set check, which tells you *all* bad characters upfront. That's nice for debugging, but it's a second pass through the data and duplicates the membership check that `MAP[c]` is already doing. For Exercism, failing on the first invalid nucleotide is typically sufficient.

Go with A?

**Pair:**

Assistant: Spot on — single pass, zero redundancy, exception carries the bad character automatically. Let me apply it.

[Edit(rna_transcription.py)]
--- before
def to_rna(dna_strand: str) -> str:
    return "".join(MAP[c] for c in dna_strand)
--- after
def to_rna(dna_strand: str) -> str:
    try:
        return "".join(MAP[c] for c in dna_strand)
    except KeyError as e:
        raise ValueError(f"invalid nucleotide: {e}") from e

[Read(rna_transcription.py)]
  1	MAP = {"G": "C", "C": "G", "T": "A", "A": "U"}
  2	
  3	def to_rna(dna_strand: str) -> str:
  4	    try:
  5	        return "".join(MAP[c] for c in dna_strand)
  6	    except KeyError as e:
  7	        raise ValueError(f"invalid nucleotide: {e}") from e
  8

Assistant: Done — 7 lines, correct, efficient. A few things worth noting about the `from e` on the last line: it chains the exceptions so the traceback shows both the `ValueError` *and* the original `KeyError`, which is useful when debugging. Without it you'd lose context on which nucleotide triggered it.

---

## Turn 4 (final)

**User:**

Looks good — the solution is solid. Valid DNA translates cleanly, invalid characters fail fast with a meaningful error. The exception chaining with `from e` is a nice touch for debugging context.

<done/>

---

**Run end**: done after 3 turns (102s)
