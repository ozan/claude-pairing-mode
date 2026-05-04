# exercism-rna-transcription

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:01:04

## Initial prompt

Exercism 'RNA Transcription': convert a DNA strand to its RNA complement. G→C, C→G, T→A, A→U. Validate input characters.

---

## Turn 1

### Tutor

[Glob(rna_transcription*)]
  No files found

Tutor: No existing file — let's start from scratch. First design question before I write anything:

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Tutor: Good, let me kick things off with the core design question — how to handle the mapping + validation together:

OPTIONS:
[A] str.translate + pre-validate
```diff
+++ rna_transcription.py
@@ -0,0 +1,8 @@
+VALID = set("GCTA")
+TABLE = str.maketrans("GCTA", "CGAU")
+
+def to_rna(dna_strand):
+    if not all(c in VALID for c in dna_strand):
+        raise ValueError("Invalid nucleotide in strand")
+    return dna_strand.translate(TABLE)
```

[B] Dict lookup in generator
```diff
+++ rna_transcription.py
@@ -0,0 +1,8 @@
+MAP = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}
+
+def to_rna(dna_strand):
+    try:
+        return ''.join(MAP[c] for c in dna_strand)
+    except KeyError as e:
+        raise ValueError(f"Invalid nucleotide: {e}") from e
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which do you prefer?

### Student

I think I'd go with **Option A**.

Here's my reasoning: the `str.translate()` approach feels cleaner and more efficient since it does the whole conversion in one pass, and separating validation upfront makes the error handling more explicit. With Option B, we're relying on a KeyError to catch bad input, which feels a bit indirect to me.

Also, I like that Option A clearly defines what valid characters are in one place with the `VALID` set, then uses that both for validation and for the translation table.

Should we go ahead and set that up?

---

## Turn 2

### Tutor

Tutor: Worth a quick pushback on one point: Option A is actually **two passes** — the `all(c in VALID ...)` loop walks the string, then `translate()` walks it again. Option B does it in a single pass.

The "EAFP" pattern (Easier to Ask Forgiveness than Permission) is also quite idiomatic in Python — using a `try/except KeyError` isn't indirect, it's the standard style. The dict *is* the single source of truth; valid chars are implicitly defined by its keys.

That said, Option A is totally defensible — the explicit `VALID` set and the separation of concerns are genuinely readable, and `str.translate` is very fast even if it's two passes. Up to you — want to stick with A or switch to B?

### Student

Ah, that's a really good point about the two passes — I wasn't thinking about that carefully enough. And you're right about EAFP being idiomatic Python; I appreciate the reminder that using `try/except KeyError` isn't a workaround, it's just how Python is meant to be used.

I think I'll **switch to Option B**. The single pass is more efficient, and if the dict is our single source of truth for valid mappings anyway, there's no real need to redundantly validate upfront. Plus, learning the EAFP pattern properly is probably good for me.

Let's go with that.

---

## Turn 3

### Tutor

Tutor: Exactly right — and the error message even tells you *which* character was invalid for free. Let's write it:

[Write(rna_transcription.py)]
MAP = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}


def to_rna(dna_strand):
    try:
        return ''.join(MAP[c] for c in dna_strand)
    except KeyError as e:
        raise ValueError(f"Invalid nucleotide: {e}") from e

  File created successfully at: rna_transcription.py

Tutor: Done. A few things worth noting about this implementation:

- **`from e`** — the `raise ... from e` preserves the original `KeyError` as the exception's `__cause__`, giving a clean traceback chain. Without it, Python attaches it as `__context__` (implicit chaining), which is slightly messier.
- **Empty string** — works correctly: `''.join(...)` over an empty iterable returns `""`, no special case needed.
- **The dict is the whole contract** — if you ever add a new valid nucleotide, you update one place and validation + translation both stay correct.

Want to add tests, or is there anything else to refine?

### Student

I think the implementation looks solid. Let me test it mentally against the problem:

- G→C, C→G, T→A, A→U ✓
- Validates input ✓
- Handles edge cases like empty string ✓

I'm satisfied with how it works. I don't need to add tests right now — the problem statement is satisfied, and I learned a lot about the EAFP pattern and why two-pass validation might not always be better even if it's more explicit.

Thanks for pushing back on my initial choice and walking me through the reasoning. That was helpful.

<done/>

---

**Run end:** done after 3 turn(s) in 60.3s
