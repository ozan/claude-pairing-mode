# exercism-rna-transcription

- Condition: `learning`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:05:06

## Initial prompt

Exercism 'RNA Transcription': convert a DNA strand to its RNA complement. G→C, C→G, T→A, A→U. Validate input characters.

---

## Turn 1

### Tutor

Thinking: The user wants to solve the Exercism 'RNA Transcription' exercise. Let me first explore the current directory to understand the project structure.

[Bash(find . -type f | head -30 && echo "---" && ls -la)]
  ./.claude/settings.json
  ---
  total 0
  drwx------    3 oz  staff    96  4 May 21:05 .
  drwx------@ 228 oz  staff  7296  4 May 21:05 ..
  drwxr-xr-x    3 oz  staff    96  4 May 21:05 .claude

Thinking: It seems there's no existing project structure. I need to create the solution from scratch. Let me create a Python solution for the RNA Transcription exercise on Exercism.
  
  Let me create the solution file. Exercism typically expects a specific file structure. For Python, it would be `rna_transcription.py`.

Tutor: Fresh workspace — I'll create the solution file from scratch.

Here's the mapping to implement:

| DNA | RNA |
|-----|-----|
| `G` | `C` |
| `C` | `G` |
| `T` | `A` |
| `A` | `U` |

[Write(/rna_transcription.py)]
"""RNA Transcription: convert a DNA strand to its RNA complement."""

# Maps each valid DNA nucleotide to its RNA complement
_DNA_TO_RNA = str.maketrans("GCTA", "CGAU")


def to_rna(dna_strand: str) -> str:
    """Return the RNA complement of *dna_strand*.

    Each nucleotide is transcribed according to the rule:
        G → C  |  C → G  |  T → A  |  A → U

… (10 more lines)
  error: EROFS: read-only file system, open '/rna_transcription.py'

Thinking: The filesystem is read-only at the root. Let me try writing to a different location. Let me check the current working directory.

[Bash(pwd && echo "---" && ls -la .claude/)]
  /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-7wfzsswe
  ---
  total 8
  drwxr-xr-x  3 oz  staff  96  4 May 21:05 .
  drwx------  3 oz  staff  96  4 May 21:05 ..
  -rw-r--r--  1 oz  staff  27  4 May 21:05 settings.json

[Write(/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-7wfzsswe/rna_transcription.py)]
"""RNA Transcription: convert a DNA strand to its RNA complement."""

# Maps each valid DNA nucleotide to its RNA complement
_DNA_TO_RNA = str.maketrans("GCTA", "CGAU")


def to_rna(dna_strand: str) -> str:
    """Return the RNA complement of *dna_strand*.

    Each nucleotide is transcribed according to the rule:
        G → C  |  C → G  |  T → A  |  A → U

… (10 more lines)
  File created successfully at: /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-7wfzsswe/rna_transcription.py

[Bash(cd /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-7wfzsswe && python3 -c "
from rna_transcription import to_rna

# ── happy-path tests ──────────────────────────────────────────────────────────
assert to_rna('G')    == 'C',  'G→C'
assert to_rna('C')    == 'G',  'C→G'
assert to_rna('T')    == 'A',  'T→A'
assert to_rna('A')    == 'U',  'A→U'
assert to_rna('')     == '',   'empty strand'
assert to_rna('ACGT') == 'UGCA', 'all four nucleotides'
assert to_rna('GATGGAACTTGACTACGTAAATT') == 'CUACCUUGAACUGAUGCAUUUAA', 'long strand'

# ── error-path tests ──────────────────────────────────────────────────────────
for bad in ('U', 'X', 'ACGU', 'ACGTx'):
    try:
        to_rna(bad)
        raise AssertionError(f'Expected ValueError for {bad!r}')
    except ValueError:
        pass   # correct

print('All tests passed.')
"
)]
  All tests passed.

Tutor: All tests pass. Here's a walkthrough of every decision made:

---

## Solution — `rna_transcription.py`

```python
_DNA_TO_RNA = str.maketrans("GCTA", "CGAU")

def to_rna(dna_strand: str) -> str:
    invalid = set(dna_strand) - set("GCTA")
    if invalid:
        raise ValueError(
            f"Invalid DNA nucleotide(s): {', '.join(sorted(invalid))}"
        )
    return dna_strand.translate(_DNA_TO_RNA)
```

---

### 🔑 Key concepts

**`str.maketrans` + `str.translate`** — the right tool for character-by-character substitution.  
`str.maketrans("GCTA", "CGAU")` builds a lookup table (a `dict[int, int]`) mapping each source character's ordinal to its replacement's ordinal. `translate` then applies that table in one O(n) pass — no loops, no `if`/`elif` chains.

