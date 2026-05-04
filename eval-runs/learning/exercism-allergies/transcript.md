# exercism-allergies

- Source: `exercism`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Output style: `Learning`
- Started: 2026-05-03T19:58:39.725Z

---

## Turn 1

**User:**

Exercism 'Allergies': allergens encode as bitfield flags in a single int score (eggs=1, peanuts=2, shellfish=4, ... cats=128). Write `is_allergic_to(score, allergen)` and `allergies(score)` returning the list of allergens.

**Pair:**

Assistant: ## Allergies — Bitfield Decoding

Each allergen occupies exactly **one bit** in the score integer. Testing for an allergy is just a bitwise AND check.

```
score bits:  … 1 0 0 0 0 1 1 0
                ↑           ↑ ↑
              cats     peanuts eggs
```

```python
# The allergens in bit-position order (index = bit position 0..7)
ALLERGENS = [
    "eggs",         # bit 0  → value 1
    "peanuts",      # bit 1  → value 2
    "shellfish",    # bit 2  → value 4
    "strawberries", # bit 3  → value 8
    "tomatoes",     # bit 4  → value 16
    "chocolate",    # bit 5  → value 32
    "pollen",       # bit 6  → value 64
    "cats",         # bit 7  → value 128
]


def is_allergic_to(score: int, allergen: str) -> bool:
    """Return True if the allergen's bit is set in score."""
    bit = 1 << ALLERGENS.index(allergen)   # e.g. "peanuts" → 1 << 1 → 2
    return bool(score & bit)               # nonzero iff that bit is set


def allergies(score: int) -> list[str]:
    """Return every allergen whose bit is set in score."""
    return [a for a in ALLERGENS if is_allergic_to(score, a)]
```

### Walkthrough — score = 34

```
34  =  0b00100010
              ↑ ↑
        peanuts  shellfish... wait, let's check:

bit 1 (peanuts=2):    34 & 2  = 2  ✓
bit 5 (chocolate=32): 34 & 32 = 32 ✓

>>> allergies(34)
['peanuts', 'chocolate']
```

### Key ideas

| Concept | Code | Why it works |
|---|---|---|
| **Bit mask for allergen** | `1 << index` | shifts `1` left to the allergen's bit position |
| **Test a bit** | `score & mask` | nonzero only when that bit is set in score |
| **High bits ignored** | naturally | scores > 255 just have extra bits; the 8 allergen bits are always the low 8 |

Because `allergies()` calls `is_allergic_to()` rather than duplicating the bit logic, the single source of truth is in one place — if you ever added a 9th allergen you'd only touch `ALLERGENS`.

---

## Turn 2

**User:**

Great setup! I've sketched the approach above. Before I write actual code, let me clarify the shape of what you're looking for:

**Questions:**

1. **Language?** — Exercism supports Python, TypeScript/JavaScript, Go, Rust, etc. What's your target?
2. **Is this in the ai-pair-proto codebase, or standalone?** — Should I create a new file in the project, or are you solving this as a standalone exercise?
3. **Tests?** — Do you want me to write test cases to verify the logic, or just the two functions?

Once I know those, I can write it out, propose two different styles (e.g. *direct bitwise vs. iterative check*, or *dict lookup vs. list index*), and we can choose which approach to go with. That fits the pair-programming pedagogy — you'll see the trade-offs and pick what clicks.

**Pair:**

Assistant: Those are great questions to ask *before* writing — the answer I gave you jumped straight to code, which is fine when the problem is clear, but the interactive check-in is better pedagogy. Let me answer each:

1. **Language** — I defaulted to Python since you didn't specify. Same logic ports cleanly to any language; the bit operations are universal.

2. **Standalone** — treat it as a standalone exercise file, not wired into a larger codebase.

3. **Tests** — yes, worth adding. Here they are:

```python
# --- tests ---
assert is_allergic_to(1, "eggs")          == True
assert is_allergic_to(0, "eggs")          == False
assert is_allergic_to(2, "eggs")          == False   # only peanuts bit set
assert is_allergic_to(255, "cats")        == True    # all bits set
assert is_allergic_to(256, "eggs")        == False   # bit 8 is beyond allergens

assert allergies(0)   == []
assert allergies(1)   == ["eggs"]
assert allergies(3)   == ["eggs", "peanuts"]         # bits 0+1
assert allergies(255) == ALLERGENS                   # all 8
assert allergies(257) == ["eggs"]                    # 256 + 1; bit 8 ignored
```

---

### Two alternative styles I mentioned

**Style A — index lookup (what I wrote):**
```python
bit = 1 << ALLERGENS.index(allergen)
return bool(score & bit)
```
*Pros:* list stays the single source of truth. *Cons:* `index()` raises `ValueError` for unknown allergens.

