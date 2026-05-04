# exercism-rna-transcription

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:24:23

## Initial prompt

Exercism 'RNA Transcription': convert a DNA strand to its RNA complement. G→C, C→G, T→A, A→U. Validate input characters.

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Dict + comprehension
```diff
+++ rna_transcription.py
@@ -0,0 +1,8 @@
+MAP = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}
+
+def to_rna(dna_strand):
+    result = []
+    for ch in dna_strand:
+        if ch not in MAP:
+            raise ValueError(f"Invalid nucleotide: {ch!r}")
+        result.append(MAP[ch])
+    return ''.join(result)
```

[B] str.translate
```diff
+++ rna_transcription.py
@@ -0,0 +1,8 @@
+TABLE = str.maketrans('GCTA', 'CGAU')
+VALID = frozenset('GCTA')
+
+def to_rna(dna_strand):
+    if invalid := set(dna_strand) - VALID:
+        raise ValueError(f"Invalid nucleotide(s): {invalid}")
+    return dna_strand.translate(TABLE)
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Two approaches — which do you prefer?

### Student

I think I'll go with **[A]** for now.

The dict + comprehension approach feels more straightforward to me — I can clearly see the mapping from DNA to RNA, and the validation logic with the loop is easy to follow. Each character gets checked and mapped one at a time, which makes sense for this problem.

I'm curious about option B though — what's the advantage of `str.translate` and `maketrans`? Is it just faster for really long strands, or is there something else I'm missing? And that walrus operator (`invalid := ...`) — I've seen it before but don't use it much yet. Would it be worth learning for this, or is it more of a "nice to have"?

But yeah, let's go with A and get this working first.

---

## Turn 2

### Tutor

Tutor: Good choice to start readable. On your questions:

- **`str.translate`** isn't just faster — it's the Python idiom *built for* character-level substitution. For a 1M-nucleotide strand it can be ~10× faster because it runs in C with no per-character Python overhead. Worth knowing it exists.
- **The walrus operator** (`:=`) is genuinely useful when you want to assign *and* test in the same `if`. Here: `if invalid := set(dna_strand) - VALID` — avoids a separate assignment line. Nice to have, not essential.

Let's build option A:

[Glob(rna_transcription.py)]
  No files found

[Write(rna_transcription.py)]
MAP = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}

def to_rna(dna_strand):
    result = []
    for ch in dna_strand:
        if ch not in MAP:
            raise ValueError(f"Invalid nucleotide: {ch!r}")
        result.append(MAP[ch])
    return ''.join(result)

  File created successfully at: rna_transcription.py

Tutor: That's working code. Now a refinement worth thinking about — the loop currently validates and translates in one pass. There's an alternative structure:

OPTIONS:
[A] Single pass validate + build
Keep as-is: one loop checks and appends. Fails on the **first** bad character, immediately.

```diff
+++ rna_transcription.py
@@ -3,6 +3,6 @@
 def to_rna(dna_strand):
     result = []
     for ch in dna_strand:
         if ch not in MAP:
             raise ValueError(f"Invalid nucleotide: {ch!r}")
         result.append(MAP[ch])
     return ''.join(result)
```

[B] Validate first then translate
Two passes: validate the whole strand up front, then use a clean generator to build the result.

```diff
+++ rna_transcription.py
@@ -3,6 +3,7 @@
 def to_rna(dna_strand):
+    invalid = set(dna_strand) - set(MAP)
+    if invalid:
+        raise ValueError(f"Invalid nucleotide(s): {invalid}")
-    result = []
-    for ch in dna_strand:
-        if ch not in MAP:
-            raise ValueError(f"Invalid nucleotide: {ch!r}")
-        result.append(MAP[ch])
-    return ''.join(result)
+    return ''.join(MAP[ch] for ch in dna_strand)
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which structure do you prefer — and why might one outperform the other on a very long invalid strand?

### Student

Oh, interesting question. Let me think through this...

Option A fails fast — as soon as it hits a bad character, it stops and raises. That's good for short invalid strands.

But option B validates the *whole* strand first, then translates. On a very long invalid strand, option A would catch the error early and bail out, which seems better. But option B would scan the entire thing before raising...

Wait, actually — I think I see the trade-off. If the strand is long and invalid, option A stops immediately (good). But if the strand is long and *valid*, option B might be more efficient because it does two clean passes (one validation sweep, one translation sweep) instead of checking `ch not in MAP` for every single character during the loop.

Hmm, but actually for a long invalid strand, option A wins — it doesn't waste time translating characters that will never be used.

I think I'll go with **[A]** — the fail-fast behavior makes sense, and I like that the code is simpler (no separate validation phase). Plus, if the input is bad, why build the result at all?

Am I thinking about this right?

---

## Turn 3

### Tutor

Tutor: Your reasoning is mostly right — nice analysis. One small correction though: for a **valid** strand, option B is actually *slower*, not faster. It still iterates the whole strand twice (once to build the set, once to translate), while option A does a single pass with one `dict` lookup per character. There's no free lunch in the two-pass approach.

So option A wins in both cases:
- **Invalid strand** → fails fast, stops early ✓
- **Valid strand** → single pass, less work ✓

Your instinct was right, the reasoning just needed a small adjustment. The code stands as-is:

[Read(rna_transcription.py)]
  1	MAP = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}
  2	
  3	def to_rna(dna_strand):
  4	    result = []
  5	    for ch in dna_strand:
  6	        if ch not in MAP:
  7	            raise ValueError(f"Invalid nucleotide: {ch!r}")
  8	        result.append(MAP[ch])
  9	    return ''.join(result)
  10

Tutor: Clean and done. A few edge cases worth verifying manually:

- `to_rna("GCTA")` → `"CGAU"` ✓  
- `to_rna("")` → `""` ✓ (empty strand, loop never runs)
- `to_rna("GXTA")` → `ValueError: Invalid nucleotide: 'X'` ✓
- lowercase `"a"` → also raises, since `MAP` only has uppercase keys

That last one is worth a conscious decision: Exercism's test suite expects the raise on lowercase, which you get for free here. The `!r` in the error message (`{ch!r}`) is a nice touch — it shows quotes around the character, making it unambiguous in the output.

### Student

Thanks for the clarification — that makes total sense now. I was confusing "two passes" with "two efficient passes," but yeah, you're still iterating the whole string twice no matter what, so option A is strictly better.

I like how the code handles those edge cases naturally:
- Empty strand works because the loop just doesn't run
- Lowercase fails automatically because the keys are uppercase only
- The `!r` in the error message is a small detail but really useful for debugging

I feel confident about this solution. It's readable, efficient, validates correctly, and handles the cases the problem expects. 

<done/>

---

**Run end:** done after 3 turn(s) in 83.3s
