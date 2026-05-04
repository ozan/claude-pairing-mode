# exercism-rna-transcription

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:28:32.147Z

---

## Turn 1

**User:**

Exercism 'RNA Transcription': convert a DNA strand to its RNA complement. G→C, C→G, T→A, A→U. Validate input characters.

**Pair:**

[Bash(ls)]
  (Bash completed with no output)

[Bash(ls -la)]
  total 0
  drwx------    2 oz  staff    64  3 May 20:28 .
  drwx------@ 182 oz  staff  5824  3 May 20:28 ..

Assistant: Empty directory — I'll create the solution from scratch. For Exercism Python exercises the convention is a single module file.

[Write(/rna_transcription.py)]
_DNA_TO_RNA = str.maketrans("GCTA", "CGAU")
_VALID_DNA = frozenset("GCTA")


def to_rna(dna_strand: str) -> str:
    """Return the RNA complement of the given DNA strand.

    Mapping: G→C  C→G  T→A  A→U

    Raises ValueError for any character not in {G, C, T, A}.
    """
    invalid = set(dna_strand) - _VALID_DNA
… (6 more lines)

[Bash(pwd && ls -la /tmp/)]
  /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-rna-transcription-oR33Ni
  total 49400
  drwxrwxrwt   85 root  wheel      2720  3 May 20:28 .
  drwxr-xr-x    6 root  wheel       192 30 Apr 07:51 ..
  -rw-r--r--    1 root  wheel        65  7 Apr 06:14 .BBE72B41371180178E084EEAF106AED4F350939DB95D3516864A1CC62E7AE82F
  drwxr-xr-x    6 oz    wheel       192  3 May 19:06 .pytest_cache
  -rw-r--r--    1 oz    wheel      1960  3 May 19:20 acronym.py
  drwxr-xr-x    3 oz    wheel        96  3 May 14:35 allergies-test
  drwxr-xr-x    3 oz    wheel        96  1 May 19:13 bun-extract
  drwxr-xr-x    4 oz    wheel       128  1 May 19:21 bun-node-bf2e2cecf
  -rw-r--r--    1 oz    wheel  23094987  1 May 19:13 bun.zip
  -rw-r--r--    1 oz    wheel      1646 30 Apr 13:40 capture_claude.py
  … (75 more lines)

[Bash(ls -la /tmp/rna/)]
  total 8
  drwxr-xr-x   3 oz    wheel    96  3 May 19:22 .
  drwxrwxrwt  85 root  wheel  2720  3 May 20:28 ..
  -rw-r--r--   1 oz    wheel   256  3 May 19:22 rna_transcription.py

[Bash(ls -la /tmp/claude-501/ | grep rna)]
  drwxr-xr-x    3 oz    wheel    96  3 May 15:45 -private-var-folders-q0-dv7j0tf55lb21cgdzz7h4khw0000gn-T-ai-pair-eval-exercism-rna-transcription-mQNcVq
  drwxr-xr-x    3 oz    wheel    96  3 May 20:28 -private-var-folders-q0-dv7j0tf55lb21cgdzz7h4khw0000gn-T-ai-pair-eval-exercism-rna-transcription-oR33Ni
  drwxr-xr-x    3 oz    wheel    96  3 May 19:14 -private-var-folders-q0-dv7j0tf55lb21cgdzz7h4khw0000gn-T-ai-pair-eval-exercism-rna-transcription-qgroh8
  drwxr-xr-x    3 oz    wheel    96  3 May 14:25 -private-var-folders-q0-dv7j0tf55lb21cgdzz7h4khw0000gn-T-ai-pair-eval-exercism-rna-transcription-RMDY86
  drwxr-xr-x    3 oz    wheel    96  3 May 09:16 -Users-oz-dev-ai-pair-proto-eval-runs-003-baseline-exercism-rna-transcription
  drwxr-xr-x    3 oz    wheel    96  3 May 10:22 -Users-oz-dev-ai-pair-proto-eval-runs-004-initial-exercism-rna-transcription

[Bash(ls -la /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-rna-transcription-oR33Ni/)]
  total 0
  drwx------    2 oz  staff    64  3 May 20:28 .
  drwx------@ 182 oz  staff  5824  3 May 20:28 ..

