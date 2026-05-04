# exercism-zebra-puzzle

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:42:00

## Initial prompt

Exercism 'Zebra Puzzle': solve the classic 5-houses constraint puzzle (Englishman/red house, Spaniard/dog, etc.) and return who drinks water and who owns the zebra. Use itertools.permutations or a constraint solver.

---

## Turn 1

### Tutor

[Glob(zebra_puzzle*)]
  No files found

Tutor: No file yet. Before we write anything, here's the core design question:

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Nested permutations, prune early
Generate permutations of each attribute (nationality, color, drink, smoke, pet) in nested loops — but apply relevant constraints at each level before descending. 120⁵ worst-case collapses to a handful of paths in practice.

[B] Single flat permutation product
Use `itertools.product(permutations(range(5)), repeat=5)` to generate all attribute combos at once, then filter with one big predicate. Simpler structure, same `itertools` primitives.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach — **A** (nested loops, prune early) or **B** (flat product, filter at end)?

### Student

I think I'll go with **A** (nested loops, prune early).

My reasoning: the Zebra Puzzle has a lot of constraints, and if we can eliminate invalid partial assignments early, we'll avoid generating and testing tons of dead-end combinations. Option B would generate everything first and then filter, which seems wasteful. Plus, building it step-by-step might help me understand how the constraints actually work together.

Let me start by sketching out the structure — should I begin by listing all the constraints first, or jump straight into writing the nested loop skeleton?

---

## Turn 2

### Tutor

Tutor: Good instinct on the reasoning. One more structural question before we write anything:

OPTIONS:
[A] Skeleton first, fill in later
Write the 5 nested `for perm in permutations(...)` loops first, then slot constraints in wherever they seem to fit.

[B] Map constraints to depth first
List all 15 clues and tag each with the attributes it involves (e.g. "Englishman↔Red" needs nationality+color). That tells you exactly which loop level is the earliest you can check it — *before* writing any code.

(Reply with A or B, or ask a follow-up question.)

Tutor: **A** or **B** — does the order matter here?

### Student

I'll go with **B** (map constraints to depth first).

I think understanding *when* each constraint can be checked will make the code cleaner and help me avoid building constraints that depend on attributes I haven't permuted yet. Plus, it'll give me confidence that the early pruning will actually work before I start writing loops.

Can we list out the 15 clues and tag them? I want to see which attributes each constraint touches so I know at what nesting level I can start filtering.

---

## Turn 3

### Tutor

Tutor: Sure. Let's lay them all out. We'll permute in this order: **Nationality → Color → Drink → Smoke → Pet** — so the depth at which a constraint becomes checkable depends on which of those five it touches.

---

**Depth 1 — Nationality only**
| # | Clue | Attributes |
|---|------|-----------|
| 9 | Norwegian lives in house 1 (leftmost) | Nationality |

**Depth 2 — + Color**
| # | Clue | Attributes |
|---|------|-----------|
| 1 | Englishman lives in the red house | Nationality + Color |
| 5 | Green house is immediately right of ivory | Color |
| 14 | Norwegian lives next to the blue house | Nationality + Color |

**Depth 3 — + Drink**
| # | Clue | Attributes |
|---|------|-----------|
| 3 | Coffee is drunk in the green house | Color + Drink |
| 4 | Ukrainian drinks tea | Nationality + Drink |
| 8 | Milk is drunk in the middle house | Drink |

**Depth 4 — + Smoke**
| # | Clue | Attributes |
|---|------|-----------|
| 7 | Kools smoked in the yellow house | Color + Smoke |
| 12 | Lucky Strike smoker drinks OJ | Drink + Smoke |
| 13 | Japanese smokes Parliaments | Nationality + Smoke |

**Depth 5 — + Pet (innermost)**
| # | Clue | Attributes |
|---|------|-----------|
| 2 | Spaniard owns the dog | Nationality + Pet |
| 6 | Old Gold smoker owns snails | Smoke + Pet |
| 10 | Chesterfields smoker lives next to the fox owner | Smoke + Pet |
| 11 | Kools smoker lives next to the horse | Smoke + Pet |

