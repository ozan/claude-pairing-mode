# exercism-bowling

- Source: `exercism`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T05:50:01.771Z

---

## Turn 1

**User:**

Exercism 'Bowling': implement a 10-pin bowling scorer. Track frames, handle strikes (next two rolls bonus), spares (next roll bonus), and the special 10th-frame bonus rolls. Return the final score from a list of rolls.

**Pair:**

[Glob(bowling*)]
  No files found

Assistant: Good, blank slate. Before we write any code, let me ask about the core algorithm — this is the decision that shapes everything else.

The `score()` method needs to walk through 10 frames, applying strike/spare bonuses. Two ways to do it:

**Option A — Index-based walk:** keep a flat `rolls` list, iterate with an integer index that advances 1 or 2 per frame, and peek ahead for bonuses.

**Option B — Frame objects:** as each `roll()` comes in, package rolls into `Frame` dataclass instances, then sum them.

Which approach do you think handles the 10th frame more cleanly?

---

## Turn 2

**User:**

I'd pick **A — Index-based walk**.

Here's my reasoning: Option B requires knowing the 10th frame's roll count *before* you parse it (to stop after 2 rolls if it's open, or 3 if it's a strike/spare). That creates a chicken-egg problem — you'd need to look ahead as you parse, which adds complexity.

With Option A, you just iterate frames 1–9 with fixed logic (strike → skip 1 index, otherwise take 2), then frame 10 is "whatever rolls remain." The lookahead bonuses for frames 1–9 are simple array peeks, and the 10th frame never needs bonuses because it's the end. Much cleaner.

**Pair:**

Assistant: Exactly right — and your point about frame 10 being "sum the rest" is the key insight that makes the index approach so clean. Let's build it.

[Write(bowling.py)]
class BowlingGame:
    def __init__(self):
        self._rolls = []

    def roll(self, pins):
        self._rolls.append(pins)

    def score(self):
        total = 0
        i = 0  # index into self._rolls
        for frame in range(10):
            pass  # TODO
… (2 more lines)

Assistant: Good skeleton. Now the real question: how do we write the body of that loop? Here are two ways to fill in `score()`:

Assistant: Two ways to fill in the loop body:

**Option A**
```diff
+++ bowling.py
@@ -8,7 +8,13 @@
         total = 0
         i = 0
         for frame in range(10):
-            pass  # TODO
+            if frame == 9:
+                total += sum(self._rolls[i:])
+            elif self._rolls[i] == 10:          # strike
+                total += 10 + self._rolls[i+1] + self._rolls[i+2]
+                i += 1
+            elif self._rolls[i] + self._rolls[i+1] == 10:  # spare
+                total += 10 + self._rolls[i+2]
+                i += 2
+            else:
+                total += self._rolls[i] + self._rolls[i+1]
+                i += 2
         return total
```

**Option B**
```diff
+++ bowling.py
@@ -8,7 +8,13 @@
         total = 0
         i = 0
         for frame in range(10):
-            pass  # TODO
+            if self._rolls[i] == 10:            # strike
+                total += 10 + self._rolls[i+1] + self._rolls[i+2]
+                i += 1
+            elif self._rolls[i] + self._rolls[i+1] == 10:  # spare
+                total += 10 + self._rolls[i+2]
+                i += 2
+            else:
+                total += self._rolls[i] + self._rolls[i+1]
+                i += 2
         return total
```

Option B is shorter — no special-case for frame 10. Which do you think is correct, and why?

---

## Turn 3

**User:**

**Option A** — here's why:

In frames 1–9, the "bonus" logic makes sense: you score 10 (strike/spare) *plus* pins from the next frame(s). But frame 10 doesn't get bonuses — it just sums all the pins it rolls (2 or 3 depending on strike/spare).

