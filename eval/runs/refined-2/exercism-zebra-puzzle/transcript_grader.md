# exercism-zebra-puzzle

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:24:52

## Initial prompt

Exercism 'Zebra Puzzle': solve the classic 5-houses constraint puzzle (Englishman/red house, Spaniard/dog, etc.) and return who drinks water and who owns the zebra. Use itertools.permutations or a constraint solver.

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Tutor: Before writing any code, let's nail the search strategy. The puzzle has 5 attributes × 5 houses — that's 5 values each. Which approach do we take?

OPTIONS:
[A] Flat brute force
Generate all `(5!)^5` combinations upfront, then filter by all 14 clues at the end.

```diff
+++ zebra_puzzle.py
@@ -0,0 +1,7 @@
+from itertools import permutations, product
+
+def solve():
+    attrs = [permutations(range(5)) for _ in range(5)]
+    for combo in product(*attrs):
+        nat, color, drink, smoke, pet = combo
+        if check_all_clues(nat, color, drink, smoke, pet):
+            return answer(nat, drink, pet)
```

[B] Nested loops, prune early
Nest `permutations` loops and apply relevant clues *inside* each loop level before going deeper.

```diff
+++ zebra_puzzle.py
@@ -0,0 +1,8 @@
+from itertools import permutations
+
+def solve():
+    for color in permutations(range(5)):
+        if not color_clues(color): continue
+        for nat in permutations(range(5)):
+            if not nat_clues(nat, color): continue
+            # ... drink, smoke, pet loops
```

(Reply with A or B, or ask a follow-up question.)

Tutor: `5! = 120` permutations per attribute — how many total combinations does option A actually need to check?

### Student

Let me think through this...

Option A generates all permutations independently for each of the 5 attributes. That's `(5!)^5` total combinations to check before filtering.

So that's `120^5` = `24,883,200,000` combinations to check upfront before we even apply a single clue. That's a lot of wasted work if we can eliminate invalid branches earlier.

Option B sounds much smarter — we'd apply clues as we build up each attribute, so we never explore branches that are already known to be invalid. We'd prune the search space dramatically before we get to the later attributes.

I think I should go with **B**. Early pruning seems way more efficient for this constraint problem.

---

## Turn 2

### Tutor

Tutor: Exactly right — 24.8 billion vs. a few thousand. Good reasoning.

Now, within the nested approach, loop order matters. Which attribute should be the **outermost** loop?

OPTIONS:
[A] Color outermost
Put `color` in the outermost loop. Clue 5 says the green house is *immediately right* of the ivory house — only 4 of 120 color permutations satisfy this.

[B] Nationality outermost
Put `nationality` in the outermost loop. It feels natural as the "main" attribute, and clue 9 (Norwegian in house 1) does constrain it significantly.

(Reply with A or B, or ask a follow-up question.)

Tutor: How many valid permutations does each clue leave for its attribute?

### Student

Good question. Let me think about the pruning power of each:

**Color (Clue 5):** "Green house is immediately right of ivory house"
- Out of 120 permutations, only 4 satisfy this (ivory at position 0 with green at 1, ivory at 1 with green at 2, etc.)
- That's massive pruning — we'd eliminate 116 invalid permutations right away.

**Nationality (Clue 9):** "Norwegian in house 1"
- This constrains the Norwegian to a specific position, but doesn't fully order the nationality permutation.
- We'd still have `4! = 24` valid permutations (the remaining 4 nationalities in the remaining 4 positions).
- Much less pruning than color.

So **A** is the way to go. Starting with color as the outermost loop gives us the tightest initial filter — we only keep 4 out of 120 permutations before moving deeper into the nested loops. That eliminates way more branches early on.

---

## Turn 3

### Tutor

Tutor: Nailed it — the MRV (Most Restricted Variable) heuristic. Color's 4/120 vs Nationality's 24/120 means color as the outer loop cuts inner work by 6×.

Now let's write the actual code. One small but real design question before we do — how should the adjacency helpers work?

OPTIONS:
[A] Helpers take house indices
```diff
+++ zebra_puzzle.py
@@ -0,0 +1,6 @@
+def next_to(h1, h2):
+    return abs(h1 - h2) == 1
+
+def right_of(h1, h2):
+    return h1 - h2 == 1
+# usage: next_to(nat.index(Norwegian), color.index(Blue))
```

