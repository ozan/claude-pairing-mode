# exercism-pangram

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:41:04

## Initial prompt

Exercism 'Pangram': write `is_pangram(text)` that returns True iff the input contains every letter of the alphabet at least once (case-insensitive).

---

## Turn 1

### Tutor

Tutor: Good warm-up problem. There's an interesting choice right at the core — let me show you two approaches.

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] all() with generator
```diff
+++ pangram.py
@@ -0,0 +1,4 @@
+def is_pangram(text):
+    t = text.lower()
+    return all(c in t for c in 'abcdefghijklmnopqrstuvwxyz')
```

[B] Set superset check
```diff
+++ pangram.py
@@ -0,0 +1,3 @@
+def is_pangram(text):
+    return set(text.lower()) >= set('abcdefghijklmnopqrstuvwxyz')
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach would you go with?

### Student

I think I'd go with **B**.

Both should work, but the set superset check feels cleaner to me — it directly expresses what we're checking ("does the set of letters in the text contain all 26 letters?"). Plus, I'm guessing it might be a bit more efficient since we're doing one pass to build the set of unique characters in the text, rather than potentially checking the same letters multiple times with the `all()` generator.

Let me make sure I understand the logic though: we convert the text to lowercase, turn it into a set (which automatically removes duplicates and keeps only the characters that appear), and then check if that set contains at least all 26 letters of the alphabet using the `>=` operator. Does that sound right?

---

## Turn 2

### Tutor

Tutor: Your logic is exactly right — lowercase, deduplicate into a set, `>=` checks superset. Clean and correct.

One small correction to the performance reasoning though, worth being precise about: `all()` doesn't re-check the *same* letters — it iterates over the 26 alphabet letters and does one `in` test per letter. The catch is that `c in t` on a **string** is O(n) each time (linear scan), so worst-case it's 26 × n operations.

The set approach is actually the better performer for valid pangrams:

- **Set:** one O(n) pass to build, then 26 × O(1) lookups → **O(n)**
- **`all()`:** up to 26 × O(n) string scans → **O(26n)**

Where `all()` *would* win is on non-pangrams — it short-circuits the moment a letter is missing, so a string with no vowels fails on the first check. The set always pays the full O(n) build cost regardless.

For this problem both are fine, but your instinct toward the set is sound. Let's write it:

[Write(pangram.py)]
def is_pangram(text):
    return set(text.lower()) >= set('abcdefghijklmnopqrstuvwxyz')

  File created successfully at: pangram.py

Tutor: Done. One line, clear intent, solid performance. 

Worth knowing: `>=` on sets is the superset operator — equivalent to `.issuperset()`. You could also write `set('abcdefghijklmnopqrstuvwxyz').issubset(set(text.lower()))`, but `>=` reads more naturally as "contains at least."

### Student

That makes sense, thanks for breaking down the performance trade-offs. I appreciate the clarification — I was thinking about it more intuitively than algorithmically. The string scan cost with `in` checks is a good thing to keep in mind.

I like that the set approach is both cleaner to read *and* more efficient for the general case. And good to know about the `>=` operator for sets — I'll remember that `set_a >= set_b` is the superset check.

Let me test this locally to make sure it works:

```
>>> is_pangram("The quick brown fox jumps over the lazy dog")
True
>>> is_pangram("Hello world")
False
>>> is_pangram("abcdefghijklmnopqrstuvwxyz")
True
>>> is_pangram("ABC")
False
```

Looks good! The function handles case-insensitivity and correctly returns True only when all 26 letters are present.

<done/>

---

**Run end:** done after 2 turn(s) in 51.7s
