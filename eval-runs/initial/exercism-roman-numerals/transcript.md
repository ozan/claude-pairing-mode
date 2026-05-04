# exercism-roman-numerals

- Source: `exercism`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:38:59.842Z

---

## Turn 1

**User:**

Exercism 'Roman Numerals': write `to_roman(n)` for 1 ≤ n ≤ 3999. Use subtractive notation (IV, IX, XL, XC, CD, CM).

**Pair:**

Assistant: Good problem. The core design question is what goes in the lookup table. Both options below use the same greedy loop — the difference is in the table itself:

Assistant: Let me just present the two approaches directly and ask which you'd go with:

**Option A — 7-symbol table** (the "natural" Roman symbols only):

```diff
+++ roman_numerals.py
@@ -0,0 +1,11 @@
+NUMERALS = [
+    (1000,'M'),(500,'D'),(100,'C'),
+    (50,'L'),(10,'X'),(5,'V'),(1,'I'),
+]
+
+def to_roman(n):
+    result = ''
+    for value, numeral in NUMERALS:
+        while n >= value:
+            result += numeral
+            n -= value
+    return result
```

**Option B — 13-symbol table** (includes the subtractive pairs as explicit entries):

```diff
+++ roman_numerals.py
@@ -0,0 +1,13 @@
+NUMERALS = [
+    (1000,'M'),(900,'CM'),(500,'D'),(400,'CD'),
+    (100,'C'),(90,'XC'),(50,'L'),(40,'XL'),
+    (10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I'),
+]
+
+def to_roman(n):
+    result = ''
+    for value, numeral in NUMERALS:
+        while n >= value:
+            result += numeral
+            n -= value
+    return result
```

Which would you go with, and why?

---

## Turn 2

**User:**

I'd go with **Option B** — and let me walk through why I think Option A has a problem.

Let me trace through what happens with a small example in Option A. Say `n = 4`:

```
NUMERALS ordered: (1000,'M'), (500,'D'), (100,'C'), (50,'L'), (10,'X'), (5,'V'), (1,'I')

n=4:
  - 4 >= 1000? No
  - 4 >= 500? No
  - ... (skip non-matches)
  - 4 >= 5? No
  - 4 >= 1? Yes → result = 'I', n = 3
  - 3 >= 1? Yes → result = 'II', n = 2
  - 2 >= 1? Yes → result = 'III', n = 1
  - 1 >= 1? Yes → result = 'IIII', n = 0
```

Returns `'IIII'` — but we need `'IV'`.

The greedy algorithm only works if the table *already contains* the subtractive pairs. Without them explicitly listed (and ordered), there's no way the loop can pick up `(4, 'IV')` when it encounters `n=4`.

**Option B** solves this by including all 13 entries—the 7 base symbols *plus* the 6 subtractive pairs—in descending order. Now `n=4` immediately matches `(4, 'IV')` and returns the right answer.

So **I'd pick Option B**. It's the approach that actually works. Should I write it to a file?

**Pair:**

Assistant: Exactly right — the greedy algorithm can only "see" what's in the table. Without `(4, 'IV')` as an explicit entry, it has no way to emit `IV`. Nice trace.

Let me write it out:

[Glob(roman_numerals.py)]
  No files found