[B] Helpers take values + perm
```diff
+++ zebra_puzzle.py
@@ -0,0 +1,6 @@
+def next_to(a, b, perm):
+    return abs(perm.index(a) - perm.index(b)) == 1
+
+def right_of(a, b, perm):
+    return perm.index(a) - perm.index(b) == 1
+# usage: next_to(Norwegian, Blue, ???)
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Consider clue 14: *"The Norwegian lives next to the blue house."* Norwegian comes from `nat`, blue from `color` — which helper signature handles that?

### Student

Ah, that's the key insight. Clue 14 involves two *different* attributes — Norwegian is a value in the `nat` permutation, and Blue is a value in the `color` permutation.

With option A, I'd need to do:
```python
next_to(nat.index(Norwegian), color.index(Blue))
```

This works because I'm converting both values to their house positions (indices in their respective permutations), then comparing those positions.

With option B, I'd need to pass the permutation(s), but which one? Norwegian is in `nat` and Blue is in `color` — I'd need both permutations, not just one. The signature breaks down.

So **A** is the right design. The helpers work on house indices (positions), which are universal across all attributes. I can mix and match values from different permutations by looking up their indices.

That makes sense — the constraint is about *positions in the house lineup*, not about which attribute a value belongs to.

---

## Turn 4

### Tutor

Tutor: Exactly — positions are the common currency. House indices let you join across attributes cleanly.

One more design question before we write the full solution. The Exercism interface wants two separate functions: `drinks_water()` and `owns_zebra()`. How should they share the work?

OPTIONS:
[A] Solve once, cache result
```diff
+++ zebra_puzzle.py
@@ -0,0 +1,6 @@
+from functools import lru_cache
+
+@lru_cache(maxsize=None)
+def _solution():
+    ...  # nested permutation search
+    return water_drinker, zebra_owner
```
`drinks_water()` and `owns_zebra()` each call `_solution()` and unpack.

[B] Each function solves independently
```diff
+++ zebra_puzzle.py
@@ -0,0 +1,6 @@
+def drinks_water():
+    for color in permutations(...):
+        ...  # full search
+
+def owns_zebra():
+    for color in permutations(...):
+        ...  # full search again
```

(Reply with A or B, or ask a follow-up question.)

### Student

This is straightforward — **A** is the way to go.

Option B would solve the entire puzzle *twice*, doing all that constraint checking and permutation work from scratch each time. That's wasteful.

Option A solves it once, caches the result, and both `drinks_water()` and `owns_zebra()` just call the cached `_solution()` function and extract what they need. The second call gets the cached result instantly.

Since the puzzle has a unique solution and it's deterministic, caching makes perfect sense. We do the hard work once and reuse it.

---

## Turn 5

### Tutor

Tutor: Right. Now let's build the whole thing. All decisions are locked in:

- Color outermost (4 valid perms), prune inside each level
- `next_to`/`right_of` on house indices
- `lru_cache` on a private `_solution()`

[Glob(zebra_puzzle.py)]
  No files found

[Write(zebra_puzzle.py)]
from itertools import permutations
from functools import lru_cache

# Each permutation is indexed by house (0 = leftmost).
# perm[house] = attribute_value   →   perm.index(value) = house number

Red, Green, Ivory, Yellow, Blue = range(5)
Englishman, Spaniard, Ukrainian, Norwegian, Japanese = range(5)
Coffee, Tea, Milk, OrangeJuice, Water = range(5)
OldGold, Kools, Chesterfields, LuckyStrike, Parliaments = range(5)
Dog, Snail, Fox, Horse, Zebra = range(5)

… (80 more lines)
  File created successfully at: zebra_puzzle.py

[Bash(cd /root && python -c "
from zebra_puzzle import drinks_water, owns_zebra
print('Drinks water:', drinks_water())
print('Owns zebra:  ', owns_zebra())
")]
  error: Exit code 1

[Bash(python -c "
from zebra_puzzle import drinks_water, owns_zebra
print('Drinks water:', drinks_water())
print('Owns zebra:  ', owns_zebra())
")]
  Drinks water: Norwegian
  Owns zebra:   Japanese

Tutor: It works. Here's the final structure:

```
color loop      →  4 pass  (clue 5: green right of ivory)
  nat loop      →  ~2 pass (clues 9, 1, 14)
    drink loop  →  ~2 pass (clues 8, 3, 4)
      smoke loop→  ~2 pass (clues 7, 13, 12)
        pet loop→  1 pass  (clues 2, 6, 10, 11)
```

Instead of 24.8 billion candidates, we explore a few thousand at most.

**The answer:** The **Norwegian** drinks water, the **Japanese** owns the zebra.

One thing worth noting: `nat[0] != Norwegian` (clue 9) lets us replace `nat.index(Norwegian)` with the literal `0` in clue 14 — a small but clean simplification since Norwegian's house is always known to be `0` by the time we check it.

### Student

That's a great point about the simplification. Since clue 9 locks Norwegian into house 0, we could hardcode that constraint and skip the index lookup in clue 14. That's a nice optimization that makes the code slightly faster and clearer — we're leveraging what we've already established rather than redundantly looking it up.

The pruning structure is really satisfying to see laid out:
- Start with 4 valid color permutations
- Nest nationality checks (down to ~2 per color)
- Nest drink checks (down to ~2 per nationality)
- And so on...

Going from 24.8 *billion* candidates down to a few thousand by applying constraints incrementally is exactly why the nested-loop approach with early pruning beats flat brute force.

I feel like I've got a solid understanding of the strategy now:
1. Identify the most constrained attribute first (color, via the adjacency clue)
2. Use house indices as the universal currency for joining constraints across attributes
3. Nest loops and prune at each level
4. Cache the result so both output functions reuse it

The solution is correct — Norwegian drinks water, Japanese owns the zebra. Thanks for walking through the design decisions before jumping into code; it made the actual implementation much clearer.

<done/>

---

**Run end:** done after 5 turn(s) in 177.6s
