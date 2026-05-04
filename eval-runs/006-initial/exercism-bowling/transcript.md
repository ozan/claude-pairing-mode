# exercism-bowling

- Source: `exercism`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T02:53:39.729Z

---

## Turn 1

**User:**

Exercism 'Bowling': implement a 10-pin bowling scorer. Track frames, handle strikes (next two rolls bonus), spares (next roll bonus), and the special 10th-frame bonus rolls. Return the final score from a list of rolls.

**Pair:**

Thinking: Let me start building a bowling scorer. This is a classic problem with some interesting implementation decisions. Let me think about the key design choices:
  
  1. How to track frames vs. rolls - this is the crux
  2. How to handle the 10th frame special rules
  
  Let me start with a foundational design question: how to represent the game state.
  
  Key design decisions:
  1. **Frame-by-frame vs. roll array** - Two main approaches:
     - Process rolls sequentially with frame tracking
     - Pre-parse all rolls into frames then score
  
  Let me think about what makes a good teaching moment here. The first big decision is probably the overall approach to scoring.
  
  
  Now I'm going to start implementing this.

Assistant: Let's build this up step by step. First, a key design question before we write any code:

OPTIONS:
[A] Roll array + frame scan
Store all rolls in a flat list. Score by scanning through rolls with a frame index, skipping ahead for strikes/spares to find bonus balls.

[B] Frame objects
Parse rolls into Frame objects as they arrive, each storing their pins and knowing if they're a strike/spare.

(Reply with A or B, or ask a follow-up question.)

Thinking: The tool isn't available in this context. Let me just proceed directly with building the bowling scorer. I'll make the design decisions and explain my reasoning as I go.
  
  Let me use the flat roll array approach since it's the better choice, and I'll explain why as I build it out.

Assistant: The tool isn't available right now, so let me just build this — I'll explain key decisions as we go.

The classic approach: store all rolls in a **flat list**, then scan through with a frame index. This sounds too simple, but it's elegant — bonus balls for strikes/spares are just `rolls[i+1]`, `rolls[i+2]` with no frame-boundary bookkeeping.

Let me check if the file exists first:

[Glob(bowling.py)]
  No files found

[Write(bowling.py)]
class BowlingGame:
    def __init__(self):
        self.rolls = []

    def roll(self, pins):
        self.rolls.append(pins)

    def score(self):
        total = 0
        i = 0  # index into self.rolls

        for frame in range(10):
… (26 more lines)

Assistant: Now let's add validation and make sure we handle the Exercism-style interface (which often uses a `score()` function rather than a class). Let me check:

[Bash(ls *.py 2>/dev/null; ls tests/ 2>/dev/null || ls *test* 2>/dev/null || echo "no test files found")]
  bowling.py
  no test files found

[Bash(exercism download --exercise=bowling --track=python 2>/dev/null || echo "exercism CLI not available or not logged in")]
  exercism CLI not available or not logged in

Assistant: No Exercism CLI — let me write the scorer to match the standard Exercism bowling interface (a `score(rolls)` function) and add proper validation. Let me also think about what the 10th frame really requires.

The tricky part: in the **10th frame**, a strike or spare earns bonus rolls, but those bonus rolls are *not* extra frames — they just extend the roll list. The flat-array approach handles this automatically since `for frame in range(10)` stops at 10 frames, and any bonus rolls in the 10th frame are already present in `self.rolls` for the lookahead.

Let me rewrite to the Exercism interface and add validation:

[Write(bowling.py)]
class BowlingGame:
    def __init__(self):
        self.rolls = []
        self._game_over = False
        self._current_frame = 1
        self._rolls_in_frame = 0
        self._frame_first_roll = 0  # pins on first roll of current frame

    def roll(self, pins):
        if self._game_over:
            raise Exception("Game is already over, cannot add more rolls")
        if pins < 0 or pins > 10:
… (68 more lines)

Assistant: Now let's test it with some key scenarios:

[Write(test_bowling.py)]
import pytest
from bowling import BowlingGame


def make_game(rolls):
    g = BowlingGame()
    for r in rolls:
        g.roll(r)
    return g


def test_gutter_game():
… (87 more lines)

[Bash(python -m pytest test_bowling.py -v 2>&1)]
  error: Exit code 127

[Bash(python3 -m pytest test_bowling.py -v 2>&1)]
  error: Exit code 1