[Write(roman_numerals.py)]
NUMERALS = [
    (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
    (100,  'C'), (90,  'XC'), (50,  'L'), (40,  'XL'),
    (10,   'X'), (9,   'IX'), (5,   'V'), (4,   'IV'),
    (1,    'I'),
]

def to_roman(n):
    result = ''
    for value, numeral in NUMERALS:
        while n >= value:
            result += numeral
… (3 more lines)

Assistant: Done. A couple of quick sanity checks worth running mentally:

- `to_roman(4)` → hits `(4,'IV')` immediately → `'IV'` ✓  
- `to_roman(1994)` → `M` (994 left) → `CM` (94 left) → `XC` (4 left) → `IV` → `'MCMXCIV'` ✓  
- `to_roman(3999)` → `MMM` + `CM` + `XC` + `IX` → `'MMMCMXCIX'` ✓  

One small thing worth noticing: the 6 subtractive pairs aren't arbitrary — they're always `value = next_higher - smallest_in_same_tier`. That's why there are exactly 6: one for each "demotion" (I→V, I→X, X→L, X→C, C→D, C→M). The table encodes the *rules* of Roman numeral construction implicitly through ordering and value choice.

Want to add tests, or move on to something else?

---

## Turn 3

**User:**

The core problem is solved and working. Tests would be nice for confidence, but they're not required by the problem statement.

Quick question: Do you want to add tests here, or are you satisfied with the solution as-is? If you're just exploring the problem and moving on to the next one, we can leave it as-is. If you want to be thorough (good practice), I can write a few test cases covering the edge cases and a couple of mid-range numbers.

What sounds right to you?

**Pair:**

Assistant: Ha — that's my line! You're the one deciding. But since you asked: I'd add a small test file. Not because the problem requires it, but because Roman numeral conversion has a handful of well-known edge cases, and a few targeted assertions make a much better safety net than eyeballing traces.

The interesting cases to hit are:

- **Boundary values**: 1, 3999
- **All 6 subtractive pairs**: 4, 9, 40, 90, 400, 900
- **A mid-range composite**: something like 1994 (`MCMXCIV`) that chains several subtractive forms

Want me to write that? It'd be maybe 15 lines with `unittest` or plain `assert`s — your preference on style.

---

## Turn 4

**User:**

Two quick testing approaches — pick the one that feels right:

**Option A — Plain asserts** (minimal, quick):
```diff
+++ test_roman_numerals.py
@@ -0,0 +1,20 @@
+from roman_numerals import to_roman
+
+def test_to_roman():
+    # Boundaries
+    assert to_roman(1) == 'I'
+    assert to_roman(3999) == 'MMMCMXCIX'
+    
+    # All 6 subtractive pairs
+    assert to_roman(4) == 'IV'
+    assert to_roman(9) == 'IX'
+    assert to_roman(40) == 'XL'
+    assert to_roman(90) == 'XC'
+    assert to_roman(400) == 'CD'
+    assert to_roman(900) == 'CM'
+    
+    # Mid-range composites
+    assert to_roman(1994) == 'MCMXCIV'
+    assert to_roman(58) == 'LVIII'
+    
+if __name__ == '__main__':
+    test_to_roman()
+    print('All tests passed')
```

**Option B — unittest** (more structured, better for growing):
```diff
+++ test_roman_numerals.py
@@ -0,0 +1,25 @@
+import unittest
+from roman_numerals import to_roman
+
+class TestToRoman(unittest.TestCase):
+    def test_boundaries(self):
+        self.assertEqual(to_roman(1), 'I')
+        self.assertEqual(to_roman(3999), 'MMMCMXCIX')
+    
+    def test_subtractive_pairs(self):
+        pairs = [(4, 'IV'), (9, 'IX'), (40, 'XL'),
+                 (90, 'XC'), (400, 'CD'), (900, 'CM')]
+        for num, expected in pairs:
+            self.assertEqual(to_roman(num), expected)
+    
+    def test_mid_range_composites(self):
+        self.assertEqual(to_roman(1994), 'MCMXCIV')
+        self.assertEqual(to_roman(58), 'LVIII')
+
+if __name__ == '__main__':
+    unittest.main()
```

Which style appeals to you?

**Pair:**

Assistant: For a single-file exercise, **Option A**. The `unittest` scaffolding earns its keep when you have fixtures, `setUp`/`tearDown`, or a suite of test classes — none of which apply here. Plain asserts are less noise for the same signal.

One small improvement: `assert` failures give you nothing but `AssertionError`. If you ever want to see *what* value came back, `pytest`-style asserts (just run `pytest test_roman_numerals.py`) rewrite them to show the diff automatically — no code change needed.

[Glob(test_roman_numerals.py)]
  No files found

[Write(test_roman_numerals.py)]
from roman_numerals import to_roman

def test_to_roman():
    # Boundaries
    assert to_roman(1) == 'I'
    assert to_roman(3999) == 'MMMCMXCIX'

    # All 6 subtractive pairs
    assert to_roman(4) == 'IV'
    assert to_roman(9) == 'IX'
    assert to_roman(40) == 'XL'
    assert to_roman(90) == 'XC'
… (11 more lines)

[Bash(cd "$(dirname $(find . -name roman_numerals.py | head -1))" && python test_roman_numerals.py)]
  error: Exit code 127

[Bash(python3 test_roman_numerals.py)]
  All tests passed

Assistant: All green. You've got `roman_numerals.py` with the 13-entry greedy table and a tight test file covering boundaries, all 6 subtractive pairs, and composites. Ready for the next Exercism problem whenever you are.

---

## Turn 5 (final)

**User:**

Perfect wrap-up. The solution is solid, well-tested, and you've got a clear mental model of why the greedy approach with the 13-entry table is the right design here.

A few takeaways worth carrying forward:
- **Greedy algorithms need the right state space** — the algorithm can only "see" what's explicitly in your lookup table.
- **Ordering matters** — descending value order lets you match larger values first, which is essential for the greedy choice to be correct.
- **Test the edge cases, not just the happy path** — Roman numeral conversion has 6 specific subtractive rules; hitting all of them in tests means you've validated the hard part.

<done/>

---

**Run end**: done after 4 turns (148s)
