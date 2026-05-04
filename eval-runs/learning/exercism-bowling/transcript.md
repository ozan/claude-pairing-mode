# exercism-bowling

- Source: `exercism`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Output style: `Learning`
- Started: 2026-05-03T19:58:33.919Z

---

## Turn 1

**User:**

Exercism 'Bowling': implement a 10-pin bowling scorer. Track frames, handle strikes (next two rolls bonus), spares (next roll bonus), and the special 10th-frame bonus rolls. Return the final score from a list of rolls.

**Pair:**

[Glob(**/*bowling*)]
  No files found

[Bash(exercism download --exercise=bowling --track=python 2>/dev/null || echo "not found")]
  not found

[Bash(ls ~/exercism/ 2>/dev/null || ls ~/Exercism/ 2>/dev/null || find ~ -name "bowling" -type d 2>/dev/null | head -5)]
  pangram
  roman-numerals
  zebra-puzzle

[Bash(ls ~/exercism/)]
  pangram
  roman-numerals
  zebra-puzzle

[Bash(exercism download --exercise=bowling --track=python)]
  error: Exit code 127

[Bash(ls ~/exercism/pangram/)]
  pangram.py
  test_pangram.py

Assistant: Let me look at the existing exercise structure, then build the implementation.

[Read(/root/exercism/pangram/pangram.py)]
  error: File does not exist. Note: your current working directory is /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-bowling-kdqdp8.

[Bash(pwd && ls)]
  /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-bowling-kdqdp8

[Bash(ls -la)]
  total 0
  drwx------    3 oz  staff    96  4 May 05:58 .
  drwx------@ 186 oz  staff  5952  4 May 05:59 ..
  drwxr-xr-x    3 oz  staff    96  4 May 05:58 .claude

Assistant: Fresh directory — I'll create both the implementation and the test file.

[Write(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-bowling-kdqdp8/bowling.py)]
def score(rolls):
    """Return the total score for a 10-pin bowling game.

    Args:
        rolls: list of pin counts, one integer per roll.

    Returns:
        Total score as an integer.

    Raises:
        ValueError: if the rolls list is invalid (wrong length,
                    negative counts, pin counts exceeding what
… (128 more lines)

Assistant: Now let me write a thorough test suite that mirrors Exercism's official test cases:

[Write(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-bowling-kdqdp8/bowling_test.py)]
import pytest
from bowling import score


# ── Scoring ──────────────────────────────────────────────────────────────────

class TestScoring:
    def test_all_zeros(self):
        assert score([0] * 20) == 0

    def test_no_strikes_or_spares(self):
        # 6+3 per frame × 10 = 90
… (106 more lines)

[Bash(python -m pytest bowling_test.py -v 2>&1)]
  error: Exit code 127

[Bash(python3 -m pytest bowling_test.py -v 2>&1)]
  error: Exit code 1

Assistant: 25/27 pass. Two test bugs to fix — the implementation is correct in both cases:

1. **`test_consecutive_spares`**: `10 + 3 = 13` (not 15), so total is 31, not 33  
2. **`test_consecutive_strikes`**: 3 strikes + 7 open frames = 17 rolls, but I gave 19 (`+ [0]*14` should be `+ [0]*12`)

[Edit(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-bowling-kdqdp8/bowling_test.py)]
--- before
    def test_consecutive_spares(self):
        # 5/5 bonus=5 → 15; 5/5 bonus=3 → 15; 3+0=3; rest zero → 33
        assert score([5, 5, 5, 5, 3, 0] + [0] * 14) == 33
--- after
    def test_consecutive_spares(self):
        # frame 1: spare, bonus=5 → 10+5=15
        # frame 2: spare, bonus=3 → 10+3=13
        # frame 3: 3+0=3; rest zero → total 31
        assert score([5, 5, 5, 5, 3, 0] + [0] * 14) == 31

[Edit(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-bowling-kdqdp8/bowling_test.py)]
--- before
    def test_consecutive_strikes(self):
        # frame 1: 10+10+10=30; frame 2: 10+10+0=20; frame 3: 10+0+0=10; rest zero → 60
        assert score([10, 10, 10, 0, 0] + [0] * 14) == 60
--- after
    def test_consecutive_strikes(self):
        # frame 1: 10+10+10=30; frame 2: 10+10+0=20; frame 3: 10+0+0=10; rest zero → 60
        # 3 strikes (3 rolls) + 7 open frames of 0,0 (14 rolls) = 17 rolls total
        assert score([10, 10, 10, 0, 0] + [0] * 12) == 60

[Bash(python3 -m pytest bowling_test.py -v 2>&1)]
  ============================= test session starts ==============================
  platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0 -- /Library/Developer/CommandLineTools/usr/bin/python3
  cachedir: .pytest_cache
  rootdir: /private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-bowling-kdqdp8
  collecting ... collected 27 items
  
  bowling_test.py::TestScoring::test_all_zeros PASSED                      [  3%]
  bowling_test.py::TestScoring::test_no_strikes_or_spares PASSED           [  7%]
  bowling_test.py::TestScoring::test_spare_followed_by_zeros PASSED        [ 11%]
  bowling_test.py::TestScoring::test_roll_after_spare_counts_twice PASSED  [ 14%]
  bowling_test.py::TestScoring::test_consecutive_spares PASSED             [ 18%]
  bowling_test.py::TestScoring::test_spare_in_last_frame_one_bonus_roll PASSED [ 22%]
  … (23 more lines)

Assistant: 27/27. Let's look at the final implementation:

[Read(/private/var/folders/q0/dv7j0tf55lb21cgdzz7h4khw0000gn/T/ai-pair-eval-exercism-bowling-kdqdp8/bowling.py)]
  1	def score(rolls):
  2	    """Return the total score for a 10-pin bowling game.
  3	
  4	    Args:
  5	        rolls: list of pin counts, one integer per roll.
  6	
  7	    Returns:
  8	        Total score as an integer.
  9	
  10	    Raises:
  11	        ValueError: if the rolls list is invalid (wrong length,
  12	                    negative counts, pin counts exceeding what
  … (128 more lines)

Assistant: 27/27 ✅. Here's how everything fits together:

---

## How it works

### Scoring (`score`)

The function makes **two passes** over `rolls`: validation first, then scoring.

**Scoring loop** walks through 10 frames with a `cursor` index:

| Frame | Condition | Points added | `cursor` moves |
|---|---|---|---|
| 1–9, strike | `rolls[cursor] == 10` | `10 + next 2 rolls` | `+1` (one roll in frame) |
| 1–9, spare | `first + second == 10` | `10 + next 1 roll` | `+2` |
| 1–9, open | otherwise | `first + second` | `+2` |
| **10th** | always | `sum(rolls[cursor:])` | consume all |

The 10th frame is special: bonus rolls are **already in the list** and scored at face value — no extra bonus is applied on top of them.

---

### Validation (`_validate` + `_validate_tenth_frame`)

Validation mirrors the scoring walk, but checks every constraint:

**Frames 1–9** — raise `ValueError` if:
- any roll is negative or `> 10`
- two rolls in a non-strike frame sum `> 10`
- rolls run out mid-game

**Frame 10** — three cases for the bonus rolls allowed:

```
Strike on first ball  → exactly 2 bonus rolls (3 total)
  └─ Second also a strike → third can be 0–10 freely
  └─ Second not a strike  → second + third ≤ 10

Spare on first two    → exactly 1 bonus roll  (3 total)

Open frame            → no bonus roll          (2 total)
```

After the loop, `cursor == len(rolls)` is asserted — any leftover rolls after a completed game are rejected.

---

### Key insight — the 10th-frame "trick"

```python
total += sum(rolls[cursor:])   # frame 10 scoring
```

Because bonus balls for the 10th are appended to the list (not given a separate bonus on top), the simplest correct thing to do is **just add them all up**. The validation pass already guarantees there are exactly the right number of rolls remaining.

---

## Turn 2 (final)

**User:**

Looking at this transcript, I can see the bowling scorer has been fully implemented and tested:

✅ **Implementation complete** — `bowling.py` handles all the logic:
  - Validation pass for constraint checking
  - Scoring walk through 10 frames with proper bonuses for strikes/spares
  - Special handling for the 10th frame (no extra bonus, just sum the rolls)

✅ **Comprehensive test suite** — 27/27 passing after fixing two test expectations:
  - Edge cases: all zeros, consecutive strikes, spares, invalid rolls
  - 10th frame variations: strikes, spares, open frames
  - Proper error detection for invalid inputs

✅ **Clear explanation** — The solution correctly models:
  - Strikes: next two rolls added as bonus
  - Spares: next one roll added as bonus  
  - 10th frame: bonus rolls already in list, scored at face value
  - Validation enforces pin counts, frame structures, and exact roll count

The implementation is solid and production-ready.

<done/>

---

**Run end**: done after 1 turn (201s)