Thinking: The test is failing for the 10th frame spare. Let me trace through:
  
  - Rolls: [0] * 18 + [5, 5, 7]
  - Frames 1-9: all gutter (0+0 = 0 each) → 0 total
  - Frame 10: 5+5 = spare → bonus next roll = 7 → frame score = 10+7 = 17
  
  But I put `assert g.score() == 22` in the test. Wait, 0*18 = 0, then 10+7 = 17 for the 10th frame. But wait... the test says:
  
  
  I wrote 22 but the comment says 17 for 10th + rest 0 = 17. So my test had a wrong expected value! Let me fix the test.
  
  Wait, actually: 0 * 9 frames (18 rolls) = 0. Frame 10: spare 5+5 → score = 10 + 7 = 17.
  
  I see the issue now—my comment correctly calculated 17, but I mistakenly put 22 as the expected value. I need to correct that.

Assistant: The failure is actually a bug in my test — I wrote `22` but my own comment says `10+7=17`. Let me fix that and also double-check the scoring logic is correct:

Frames 1–9: `[0]*18` → 0 each → 0 total. Frame 10: spare `5+5`, bonus `7` → `10+7 = 17`. Total = **17**. My test had a typo.

[Edit(test_bowling.py)]
--- before
    assert g.score() == 22  # 10+7 = 17 for 10th, rest 0
--- after
    assert g.score() == 17  # 10+7 = 17 for 10th, rest 0

[Bash(python3 -m pytest test_bowling.py -v 2>&1)]
  ============================= test session starts ==============================
  platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0 -- /Library/Developer/CommandLineTools/usr/bin/python3
  cachedir: .pytest_cache
  rootdir: /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-bowling-Wz1mYl
  collecting ... collected 13 items
  
  test_bowling.py::test_gutter_game PASSED                                 [  7%]
  test_bowling.py::test_all_ones PASSED                                    [ 15%]
  test_bowling.py::test_spare_in_first_frame PASSED                        [ 23%]
  test_bowling.py::test_strike_in_first_frame PASSED                       [ 30%]
  test_bowling.py::test_perfect_game PASSED                                [ 38%]
  test_bowling.py::test_tenth_frame_spare PASSED                           [ 46%]
  … (9 more lines)

Assistant: 13/13. Let's look at the final implementation:

[Read(bowling.py)]
  1	class BowlingGame:
  2	    def __init__(self):
  3	        self.rolls = []
  4	        self._game_over = False
  5	        self._current_frame = 1
  6	        self._rolls_in_frame = 0
  7	        self._frame_first_roll = 0  # pins on first roll of current frame
  8	
  9	    def roll(self, pins):
  10	        if self._game_over:
  11	            raise Exception("Game is already over, cannot add more rolls")
  12	        if pins < 0 or pins > 10:
  … (68 more lines)

Assistant: All 13 tests pass. Here's a summary of what we built and why it works:

---

**Architecture: flat roll array + frame scan**

The `score()` loop is beautifully simple because of one key insight: **bonus balls live in the same flat list**. When you score a strike in frame 3, you just look at `rolls[i+1]` and `rolls[i+2]` — those might be from frame 4, or even frame 5 if there's another strike. You don't need to cross frame object boundaries.

The 10th frame "just works" too: after the loop hits frame 10 with index `i`, `rolls[i+1]` and `rolls[i+2]` are the bonus balls already appended to the list.

**Two separate concerns**

- `_advance_state()` handles *validation and game-over detection* — it needs to understand frame structure so it knows when rolls are illegal and when to stop accepting input.
- `score()` handles *calculation* — it only needs the flat list and the simple lookahead.

