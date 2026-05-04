# exercism-rna-transcription

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:41:07

## Initial prompt

Exercism 'RNA Transcription': convert a DNA strand to its RNA complement. G→C, C→G, T→A, A→U. Validate input characters.

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Tutor: Good problem. First decision — how to map each DNA nucleotide to its RNA complement:

OPTIONS:
[A] str.translate table
```diff
+++ rna_transcription.py
@@ -0,0 +1,4 @@
+_TABLE = str.maketrans("GCTA", "CGAU")
+
+def to_rna(dna_strand):
+    return dna_strand.translate(_TABLE)
```

[B] Dict lookup loop
```diff
+++ rna_transcription.py
@@ -0,0 +1,5 @@
+_MAP = {"G": "C", "C": "G", "T": "A", "A": "U"}
+
+def to_rna(dna_strand):
+    return "".join(_MAP[c] for c in dna_strand)
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach do you want to go with?

### Student

I think I'll go with **B** (the dict lookup loop). 

I like that it's more explicit — I can clearly see the mapping for each nucleotide at a glance. The `str.translate` approach is probably more efficient, but since this is a learning problem, I'd rather have code that's easy to understand and modify if needed.

Plus, the dict approach will make it easier to add validation later. Should we add the input validation next to check for invalid characters?

---

## Turn 2

### Tutor

Tutor: Good reasoning — readability is a real virtue, especially when maintainability matters. Worth noting: the dict loop *already* raises a `KeyError` on invalid chars, so validation is almost free. The question is just how to surface it:

OPTIONS:
[A] Catch and re-raise ValueError
```diff
+++ rna_transcription.py
@@ -3,3 +3,6 @@
 def to_rna(dna_strand):
-    return "".join(_MAP[c] for c in dna_strand)
+    try:
+        return "".join(_MAP[c] for c in dna_strand)
+    except KeyError as e:
+        raise ValueError(f"Invalid nucleotide: {e}") from e
```

[B] Pre-validate with a set check
```diff
+++ rna_transcription.py
@@ -3,3 +3,5 @@
 def to_rna(dna_strand):
+    invalid = set(dna_strand) - _MAP.keys()
+    if invalid:
+        raise ValueError(f"Invalid nucleotide(s): {invalid}")
     return "".join(_MAP[c] for c in dna_strand)
```

(Reply with A or B, or ask a follow-up question.)

### Student

I'll go with **A** (catch and re-raise ValueError).

Here's my thinking: option B pre-validates by building a set of invalid characters, which means we're scanning the string twice — once to find invalids, then again in the join. Option A only scans once, and we only pay the validation "cost" if there actually *is* an invalid character.

Plus, the try-except approach feels more Pythonic to me — we're following the "easier to ask forgiveness than permission" pattern. And the error message from the KeyError will already tell us which character caused the problem.

Should we write a quick test to make sure both the happy path and the error case work?

---

## Turn 3

### Tutor

Tutor: Nailed it — EAFP is exactly the right framing. Let me write the file first, then we'll do tests.

[Glob(rna_transcription.py)]
  No files found

[Write(rna_transcription.py)]
_MAP = {"G": "C", "C": "G", "T": "A", "A": "U"}


def to_rna(dna_strand):
    try:
        return "".join(_MAP[c] for c in dna_strand)
    except KeyError as e:
        raise ValueError(f"Invalid nucleotide: {e}") from e

  File created successfully at: rna_transcription.py

Tutor: Now for tests — one small decision worth thinking about:

OPTIONS:
[A] pytest with parametrize
```diff
+++ test_rna_transcription.py
@@ -0,0 +1,16 @@
+import pytest
+from rna_transcription import to_rna
+
+@pytest.mark.parametrize("dna, rna", [
+    ("G", "C"),
+    ("C", "G"),
+    ("T", "A"),
+    ("A", "U"),
+    ("ACGT", "UGCA"),
+    ("", ""),
+])
+def test_to_rna(dna, rna):
+    assert to_rna(dna) == rna
+
+def test_invalid_raises():
+    with pytest.raises(ValueError):
+        to_rna("ACGX")
```

[B] Plain unittest cases
```diff
+++ test_rna_transcription.py
@@ -0,0 +1,16 @@
+import unittest
+from rna_transcription import to_rna
+
+class TestRna(unittest.TestCase):
+    def test_each_nucleotide(self):
+        self.assertEqual(to_rna("G"), "C")
+        self.assertEqual(to_rna("C"), "G")
+        self.assertEqual(to_rna("T"), "A")
+        self.assertEqual(to_rna("A"), "U")
+
+    def test_strand(self):
+        self.assertEqual(to_rna("ACGT"), "UGCA")
+
+    def test_invalid(self):
+        with self.assertRaises(ValueError):
+            to_rna("ACGX")
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which test style do you prefer?

