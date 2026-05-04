# exercism-bowling

- Condition: `baseline`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T20:51:21

## Initial prompt

Exercism 'Bowling': implement a 10-pin bowling scorer. Track frames, handle strikes (next two rolls bonus), spares (next roll bonus), and the special 10th-frame bonus rolls. Return the final score from a list of rolls.

---

## Turn 1

### Tutor

Thinking: The user wants me to implement a 10-pin bowling scorer for the Exercism "Bowling" exercise. Let me first explore the repository structure to understand what's already there.

[Glob(**/*)]
  No files found

Thinking: It seems the directory is empty. Let me check where we are and what language we should use.

[Bash(pwd && ls -la)]
  /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-0mb5h6hd
  total 0
  drwx------    2 oz  staff    64  4 May 20:51 .
  drwx------@ 222 oz  staff  7104  4 May 20:51 ..

Thinking: The directory is empty. The user wants me to implement a 10-pin bowling scorer. Since there's no specific language mentioned, I'll implement it in Python as that's a common choice for Exercism. Let me create the bowling.py file.
  
  For Exercism's Bowling exercise, the typical interface is:
  - A `BowlingGame` class (or just a function) that takes a list of rolls and returns a score
  - The standard Exercism Python exercise has a `score(rolls)` function or a class
  
  Let me implement a clean solution:
  
  Rules:
  1. A game consists of 10 frames
  2. In each frame, a player has up to 2 rolls to knock down 10 pins
  
  
  3. Strikes award 10 plus the next two rolls, and the frame ends immediately
  4. Spares award 10 plus the next roll
  5. Open frames are just the sum of the two rolls
  6. The 10th frame is special—if you get a strike or spare, you get bonus rolls to complete the scoring
  
  I'll need to handle validation too, checking for invalid inputs like too many rolls, out-of-range pin counts, and incomplete games. Now I'm implementing the scoring logic...
  
  Implementing the function... Writing the scoring logic...

Tutor: Empty directory — I'll implement the full Exercism Bowling exercise from scratch in Python, including validation and a test suite.

[Write(/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-0mb5h6hd/bowling.py)]
"""10-pin bowling scorer.

Scoring rules
-------------
* A game is exactly 10 frames.
* Frame 1-9:
    - Strike  (first roll = 10): score = 10 + next two rolls; only 1 roll used
      in the frame.
    - Spare   (two rolls = 10): score = 10 + next one roll; 2 rolls used.
    - Open    (two rolls < 10): score = sum of both rolls; 2 rolls used.
* Frame 10 (bonus-roll frame):
    - Strike on first roll  → 2 extra rolls allowed.
… (242 more lines)
  File created successfully at: /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-0mb5h6hd/bowling.py

Tutor: Now add a thorough test suite:

[Write(/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-0mb5h6hd/bowling_test.py)]
"""Tests for the Exercism Bowling exercise.

Covers the functional `score()` API and the mutable `BowlingGame` class.
"""

import pytest
from bowling import BowlingGame, score


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
… (233 more lines)
  File created successfully at: /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-0mb5h6hd/bowling_test.py

[Bash(cd /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-0mb5h6hd && python -m pytest bowling_test.py -v 2>&1)]
  error: Exit code 1

[Bash(cd /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-0mb5h6hd && python -m pip install pytest -q && python -m pytest bowling_test.py -v 2>&1)]
  error: Exit code 1

[Bash(which python3 && python3 -m pytest --version 2>&1 || pip3 install pytest -q 2>&1)]
  /Users/oz/dev/ai-pair-proto/eval/.venv/bin/python3
  /Users/oz/dev/ai-pair-proto/eval/.venv/bin/python3: No module named pytest
  WARNING: You are using pip version 21.2.4; however, version 26.0.1 is available.
  You should consider upgrading via the '/Library/Developer/CommandLineTools/usr/bin/python3 -m pip install --upgrade pip' command.

[Bash(pip3 install pytest -q 2>&1 && cd /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-0mb5h6hd && python3 -m pytest bowling_test.py -v 2>&1)]
  error: Exit code 1

[Bash(ls /Users/oz/dev/ai-pair-proto/eval/.venv/bin/ | grep -i py && /Users/oz/dev/ai-pair-proto/eval/.venv/bin/pip install pytest -q 2>&1)]
  error: Exit code 127

[Bash(/Users/oz/dev/ai-pair-proto/eval/.venv/bin/python3 -m ensurepip 2>&1 && /Users/oz/dev/ai-pair-proto/eval/.venv/bin/python3 -m pip install pytest -q 2>&1 && cd /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-0mb5h6hd && /Users/oz/dev/ai-pair-proto/eval/.venv/bin/python3 -m pytest bowling_test.py -v 2>&1)]
  error: Exit code 1

Thinking: I have 2 failing tests:
  
  1. `TestStrikes::test_consecutive_strikes` - The test has `[10, 10, 10, 4, 3] + [0] * 14` (19 total rolls). After three strikes and an open frame (4,3), the rest should be 7 open frames × 2 rolls = 14 rolls, for a total of 1+1+1+2+14 = 19 rolls. But the validation fails in the open 10th frame check because `idx + 2 < len(rolls)` is True (there are trailing zeros that appear after the 10th frame). 
     
  Let me trace through the frame consumption more carefully. The first three frames consume one roll each, the fourth frame consumes two rolls for the open (4,3), then five more open frames consume 10 rolls of zeros, leaving the 10th frame at index 15 with two zeros—but there's still a trailing zero at index 17, which triggers the validation error.
  
  Actually, I see the issue now. My test data has 19 rolls total, but a complete game only needs 17: three strikes take three rolls, the open frame takes two, and the remaining six frames take twelve rolls combined. The extra two zeros shouldn't be there.
  
  Let me recalculate the score with the corrected test case of `[10, 10, 10, 4, 3] + [0] * 12`. Frame 1 scores 30 (strike plus next two rolls), frame 2 scores 24 (strike plus 10 and 4), frame 3 scores 17 (strike plus 4 and 3), frame 4 scores 7 (open frame), and frames 5-10 are all zeros, giving a total of 78 points.
  
  So the test assertion of 81 is incorrect—it should be 78. Now looking at the validation issue, I have a check in the `roll()` method that rejects negative pins, but the `_validate()` function used by `score()` doesn't perform that same validation on individual rolls.
  
  I need to add a loop at the start of `_validate()` that iterates through the rolls and raises an error if any pin count is negative.

Tutor: Two issues to fix: the consecutive-strikes test has a wrong roll count/score, and `_validate` doesn't catch negative pins. Let me fix both:

[Edit(/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-0mb5h6hd/bowling.py)]
--- before
    idx = 0

    for frame in range(10):
--- after
    # Check every individual roll value first.
    for pin in rolls:
        if pin < 0:
            raise ValueError(f"Negative pin count is not allowed: {pin}")
        if pin > 10:
            raise ValueError(f"Pin count exceeds pins on the lane: {pin}")

    idx = 0

    for frame in range(10):
  The file /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-0mb5h6hd/bowling.py has been updated successfully.

Tutor: Now fix the test — three consecutive strikes + (4,3) + 6 open zero frames = 17 rolls, score = 78:

[Edit(/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-0mb5h6hd/bowling_test.py)]
--- before
    def test_consecutive_strikes(self):
        # Three strikes then open: 10+(10+10) + 10+(10+4) + 10+(4+3) + 7 + rest
        rolls = [10, 10, 10, 4, 3] + [0] * 14
        assert score(rolls) == 81
--- after
    def test_consecutive_strikes(self):
        # Strike scores:  10+(10+10)=30, 10+(10+4)=24, 10+(4+3)=17, (4+3)=7, rest 0
        # 3 strike rolls + 2 open rolls + 6 frames × 2 = 17 rolls total
        rolls = [10, 10, 10, 4, 3] + [0] * 12
        assert score(rolls) == 78
  The file /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-0mb5h6hd/bowling_test.py has been updated successfully.

[Bash(cd /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-0mb5h6hd && /Users/oz/dev/ai-pair-proto/eval/.venv/bin/python3 -m pytest bowling_test.py -v 2>&1)]
  ============================= test session starts ==============================
  platform darwin -- Python 3.14.4, pytest-9.0.3, pluggy-1.6.0 -- /Users/oz/dev/ai-pair-proto/eval/.venv/bin/python3
  cachedir: .pytest_cache
  rootdir: /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-0mb5h6hd
  plugins: anyio-4.13.0
  collecting ... collected 39 items
  
  bowling_test.py::TestOpenFrames::test_all_gutter_balls PASSED            [  2%]
  bowling_test.py::TestOpenFrames::test_all_ones PASSED                    [  5%]
  bowling_test.py::TestOpenFrames::test_mixed_open_frames PASSED           [  7%]
  bowling_test.py::TestOpenFrames::test_single_pin_each_roll PASSED        [ 10%]
  bowling_test.py::TestSpares::test_spare_followed_by_zeros PASSED         [ 12%]
  … (36 more lines)

Tutor: **39/39 passing.** Here's a walkthrough of every design decision:

---

## `bowling.py` — design overview

### Two public APIs

| API | Use-case |
|---|---|
| `score(rolls)` | Functional: pass a complete flat list of rolls, get the score back |
| `BowlingGame` | Object-oriented: feed rolls one at a time via `.roll()`, read `.score` |

Both share the same `_validate` / `_score` / `_game_complete` helpers.

---

### `_score` — frame walking

```
idx  →  moves through rolls[]  one frame at a time
```

| Frame type | Rolls consumed | Points added |
|---|---|---|
| Strike (frames 1–9) | `idx += 1` | `10 + rolls[idx+1] + rolls[idx+2]` |
| Spare (frames 1–9) | `idx += 2` | `10 + rolls[idx+2]` |
| Open (frames 1–9) | `idx += 2` | `rolls[idx] + rolls[idx+1]` |
| **10th frame** | N/A | `sum(rolls[idx:])` — bonus rolls are already in the list |

The 10th frame is handled by summing whatever remains; the validator guarantees the correct number of bonus rolls are present.

---

### `_validate` — two-pass check

1. **Per-roll sweep** — rejects negatives and values > 10 immediately.  
2. **Frame-by-frame walk** — enforces:
   - Two-roll total ≤ 10 in open frames  
   - Correct number of 10th-frame bonus rolls (0, 1, or 2)  
   - No extra rolls after the game ends  
   - No missing rolls in non-partial mode  

The `partial=True` flag lets `BowlingGame.roll()` call it after every single roll for early error detection, without requiring a complete game.

---

### 10th-frame bonus-roll rules

| 10th frame result | Bonus rolls |
|---|---|
| Open (`r1+r2 < 10`) | 0 |
| Spare (`r1+r2 = 10`) | 1 |
| Strike on first roll | 2 (second may also be a strike; if so third is fresh 10-pin set) |

### Student

Thanks for the full walkthrough! This is really helpful. Let me make sure I understand the core logic before we wrap up.

I want to trace through one specific example to solidify my understanding: a game with two strikes, then a spare, then all open zeros.

So that'd be: `[10, 10, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`

Let me work through the scoring:
- Frame 1 (strike): `idx=0`. Score = `10 + rolls[1] + rolls[2]` = `10 + 10 + 5` = `25`
- Frame 2 (strike): `idx=1`. Score = `10 + rolls[2] + rolls[3]` = `10 + 5 + 5` = `20`
- Frame 3 (spare): `idx=2`. Score = `10 + rolls[4]` = `10 + 0` = `10`
- Frames 4–9 (all open zeros): each scores `0`
- Frame 10 (open zeros): scores `0`

Total: `25 + 20 + 10 + 0 = 55`

Can you confirm that's right? I'm mainly checking that I'm correctly tracking the `idx` pointer as we move through the frame types.

---

## Turn 2

### Tutor

Thinking: The user wants to trace through a specific example to verify their understanding. Let me verify their roll list and scoring manually.
  
  The rolls are: `[10, 10, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
  
  That's 17 rolls. Let me count: 10, 10, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 = 17 rolls.
  
  
  Now I'm working through each frame to verify the scoring. The first frame is a strike with a score of 25 (10 plus the next two rolls of 10 and 5). The second frame is also a strike scoring 20 (10 plus the next two rolls of 5 and 5). The third frame is a spare with rolls of 5 and 5, giving a base score of 10.
  
  Continuing with frame 3, I add the next roll of 0 to get 10 total. Frames 4 through 9 are all gutter balls with consecutive pairs of zeros, each scoring nothing. Frame 10 appears to be cut off, but I'm checking the final frame's scoring. I'm realizing the roll list is incomplete—it only has 17 rolls when this bowling game needs 18 total. With two strikes, a spare, and seven open frames, the math works out to needing one more roll at the end to properly complete the 10th frame. I should verify this by running through the code to confirm the user's trace is accurate and that 55 is indeed the correct score.

Tutor: Your `idx` tracking is exactly right. Let me quickly run it through the scorer to confirm the number, then flag one small thing about the roll list:

[Bash(cd /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-0mb5h6hd && /Users/oz/dev/ai-pair-proto/eval/.venv/bin/python3 -c "
from bowling import score, _game_complete

rolls_17 = [10, 10, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
rolls_18 = [10, 10, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

print(f'17-roll list complete? {_game_complete(rolls_17)}')
print(f'18-roll list complete? {_game_complete(rolls_18)}')
print(f'Score (18 rolls):      {score(rolls_18)}')
"
)]
  17-roll list complete? False
  18-roll list complete? True
  Score (18 rolls):      55

Tutor: Your frame-by-frame trace is **completely correct** — the `idx` pointer moves exactly as you described, and **55 is the right score**. One small fix needed though: the roll list is one zero short.

---

### The roll count

You need **18 rolls**, not 17. Count up what each frame *actually consumes* in the rolls array:

| Frame | Type | Rolls consumed | `idx` before → after |
|-------|------|---------------|----------------------|
| 1 | Strike | 1 | 0 → 1 |
| 2 | Strike | 1 | 1 → 2 |
| 3 | Spare | 2 | 2 → 4 |
| 4–9 | Open (×6) | 2 each = 12 | 4 → 16 |
| 10 | Open | **2** | 16 → 18 |

The 10th frame is an open frame, so it still needs **two** rolls — `rolls[16]` and `rolls[17]` — even though they're both zero.

```python
# 17 rolls — incomplete (missing the 2nd roll of frame 10)
[10, 10, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# 18 rolls — complete ✓
[10, 10, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

The key intuition: **strikes shorten frames 1 and 2** (each advances `idx` by only 1 instead of 2), which is why this game uses fewer total rolls than an all-open game (20). But the 10th frame always uses at least 2 rolls regardless — it has no "strike shortcut" like frames 1–9 do.

### Student

Ah, that makes perfect sense! I see it now — I was mentally shortcutting the 10th frame without thinking it through. Even though it's open (no bonus rolls), it still *consumes* two rolls from the array. Strikes compress frames 1–9, but the 10th frame always needs at least its base two rolls.

So the rule is:
- **Frames 1–9**: strikes use 1 roll, spares/opens use 2 rolls
- **Frame 10**: always uses at least 2 rolls, plus 0, 1, or 2 bonus rolls depending on what happened

That's why the all-gutter game is exactly 20 rolls (10 frames × 2), but this mixed game with two strikes is 18 — we "saved" 2 rolls by striking twice.

Thanks for walking me through that! I feel solid on how the `idx` pointer works now and how frames consume rolls differently. The implementation makes a lot of sense, and all 39 tests passing confirms the logic is sound.

<done/>

---

**Run end:** done after 2 turn(s) in 177.3s
