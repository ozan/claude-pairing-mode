# exercism-rna-transcription

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-02T23:16:06.455Z

---

## Turn 1

**User:**

Exercism 'RNA Transcription': convert a DNA strand to its RNA complement. G→C, C→G, T→A, A→U. Validate input characters.

**Pair:**

[Glob(**/*rna*)]
  No files found

[Glob(**/*transcription*)]
  No files found

[Bash(find ~ -maxdepth 4 -type d -name "rna-transcription" 2>/dev/null | head -5)]
  Command running in background with ID: b3e1dvhf4. Output is being written to: /private/tmp/claude-501/-Users-oz-dev-ai-pair-proto-eval-runs-003-baseline-exercism-rna-transcription/3f06f956-bf80-4c6b-892d-9eac8e9da2e1/tasks/b3e1dvhf4.output

[Bash(ls ~/exercism 2>/dev/null || echo "no exercism dir")]
  no exercism dir

[Bash(cat /private/tmp/claude-501/-Users-oz-dev-ai-pair-proto-eval-runs-003-baseline-exercism-rna-transcription/3f06f956-bf80-4c6b-892d-9eac8e9da2e1/tasks/b3e1dvhf4.output)]
  (Bash completed with no output)

[Bash(ls /Users/oz/dev/ai-pair-proto/ 2>/dev/null | head -20)]
  CLAUDE.md
  eval-runs
  experiments
  test_valid_parens.py
  trapping_rain_water.py
  tui
  valid_parentheses.py

[Bash(ls /Users/oz/dev/ai-pair-proto/eval-runs/ 2>/dev/null)]
  001-smoke-test
  002-baseline
  003-baseline
  count_options.py

[Bash(ls /Users/oz/dev/ai-pair-proto/eval-runs/003-baseline/)]
  exercism-leap-year
  exercism-rna-transcription
  leetcode-longest-substring
  leetcode-trap-rain-water
  leetcode-two-sum

[Bash(ls /Users/oz/dev/ai-pair-proto/eval-runs/003-baseline/exercism-rna-transcription/)]
  transcript.jsonl
  transcript.md

[Bash(ls /Users/oz/dev/ai-pair-proto/eval-runs/003-baseline/exercism-leap-year/ && ls /Users/oz/dev/ai-pair-proto/eval-runs/002-baseline/exercism-rna-transcription/ 2>/dev/null || echo "no 002 rna")]
  transcript.jsonl
  transcript.md
  no 002 rna

Assistant: The project has Python files at the root. I'll create the standard Exercism Python solution here.

[Write(/Users/oz/dev/ai-pair-proto/rna_transcription.py)]
DNA_TO_RNA = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}


def to_rna(dna_strand):
    result = []
    for nucleotide in dna_strand:
        if nucleotide not in DNA_TO_RNA:
            raise ValueError(f"Invalid nucleotide: {nucleotide!r}")
        result.append(DNA_TO_RNA[nucleotide])
    return ''.join(result)


Assistant: Done. Here's a quick breakdown of the solution:

**`rna_transcription.py`**

| DNA | RNA |
|-----|-----|
| `G` | `C` |
| `C` | `G` |
| `T` | `A` |
| `A` | `U` |

**Key design choices:**

- **`DNA_TO_RNA` dict** — O(1) per-character lookup, trivially extensible.
- **`result` list + `''.join()`** — avoids quadratic string concatenation; idiomatic Python for building strings character-by-character.
- **`ValueError` on unknown characters** — Exercism's standard contract for invalid input; the message includes the offending character for easier debugging.
- **Iterates lazily** — works on any iterable of characters (string, generator, etc.).

Example usage:
```python
to_rna("GCTA")   # → "CGAU"
to_rna("ACGT")   # → "UGCA"
to_rna("X")      # → ValueError: Invalid nucleotide: 'X'
to_rna("")       # → ""
```

---

## Turn 2

**User:**

Hold on — where's option B? The pair-programming setup is supposed to show me *two* approaches so I can choose one. I only see one solution here. 

Can you present two different ways to solve this? One should be the honest best approach, and the other a plausible-looking alternative with a subtle flaw — then I'll pick which one you implement.

**Pair:**

Assistant: You're right, my mistake — I skipped the whole point. Here are two approaches. One is the honest best; the other is plausible-looking but has a subtle flaw. Pick A or B.

---

## Option A — `str.translate()` with upfront set validation