[Bash(touch /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-rna-transcription-oR33Ni/rna_transcription.py && echo "writable")]
  writable

[Write(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-rna-transcription-oR33Ni/rna_transcription.py)]
_DNA_TO_RNA = str.maketrans("GCTA", "CGAU")
_VALID_DNA = frozenset("GCTA")


def to_rna(dna_strand: str) -> str:
    """Return the RNA complement of the given DNA strand.

    Mapping: G→C  C→G  T→A  A→U

    Raises ValueError for any character not in {G, C, T, A}.
    """
    invalid = set(dna_strand) - _VALID_DNA
… (6 more lines)

[Read(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-rna-transcription-oR33Ni/rna_transcription.py)]
  <system-reminder>Warning: the file exists but is shorter than the provided offset (1). The file has 1 lines.</system-reminder>

[Write(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-rna-transcription-oR33Ni/rna_transcription.py)]
_DNA_TO_RNA = str.maketrans("GCTA", "CGAU")
_VALID_DNA = frozenset("GCTA")


def to_rna(dna_strand: str) -> str:
    """Return the RNA complement of the given DNA strand.

    Mapping: G→C  C→G  T→A  A→U

    Raises ValueError for any character not in {G, C, T, A}.
    """
    invalid = set(dna_strand) - _VALID_DNA
… (6 more lines)

Assistant: Now let me verify the solution works correctly with a quick test:

[Bash(python3 -c "
from rna_transcription import to_rna

# Basic mappings
assert to_rna('G') == 'C'
assert to_rna('C') == 'G'
assert to_rna('T') == 'A'
assert to_rna('A') == 'U'

# Empty strand
assert to_rna('') == ''

# Mixed strand
assert to_rna('ACGT') == 'UGCA'
assert to_rna('GCTA') == 'CGAU'

# Longer strand
assert to_rna('GATTACA') == 'CUAAUGU'

# Invalid input
try:
    to_rna('ACGTX')
    assert False, 'Should have raised ValueError'
except ValueError as e:
    print(f'Caught expected error: {e}')

try:
    to_rna('U')  # RNA char, not valid DNA
    assert False, 'Should have raised ValueError'
except ValueError as e:
    print(f'Caught expected error: {e}')

print('All tests passed!')
"
)]
  Caught expected error: Invalid DNA nucleotide(s): X
  Caught expected error: Invalid DNA nucleotide(s): U
  All tests passed!

Assistant: All tests pass. Here's the solution:

```python
_DNA_TO_RNA = str.maketrans("GCTA", "CGAU")
_VALID_DNA = frozenset("GCTA")


def to_rna(dna_strand: str) -> str:
    """Return the RNA complement of the given DNA strand.

    Mapping: G→C  C→G  T→A  A→U

    Raises ValueError for any character not in {G, C, T, A}.
    """
    invalid = set(dna_strand) - _VALID_DNA
    if invalid:
        raise ValueError(
            f"Invalid DNA nucleotide(s): {', '.join(sorted(invalid))}"
        )
    return dna_strand.translate(_DNA_TO_RNA)
```

**Key design choices:**

- **`str.maketrans` + `str.translate`** — a single O(n) pass over the string with a C-level lookup table; cleaner and faster than a dict comprehension or `str.replace`.
- **`frozenset` for validation** — set difference in O(k) where k is unique chars, not O(n·4). We validate *before* translating so invalid input is always rejected with a clear message.
- **Sorted invalid chars in the error** — deterministic output makes the error message testable and easier to read.
- **Empty string handled naturally** — both the set difference and translate produce `""` with no special-casing needed.

---

## Turn 2 (final)

**User:**

Perfect! The solution is complete and fully tested. 

**Summary:**

The RNA Transcription solution uses:
- **`str.maketrans` + `translate`** for efficient O(n) character mapping
- **`frozenset` validation** to catch invalid nucleotides with O(k) set difference (k = unique invalid chars)
- **Clear error messages** listing invalid characters in sorted order
- **No special cases** — empty strings work naturally

All test cases pass:
- ✅ Individual mappings (G→C, C→G, T→A, A→U)
- ✅ Empty strand
- ✅ Mixed and long strands
- ✅ Invalid character rejection with descriptive errors

<done/>

---

**Run end**: done after 1 turn (70s)
