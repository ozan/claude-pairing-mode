# exercism-rna-transcription

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:52:05

## Initial prompt

Exercism 'RNA Transcription': convert a DNA strand to its RNA complement. G→C, C→G, T→A, A→U. Validate input characters.

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] str.translate approach
```diff
+++ rna_transcription.py
@@ -0,0 +1,5 @@
+_TABLE = str.maketrans("GCTA", "CGAU")
+
+def to_rna(dna_strand):
+    if invalid := set(dna_strand) - set("GCTA"):
+        raise ValueError(f"Invalid nucleotide(s): {invalid}")
+    return dna_strand.translate(_TABLE)
```

[B] Dict comprehension approach
```diff
+++ rna_transcription.py
@@ -0,0 +1,8 @@
+_MAP = {"G": "C", "C": "G", "T": "A", "A": "U"}
+
+def to_rna(dna_strand):
+    result = []
+    for nucleotide in dna_strand:
+        if nucleotide not in _MAP:
+            raise ValueError(f"Invalid nucleotide: {nucleotide}")
+        result.append(_MAP[nucleotide])
+    return "".join(result)
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach do you prefer?

### Student

I think I'd like to understand both a bit better before choosing. Let me ask a couple of questions:

For option A, I see it uses `str.maketrans` and `translate`. That looks pretty concise, but I'm not totally familiar with how `maketrans` works. Does it create a mapping table that `translate` then uses to swap characters all at once?

And for option B, it's more explicit — we loop through each character, check if it's valid, and build the result. That feels easier to follow, but it seems like it might be slower for very long DNA strands since we're doing validation and mapping character-by-character.

Also, I noticed option A uses a walrus operator (`:=`) in the validation check. Is that just a style thing, or does it actually help here?

Before I pick, maybe you could clarify what happens if the input is empty? Both should handle that fine, right?

---

## Turn 2

### Tutor

Tutor: Great questions — let me go through them:

**`str.maketrans` / `translate`:** Yes, exactly. `maketrans("GCTA", "CGAU")` builds a dict mapping each character's Unicode ordinal to its replacement. `translate` then walks the string at the C level using that table — no Python loop. It's one pass through the string, very fast.

**Speed:** Your intuition is right. Option B pays Python interpreter overhead per character — function call dispatch, dict lookup, list append. For a 10-char strand it's imperceptible; for a 10M-char genomic sequence, `translate` is meaningfully faster (typically 5–10×).

**Walrus operator:** More than style. Without it you'd write:
```python
invalid = set(dna_strand) - set("GCTA")
if invalid:
    raise ValueError(...)
```
The walrus does the assignment *inside* the `if`, so it's one statement instead of two. It's also a signal to the reader that `invalid` only matters if it's truthy — the variable has no life outside that branch.

**Empty input:** Both handle it correctly. In A, `set("") - set("GCTA")` is an empty set → falsy → no error, and `"".translate(...)` returns `""`. In B, the loop body never executes. So `to_rna("")` → `""` in both cases, which is the right answer.

One subtle difference worth knowing: if the input has *multiple* invalid characters, Option A reports them **all at once** (as a set, so unordered), while Option B reports only the **first** one it encounters (in order). Depending on what error UX you want, either can be preferable.

Ready to pick one?

### Student

That's really helpful — thank you. I think I'll go with **option A**.

Here's my reasoning: the `str.translate` approach is more elegant and efficient, especially if someone later runs this on real genomic data. I like that it validates the entire input upfront and reports all invalid characters together, which feels more thorough. And honestly, learning to use `maketrans` and `translate` is a good skill to add to my toolkit — I haven't used them before, so this is a nice chance to get comfortable with them.

The walrus operator is also a nice touch. I can see how it makes the intent clearer — the `invalid` set is created and tested in one expression, which signals that it's only relevant in that conditional branch.

Let me go ahead and implement option A and run it against the test cases to make sure it works.

<done/>

---

**Run end:** done after 2 turn(s) in 40.2s