```diff
+++ rna_transcription.py
@@ -1,10 +1,8 @@
-DNA_TO_RNA = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}
-
+_TABLE = str.maketrans('GCTA', 'CGAU')
+_VALID = frozenset('GCTA')
 
 def to_rna(dna_strand):
-    result = []
-    for nucleotide in dna_strand:
-        if nucleotide not in DNA_TO_RNA:
-            raise ValueError(f"Invalid nucleotide: {nucleotide!r}")
-        result.append(DNA_TO_RNA[nucleotide])
-    return ''.join(result)
+    if bad := set(dna_strand) - _VALID:
+        raise ValueError(f"Invalid nucleotide(s): {bad}")
+    return dna_strand.translate(_TABLE)
```

`str.maketrans` + `str.translate` is the standard library's purpose-built primitive for character-to-character substitution. Validation collects all bad characters at once before touching the string.

---

## Option B — fluent chained `.replace()` calls

```diff
+++ rna_transcription.py
@@ -1,10 +1,10 @@
-DNA_TO_RNA = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}
-
+_VALID = frozenset('GCTA')
 
 def to_rna(dna_strand):
-    result = []
-    for nucleotide in dna_strand:
-        if nucleotide not in DNA_TO_RNA:
-            raise ValueError(f"Invalid nucleotide: {nucleotide!r}")
-        result.append(DNA_TO_RNA[nucleotide])
-    return ''.join(result)
+    if bad := set(dna_strand) - _VALID:
+        raise ValueError(f"Invalid nucleotide(s): {bad}")
+    return (dna_strand
+            .replace('G', 'C')
+            .replace('C', 'G')
+            .replace('T', 'A')
+            .replace('A', 'U'))
```

Upfront validation is identical. The mapping is expressed as a readable chain of named substitutions rather than a lookup table.

---

**Which do you want applied — A or B?**

---

## Turn 3

**User:**

**A**

The chained `.replace()` calls in B have a subtle bug—they interfere with each other. When you do `.replace('G', 'C')` first, you create new `C`s. Then `.replace('C', 'G')` transforms *both* the original `C`s *and* the new ones you just created, messing up the result.

Example: `"GC"` should become `"CG"`, but with B:
- After `replace('G', 'C')`: `"CC"`
- After `replace('C', 'G')`: `"GG"` ← wrong!

`str.translate()` in A does all substitutions simultaneously without interference, which is exactly what this problem needs. That's the honest best choice.

**Pair:**

Assistant: Spot on — that's exactly the flaw. `str.translate` applies the entire mapping atomically in a single pass; chained `.replace` is sequential and each call operates on the already-mutated string. Any pair of nucleotides that map *to* each other (G↔C, as here) will get double-converted.

Applying Option A now:

[Read(/Users/oz/dev/ai-pair-proto/rna_transcription.py)]
  1	DNA_TO_RNA = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}
  2	
  3	
  4	def to_rna(dna_strand):
  5	    result = []
  6	    for nucleotide in dna_strand:
  7	        if nucleotide not in DNA_TO_RNA:
  8	            raise ValueError(f"Invalid nucleotide: {nucleotide!r}")
  9	        result.append(DNA_TO_RNA[nucleotide])
  10	    return ''.join(result)
  11

[Write(/Users/oz/dev/ai-pair-proto/rna_transcription.py)]
_TABLE = str.maketrans('GCTA', 'CGAU')
_VALID = frozenset('GCTA')


def to_rna(dna_strand):
    if bad := set(dna_strand) - _VALID:
        raise ValueError(f"Invalid nucleotide(s): {bad}")
    return dna_strand.translate(_TABLE)


Assistant: Done. A few things worth noting about what you chose and why it wins:

- **Atomicity** — as you nailed, `translate` maps every character in one pass from a pre-built lookup table. There's no intermediate string for a second substitution to corrupt.
- **Speed** — `str.translate` is implemented in C and operates on the whole string in one shot, vs. four full O(n) scans with `.replace`.
- **`maketrans` enforces symmetry at definition time** — the two positional strings `'GCTA'` / `'CGAU'` must be the same length, so a missing or extra mapping is a `ValueError` at module load, not a silent wrong answer at runtime.
- **Upfront bulk validation** — collecting all bad characters before touching the string gives the caller a complete error (`{'X', 'Z'}`) rather than stopping at the first bad byte.

---

## Turn 4 (final)

**User:**

Perfect — you've internalized exactly why `translate` is the right tool. The solution is now live at `/Users/oz/dev/ai-pair-proto/rna_transcription.py` with the atomic mapping, validated upfront, and no risk of character interference.

Quick test to confirm:
```python
to_rna("GCTA")   # → "CGAU" ✓
to_rna("GC")     # → "CG" ✓ (would fail with chained .replace)
to_rna("X")      # → ValueError: Invalid nucleotide(s): {'X'} ✓
to_rna("")       # → "" ✓
```

<done/>

---

**Run end**: done after 3 turns (281s)