The one edge case worth noting: the 10th-frame validation in `_advance_state` has some missing detail (e.g. `10, 6, 5` should be invalid since you can't knock down 11 pins after a strike resets to 10). That's a good place to harden if Exercism's test suite catches it.

---

## Turn 2

**User:**

Thanks for walking me through this. I'm seeing how the flat roll array really does simplify the scoring loop — I was worried the 10th frame would be a mess, but since the bonus balls are already in the same list, the lookahead just works.

One thing caught my eye though: you mentioned at the end that `10, 6, 5` should be invalid (can't have 11 pins after a strike resets). Looking back at `_advance_state`, I see we check `pins + frame_first_roll <= 10` for non-strike frames, but in the 10th frame after a strike, do we reset that constraint? Let me trace through:

- Roll 1 of frame 10: strike (10) → `_frame_first_roll = 0`
- Roll 2 of frame 10: 6 → `pins + 0 = 6` ✓
- Roll 3 of frame 10: 5 → but we check `pins + _frame_first_roll`... which is still 0 from the reset?

So it looks like it'd allow `10, 6, 5` when it shouldn't. Should we add a stricter constraint for the 10th frame bonus rolls? Or is the actual Exercism test suite going to catch this and we should just verify against that first?

**Pair:**

Thinking: The user has correctly identified a bug in the 10th frame validation. Let me trace through carefully:
  
  In `_advance_state`, when we're in the 10th frame:
  - roll_in == 0: first roll is a strike (10), `_frame_first_roll = 10`, `_rolls_in_frame = 1`
  - roll_in == 1: since `_frame_first_roll == 10` (strike), we go into that branch, `_rolls_in_frame = 2`, and `_frame_first_roll = pins` (we store the second roll, e.g. 6)
  
  
  - roll_in == 2: the third roll just sets `_game_over = True` without validating that the second and third rolls sum to 10 or less
  
  For the sequence `10, 6, 5`, the third roll gets accepted even though `6 + 5 = 11`, which violates the constraint that non-strike rolls in the 10th frame can't exceed 10 pins total. The fix needs to validate this sum before marking the game as over.
  
  The validation rule for the 10th frame's bonus rolls should be: if the second roll wasn't a strike, then the second and third rolls must sum to 10 or less. But if the second roll was a strike, the third roll can be anything from 0-10 independently. I'm working through the logic for validating the third roll in the 10th frame—if the first roll was a strike, the second roll can be anything from 0-10, and then the third roll's validity depends on whether the second roll was also a strike or not. If the second roll wasn't a strike, the third roll is capped so that the second and third rolls together don't exceed 10 pins. I'm realizing the logic gets tricky here—in the spare case, `_frame_first_roll` still holds the original first roll value, not the second roll, so I need a way to track that a spare occurred to properly validate the third roll without constraints. I need to distinguish between different scenarios in the tenth frame based on what happened with the first two rolls. If the second roll was a strike after the first strike, the third roll can be anything from 0-10, but if the second roll wasn't a strike, then the second and third rolls together can't exceed 10. The cleanest solution is probably adding a flag to track whether the first roll was a strike, so I can make the right validation decision when the third roll comes in. I need to track additional state to distinguish between a strike followed by a non-strike versus a spare—either with a boolean flag like `_tenth_was_spare` or by storing the second roll value separately. The simplest approach is probably to track `_tenth_second_roll` so I can reference what happened on the second roll when validating the third. I see the issue now—when the first roll is a strike, the second roll gets stored in `_frame_first_roll`, so I need to check whether that second roll was also a strike to determine what constraint applies to the third roll. If the second roll wasn't a strike, the sum must stay under 10; if it was a strike, there's no such constraint. The spare case is different because `_frame_first_roll` stays as the actual first roll, so I can distinguish the paths by checking whether `_frame_first_roll` equals 10.
  
  Adding a flag to track when the first roll was a strike gives me a clean way to handle this logic in the bonus roll validation.
  
  Now I'm walking through some test cases to verify the constraint works correctly: a strike followed by another strike and a third roll should be valid, while a strike followed by a non-strike where the two rolls sum to more than 10 should fail. For spares, the flag stays false so the constraint doesn't apply. flag is False, so no constraint. Third roll = 7, valid. ✓
  
  Looks good. Let me present this fix.
  
  Actually, I also want to think about whether there's a case where the user rolls `5, 5, 11` in the 10th frame. That would fail the basic `pins > 10` check in `roll()`. Good.
  
  And `10, 3, 9`? First strike, second 3, third 9. `_frame_first_roll = 3`. Check: `3 + 9 = 12 > 10` → invalid. ✓
  
  What about `10, 0, 10`? First strike, second 0, third 10. `_frame_first_roll = 0`. Check: `0 + 10 = 10 <= 10` → valid. That should be valid right? Yes, if you roll 0 pins then 10 pins, you got a spare on that mini-game. ✓
  
  The fix looks solid. Now I should add a test case to cover this scenario.

Assistant: You traced it exactly right. Here's what happens with `10, 6, 5` in our code:

- roll_in 0: strike → `_frame_first_roll = 10`, `_rolls_in_frame = 1`
- roll_in 1: first was strike, so → `_frame_first_roll = 6` (updated to second roll), `_rolls_in_frame = 2`  
- roll_in 2: falls into `else` branch → **just sets `_game_over = True`, no validation at all**

The fix needs one new boolean. The tricky part is that at roll_in 2 we need to distinguish two valid paths that got there differently:

| Path | `_frame_first_roll` at roll_in 2 | Constraint on roll 3 |
|---|---|---|
| strike → non-strike | second roll value (e.g. 6) | `second + third ≤ 10` |
| strike → strike | 10 | none (fresh 10 pins) |
| spare | first roll value (e.g. 5) | none (pins reset after spare) |

Without a flag, we can't tell path 1 from path 3 — both have `_frame_first_roll < 10`. Let's fix it:

[Edit(bowling.py)]
--- before
        self._current_frame = 1
        self._rolls_in_frame = 0
        self._frame_first_roll = 0  # pins on first roll of current frame
--- after
        self._current_frame = 1
        self._rolls_in_frame = 0
        self._frame_first_roll = 0  # pins on first roll of current frame
        self._tenth_first_was_strike = False

[Edit(bowling.py)]
--- before
            elif roll_in == 1:
                if self._frame_first_roll == 10:
                    # First was a strike; second can be 0-10
                    self._rolls_in_frame = 2
                    self._frame_first_roll = pins  # track second roll for validation
                elif self._frame_first_roll + pins == 10:
--- after
            elif roll_in == 1:
                if self._frame_first_roll == 10:
                    # First was a strike; second can be 0-10
                    self._tenth_first_was_strike = True
                    self._rolls_in_frame = 2
                    self._frame_first_roll = pins  # track second roll for validation
                elif self._frame_first_roll + pins == 10:

[Edit(bowling.py)]
--- before
            else:  # roll_in == 2 (bonus roll)
                # If first roll was a strike and second was also a strike,
                # third can be 0-10; otherwise second + third must be <= 10
                # unless second was also a strike.
                self._game_over = True
--- after
            else:  # roll_in == 2 (bonus roll)
                if self._tenth_first_was_strike and self._frame_first_roll != 10:
                    # Strike then non-strike: pins reset but were partially knocked down.
                    # second + third must not exceed 10.
                    if self._frame_first_roll + pins > 10:
                        raise Exception("Pin count exceeds pins on the lane")
                self._game_over = True

Assistant: Now add a test that would have caught this:

[Edit(test_bowling.py)]
--- before
def test_typical_game():
--- after
def test_tenth_frame_strike_then_invalid_bonus():
    # 10, 6, 5 is invalid: after a strike, second=6 leaves 4 pins, can't knock 5
    g = BowlingGame()
    for r in [0] * 18 + [10, 6]:
        g.roll(r)
    with pytest.raises(Exception):
        g.roll(5)


def test_tenth_frame_strike_then_valid_bonus():
    # 10, 6, 4 is valid: second=6, third=4 (spare on the mini-frame)
    g = make_game([0] * 18 + [10, 6, 4])
    assert g.score() == 20  # 10+6+4 = 20


def test_tenth_frame_double_strike_then_any():
    # 10, 10, 7 is valid: after two strikes, fresh 10 pins for third
    g = make_game([0] * 18 + [10, 10, 7])
    assert g.score() == 27


def test_typical_game():

[Bash(python3 -m pytest test_bowling.py -v 2>&1)]
  ============================= test session starts ==============================
  platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0 -- /Library/Developer/CommandLineTools/usr/bin/python3
  cachedir: .pytest_cache
  rootdir: /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-bowling-Wz1mYl
  collecting ... collected 16 items
  
  test_bowling.py::test_gutter_game PASSED                                 [  6%]
  test_bowling.py::test_all_ones PASSED                                    [ 12%]
  test_bowling.py::test_spare_in_first_frame PASSED                        [ 18%]
  test_bowling.py::test_strike_in_first_frame PASSED                       [ 25%]
  test_bowling.py::test_perfect_game PASSED                                [ 31%]
  test_bowling.py::test_tenth_frame_spare PASSED                           [ 37%]
  … (12 more lines)

Assistant: 16/16. The fix is minimal — one flag, one guard. 

The reason you need the flag and can't just inspect `_frame_first_roll` is exactly what you suspected: at roll_in 2, both the "strike→non-strike" and "spare" paths have `_frame_first_roll < 10`, so the value alone is ambiguous about whether the pin constraint applies. The flag records *how* we arrived at the bonus roll, not just what the pin count was.

One thing worth noting about the three valid 10th-frame bonus cases:

```
10, 10, X  → two strikes: fresh 10 pins, X can be 0–10
10, N, M   → strike then N: M ≤ 10-N  (what we just fixed)
A, B, X    → spare (A+B=10): fresh 10 pins, X can be 0–10
```

The spare case gets away without the constraint because pins physically reset after you clear the lane on a spare — same as after a strike.

---

## Turn 3 (final)

**User:**

That makes sense now. The flag lets us distinguish the paths:

- `_tenth_first_was_strike = True` + `_frame_first_roll != 10` → "strike then non-strike", so constrain the third roll
- `_tenth_first_was_strike = True` + `_frame_first_roll == 10` → "strike then strike", no constraint
- `_tenth_first_was_strike = False` → spare path, flag never set, so constraint skipped

I was confused because I thought we could just check `_frame_first_roll` at the end, but you're right — it gets reused to store the second roll value, so we'd lose the original signal. The flag is the clean way to carry that information forward.

The three patterns you listed make it click for me. And the fix is tight — just one boolean and one guard clause. Looks solid.

<done/>

---

**Run end**: done after 2 turns (193s)