```
maketrans("GCTA", "CGAU")
  → { ord('G'): ord('C'),
      ord('C'): ord('G'),
      ord('T'): ord('A'),
      ord('A'): ord('U') }
```

**Validation before translation** — `translate` silently passes through characters it doesn't recognise, so we must check *first*.  
`set(dna_strand) - set("GCTA")` computes the set of characters in the input that aren't valid nucleotides. This is O(n) and reports *all* bad characters at once rather than stopping at the first one.

**Module-level constant** — `_DNA_TO_RNA` is built once at import time, not on every call.

---

### 🧪 Test coverage

| Category | Examples |
|---|---|
| Single nucleotides | `G→C`, `C→G`, `T→A`, `A→U` |
| Empty string | `""→""` |
| Mixed strand | `"ACGT"→"UGCA"` |
| Long strand | 23-char Exercism canonical case |
| Invalid: RNA char | `"U"` → `ValueError` |
| Invalid: unknown char | `"X"` → `ValueError` |
| Invalid: mixed valid+bad | `"ACGTx"` → `ValueError` |

### Student

Thanks for walking me through this! I can see how the solution works now.

A couple of quick clarifications before we wrap up:

1. **The `str.maketrans` approach** — I get that it builds a lookup table once at the module level, which is more efficient than doing character-by-character replacements in a loop. Is `translate` actually faster than, say, a dictionary lookup in a loop, or is it mainly just cleaner code?

2. **The validation logic** — using `set(dna_strand) - set("GCTA")` to find invalid characters all at once makes sense. But I'm curious: is there a reason we prefer reporting all invalid characters instead of raising on the first one? Is that part of the Exercism spec, or just a nice-to-have?

Also, one tiny thing — I notice the error message mentions "nucleotide(s)" plural even for a single bad character. Should that message be more precise, or is it fine as-is?

---

## Turn 2

### Tutor

Thinking: The user has three questions:
  
  1. Is `str.translate` actually faster than a dictionary lookup in a loop, or just cleaner?
  2. Why report all invalid characters vs. stopping at the first one — spec requirement or nice-to-have?
  3. The error message says "nucleotide(s)" even for a single bad character — should it be more precise?
  
  Let me answer these concisely and accurately.
  
  **Question 1: translate vs loop performance**
  
  `str.translate` is genuinely faster, not just cleaner. It's implemented in C in CPython, so it avoids Python-level loop overhead entirely. A Python `for` loop with a `dict` lookup per character has:
  
  
  - Python bytecode execution overhead per iteration
  - A Python dict `__getitem__` call per character
  
  `str.translate` does:
  - One C-level loop over the string's internal buffer
  - Direct array/hash lookup in C
  
  So yes, it's measurably faster, especially for long strings. For short strings the difference is negligible, but the intent is also clearer.
  
  **Question 2: Report all invalid characters vs fail-fast**
  
  The Exercism spec only tests that a `ValueError` is raised — it doesn't mandate the message content or whether all bad characters are reported. So reporting all at once is a nice-to-have that improves the user experience without violating the spec.
  
  **Question 3: "nucleotide(s)" for a single bad character**
  
  The `(s)` notation is a practical shorthand, though production code would typically handle singular and plural forms separately for better clarity. For this exercise, it's acceptable as-is, but I can refine it if message precision matters.
  
  Let me run a quick benchmark to get concrete numbers on the performance difference.

Tutor: Great questions — let me tackle all three directly.

[Bash(cd /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-7wfzsswe && python3 -c "
import timeit, random

nucleotides = 'GCTA'
strand = ''.join(random.choices(nucleotides, k=10_000))

table = str.maketrans('GCTA', 'CGAU')
mapping = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}

t_translate = timeit.timeit(lambda: strand.translate(table),   number=5000)
t_join_dict = timeit.timeit(lambda: ''.join(mapping[c] for c in strand), number=5000)
t_join_get  = timeit.timeit(lambda: ''.join(mapping.get(c, c) for c in strand), number=5000)

print(f'translate:      {t_translate*1000:.1f} ms total  ({t_translate/5000*1e6:.1f} µs/call)')
print(f'join+dict[]:    {t_join_dict*1000:.1f} ms total  ({t_join_dict/5000*1e6:.1f} µs/call)')
print(f'join+dict.get:  {t_join_get*1000:.1f} ms total  ({t_join_get/5000*1e6:.1f} µs/call)')
print(f'speedup vs join+dict[]:   {t_join_dict/t_translate:.1f}x')
"
)]
  translate:      34.7 ms total  (6.9 µs/call)
  join+dict[]:    1381.8 ms total  (276.4 µs/call)
  join+dict.get:  1850.9 ms total  (370.2 µs/call)
  speedup vs join+dict[]:   39.8x