---

That's all 14 structural clues placed. Clue 15 ("there is a zebra") just names the fifth pet — it's implicit in the permutation.

Notice that **4 constraints land at depth 5** vs. **3 at depth 2** — that's where most dead-ends are caught. The color-level pruning (depth 2) is especially powerful: clue 5 (`green = ivory + 1`) eliminates ~80% of color permutations before we ever touch drinks.

Ready to write the skeleton + constraints?

### Student

Yes, I'm ready. This breakdown is really helpful — I can see now that clue 5 (green immediately right of ivory) will do a ton of early pruning, and the depth-5 constraints are the real filters at the end.

Let me start writing the skeleton with the constraint checks slotted in at the right levels. I'll write the nested loops for nationality → color → drink → smoke → pet, and add the constraint checks as I go down.

Should I write this as a series of nested `for` loops with `if` conditions that skip ahead when a constraint fails, or would it be clearer to write helper functions for each constraint check? I'm thinking helper functions might make it easier to read, but I want to make sure that doesn't add overhead or make the early pruning less obvious.

---

## Turn 4

### Tutor

OPTIONS:
[A] Per-clue helper functions
Wrap each constraint in its own function (`check_nationality`, `check_color`, etc.) and call them at the appropriate loop level. Reads like prose, each check is named.

[B] Inline checks, tiny predicate helpers
Keep the `if` guards inline in the loops, but extract only the two reusable spatial predicates:
```diff
+++ zebra_puzzle.py
@@ -0,0 +1,4 @@
+def next_to(a, b):
+    return abs(a - b) == 1
+
+def right_of(a, b):
+    return a == b + 1
```
All constraint checks stay at their loop level — the depth structure stays visible.

(Reply with A or B, or ask a follow-up question.)

Tutor: **A** or **B** — do the helper functions help or hurt readability here?

### Student

I'll go with **B** (inline checks, tiny predicate helpers).

I think keeping the constraint checks inline at their loop levels will make it crystal clear *where* each pruning happens — that's the whole point of the depth-first strategy we just mapped out. If I wrap everything in named helper functions, I lose that visual structure even if the code reads nicely in isolation.

The two spatial predicates (`next_to` and `right_of`) are genuinely reusable and worth extracting, so let's do that. Everything else stays inline so I can see the pruning happening at each nesting level.

Let me start writing the skeleton now — should I set up the basic 5 nested loops first, then add the constraints level by level?

---

## Turn 5

### Tutor

Tutor: Yes — let's just write the whole thing now. The design is fully mapped; building it level-by-level in conversation would just slow us down. I'll write it all at once with the constraints slotted in at exactly the depths we planned.

[Write(zebra_puzzle.py)]
from itertools import permutations


def next_to(a, b):
    return abs(a - b) == 1


def right_of(a, b):
    return a == b + 1


def _solve():
… (59 more lines)
  File created successfully at: zebra_puzzle.py

