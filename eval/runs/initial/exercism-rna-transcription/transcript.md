# exercism-rna-transcription

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:01:04

## Initial prompt

Exercism 'RNA Transcription': convert a DNA strand to its RNA complement. G→C, C→G, T→A, A→U. Validate input characters.

---

## Turn 1

### Tutor

Thinking: The user wants to solve the Exercism "RNA Transcription" problem. Let me start by checking if there's an existing file, then propose a design decision to make it educational.
  
  The problem is:
  - Convert DNA to RNA complement
  - G→C, C→G, T→A, A→U
  - Validate input characters
  
  Let me first check if there's an existing file, then think about what would make a good teaching moment here.
  
  Key design decisions:
  1. Language choice - they didn't specify, I'll go with Python
  2. How to handle the mapping and validation - good teaching opportunity here
  
  For the mapping, I could propose:
  - Option A: Use `str.translate()` with a translation table
  
  
  - Option B: Use a dict lookup in a loop
  
  `str.translate()` is the Pythonic, efficient approach for character-by-character substitution, while a dict loop is more explicit but less idiomatic. I'll lean toward `str.translate()` as the cleaner solution. For validation, I can either check upfront that all characters are valid DNA bases, or let the dict approach handle it by raising an error on unknown characters. Let me check if any file exists first.

[Glob(rna_transcription*)]
  No files found

Tutor: No existing file — let's start from scratch. First design question before I write anything:

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Thinking: Now let me propose two options for how to implement the character mapping and validation. This is a good teaching moment about Python's `str.translate()` vs a dict-based loop.
  
  Option A: `str.translate()` with `maketrans`
  Option B: A dict lookup in a generator/loop
  
  Let me think about which is better:
  - `str.translate()` is O(n) and very fast, very Pythonic for character-by-character substitution
  - A dict loop is also O(n) but has more overhead per character
  - Both can handle validation, but the approaches differ
  
  For validation with `str.translate()`, you need to either pre-validate or check for unmapped characters. 
  
  I'm realizing that `str.translate()` leaves unmapped characters alone by default when using a dict, or you can delete them with `None`, but for strict validation where I need to raise errors on invalid input, a loop with explicit dictionary lookups is actually clearer and more straightforward than trying to validate after translation.
  
  Let me settle on two solid approaches: Option A uses `str.translate()` for speed and Pythonic style but requires separate validation logic, while Option B uses a dict comprehension with explicit key lookups that naturally catches invalid characters and raises errors. I'm leaning toward Option B because the validation integrates seamlessly with the transformation itself, whereas `str.translate()` would pass through unmapped characters unless I add extra validation steps. validation and error handling together. I'll go with option B—using a generator expression with dictionary lookup that naturally converts KeyError to ValueError when an invalid character is encountered.

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

PRIVATE: best=B
PRIVATE: rationale=The dict/generator approach is cleaner because validation and translation are unified — an invalid character naturally raises KeyError which we convert to ValueError. The str.translate approach requires two passes (validate then translate), and str.translate actually silently passes through unmapped characters by default, making it easy to accidentally skip validation. The dict approach is also more readable — the mapping is explicit and obvious. str.translate shines for performance on very large strings, but that's not a concern here.

Tutor: Which do you prefer?

### Student

I think I'd go with **Option A**.

Here's my reasoning: the `str.translate()` approach feels cleaner and more efficient since it does the whole conversion in one pass, and separating validation upfront makes the error handling more explicit. With Option B, we're relying on a KeyError to catch bad input, which feels a bit indirect to me.

Also, I like that Option A clearly defines what valid characters are in one place with the `VALID` set, then uses that both for validation and for the translation table.

Should we go ahead and set that up?

---

## Turn 2

### Tutor

Thinking: The user picked Option A. Let me share my reasoning briefly - I prefer B, so I should explain why without being preachy, and give them a chance to switch or proceed.
  
  Key points to make:
  1. `str.translate()` is actually ONE pass, but the pre-validation loop is a SECOND pass, so it's actually two passes total (not one pass as they stated)
  2. KeyError→ValueError is actually idiomatic Python ("ask forgiveness not permission" / EAFP style)
  3. However, Option A is totally reasonable and their `VALID` set point is a good one
  
  I should be concise and let them decide.

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

Thinking: The user switched to Option B. Now I should write the file with Option B's implementation. Let me do that.

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
