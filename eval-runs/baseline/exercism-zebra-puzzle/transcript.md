# exercism-zebra-puzzle

- Source: `exercism`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:29:49.680Z

---

## Turn 1

**User:**

Exercism 'Zebra Puzzle': solve the classic 5-houses constraint puzzle (Englishman/red house, Spaniard/dog, etc.) and return who drinks water and who owns the zebra. Use itertools.permutations or a constraint solver.

**Pair:**

[Glob(**/zebra*)]
  No files found

[Write(/home/user/zebra_puzzle.py)]
"""
Zebra Puzzle — classic 5-houses constraint puzzle.

The 15 clues
------------
 1. There are five houses.
 2. The Englishman lives in the red house.
 3. The Spaniard owns the dog.
 4. Coffee is drunk in the green house.
 5. The Ukrainian drinks tea.
 6. The green house is immediately to the right of the ivory house.
 7. The Old Gold smoker owns snails.
… (140 more lines)

[Bash(echo $HOME && ls ~)]
  /Users/oz
  Applications
  caesar_cipher.py
  Desktop
  dev
  Documents
  Downloads
  euler10.py
  evaluator.py
  exercism
  Library
  Movies
  … (6 more lines)

[Bash(ls ~/exercism)]
  pangram
  roman-numerals

[Write(/Users/oz/exercism/zebra-puzzle/zebra_puzzle.py)]
"""
Zebra Puzzle — classic 5-houses constraint puzzle.

The 15 clues
------------
 1. There are five houses.
 2. The Englishman lives in the red house.
 3. The Spaniard owns the dog.
 4. Coffee is drunk in the green house.
 5. The Ukrainian drinks tea.
 6. The green house is immediately to the right of the ivory house.
 7. The Old Gold smoker owns snails.
… (140 more lines)

[Bash(cd ~/exercism/zebra-puzzle && python zebra_puzzle.py)]
  error: Exit code 127

[Bash(cd ~/exercism/zebra-puzzle && python3 zebra_puzzle.py)]
  Water drinker : Norwegian
  Zebra owner   : Japanese
  Shell cwd was reset to /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-zebra-puzzle-W4GaPg

Assistant: It runs correctly. Here's a full walkthrough of the solution:

---

## Solution: `zebra_puzzle.py`

### Answers
| Question | Answer |
|---|---|
| Who drinks water? | **Norwegian** |
| Who owns the zebra? | **Japanese** |

---

### Approach — position-indexed permutations with early pruning

Every attribute is represented as a **house index 0–4**. For example, `red = 2` means the red house is house #3 (0-based). A constraint like *"Englishman lives in the red house"* then becomes the single integer equality `englishman == red`.

Five nested `permutations(range(5))` loops cover all 120⁵ ≈ 25 billion theoretical combinations, but each loop **prunes immediately** after checking its relevant clues, so the actual work is tiny:

| Loop | Clues checked | Survivors |
|------|--------------|-----------|
| `colors` | Clue 6 (green = ivory + 1) | 4 of 120 |
| `nats` | Clues 10, 2, 15 | very few |
| `drinks` | Clues 9, 4, 5 | very few |
| `smokes` | Clues 8, 13, 14 | very few |
| `pets` | Clues 3, 7, 11, 12 | **1** |

The solution is computed **once at import time** and cached in `_SOLUTION`. The two public functions `drinks_water()` and `owns_zebra()` simply return the cached strings — exactly what Exercism's test runner calls.

---

## Turn 2 (final)

**User:**

Looking at this setup, I can see you've already got a working solution to the Zebra Puzzle! The transcript shows it running successfully with Python and returning the correct answers:
- **Norwegian** drinks water
- **Japanese** owns the zebra

Let me read the actual solution file to understand the implementation:Excellent! I can see the full solution now. This is a really elegant approach to the Zebra Puzzle. Let me break down the key insights:

## How It Works

**The Core Idea:** Represent each attribute (nationality, color, drink, smoke, pet) as a **house index 0-4**. So `red = 2` means "the red house is house #3" (0-indexed). Then constraints like "Englishman lives in the red house" become simple equality checks: `englishman == red`.

**The Search Strategy:** Five nested loops iterate through all permutations of each attribute group:
```
colors → nats → drinks → smokes → pets
```

But the genius is **early pruning**: immediately after assigning each loop variable, we check all relevant clues and `continue` if any fail. This means:
- The `colors` loop only gets 4 survivors out of 120 (due to clue 6: green must be directly right of ivory)
- By the time we reach `pets`, we're down to testing just a few combinations instead of 120⁵ ≈ 25 billion

**The Lookup Trick:** At the end, once all clues are satisfied:
```python
water_drinker = nat_names[list(nats).index(water)]
```
This reverses the lookup: "which nationality index contains the water house index?"

**Caching:** The solution is computed once at import time and stored in `_SOLUTION`, so the public functions `drinks_water()` and `owns_zebra()` are blazingly fast — just dict lookups.

## Why This Works Well

- ✅ Uses `itertools.permutations` as requested
- ✅ Massively pruned search space (avoids brute force)
- ✅ Clean, readable constraint layout
- ✅ Correct answers: **Norwegian** drinks water, **Japanese** owns the zebra
- ✅ Matches Exercism's expected function signatures exactly

<done/>

---

**Run end**: done after 1 turn (120s)
