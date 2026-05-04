# exercism-rna-transcription

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Output style: `Learning`
- Started: 2026-05-03T19:57:39.792Z

---

## Turn 1

**User:**

Exercism 'RNA Transcription': convert a DNA strand to its RNA complement. G→C, C→G, T→A, A→U. Validate input characters.

**Pair:**

[Bash(ls)]
  (Bash completed with no output)

[Bash(exercism download --exercise=rna-transcription --track=python 2>/dev/null || echo "Not found via exercism CLI")]
  Not found via exercism CLI

Assistant: No exercise files present — I'll build the solution from scratch.

## The Mapping

| DNA | RNA |
|-----|-----|
| `G` | `C` |
| `C` | `G` |
| `T` | `A` |
| `A` | `U` |

Any character outside `{G, C, T, A}` is invalid and should raise an error.

[Write(/home/user/rna_transcription.py)]
DNA_TO_RNA = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}


def to_rna(dna_strand):
    """Return the RNA complement of the given DNA strand.

    Raises ValueError for any character not in {G, C, T, A}.
    """
    rna = []
    for nucleotide in dna_strand:
        if nucleotide not in DNA_TO_RNA:
            raise ValueError(f"Invalid nucleotide: {nucleotide!r}")
… (3 more lines)

[Bash(pwd)]
  /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-rna-transcription-gxRrin

[Write(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-rna-transcription-gxRrin/rna_transcription.py)]
DNA_TO_RNA = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}


def to_rna(dna_strand):
    """Return the RNA complement of the given DNA strand.

    Raises ValueError for any character not in {G, C, T, A}.
    """
    rna = []
    for nucleotide in dna_strand:
        if nucleotide not in DNA_TO_RNA:
            raise ValueError(f"Invalid nucleotide: {nucleotide!r}")
… (3 more lines)

Assistant: Now let's verify it works:

[Bash(python3 -c "
from rna_transcription import to_rna

# Basic mappings
print(to_rna('G'))      # C
print(to_rna('C'))      # G
print(to_rna('T'))      # A
print(to_rna('A'))      # U

# Full strand
print(to_rna('ACGT'))   # UGCA
print(to_rna('GCTA'))   # CGAU

# Empty strand
print(repr(to_rna(''))) # ''

# Validation
try:
    to_rna('ACGX')
except ValueError as e:
    print(f'Error: {e}')
"
)]
  C
  G
  A
  U
  UGCA
  CGAU
  ''
  Error: Invalid nucleotide: 'X'

Assistant: All correct. Here's a walkthrough of every decision made:

---

## How it works

### 1. Lookup table instead of `if/elif`
```python
DNA_TO_RNA = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}
```
A dict is the clearest way to express a fixed mapping — one entry per rule, easy to audit at a glance.

### 2. Loop + validate in one pass
```python
for nucleotide in dna_strand:
    if nucleotide not in DNA_TO_RNA:   # ← validation
        raise ValueError(...)
    rna.append(DNA_TO_RNA[nucleotide]) # ← translation
```
Instead of two separate passes (validate *then* translate), a single loop handles both. The error is raised at the first bad character, which gives a precise message.

### 3. Build a list, join at the end
```python
rna = []
...
return ''.join(rna)
```
Strings are **immutable** in Python — `result += char` inside a loop creates a new string object every iteration (O(n²) in the worst case). Appending to a list and joining once is O(n).

### 4. `''.join(rna)` handles the empty-string edge case for free
If `dna_strand = ""` the loop body never runs and `join` returns `""` — no special case needed.

---

### Alternative one-liner (good to know)
```python
def to_rna(dna_strand):
    return ''.join(DNA_TO_RNA[n] for n in dna_strand)
```
This is elegant but raises a **`KeyError`** (not a `ValueError`) on bad input. Exercism tests typically expect `ValueError`, so the explicit check in the main solution is safer.

---

## Turn 2 (final)

**User:**

Looking at this transcript, I can see the complete solution has been developed, tested, and thoroughly explained:

✅ **Solution written** — `DNA_TO_RNA` lookup table with input validation  
✅ **All test cases pass** — single chars, full strands, empty input, error cases  
✅ **Design explained** — dict for clarity, single-pass validation, list+join for O(n) efficiency, KeyError vs ValueError trade-off  

The implementation is solid:
- Uses an immutable mapping for clarity
- Validates and translates in one efficient pass  
- Handles edge cases (empty strand, invalid nucleotides)
- Raises the expected `ValueError` with a clear message

The walkthrough at the end covers the key learning points: why a dict over `if/elif`, why list+join over string concatenation, and the trade-offs of different approaches (e.g., one-liner vs. explicit error type).

There's nothing meaningful left to do — the problem is solved, tested, and well-understood.

<done/>

---

**Run end**: done after 1 turn (54s)
