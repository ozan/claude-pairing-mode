# exercism-bowling

- Source: `exercism`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:29:41.802Z

---

## Turn 1

**User:**

Exercism 'Bowling': implement a 10-pin bowling scorer. Track frames, handle strikes (next two rolls bonus), spares (next roll bonus), and the special 10th-frame bonus rolls. Return the final score from a list of rolls.

**Pair:**

[Glob(**/*bowling*)]
  No files found

[Bash(ls)]
  (Bash completed with no output)

Assistant: No existing files — I'll build the solution from scratch. Let me implement a clean Python bowling scorer with proper frame tracking and validation.

[Write(/bowling.py)]
"""10-pin bowling scorer (Exercism exercise)."""


class BowlingGame:
    """Track rolls and compute the final score of a 10-pin bowling game.

    Rules summary
    -------------
    * A game has 10 frames; each frame normally has up to 2 rolls.
    * **Strike** (10 pins on the first roll of a frame): frame score is
      10 + the next *two* rolls as a bonus.  Only one roll is consumed for
      the frame itself, so the index advances by 1.
… (207 more lines)

[Bash(pwd && ls -la)]
  /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-bowling-RQoWek
  total 0
  drwx------    2 oz  staff    64  3 May 20:29 .
  drwx------@ 182 oz  staff  5824  3 May 20:30 ..

[Bash(chmod 755 /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-bowling-RQoWek && ls -la /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-bowling-RQoWek)]
  total 0
  drwxr-xr-x    2 oz  staff    64  3 May 20:29 .
  drwx------@ 182 oz  staff  5824  3 May 20:30 ..

[Write(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-bowling-RQoWek/bowling.py)]
"""10-pin bowling scorer (Exercism exercise)."""


class BowlingGame:
    """Track rolls and compute the final score of a 10-pin bowling game.

    Rules summary
    -------------
    * A game has 10 frames; each frame normally has up to 2 rolls.
    * **Strike** (10 pins on the first roll of a frame): frame score is
      10 + the next *two* rolls as a bonus.  Only one roll is consumed for
      the frame itself, so the index advances by 1.
… (205 more lines)

Assistant: Now let's write a thorough test suite and run it:

[Write(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-bowling-RQoWek/test_bowling.py)]
"""Tests for the bowling scorer, mirroring the Exercism test suite."""

import pytest
from bowling import BowlingGame, score


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def play(rolls: list[int]) -> BowlingGame:
    g = BowlingGame()
… (188 more lines)

[Bash(python -m pytest test_bowling.py -v 2>&1)]
  error: Exit code 127

[Bash(python3 -m pytest test_bowling.py -v 2>&1)]
  error: Exit code 1

Assistant: The failure is a test bug — `[10, 10, 3, 0] + [0] * 15` is 19 rolls (one too many for that game). Two strikes + `3,0` + 7 open frames uses exactly 18 rolls. Let me fix that:

[Edit(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-bowling-RQoWek/test_bowling.py)]
--- before
    def test_two_consecutive_strikes(self):
        # frame1: 10, bonus=10+3 => 23
        # frame2: 10, bonus=3+0 => 13
        # frame3: 3+0 => 3
        # rest zeros
        rolls = [10, 10, 3, 0] + [0] * 15
        assert score(rolls) == 39
--- after
    def test_two_consecutive_strikes(self):
        # frame1: strike, bonus=10+3 => 23
        # frame2: strike, bonus=3+0 => 13
        # frame3: 3+0 => 3
        # frames 4-10: zeros
        # rolls used: 1+1+2+14 = 18 total
        rolls = [10, 10, 3, 0] + [0] * 14
        assert score(rolls) == 39

[Bash(python3 -m pytest test_bowling.py -v 2>&1)]
  ============================= test session starts ==============================
  platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0 -- /Library/Developer/CommandLineTools/usr/bin/python3
  cachedir: .pytest_cache
  rootdir: /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-bowling-RQoWek
  collecting ... collected 29 items
  
  test_bowling.py::TestBasicScoring::test_all_gutters PASSED               [  3%]
  test_bowling.py::TestBasicScoring::test_all_ones PASSED                  [  6%]
  test_bowling.py::TestBasicScoring::test_open_game PASSED                 [ 10%]
  test_bowling.py::TestSpares::test_spare_followed_by_zeros PASSED         [ 13%]
  test_bowling.py::TestSpares::test_spare_bonus_is_next_roll PASSED        [ 17%]
  test_bowling.py::TestSpares::test_consecutive_spares PASSED              [ 20%]
  … (25 more lines)

Assistant: 29/29 passing. Here's a full walkthrough of the implementation:

---

## `bowling.py` — design overview

### `BowlingGame` class

| Method | Purpose |
|---|---|
| `roll(pins)` | Appends a pin count after validating it, then marks the game done when complete |
| `score()` | Walks through all 10 frames with look-ahead for bonus rolls |
| `_current_frame_info()` | Returns `(frame_idx, roll_pos_in_frame, list_offset)` by replaying frames — the single source of truth for "where are we?" |
| `_validate_mid_frame(pins)` | Delegates to frame-1-9 or 10th-frame validation |
| `_validate_tenth_frame(pins)` | Handles the 10th frame's three sub-cases |
| `_game_over()` | Uses `_current_frame_info` + 10th-frame rules to decide when to seal the game |

### Scoring (the core loop)

```python
for frame in range(10):
    if rolls[idx] == 10:           # strike → bonus = next 2 rolls; advance 1
        total += 10 + rolls[idx+1] + rolls[idx+2]
        idx += 1
    elif rolls[idx]+rolls[idx+1] == 10:  # spare → bonus = next roll; advance 2
        total += 10 + rolls[idx+2]
        idx += 2
    else:                          # open → just sum; advance 2
        total += rolls[idx] + rolls[idx+1]
        idx += 2
```

The 10th-frame bonus rolls live naturally at the end of `self._rolls`, so the look-ahead (`idx+1`, `idx+2`) picks them up without any special-casing in the scoring loop.

### Key validation rules
- **Frames 1-9:** two rolls in a frame may not exceed 10 (a strike closes the frame in one roll).
- **10th frame, roll 2:** pin constraint only applies when roll 1 was *not* a strike (strike resets the lane).
- **10th frame, roll 3 (fill ball):** allowed only after a strike or spare; constrained by roll 2 only when roll 1 was a strike *and* roll 2 was not.

### Functional wrapper
`score(rolls)` creates a `BowlingGame`, feeds it all rolls, and returns the result — handy for one-liners in tests.

---

## Turn 2 (final)

**User:**

Perfect! The bowling scorer is complete and all tests pass. Here's a summary of what makes this solution robust:

**Key strengths:**
1. **Single source of truth** — `_current_frame_info()` replays the frame index from scratch each time, ensuring consistency between validation and scoring.
2. **10th-frame logic** — The bonus rolls naturally live at the end of `self._rolls`, so the scoring loop doesn't need special cases; the index just reaches them naturally.
3. **Validation** — Catches invalid states early (negative pins, frame totals >10, incomplete games, extra rolls).
4. **Edge cases covered** — Perfect games (all strikes), all spares, consecutive strikes, 10th-frame fills after spares/strikes.

All 29 tests passing, including the full Exercism test suite expectations.

<done/>

---

**Run end**: done after 1 turn (166s)