**Style B — dict lookup:**
```python
ALLERGEN_BITS = {name: 1 << i for i, name in enumerate(ALLERGENS)}

def is_allergic_to(score, allergen):
    return bool(score & ALLERGEN_BITS.get(allergen, 0))
```
*Pros:* O(1) lookup, graceful default for unknown names. *Cons:* two data structures to keep in sync (though the dict is derived from the list, not hand-written).

For an exercise, Style A is fine. In production code where unknown allergen strings are possible, Style B is safer.

---

## Turn 3

**User:**

You're absolutely right — that's much better pedagogy. I jumped straight to an answer without checking the shape of the problem first. Let me actually ask you:

1. **Language?** — Exercism supports many. For the ai-pair-proto codebase (which is TS/Bun), should this be **TypeScript**? Or do you prefer **Python** for a standalone exercise?

2. **Location?** — Does this go:
   - Inside the ai-pair-proto project (maybe `exercises/allergies/`)?
   - Or just as a standalone file/directory outside the codebase?

3. **Tests?** — I'd suggest writing them. Do you want:
   - A separate test file (e.g., `test_allergies.py` or `.test.ts`)?
   - Tests alongside the functions in the same file?
   - Both, using a framework like `pytest` or `vitest`?

Once you answer these, I'll propose two distinct approaches (e.g., *eager bitfield set vs. lazy bitfield iteration*, or *constants dict vs. derived enum*) with trade-offs written out, and you can pick which one clicks for you.

**Pair:**

Assistant: Those are the right questions — let me actually look at the codebase before proposing anything, so the file structure and tooling choices aren't guesswork.

[Bash]
  /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-allergies-VS2xRk
  /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-allergies-VS2xRk/.claude
  /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-allergies-VS2xRk/.claude/settings.json

[Bash]
  total 0
  drwx------    3 oz  staff    96  4 May 05:58 .
  drwx------@ 186 oz  staff  5952  4 May 06:00 ..
  drwxr-xr-x    3 oz  staff    96  4 May 05:58 .claude

[Bash]
  /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-allergies-VS2xRk/.claude/settings.json

[Read]
  1	{"outputStyle":"Learning"}

