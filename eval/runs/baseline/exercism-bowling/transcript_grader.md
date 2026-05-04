# exercism-bowling

- Condition: `baseline`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T20:51:21

## Initial prompt

Exercism 'Bowling': implement a 10-pin bowling scorer. Track frames, handle strikes (next two rolls bonus), spares (next roll bonus), and the special 10th-frame bonus rolls. Return the final score from a list of rolls.

---

## Turn 1

### Tutor

[Glob(**/*)]
  No files found

[Bash(pwd && ls -la)]
  /var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-0mb5h6hd
  total 0
  drwx------    2 oz  staff    64  4 May 20:51 .
  drwx------@ 222 oz  staff  7104  4 May 20:51 ..

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