[Bash(cd /tmp && python -c "
import sys, time
sys.path.insert(0, '.')
import zebra_puzzle
t = time.time()
w = zebra_puzzle.drinks_water()
z = zebra_puzzle.owns_zebra()
print(f'Water drinker : {w}')
print(f'Zebra owner   : {z}')
print(f'Time          : {(time.time()-t)*1000:.1f} ms')
" 2>&1 || python3 -c "
import sys, time
sys.path.insert(0, '/tmp')
import importlib.util, pathlib
spec = importlib.util.spec_from_file_location('zebra_puzzle', 'zebra_puzzle.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
t = time.time()
w = m.drinks_water(); z = m.owns_zebra()
print(f'Water drinker : {w}')
print(f'Zebra owner   : {z}')
print(f'Time          : {(time.time()-t)*1000:.1f} ms')
"
)]
  error: Exit code 1

[Bash(python3 -c "
import sys, time, importlib.util
spec = importlib.util.spec_from_file_location('zebra_puzzle', 'zebra_puzzle.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
t = time.time()
w = m.drinks_water(); z = m.owns_zebra()
print(f'Water drinker : {w}')
print(f'Zebra owner   : {z}')
print(f'Time          : {(time.time()-t)*1000:.1f} ms')
"
)]
  Water drinker : Norwegian
  Zebra owner   : Japanese
  Time          : 0.2 ms

Tutor: **Norwegian** drinks water. **Japanese** owns the zebra. Runs in 0.2 ms.

---

A few things worth noting about the final code:

**`nat.index(Water)`** — this is the key lookup. `nat` is a tuple of house positions indexed by person (position 0 = Norwegian, 1 = Englishman, …). `Water` is a house number 0–4. So `nat.index(Water)` finds *which person lives in the water house*, giving us the index into `people`. Clean one-liner that avoids any explicit loop.

**Why `_solve()` is called twice** (once for each public function) — for a puzzle that solves in 0.2 ms, that's fine. If you wanted to cache it, `@functools.lru_cache` on a zero-argument function is the idiomatic tool — but it'd be premature here.

**The depth 2 prune does the heavy lifting** — clues 1, 5, and 14 together reduce 120 color permutations down to just a few before we ever touch drinks or smokes. That's why the whole search completes in < 1 ms despite being written in pure Python.

### Student

That's really satisfying. The solution works cleanly and efficiently.

I want to understand the `nat.index(Water)` lookup better though — let me trace through it:

- `nat` is a permutation of `(0, 1, 2, 3, 4)` representing which house each nationality lives in, indexed by nationality (0=Norwegian, 1=Englishman, etc.)
- `Water` is a house number (0–4)
- `nat.index(Water)` finds the *position* in the `nat` tuple where `Water` appears, which tells us which nationality lives there
- Then we index into `people` to get the actual name

So if `nat = (0, 2, 4, 3, 1)` and `Water = 2`, then `nat.index(2) = 1`, and `people[1] = "Englishman"` — the Englishman lives in house 2 which is the water house.

Is that right?

Also, one last thing — I'm curious why the depth-2 constraint (green immediately right of ivory) was so powerful. Is it just that color adjacency is a hard constraint that eliminates most arrangements, or is there something else making it so effective?

---

## Turn 6

### Tutor

Tutor: Your trace is exactly right. Nicely done.

---

On why clue 5 is so powerful — let's count. Out of 5! = 120 color permutations, how many have `Green == Ivory + 1`?

The valid (Ivory, Green) position pairs are only: `(0,1) (1,2) (2,3) (3,4)` — just **4** pairs. The remaining 3 colors fill the leftover positions in 3! = 6 ways each:

```
4 pairs × 6 arrangements = 24 survivors out of 120
```

Clue 5 alone eliminates **80%** of color permutations before any other constraint fires. That's why it's so effective — it's not just an adjacency check, it's a *directional* ordering constraint on two specific values, and 5 houses don't leave many slots for that.

Compare it to a plain equality constraint like clue 1 (`Englishman == Red`): once `Englishman`'s position is fixed from the outer loop, that also eliminates 4/5 of color permutations — but it *depends* on the nationality loop to do so. Clue 5 is self-contained within the color loop and fires unconditionally, making it a pure structural filter.

The general principle: **the tightest constraints are ones that impose a relative order between two variables** (adjacency + direction), because those reduce `n!` arrangements to roughly `(n-1) × (n-2)!` — a factor-of-n reduction by themselves.

### Student

That makes complete sense now. The directional adjacency constraint is so powerful because it's not just saying "these two must be adjacent" — it's saying "this one must be immediately to the right of that one," which cuts the search space by a fixed factor regardless of what else permutes around it.

I can see how that principle generalizes: any constraint that imposes a strict relative ordering between two specific values in a sequence will give you those kinds of dramatic early prunings, especially in smaller spaces like 5 houses.

This was a really solid walkthrough. The problem is solved, the code works efficiently, and I understand both *how* it works and *why* the depth-first constraint mapping strategy was worth doing upfront. 

Thanks for breaking down the design before jumping into code — that made the whole thing much clearer than if we'd just started writing nested loops and bolted constraints on afterward.

<done/>

---

**Run end:** done after 6 turn(s) in 204.1s