[Agent({"description":"Explore ai-pair-proto project structure","subagent_type":"Exp...)]
  The codebase appears to be an empty template directory. There are no actual source files, package.json, tsconfig, or exercises yet—just a `.claude/settings.json` stub with output style configuration.
  
  **Structural Overview:**
  - **Root:** Empty template with only `.claude/settings.json`
  - **No exercises/** directory or source code present
  - **No test framework:** No package.json, vitest/jest configs
  - **No TypeScript setup:** No tsconfig.json, no module configuration
  - **Status:** This appears to be a fresh Exercism allergies exercise template awaiting implementation
  
  The project needs initialization (package.json, source files, test configuration, etc.) before development can begin.

Assistant: Fresh slate — nothing to adapt to, which means we get to choose the shape from scratch. That makes the earlier questions more important, not less:

**What I found:** one `.claude/settings.json`, nothing else. No runtime, no test framework, no `tsconfig`.

**So — three real decisions before I write a line:**

1. **Language & runtime**
   - **Python** (standalone, no setup needed — just a `.py` file you can run immediately)
   - **TypeScript + Bun** (needs a `package.json` + `tsconfig.json` bootstrap, but matches what you said "ai-pair-proto" uses)

2. **Project layout** — given it's empty, I'd propose one of:
   ```
   # Option A — flat (simplest)
   allergies.ts / allergies.py
   allergies.test.ts / test_allergies.py

   # Option B — exercise folder (Exercism-style)
   allergies/
     allergies.ts
     allergies.test.ts
     package.json
   ```

3. **Two implementation approaches to compare** (I'll write both and annotate the trade-offs):
   - **Approach 1 — bitmask at call time:** compute `1 << index` on every call; no pre-built data structure
   - **Approach 2 — pre-built lookup:** derive a `{name → mask}` map once at module load; O(1) lookups after that

Pick a language and a layout and I'll bootstrap the whole thing — runtime config, two annotated implementations side-by-side, and a test file that exercises both.

---

## Turn 4

**User:**

Based on the CLAUDE.md context (the project uses **TS/Bun/Ink**), I'd recommend:

**My proposal:**
1. **TypeScript** — aligns with `ai-pair-proto`'s stack; you're already familiar with it
2. **Flat layout** — `allergies.ts` + `allergies.test.ts` in the project root for simplicity
3. **Two approaches to choose between:**
   - **Approach 1 — Lazy bitmask:** compute `1 << index(allergen)` at call time; no pre-built data
   - **Approach 2 — Pre-built lookup:** derive a `Map<string, number>` once on load; O(1) per lookup

Both pass the same tests. I'll write them side-by-side with comments on the trade-offs (memory vs. latency, simplicity vs. efficiency), you pick which one feels right, and I'll apply it.

**Sound good?** Say "yes" and I'll bootstrap `package.json`, `tsconfig.json`, both implementations, and a test suite using `vitest` (Bun's test runner).

**Pair:**

Assistant: Yes — let's build it. I'll bootstrap the whole thing now.

[Bash(ls)]
  (Bash completed with no output)

[Bash(ls -la)]
  total 0
  drwx------    3 oz  staff    96  4 May 05:58 .
  drwx------@ 186 oz  staff  5952  4 May 06:01 ..
  drwxr-xr-x    3 oz  staff    96  4 May 05:58 .claude

Assistant: Confirmed empty — just `.claude/`. Writing all four files now:

[Write(/Users/oz/allergies/package.json)]
{
  "name": "allergies",
  "version": "1.0.0",
  "scripts": {
    "test": "bun test"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "@types/bun": "latest"
  }
}


[Write(/Users/oz/allergies/tsconfig.json)]
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true
  }
}


[Write(/Users/oz/allergies/allergies.ts)]
// Allergens in bit-position order.
// Index 0 → bit 0 (value 1), index 7 → bit 7 (value 128).
const ALLERGENS = [
  "eggs",         // 1
  "peanuts",      // 2
  "shellfish",    // 4
  "strawberries", // 8
  "tomatoes",     // 16
  "chocolate",    // 32
  "pollen",       // 64
  "cats",         // 128
] as const;
… (41 more lines)

[Write(/Users/oz/allergies/allergies.test.ts)]
import { describe, test, expect } from "bun:test";
import {
  isAllergicTo,
  isAllergicTo_lazy,
  allergies,
  allergies_lazy,
  type Allergen,
} from "./allergies";

// Run the same suite against both implementations so they stay in sync.
const implementations = [
  { label: "pre-built lookup", isAllergicTo, allergies },
… (64 more lines)

[Bash(cd /Users/oz/allergies && bun test 2>&1)]
  bun test v1.3.13 (bf2e2cec)
  
   18 pass
   0 fail
   52 expect() calls
  Ran 18 tests across 1 file. [13.00ms]
  Shell cwd was reset to /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-allergies-VS2xRk

Assistant: **18/18 pass.** Here's what was built:

---

### File layout
```
allergies.ts        ← both implementations, side-by-side with trade-off comments
allergies.test.ts   ← one test suite, run against both impls via a loop
package.json        ← "test": "bun test"
tsconfig.json       ← strict, ESNext/bundler
```

### The key design choice in the test file

Rather than duplicating 18 tests, the suite iterates over an `implementations` array:

```ts
for (const impl of implementations) {
  describe(`isAllergicTo — ${impl.label}`, () => { … })
}
```

This guarantees both approaches are held to exactly the same contract — if you change one, the tests catch any drift in the other.

### Trade-off recap

| | Lazy (`indexOf` + `<<`) | Pre-built (`Map.get`) |
|---|---|---|
| Up-front cost | none | one Map construction |
| Per-call cost | O(n) index search | O(1) hash lookup |
| Unknown allergen | shifts bit −1 (wrong!) | returns `0` (safe) |
| Recommended for | scripts, one-offs | library / hot path |

The exported defaults (`isAllergicTo`, `allergies`) use the pre-built approach — safer unknown-input handling is the right default.

---

## Turn 5

**User:**

**Perfect** — 18 tests passing. Both implementations work identically from the outside; the difference is purely internal.

---

## What I'd like to know next (as your pair):

Now that you can see both approaches in the same file, **which one clicks for you?**

1. **Prefer the lazy approach?** Simpler to understand (just `1 << index` at call time), no upfront setup. Trade-off: slower for repeated calls, crashes on unknown allergens.

2. **Prefer the pre-built Map?** A touch more sophisticated (build once, O(1) lookups forever), safer default behavior. Trade-off: one extra data structure to keep in mind.

3. **Want me to explain one of them step-by-step** with a concrete trace? (e.g., walk through `allergies(34)` and show exactly which bits flip and what gets returned.)

Also — **do you want to keep both implementations in the file for comparison, or should I collapse to just one?** (I'd suggest keeping both for learning, but happy to strip it down if you prefer a cleaner final answer.)

**Pair:**

Assistant: Great questions to close the loop on. Here's my take on each:

**Keep the pre-built Map** — the unknown-allergen safety is the deciding factor. `indexOf` returning `-1` and then computing `1 << -1` gives `0` in JS (harmless coincidence!), but it's a trap: the *reason* it works is opaque. `Map.get(unknown) ?? 0` makes the intent explicit.

**Collapse to one** — two named exports per function (`isAllergicTo` vs `isAllergicTo_lazy`) is noise once you've made the call. Keep a comment noting the alternative existed.

**Step-by-step trace of `allergies(34)`** — here it is:

```
34 in binary:  0 0 1 0 0 0 1 0
bit position:  7 6 5 4 3 2 1 0
allergen:      c p ■ t s s p e
               a o   o t h e g
               t l   m r o a g
               s l   a a c n s
                 e   t w o u
                 n   o b l t
                         e s s

ALLERGEN_BITS.get("peanuts")    = 2   →  34 & 2  = 2  ✓  included
ALLERGEN_BITS.get("chocolate")  = 32  →  34 & 32 = 32 ✓  included
all others                             →  34 & x  = 0  ✗  skipped

result: ["peanuts", "chocolate"]
```

Now let me do the cleanup — collapse to one implementation, keep the trade-off note as a comment:

[Write(/Users/oz/allergies/allergies.ts)]
// Allergens in bit-position order.
// Index 0 → bit 0 (value 1), index 7 → bit 7 (value 128).
const ALLERGENS = [
  "eggs",         // 1
  "peanuts",      // 2
  "shellfish",    // 4
  "strawberries", // 8
  "tomatoes",     // 16
  "chocolate",    // 32
  "pollen",       // 64
  "cats",         // 128
] as const;
… (19 more lines)

[Edit(/Users/oz/allergies/allergies.test.ts)]
--- before
import {
  isAllergicTo,
  isAllergicTo_lazy,
  allergies,
  allergies_lazy,
  type Allergen,
} from "./allergies";

// Run the same suite against both implementations so they stay in sync.
const implementations = [
  { label: "pre-built lookup", isAllergicTo, allergies },
  { label: "lazy bitmask",     isAllergicTo: isAllergicTo_lazy, allergies: allergies_lazy },
];

for (const impl of implementations) {
  describe(`isAllergicTo — ${impl.label}`, () => {
--- after
import { isAllergicTo, allergies, type Allergen } from "./allergies";

const implementations = [{ label: "allergies", isAllergicTo, allergies }];

for (const impl of implementations) {
  describe(`isAllergicTo — ${impl.label}`, () => {

[Bash(cd /Users/oz/allergies && bun test 2>&1)]
  bun test v1.3.13 (bf2e2cec)
  
   9 pass
   0 fail
   26 expect() calls
  Ran 9 tests across 1 file. [12.00ms]
  Shell cwd was reset to /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-allergies-VS2xRk

Assistant: 9/9 still passing (was 18 because each test ran twice — once per implementation).

---

### Final shape of `allergies.ts`

```
ALLERGENS list (source of truth)
    ↓
ALLERGEN_BITS map (derived once at load)
    ↓
isAllergicTo(score, allergen)  →  boolean
allergies(score)               →  Allergen[]
```

The comment in the file now explains *why* the pre-built map was chosen over the lazy approach — future readers get the reasoning without having to rediscover it.

---

## Turn 6 (final)

**User:**

Perfect — this is a complete, well-reasoned solution. Let me recap what we learned by working through it together:

---

### Key lessons from this exercise

1. **Ask before coding.** You caught that jumping straight to an answer skips the pedagogical value. Clarifying language, scope, and testing strategy upfront is *part* of the work.

2. **Hold two approaches side-by-side.** Writing both the lazy and pre-built implementations let us see the trade-offs concretely — not as abstract pros/cons, but as actual code you could read and run. That's how you develop intuition for "when do I pre-build vs. compute on demand?"

3. **Same tests for both.** By looping over an `implementations` array, we guaranteed they have identical behavior from the outside. That's how you know a refactor is safe — not by hand-tracing, but by running the suite twice.

4. **Unknown inputs matter.** The decision to use `Map.get(allergen) ?? 0` came from thinking about edge cases — what happens when someone passes a typo? The lazy approach silently fails; the map approach gracefully returns "not allergic." That's a real design decision, not nitpicking.

5. **Comments capture intent.** A one-liner in the source explaining why we chose the pre-built map means future-you (or someone else) doesn't have to rediscover that reasoning.

---

### What you have now

- Two functions that correctly decode bitfield allergies
- Test coverage (9 passing tests across different edge cases)
- A clean, readable implementation with a clear comment on the design choice
- The muscle memory of how to hold multiple approaches and pick deliberately

The Exercism problem is solved, but the *pedagogical* point was getting you to think like a pair — propose, compare, decide, document.

<done/>

---

**Run end**: done after 5 turns (290s)