### Student

I'll go with **A** (pytest with parametrize).

I like how parametrize lets me test multiple cases in one clean table — it's easy to add new test cases and easy to see at a glance what inputs I'm covering. Plus it's less boilerplate than unittest.

Let me think about the test cases though — should we also add a test for an empty strand returning an empty string? I see it's already in the parametrize list (`("", "")`), so that's good. And we're testing invalid input too with the second test.

Actually, I'm wondering: should we test a longer, more realistic strand too? Like something with multiple nucleotides? I see `("ACGT", "UGCA")` is there, so we're covered.

I think this looks good. Should we write it out and run it?

---

## Turn 4

### Tutor

Tutor: Agreed, the coverage looks solid. Let's write it and run it.

[Write(test_rna_transcription.py)]
import pytest
from rna_transcription import to_rna

@pytest.mark.parametrize("dna, rna", [
    ("G", "C"),
    ("C", "G"),
    ("T", "A"),
    ("A", "U"),
    ("ACGT", "UGCA"),
    ("", ""),
])
def test_to_rna(dna, rna):
… (6 more lines)
  File created successfully at: test_rna_transcription.py

[Bash(python -m pytest test_rna_transcription.py -v)]
  ============================= test session starts ==============================
  platform darwin -- Python 3.14.4, pytest-9.0.3, pluggy-1.6.0 -- /Users/oz/dev/ai-pair-proto/eval/.venv/bin/python
  cachedir: .pytest_cache
  rootdir: /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-7gzjq744
  plugins: anyio-4.13.0
  collecting ... collected 7 items
  
  test_rna_transcription.py::test_to_rna[G-C] PASSED                       [ 14%]
  test_rna_transcription.py::test_to_rna[C-G] PASSED                       [ 28%]
  test_rna_transcription.py::test_to_rna[T-A] PASSED                       [ 42%]
  test_rna_transcription.py::test_to_rna[A-U] PASSED                       [ 57%]
  test_rna_transcription.py::test_to_rna[ACGT-UGCA] PASSED                 [ 71%]
  … (4 more lines)

Tutor: 7/7 green. Notice how pytest names each parametrized case individually — `test_to_rna[G-C]`, `test_to_rna[T-A]`, etc. — so a failure points you straight to the broken mapping rather than just "test_each_nucleotide failed."

Here's the final shape of the solution:

- **`rna_transcription.py`** — a module-level dict for the mapping, a single-pass generator in `join`, and EAFP validation that only costs anything on the error path.
- **`test_rna_transcription.py`** — each nucleotide as its own labeled row, a multi-char strand, empty string edge case, and an invalid input check.

Clean and done. Want to tackle another Exercism problem?

### Student

Great! All tests pass, and I'm happy with how the solution turned out. The code is clean, the validation is elegant, and the test coverage is solid.

I appreciate the walkthrough — especially the EAFP pattern and how the dict approach gave us validation almost for free. Those are things I'll carry forward to other problems.

But I'll pass on starting another problem right now. I want to focus on understanding this one deeply and maybe work through it once more on my own to make sure the concepts really stick before moving on.

Thanks for pairing on this!

<done/>

---

**Run end:** done after 4 turn(s) in 69.5s
