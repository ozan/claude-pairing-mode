# exercism-bowling

- Source: `exercism`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-02T23:20:47.644Z

---

## Turn 1

**User:**

Exercism 'Bowling': implement a 10-pin bowling scorer. Track frames, handle strikes (next two rolls bonus), spares (next roll bonus), and the special 10th-frame bonus rolls. Return the final score from a list of rolls.

**Pair:**

[Glob(**/bowling/**)]
  No files found

[Bash(find /Users/oz -maxdepth 5 -type d -name "bowling" 2>/dev/null)]
  Command running in background with ID: blea2hw66. Output is being written to: /private/tmp/claude-501/-Users-oz-dev-ai-pair-proto-eval-runs-003-baseline-exercism-bowling/0c1d890a-8bf8-402b-95bb-ffc5cffbdfce/tasks/blea2hw66.output

[Bash(cat /private/tmp/claude-501/-Users-oz-dev-ai-pair-proto-eval-runs-003-baseline-exercism-bowling/0c1d890a-8bf8-402b-95bb-ffc5cffbdfce/tasks/blea2hw66.output)]
  (Bash completed with no output)

[Bash(pwd && ls)]
  /Users/oz/dev/ai-pair-proto/eval-runs/003-baseline/exercism-bowling
  transcript.jsonl
  transcript.md

[Bash(ls /Users/oz/exercism/python/bowling/ 2>/dev/null || echo "not found")]
  not found

Assistant: No existing files — I'll create the solution from scratch in the current directory.

[Write(/Users/oz/dev/ai-pair-proto/eval-runs/003-baseline/exercism-bowling/bowling.py)]
"""10-pin bowling scorer (Exercism)."""


def score(rolls):
    """Return the total score for a complete, valid game of bowling.

    Args:
        rolls: list of int — pin counts in delivery order.

    Returns:
        int — final score (0–300).

… (102 more lines)

Assistant: Now let me verify with the canonical Exercism test cases manually:

[Bash(python3 -c "
from bowling import score

# Perfect game: 12 strikes → 300
assert score([10]*12) == 300, 'perfect game'

# All gutter balls → 0
assert score([0]*20) == 0, 'gutter game'

# All spares (5+5) + final bonus 5 → 150
assert score([5,5]*10 + [5]) == 150, 'all spares'

# One strike in first frame, rest normal
# 10 + 3+4 = 17, then 3+4=7 x8 more = 17+56=73... wait let me think
# rolls: 10, 3, 4, then 0,0 x8
rolls = [10, 3, 4] + [0,0]*8
assert score(rolls) == 10+3+4 + 3+4 + 0*8*2, f'one strike: got {score(rolls)}'

# All strikes = perfect 300
print('perfect game:', score([10]*12))

# Spare then 3
rolls = [6,4, 3,0] + [0,0]*8
assert score(rolls) == 13 + 3 + 0, f'spare+3 got {score(rolls)}'

# 10th frame spare
rolls = [0,0]*9 + [7,3,5]
assert score(rolls) == 15, f'10th spare got {score(rolls)}'

# 10th frame strike
rolls = [0,0]*9 + [10,5,3]
assert score(rolls) == 18, f'10th strike got {score(rolls)}'

# 10th frame double strike
rolls = [0,0]*9 + [10,10,3]
assert score(rolls) == 23, f'10th double strike got {score(rolls)}'

# 10th frame triple strike
rolls = [0,0]*9 + [10,10,10]
assert score(rolls) == 30, f'10th triple strike got {score(rolls)}'

# Incomplete game raises
try:
    score([10]*11)
    assert False, 'should raise'
except ValueError:
    pass

# Too many rolls raises
try:
    score([0]*21)
    assert False, 'should raise'
except ValueError:
    pass

# Over 10 pins raises
try:
    score([11] + [0]*19)
    assert False, 'should raise'
except ValueError:
    pass

# Frame sum > 10 raises
try:
    score([5,6] + [0]*18)
    assert False, 'should raise'
except ValueError:
    pass

print('All assertions passed.')
"
)]
  perfect game: 300
  All assertions passed.

Assistant: All checks pass. Here's a walkthrough of how the implementation works:

---

## `bowling.py` — design notes

### Core loop
One `for frame in range(10)` loop. A single `roll` cursor advances through the flat `rolls` list; the amount it advances per frame depends on what happened (1 for a strike in frames 1–9, 2 for everything else, 3 for a 10th-frame strike or spare).

### Frames 1–9
| Outcome | Score added | Cursor advance |
|---------|-------------|----------------|
| Strike (roll == 10) | 10 + next 2 rolls | +1 |
| Spare (r1 + r2 == 10) | 10 + next 1 roll | +2 |
| Open frame | r1 + r2 | +2 |

Bonus rolls are validated (no negatives, no impossible sums) but the cursor doesn't move past them — they'll be scored again as ordinary rolls in the next frame (correct — that's how the bonus works).

### 10th frame
Three sub-cases:
- **Strike first** → consume 3 rolls (first strike + 2 bonus), validate that the two bonus rolls don't exceed 10 unless the first bonus is itself a strike.
- **Spare** → consume 3 rolls, validate one bonus ball.
- **Open** → consume 2 rolls, no bonus.

### Validation
Every known invalid-game edge case raises `ValueError`:
- negative pins
- single roll > 10
- two-ball frame sum > 10 (except after a 10th-frame strike)
- too few rolls (incomplete game)
- too many rolls (extra balls after game ends — `roll != len(rolls)` check at the end)

---

## Turn 2 (final)

**User:**

Looks great. All the main bowling rules are in place:

- Frames 1–9 handle strikes (10 + next 2), spares (10 + next 1), and open frames correctly
- 10th frame has proper branching for strike/spare/open with the right number of bonus rolls
- Comprehensive validation catches all the edge cases (negatives, over-10 pins, incomplete/extra rolls)
- Tests verify perfect game (300), gutter game (0), all spares (150), and all the tricky 10th-frame scenarios

The cursor-advancing approach is clean—advancing by 1 for strikes in frames 1–9 but by 2–3 elsewhere keeps the logic straightforward without needing to look ahead or back.

<done/>

---

**Run end**: done after 1 turn (187s)