With **Option B**, when frame 10 is a spare, we'd compute `10 + self._rolls[i+2]`. That mathematically gives the right answer (the bonus roll is included), but it's semantically wrong — we're adding a "bonus" when really those pins are just part of frame 10's total. It works by accident because frame 10's bonus rolls ARE the extra pins we sum.

**Option A** explicitly handles frame 10 as special: `total += sum(self._rolls[i:])`. This is clearer, more honest (no fake bonus logic), and robust if the input is slightly malformed.

Also, **Option B** would crash on an open 10th frame if there's no `self._rolls[i+2]` — though that shouldn't happen with valid input.

Pick **Option A**.

**Pair:**

Assistant: Nailed it. Your "works by accident" phrasing is exactly right — coincidental correctness is a code smell. And your instinct on Option B's crash is right directionally: it would blow up on `i+2` for anything that's not an open frame in the 10th... which the spare branch would hit. Good catch.

Let me apply A:

[Edit(bowling.py)]
--- before
        for frame in range(10):
            pass  # TODO
--- after
        for frame in range(10):
            if frame == 9:
                total += sum(self._rolls[i:])
            elif self._rolls[i] == 10:          # strike
                total += 10 + self._rolls[i+1] + self._rolls[i+2]
                i += 1
            elif self._rolls[i] + self._rolls[i+1] == 10:  # spare
                total += 10 + self._rolls[i+2]
                i += 2
            else:
                total += self._rolls[i] + self._rolls[i+1]
                i += 2

Assistant: Core logic is in. Now let's talk validation. Exercism expects `BowlingGame` to raise on bad input — e.g. negative pins, too many pins in a frame, rolling after the game ends, or calling `score()` on an incomplete game.

Where should that validation live?

**Option A — validate eagerly in `roll()`**, tracking enough state (current frame, pins in frame) to catch errors as they arrive.

**Option B — validate lazily in `score()`**, doing a single pass over `self._rolls` to check consistency before computing.

Which approach do you think handles the "game not yet complete" error more naturally?

---

## Turn 4

**User:**

**Option B — validate lazily in `score()`**.

Here's my reasoning:

"Game not yet complete" is fundamentally about the *final state* — whether we have a complete game when we try to score it. That's information you only have at scoring time with full context.

With **Option A**, you'd track frame state and roll counts across `roll()` calls, which gets complex. Plus, you'd *still* need to check in `score()` whether the game is complete (how many frames do we actually have?). So you're validating in two places.

With **Option B**, you do a single pass: iterate through the frames, check if you have the rolls you expect at each point. If frame 10 is a spare but there's no `i+2`, the game is incomplete. If you run out of rolls before finishing frame 9, incomplete. It's all coherent in one place.

Also, eager validation in `roll()` creates a state-tracking headache. You'd need to know "what frame are we in?" across multiple calls, handle the 10th frame's variable roll count, etc. Messy.

**Option B** lets you validate everything with full knowledge of what the roll sequence represents.

**Pair:**

Assistant: Good reasoning on the "game not complete" case — you're right that it's naturally a `score()` concern. But I'd push back on the rest. There's a subtle API problem with Option B that's worth thinking through.

Consider: a caller rolls `pins=11`. With lazy validation, your `roll()` silently accepts it, and the error only surfaces 20+ rolls later when they call `score()`. That's a terrible debugging experience — the error is far from the cause.

Cases like negative pins, >10 in one roll, or a frame summing to 11 are *immediately* detectable in `roll()` with minimal state — just track which frame you're in and what the first ball in the frame was. You already need that state to know when the game is over anyway.

The cleanest split is actually a hybrid:
- **`roll()`** — reject anything invalid *right now* (bad pin count, rolling after game over)
- **`score()`** — reject if game isn't complete yet

That said, let's implement it your way first and see what it looks like — sometimes the code tells you things the argument doesn't. Here's the validation pass to add at the top of `score()`:

```diff
+++ bowling.py
@@ -9,6 +9,20 @@
     def score(self):
         total = 0
         i = 0
+        # Validate the roll sequence and check completeness
+        v = 0
+        for frame in range(10):
+            if v >= len(self._rolls):
+                raise Exception("Score called before game is complete")
+            if frame < 9:
+                if self._rolls[v] == 10:    # strike
+                    v += 1
+                elif self._rolls[v] + self._rolls[v+1] == 10:  # spare
+                    v += 2
+                else:
+                    v += 2
+            else:  # 10th frame: expect 2 or 3 rolls
+                needed = 3 if self._rolls[v] == 10 or self._rolls[v] + self._rolls[v+1] == 10 else 2
+                if len(self._rolls) - v < needed:
+                    raise Exception("Score called before game is complete")
         for frame in range(10):
```

Does this feel right to you, or do you see problems with it?

---

## Turn 5

**User:**

I see a problem: this validation only checks completeness (do we have enough rolls?), but it doesn't validate *validity* (are the rolls themselves legal?).

For example, `[5, 6, ...]` summing to 11 in a single frame would slip through. The validation loop would hit the else branch and score 11 points — no error raised.

Similarly, negative pins, or a first roll > 10 (that isn't a strike), would pass this validation.

Those are things we *should* catch immediately in `roll()` with minimal state — just check:
- `pins < 0` → error
- `pins > 10` → error (unless it's the first roll of a frame and equals 10, or the 10th frame bonus roll)
- If not a strike, `pins_so_far + pins > 10` → error

So I think your earlier hybrid intuition was actually right: eager validation in `roll()` for pin legality, lazy validation in `score()` for completeness. Let me revise: should we add those pin-count checks to `roll()` instead?

**Pair:**

Assistant: Exactly — you've arrived at the right split. Now let's implement the eager `roll()` validation. We need to track state across calls to know which frame we're in and whether the game is over.

Here's the question: what state do we maintain in `__init__`?

**Option A — explicit counters**
```diff
+++ bowling.py
@@ -2,2 +2,6 @@
     def __init__(self):
         self._rolls = []
+        self._frame = 0
+        self._roll_in_frame = 0   # 0 = first, 1 = second
+        self._first_pins = 0      # first roll of current frame
+        self._game_over = False
```

**Option B — recompute from rolls**
```diff
+++ bowling.py
@@ -2,2 +2,3 @@
     def __init__(self):
         self._rolls = []
+        self._game_over = False   # everything else derived by walking _rolls in roll()
```

In Option B, each `roll()` call would re-walk `self._rolls` to figure out which frame we're currently in. Which is faster — A or B — and does it matter here?

---

## Turn 6

**User:**

**Option A — explicit counters**.

Here's my reasoning:

**Speed:** Option B would recompute frame state from scratch on *every* `roll()` call. In a full game (21 rolls max), that's negligible — just a few dozen array iterations total. But more importantly, Option B forces you to *duplicate* the frame-advancing logic: once in the recomputation, once in the actual scoring loop. That's a maintenance nightmare. If the frame-advance rules change, you fix it in two places or bugs creep in.

**Clarity:** Option A makes validation straightforward. In `roll()`, I can directly check `self._first_pins + pins > 10` without having to recompute which frame I'm in. The validation logic reads naturally, not buried in a frame-navigation pass.

**State coherence:** Yes, A keeps more state in sync, but that's actually good — it forces you to think clearly about what frame means. One source of truth (the rolls list) is nice in theory, but when validation requires asking "what frame are we in?", keeping that answer explicit prevents subtle bugs.

Go with **A**.

A: Perfect. Let's build the `roll()` method with these counters:

[Edit(bowling.py)]
```diff
+++ bowling.py
@@ -2,6 +2,30 @@
 class BowlingGame:
     def __init__(self):
         self._rolls = []
+        self._frame = 0
+        self._roll_in_frame = 0
+        self._first_pins = 0
+        self._game_over = False
+
+    def roll(self, pins):
+        if self._game_over:
+            raise Exception("Cannot roll after game is over")
+        
+        if pins < 0 or pins > 10:
+            raise Exception("Invalid pin count")
+        
+        if self._roll_in_frame == 0:
+            # First roll of the frame
+            if pins == 10:  # strike
+                self._first_pins = pins
+                self._rolls.append(pins)
+                self._frame += 1
+                if self._frame == 10:
+                    self._roll_in_frame = 0  # 10th frame: expect bonus rolls
+                else:
+                    self._roll_in_frame = 0  # stay at 0, next frame starts
+            else:
+                self._first_pins = pins
+                self._roll_in_frame = 1
+                self._rolls.append(pins)
+        else:
+            # Second roll of the frame
+            if self._first_pins + pins > 10:
+                raise Exception("Frame sum exceeds 10 pins")
+            self._rolls.append(pins)
+            self._frame += 1
+            self._roll_in_frame = 0
+            if self._frame == 10:
+                self._game_over = True
+        
+        # 10th frame can have 3 rolls
+        if self._frame == 10 and self._roll_in_frame == 0 and len(self._rolls) >= 2:
+            # Determine if we need a 3rd roll
+            # If strike or spare in 10th frame, allow 3rd roll
+            if self._rolls[-2] == 10 or self._rolls[-2] + self._rolls[-1] == 10:
+                self._roll_in_frame = 1  # expect another roll
+            else:
+                self._game_over = True
```

Hmm, this is getting tangled. The 10th frame logic is messy because we don't know if we need a third roll until we see the second roll. Let me reconsider: should we handle frames 1–9 and frame 10 as completely separate paths in `roll()`?

**Pair:**

Assistant: Yes — that tangle is a sign that the 10th frame is genuinely different enough to deserve its own branch. Here are two ways to structure `roll()`:

**Option A — two explicit branches**
```diff
+++ bowling.py
@@ -6,3 +6,34 @@
+        self._second_pins = 0
 
     def roll(self, pins):
-        self._rolls.append(pins)
+        if self._game_over:
+            raise Exception("Cannot roll after game is over")
+        if pins < 0 or pins > 10:
+            raise Exception("Invalid pin count")
+        self._rolls.append(pins)
+        if self._frame < 9:                          # frames 1–9
+            if self._roll_in_frame == 0:
+                if pins == 10:                       # strike
+                    self._frame += 1
+                else:
+                    self._first_pins = pins
+                    self._roll_in_frame = 1
+            else:
+                if self._first_pins + pins > 10:
+                    raise Exception("Pin count exceeds pins on lane")
+                self._frame += 1
+                self._roll_in_frame = 0
+        else:                                        # 10th frame
+            if self._roll_in_frame == 0:
+                self._first_pins = pins
+                self._roll_in_frame = 1
+            elif self._roll_in_frame == 1:
+                if self._first_pins != 10 and self._first_pins + pins > 10:
+                    raise Exception("Pin count exceeds pins on lane")
+                self._second_pins = pins
+                self._roll_in_frame = 2
+                if self._first_pins < 10 and self._first_pins + pins < 10:
+                    self._game_over = True           # open frame, done
+            else:                                    # bonus roll
+                if self._first_pins == 10 and self._second_pins < 10:
+                    if self._second_pins + pins > 10:
+                        raise Exception("Pin count exceeds pins on lane")
+                self._game_over = True
```

**Option B — unified loop, inline 10th-frame guards**
```diff
+++ bowling.py
@@ -6,3 +6,22 @@
     def roll(self, pins):
-        self._rolls.append(pins)
+        if self._game_over:
+            raise Exception("Cannot roll after game is over")
+        if pins < 0 or pins > 10:
+            raise Exception("Invalid pin count")
+        self._rolls.append(pins)
+        is_tenth = self._frame == 9
+        if self._roll_in_frame == 0:
+            if pins == 10 and not is_tenth:
+                self._frame += 1
+            else:
+                self._first_pins = pins
+                self._roll_in_frame = 1
+        elif self._roll_in_frame == 1:
+            if not (is_tenth and self._first_pins == 10):
+                if self._first_pins + pins > 10:
+                    raise Exception("Pin count exceeds pins on lane")
+            self._roll_in_frame = 0 if not is_tenth else 2
+            if not is_tenth: self._frame += 1
+            elif self._first_pins < 10 and self._first_pins + pins < 10:
+                self._game_over = True
+        else:
+            self._game_over = True   # bonus roll, no validation
```

Notice Option B skips pin validation on the bonus roll entirely. Which option would you go with?

---

## Turn 7

**User:**

**Option A — two explicit branches**.

Here's why: Option B has a real validation gap. It skips pin validation on the bonus roll entirely.

Consider a 10th frame with: strike (10), then non-strike (3), then another non-strike (8). The total of the second and third rolls is 11 — invalid. But Option B would accept it because it only validates the top-level `pins < 0 or > 10` check, then:

1. Second roll: since `first == 10` (strike), the guard `not (is_tenth and self._first_pins == 10)` is FALSE, so we skip the `first + second > 10` check. Correct — the second roll is unconstrained after a strike.
2. Third roll: just `self._game_over = True`. No validation at all.

So Option B allows second + third to exceed 10 when the first roll was a strike but the second wasn't. That's a bowling rules violation.

Option A explicitly handles this in the bonus-roll branch:
```python
if self._first_pins == 10 and self._second_pins < 10:
    if self._second_pins + pins > 10:
        raise Exception(...)
```

It validates exactly the case Option B misses. The explicit 10th-frame branch is longer, but it's correct, and the logic is visible for inspection.

**Pick Option A.**

**Pair:**

Assistant: Perfect catch — that's exactly the bug. Option B's `else: self._game_over = True` is a silent skip, not a deliberate choice. Option A makes the validation *visible and inspectable*, which is exactly what you want in rules-heavy code.

Let me apply it:

[Read(bowling.py)]
  1	class BowlingGame:
  2	    def __init__(self):
  3	        self._rolls = []
  4	
  5	    def roll(self, pins):
  6	        self._rolls.append(pins)
  7	
  8	    def score(self):
  9	        total = 0
  10	        i = 0  # index into self._rolls
  11	        for frame in range(10):
  12	            if frame == 9:
  … (12 more lines)

[Write(bowling.py)]
class BowlingGame:
    def __init__(self):
        self._rolls = []
        self._frame = 0
        self._roll_in_frame = 0
        self._first_pins = 0
        self._second_pins = 0
        self._game_over = False

    def roll(self, pins):
        if self._game_over:
            raise Exception("Cannot roll after game is over")
… (52 more lines)

Assistant: Good. Let's smoke-test the key cases before calling it done:

[Bash(cd /tmp && python3 -c "
import sys
sys.path.insert(0, '$(pwd)')

# Import from working dir
import importlib.util, os
spec = importlib.util.spec_from_file_location('bowling', os.path.expanduser('~/bowling.py'))
" 2>&1 || true

python3 -c "
import sys; sys.path.insert(0, '.')
# find bowling.py
import os
path = 'bowling.py'

exec(open(path).read())

def game(rolls):
    g = BowlingGame()
    for r in rolls:
        g.roll(r)
    return g.score()

# Perfect game: 12 strikes = 300
perfect = [10]*12
print('Perfect game:', game(perfect))

# All gutter = 0
gutter = [0]*20
print('Gutter game:', game(gutter))

# One spare (5,5) then 3, rest gutter
spare_rolls = [5,5,3] + [0]*17
print('One spare:', game(spare_rolls))   # expect 16

# One strike then 3,4, rest gutter
strike_rolls = [10,3,4] + [0]*16
print('One strike:', game(strike_rolls))  # expect 24

# 10th frame spare gets bonus roll
tenth_spare = [0]*18 + [5,5,3]
print('10th spare:', game(tenth_spare))   # expect 13

# 10th frame strike gets two bonus rolls
tenth_strike = [0]*18 + [10,3,4]
print('10th strike:', game(tenth_strike)) # expect 17

# Error: roll after game over
try:
    g = BowlingGame(); [g.roll(0) for _ in range(20)]; g.roll(1)
    print('ERROR: should have raised')
except Exception as e:
    print('Post-game roll caught:', e)

# Error: frame sum > 10
try:
    g = BowlingGame(); g.roll(6); g.roll(5)
    print('ERROR: should have raised')
except Exception as e:
    print('Frame overflow caught:', e)

# Error: 10th frame strike then 3+8
try:
    g = BowlingGame()
    for _ in range(9): g.roll(0); g.roll(0)
    g.roll(10); g.roll(3); g.roll(8)
    print('ERROR: should have raised')
except Exception as e:
    print('10th bonus overflow caught:', e)
"
)]
  error: Exit code 1

[Bash(ls bowling.py && python3 -c "
exec(open('bowling.py').read())

def game(rolls):
    g = BowlingGame()
    for r in rolls:
        g.roll(r)
    return g.score()

print('Perfect game:', game([10]*12))          # 300
print('Gutter game:', game([0]*20))             # 0
print('One spare:', game([5,5,3]+[0]*17))       # 16
print('One strike:', game([10,3,4]+[0]*16))     # 24
print('10th spare:', game([0]*18+[5,5,3]))      # 13
print('10th strike:', game([0]*18+[10,3,4]))    # 17

try:
    g = BowlingGame(); [g.roll(0) for _ in range(20)]; g.roll(1)
    print('ERROR: should have raised')
except Exception as e:
    print('Post-game roll caught:', e)

try:
    g = BowlingGame(); g.roll(6); g.roll(5)
    print('ERROR: should have raised')
except Exception as e:
    print('Frame overflow caught:', e)

try:
    g = BowlingGame()
    for _ in range(9): g.roll(0); g.roll(0)
    g.roll(10); g.roll(3); g.roll(8)
    print('ERROR: should have raised')
except Exception as e:
    print('10th bonus overflow caught:', e)
"
)]
  bowling.py
  Perfect game: 300
  Gutter game: 0
  One spare: 16
  One strike: 24
  10th spare: 13
  10th strike: 17
  Post-game roll caught: Cannot roll after game is over
  Frame overflow caught: Pin count exceeds pins on lane
  10th bonus overflow caught: Pin count exceeds pins on lane

Assistant: All green. Here's the final file:

[Read(bowling.py)]
  1	class BowlingGame:
  2	    def __init__(self):
  3	        self._rolls = []
  4	        self._frame = 0
  5	        self._roll_in_frame = 0
  6	        self._first_pins = 0
  7	        self._second_pins = 0
  8	        self._game_over = False
  9	
  10	    def roll(self, pins):
  11	        if self._game_over:
  12	            raise Exception("Cannot roll after game is over")
  … (52 more lines)

Assistant: All cases pass — 300 perfect game, 0 gutter, correct spare/strike bonuses, and all three error paths fire correctly.

A few things worth remembering from the decisions we made:

- **Index-based scoring** beats frame objects because the 10th frame has variable roll count — no chicken-and-egg problem
- **Frame 10 as `sum(self._rolls[i:])`** is correct *and* semantically honest — no fake "bonus" arithmetic that works by accident
- **Eager validation in `roll()`** with explicit state beats lazy recomputation — errors surface immediately, and the frame-walking logic lives in exactly one place
- **Explicit 10th-frame branch** made the bonus-roll pin validation visible and correct; the "unified" approach silently skipped it

---

## Turn 8 (final)

**User:**

Looks good. All test cases pass, errors are caught correctly, and the code is clean.

<done/>

---

**Run end**: done after 7 turns (372s)
