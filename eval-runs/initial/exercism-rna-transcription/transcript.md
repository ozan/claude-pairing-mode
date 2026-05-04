# exercism-rna-transcription

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:38:45.168Z

---

## Turn 1

**User:**

Exercism 'RNA Transcription': convert a DNA strand to its RNA complement. G→C, C→G, T→A, A→U. Validate input characters.

**Pair:**

[Bash(ls *.py 2>/dev/null || echo "no python files")]
  no python files

Assistant: Clean slate. Let me ask a good first question about the core transform.

Assistant: No propose_options tool available — I'll just build this out directly with teaching notes inline.

Here's the plan: a `to_rna(dna_strand)` function that maps each nucleotide and raises `ValueError` on bad input. The cleanest Python idiom uses `str.translate()` with a translation table built from `str.maketrans()`.

[Write(rna_transcription.py)]
"""RNA Transcription: convert a DNA strand to its RNA complement.

Mapping: G → C, C → G, T → A, A → U
Invalid characters raise ValueError.
"""

_VALID_DNA = frozenset("GCTA")
_TABLE = str.maketrans("GCTA", "CGAU")


def to_rna(dna_strand: str) -> str:
    """Return the RNA complement of *dna_strand*.
… (10 more lines)

[Bash(python3 -c "
from rna_transcription import to_rna

# Basic cases
assert to_rna('') == ''
assert to_rna('G') == 'C'
assert to_rna('C') == 'G'
assert to_rna('T') == 'A'
assert to_rna('A') == 'U'
assert to_rna('ACGT') == 'UGCA'
assert to_rna('GATTACA') == 'CUAAUGU'

# Validation
try:
    to_rna('ACGTX')
    assert False, 'should have raised'
except ValueError as e:
    print('ValueError caught:', e)

print('All tests passed.')
"
)]
  ValueError caught: Invalid nucleotide(s) in DNA strand: ['X']
  All tests passed.

Assistant: All passing. A few things worth knowing about this implementation:

**`str.maketrans` / `str.translate`** — a built-in O(n) character-substitution mechanism. `maketrans("GCTA", "CGAU")` builds a lookup table keyed by Unicode ordinals; `translate()` then maps each character through it in one pass. Much faster than a dict comprehension or a loop with `if/elif` chains for long strands.

**Validation before translation** — we compute `frozenset(dna_strand) - _VALID_DNA` rather than scanning character-by-character. This is O(n) but constructs a set of *unique* bad characters, giving a cleaner error message (no duplicates). You could also validate lazily during translation by providing a `None`-returning lambda in the table, but that produces a worse error message.

**Module-level constants** — `_VALID_DNA` and `_TABLE` are built once at import time (underscore-prefixed to signal "private"). If `to_rna` were called in a tight loop, recreating the translation table on every call would be wasteful.

Want to run the official Exercism test suite, or extend this (e.g. lowercase handling)?

---

## Turn 2 (final)

**User:**

The solution is complete and tested. All cases pass:
- Empty strand, single nucleotides, and full sequences ✅
- Correct G↔C, T→A, A→U mappings ✅  
- ValueError on invalid characters ✅

The implementation uses Python's efficient `str.translate()` with a precomputed translation table, validates by building a set of invalid characters (for a clean error message), and stores constants at module level for reuse.

<done/>

---

**Run end**: done after 1 turn (39s)