[Read(/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-7wfzsswe/rna_transcription.py)]
  1	"""RNA Transcription: convert a DNA strand to its RNA complement."""
  2	
  3	# Maps each valid DNA nucleotide to its RNA complement
  4	_DNA_TO_RNA = str.maketrans("GCTA", "CGAU")
  5	
  6	
  7	def to_rna(dna_strand: str) -> str:
  8	    """Return the RNA complement of *dna_strand*.
  9	
  10	    Each nucleotide is transcribed according to the rule:
  11	        G → C  |  C → G  |  T → A  |  A → U
  12	
  … (10 more lines)

[Edit(/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-7wfzsswe/rna_transcription.py)]
--- before
    invalid = set(dna_strand) - set("GCTA")
    if invalid:
        raise ValueError(
            f"Invalid DNA nucleotide(s): {', '.join(sorted(invalid))}"
        )
--- after
    invalid = set(dna_strand) - set("GCTA")
    if invalid:
        label = "nucleotide" if len(invalid) == 1 else "nucleotides"
        raise ValueError(
            f"Invalid DNA {label}: {', '.join(sorted(invalid))}"
        )
  The file /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-7wfzsswe/rna_transcription.py has been updated successfully.

[Bash(cd /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-7wfzsswe && python3 -c "
from rna_transcription import to_rna

# Singular
try:
    to_rna('ACGU')
except ValueError as e:
    print(repr(str(e)))   # expect 'nucleotide'

# Plural
try:
    to_rna('XYZ')
except ValueError as e:
    print(repr(str(e)))   # expect 'nucleotides'

# Happy path still works
assert to_rna('ACGT') == 'UGCA'
print('All good.')
"
)]
  'Invalid DNA nucleotide: U'
  'Invalid DNA nucleotides: X, Y, Z'
  All good.

Tutor: ---

### 1. `translate` is genuinely faster — ~40× on a real strand

The benchmark above used a 10,000-character strand, run 5,000 times:

| Approach | µs / call |
|---|---|
| `str.translate` | **6.9 µs** |
| `''.join(mapping[c] for c in strand)` | 276 µs |
| `''.join(mapping.get(c, c) for c in strand)` | 371 µs |

The gap isn't cosmetic. `str.translate` is implemented entirely in C — it walks the string's internal buffer and does a direct array lookup per character, with no Python bytecode dispatch, no generator protocol, no `__getitem__` call on every iteration. The `join` loop pays all of those costs for every single character. For DNA strands (which can be millions of bases), this matters.

---

### 2. "All errors at once" is a nice-to-have, not a spec requirement

The Exercism canonical tests only assert that a `ValueError` is raised — they say nothing about the message. So either approach passes.

The "report all" style comes from compiler design thinking: if you stop at the first error, the user fixes it, re-runs, hits the *next* error, fixes it, and so on. Reporting everything at once means one round-trip. Here it costs nothing extra (`set` subtraction is O(n) regardless), so there's no reason *not* to.

Fail-fast makes more sense when checking is expensive, or when later checks depend on earlier ones being clean.

---

### 3. Fixed — the `(s)` trick was lazy

The `(s)` parenthetical is common shorthand in documentation prose, but in a runtime error message that a user or test suite might inspect, it reads awkwardly. The fix is a one-liner:

```python
label = "nucleotide" if len(invalid) == 1 else "nucleotides"
raise ValueError(f"Invalid DNA {label}: {', '.join(sorted(invalid))}")
```

Now: `"Invalid DNA nucleotide: U"` vs `"Invalid DNA nucleotides: X, Y, Z"`.

### Student

Perfect — that all makes sense now. The benchmark really drives home why `translate` is the right choice here; I didn't expect a 40× difference, but the C-level implementation makes total sense.

I appreciate the distinction between "nice to have" (report all errors) and "required by spec" (raise on invalid input). That's a useful frame for thinking about how much polish to add.

And yeah, the singular/plural fix is much cleaner than the parenthetical — it reads like an actual error message now rather than documentation shorthand.

I feel like I understand the solution fully at this point: the `maketrans`/`translate` pattern for efficient character mapping, the validation approach, and the trade-offs involved. The code passes all tests and I can see exactly why each decision was made.

<done/>

---

**Run end:** done after 2 turn(s) in 79.6s
