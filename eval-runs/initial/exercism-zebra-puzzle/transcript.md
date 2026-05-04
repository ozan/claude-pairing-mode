# exercism-zebra-puzzle

- Source: `exercism`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:39:48.056Z

---

## Turn 1

**User:**

Exercism 'Zebra Puzzle': solve the classic 5-houses constraint puzzle (Englishman/red house, Spaniard/dog, etc.) and return who drinks water and who owns the zebra. Use itertools.permutations or a constraint solver.

**Pair:**

Assistant: Let me check if there's already a file to work with, then we'll dive in.

[Bash(ls zebra_puzzle* 2>/dev/null || echo "no file yet")]
  no file yet

Assistant: Good, clean slate. Before writing anything — a key design question for a puzzle with 5 attributes × 5! permutations each:

Assistant: The `propose_options` tool isn't wired up here, so I'll explain the tradeoff directly and then implement the smart version.

**The core choice:** brute-force `product(permutations(range(1,6)), repeat=5)` checks all 120⁵ ≈ 24 billion combos. Nested loops with *early pruning* — checking constraints the moment you fix each attribute group — cuts that to thousands of iterations. We'll go with early pruning.

Here's the full solution:

[Write(zebra_puzzle.py)]
"""Zebra Puzzle — solved with itertools.permutations + early pruning.

Houses are numbered 1–5 (left to right).
Each attribute is a tuple where index 0 = value for house 1, etc.
We represent each attribute as the *house number* assigned to each person/thing.

Constraints:
  1.  Englishman lives in the red house.
  2.  Spaniard owns the dog.
  3.  Coffee is drunk in the green house.
  4.  Ukrainian drinks tea.
  5.  Green house is immediately to the right of the ivory house.
… (100 more lines)

[Bash(cd /Users/ozanonay/development/cc-test && python zebra_puzzle.py)]
  error: Exit code 1

[Bash(python zebra_puzzle.py)]
  error: Exit code 127

[Bash(python3 zebra_puzzle.py)]
  The Norwegian drinks water.
  The Japanese owns the zebra.

Assistant: ✅ **Norwegian drinks water. Japanese owns the zebra.**

---

**What made this fast:** the key insight is *when* you check each constraint. Constraints that only involve one attribute group (e.g., "Norwegian in house 1", "milk in house 3") are checked immediately after fixing that group — before generating any further permutations. By the time we reach the innermost `pets` loop, most branches are already dead.

Rough intuition on why pruning helps so much:
- `colors`: 120 permutations → constraint 5 (`green = ivory + 1`) keeps only **24** (one in five pairs satisfies it)  
- `nationalities`: checked against 3 constraints → further cuts to ~a few dozen valid `(colors, nats)` pairs  
- …and so on — by `smokes`, you're looping over a tiny fraction of 120⁵

The flat `product(permutations(...), repeat=5)` approach would check all 120⁵ ≈ **24 billion** combinations, no shortcuts. This version explores roughly **~50,000** states — five orders of magnitude fewer.

---

## Turn 2 (final)

**User:**

I'll solve the classic Zebra Puzzle step by step. Let me first create a solution file:Perfect! ✅ **Solution works: Norwegian drinks water, Japanese owns the zebra.**

---

## How it works

The key insight is **early pruning** on the 5! = 120 permutations for each attribute:

1. **Pre-filter attributes** where constraints are simple:
   - **Colors**: Only keep permutations where green is immediately right of ivory (constraint 5) → ~24 valid orderings instead of 120
   - **Drinks**: Only keep those where milk is in house 3 (constraint 8)
   - **Nationalities**: Only keep those where Norwegian is in house 1 (constraint 9)

2. **Nested loops** apply remaining constraints at each level:
   - Check Englishman→red, Ukrainian→tea, etc. before going deeper
   - Check adjacency constraints (Chesterfield↔fox, Kools↔horse) only when considering pet assignments

3. **Result**: Instead of checking all **5!⁵ ≈ 24.8 billion** combinations, we explore maybe **~10,000–50,000** states—five orders of magnitude fewer.

The permutation approach (vs. raw brute force) lets you iterate naturally through valid orderings, and the nested-loop pruning lets you short-circuit branches early. The Spanish—dog, Old Gold→snails, Lucky Strike→orange juice constraints collapse further as you descend.

<done/>

---

**Run end**: done after 1 turn (117s)
