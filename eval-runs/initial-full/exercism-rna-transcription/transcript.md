# exercism-rna-transcription

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T05:44:33.367Z

---

## Turn 1

**User:**

Exercism 'RNA Transcription': convert a DNA strand to its RNA complement. G→C, C→G, T→A, A→U. Validate input characters.

**Pair:**

Assistant: I'll assume Python (standard for Exercism). Let me check for any existing files first.

[Glob(rna_transcription*)]
  No files found

Assistant: Clean slate. Before I write anything — good first design question here:

OPTIONS:
[A] str.translate
```diff
+++ rna_transcription.py
@@ -0,0 +1,7 @@
+_TABLE = str.maketrans('GCTA', 'CGAU')
+
+def to_rna(dna_strand):
+    if invalid := set(dna_strand) - set('GCTA'):
+        raise ValueError(f"Invalid nucleotide(s): {invalid}")
+    return dna_strand.translate(_TABLE)
```

[B] dict lookup loop
```diff
+++ rna_transcription.py
@@ -0,0 +1,8 @@
+_MAP = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}
+
+def to_rna(dna_strand):
+    result = []
+    for nucleotide in dna_strand:
+        if nucleotide not in _MAP:
+            raise ValueError(f"Invalid nucleotide: {nucleotide!r}")
+        result.append(_MAP[nucleotide])
+    return ''.join(result)
```

(Reply with A or B, or ask a follow-up question.)

Assistant: Which approach do you prefer?

---

## Turn 2

**User:**

A.

`str.translate()` is the standard library tool built for this job — it's fast (C-level), teaches a useful pattern, and the error reporting is actually better (shows *all* invalid characters at once, not just the first). Option B is readable but slower and reports one character at a time, which feels less helpful.

**Pair:**

Assistant: Exactly right. Let's write it.

[Write(rna_transcription.py)]
_TABLE = str.maketrans('GCTA', 'CGAU')

def to_rna(dna_strand):
    if invalid := set(dna_strand) - set('GCTA'):
        raise ValueError(f"Invalid nucleotide(s): {invalid}")
    return dna_strand.translate(_TABLE)


Assistant: Done. A few things worth noting about this implementation:

- **`str.maketrans`** builds a translation table at module load time (not per-call) — that `_TABLE` prefix signals it's a module-level constant.
- **Walrus operator** (`:=`) does the set difference and binds it in one expression; no need for a separate variable before the `if`.
- **`set(dna_strand) - set('GCTA')`** collects *all* bad characters before raising, so the error message is complete rather than stopping at the first offender.
- **`str.translate`** then runs entirely in C, iterating the string once with no Python loop overhead.

Want to run the Exercism tests, or move on?

---

## Turn 3

**User:**

Let's run the tests. Good practice to verify it actually works, and Exercism problems usually come with a test suite.

**Pair:**

[Glob(*.py)]
  rna_transcription.py

Assistant: No test file bundled — typical when you're working outside the Exercism CLI. Let me grab the canonical test suite directly.

[WebFetch({})]
  # RNA Transcription Test File
  
  This is a Python unittest module for testing RNA transcription functionality. The file contains auto-generated test cases based on canonical data from the Exercism problem specifications repository.
  
  ## Key Content:
  
  The test file imports a `to_rna` function and defines a test class with six test methods:
  
  1. **Empty sequence test** - verifies that an empty string returns an empty result
  2. **Individual nucleotide tests** - confirm the transcription rules for single bases:
     - "C" → "G"
     - "G" → "C"
  … (5 more lines)

[Bash]
  # These tests are auto-generated with test data from:
  # https://github.com/exercism/problem-specifications/tree/main/exercises/rna-transcription/canonical-data.json
  # File last updated on 2023-07-19
  
  import unittest
  
  from rna_transcription import (
      to_rna,
  )
  
  
  class RnaTranscriptionTest(unittest.TestCase):
  … (17 more lines)

[Agent({"description":"Fetch Exercism RNA transcription test file","prompt":"Fetch t...)]
  Here is the full file contents exactly as-is:
  
  ```
  # These tests are auto-generated with test data from:
  # https://github.com/exercism/problem-specifications/tree/main/exercises/rna-transcription/canonical-data.json
  # File last updated on 2023-07-19
  
  import unittest
  
  from rna_transcription import (
      to_rna,
  )
  … (24 more lines)

Assistant: Got it. Writing the test file and running it.

[Write(rna_transcription_test.py)]
# These tests are auto-generated with test data from:
# https://github.com/exercism/problem-specifications/tree/main/exercises/rna-transcription/canonical-data.json
# File last updated on 2023-07-19

import unittest

from rna_transcription import (
    to_rna,
)


class RnaTranscriptionTest(unittest.TestCase):
… (18 more lines)

[Bash(python -m pytest rna_transcription_test.py -v)]
  error: Exit code 127

[Bash(python3 -m pytest rna_transcription_test.py -v)]
  ============================= test session starts ==============================
  platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0 -- /Library/Developer/CommandLineTools/usr/bin/python3
  cachedir: .pytest_cache
  rootdir: /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-rna-transcription-mQNcVq
  collecting ... collected 6 items
  
  rna_transcription_test.py::RnaTranscriptionTest::test_empty_rna_sequence PASSED [ 16%]
  rna_transcription_test.py::RnaTranscriptionTest::test_rna_complement PASSED [ 33%]
  rna_transcription_test.py::RnaTranscriptionTest::test_rna_complement_of_adenine_is_uracil PASSED [ 50%]
  rna_transcription_test.py::RnaTranscriptionTest::test_rna_complement_of_cytosine_is_guanine PASSED [ 66%]
  rna_transcription_test.py::RnaTranscriptionTest::test_rna_complement_of_guanine_is_cytosine PASSED [ 83%]
  rna_transcription_test.py::RnaTranscriptionTest::test_rna_complement_of_thymine_is_adenine PASSED [100%]
  … (2 more lines)

Assistant: 6/6, all green. The canonical test suite doesn't include an invalid-input case, but our validation is still correct — you can verify it quickly:

```python
>>> to_rna("ACGX")
ValueError: Invalid nucleotide(s): {'X'}
```

You're good to submit. Want to tackle another Exercism problem?

---

## Turn 4 (final)

**User:**

Looks good — RNA Transcription is done. The solution is clean, efficient, and handles all the edge cases.

<done/>

---

**Run end**: done after 3 turns (77s)
