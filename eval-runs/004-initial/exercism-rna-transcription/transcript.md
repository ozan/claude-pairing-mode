# exercism-rna-transcription

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T00:21:40.621Z

---

## Turn 1

**User:**

Exercism 'RNA Transcription': convert a DNA strand to its RNA complement. G→C, C→G, T→A, A→U. Validate input characters.

**Pair:**

Assistant: Good problem. The core design question is how to wire translation and validation together. Pick one:

OPTIONS:
[A] maketrans + guard
```diff
+++ rna_transcription.py
@@ -0,0 +1,7 @@
+_TABLE = str.maketrans("GCTA", "CGAU")
+
+def to_rna(dna_strand):
+    if not all(c in "GCTA" for c in dna_strand):
+        raise ValueError("Invalid nucleotide in DNA strand")
+    return dna_strand.translate(_TABLE)
```

[B] Dict lookup, one pass
```diff
+++ rna_transcription.py
@@ -0,0 +1,8 @@
+_MAP = {"G": "C", "C": "G", "T": "A", "A": "U"}
+
+def to_rna(dna_strand):
+    try:
+        return "".join(_MAP[c] for c in dna_strand)
+    except KeyError as e:
+        raise ValueError(f"Invalid nucleotide: {e}") from e
```

(Reply with A or B, or ask a follow-up question.)

---

## Turn 2

**User:**

B.

B is a single pass over the string (validate and translate together), and the error handling gives you the actual bad character in the message. Option A has to scan twice — once for validation, once for translation. For Exercism, B's clarity and better error reporting feel more appropriate.

**Pair:**

Assistant: Exactly right — and there's a subtlety worth knowing about A: `str.translate` **silently passes through** any character not in the table. So if the guard had a bug or got deleted, invalid nucleotides would slip into the output with no error. The dict approach fails loudly by design.

[Glob(rna_transcription.py)]
  No files found

[Write(rna_transcription.py)]
_MAP = {"G": "C", "C": "G", "T": "A", "A": "U"}

def to_rna(dna_strand):
    try:
        return "".join(_MAP[c] for c in dna_strand)
    except KeyError as e:
        raise ValueError(f"Invalid nucleotide: {e}") from e


Assistant: Done. `rna_transcription.py` is live — 7 lines, one pass, noisy on bad input.

Want to add tests, or move on to a different exercise?

---

## Turn 3

**User:**

Looks solid. I'd feel better if we ran a quick manual test to confirm the mapping and error handling work as expected. Do you want to test it in a REPL, or is this enough?

**Pair:**

[Bash(python3 -c "
from rna_transcription import to_rna

# happy path
print(to_rna('GCTA'))   # expect CGAU
print(to_rna('ACGT'))   # expect UGCA
print(to_rna(''))       # expect ''

# error case
try:
    to_rna('GCXTA')
except ValueError as e:
    print(f'ValueError: {e}')
")]
  CGAU
  UGCA
  
  ValueError: Invalid nucleotide: 'X'

Assistant: All good — mapping correct, empty string handled, and the bad-char error names the offending nucleotide. Ship it.

---

## Turn 4 (final)

**User:**

Perfect—the test run confirms everything works. Mapping is correct, edge cases (empty string) work, and error handling names the bad character precisely. The solution meets the Exercism requirements cleanly.

<done/>

---

**Run end**: done after 3 turns (75s)
