# exercism-bowling

- Condition: `learning`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:05:47

## Initial prompt

Exercism 'Bowling': implement a 10-pin bowling scorer. Track frames, handle strikes (next two rolls bonus), spares (next roll bonus), and the special 10th-frame bonus rolls. Return the final score from a list of rolls.

---

## Turn 1

### Tutor

[Glob(**/*bowling*)]
  No files found

[Bash(ls -la)]
  total 0
  drwx------    3 oz  staff    96  4 May 21:05 .
  drwx------@ 228 oz  staff  7296  4 May 21:05 ..
  drwxr-xr-x    3 oz  staff    96  4 May 21:05 .claude

Tutor: Let me check the directory for any existing structure, then implement the solution.

[Bash(python3 --version)]
  Python 3.14.4

Tutor: Good — Python 3.14. I'll write `bowling.py` and a test file.

---

## The algorithm, frame by frame

**Frames 1–9**
| Situation | Score | Advance index by |
|---|---|---|
| Strike (`rolls[i] == 10`) | `10 + next 2 rolls` | 1 |
| Spare (`rolls[i]+rolls[i+1] == 10`) | `10 + next 1 roll` | 2 |
| Normal | `rolls[i] + rolls[i+1]` | 2 |

**Frame 10** — no bonus calculation; just *sum the remaining rolls* (the fill balls are already in the list).

**Validation rules** that must raise `ValueError`:
- Any roll < 0 or > 10
- A non-strike frame where two rolls exceed 10 (frames 1–9)
- Too few rolls (game not finished)
- Too many rolls (game already over)
- 10th-frame: if first ball is a strike and second is *not* a strike, second + third can't exceed 10

[Write(/bowling.py)]
"""Ten-pin bowling scorer (Exercism)."""


def score(rolls: list[int]) -> int:
    """Return the total score for a completed bowling game.

    Args:
        rolls: Pin counts in delivery order, including 10th-frame fill balls.

    Returns:
        Final score (0–300).

… (83 more lines)
  error: EROFS: read-only file system, open '/bowling.py'

[Bash(mkdir -p ~/bowling && ls ~/bowling)]
  (Bash completed with no output)

[Write(/root/bowling/bowling.py)]
"""Ten-pin bowling scorer (Exercism)."""


def score(rolls: list[int]) -> int:
    """Return the total score for a completed bowling game.

    Args:
        rolls: Pin counts in delivery order, including 10th-frame fill balls.

    Returns:
        Final score (0–300).

… (83 more lines)
  error: EROFS: read-only file system, mkdir '/root'

[Bash(echo $HOME && ls $HOME)]
  /Users/oz
  __pycache__
  Applications
  bowling
  Desktop
  dev
  Documents
  Downloads
  evaluator.py
  Library
  Movies
  Music
  … (4 more lines)

[Write(/Users/oz/bowling/bowling.py)]
"""Ten-pin bowling scorer (Exercism)."""


def score(rolls: list[int]) -> int:
    """Return the total score for a completed bowling game.

    Args:
        rolls: Pin counts in delivery order, including 10th-frame fill balls.

    Returns:
        Final score (0–300).

… (83 more lines)
  File created successfully at: /Users/oz/bowling/bowling.py

Tutor: Now write the tests:

[Write(/Users/oz/bowling/bowling_test.py)]
"""Tests for the ten-pin bowling scorer."""

import pytest
from bowling import score


# ── Happy-path scores ─────────────────────────────────────────────────────────

def test_gutter_game():
    assert score([0] * 20) == 0


… (141 more lines)
  File created successfully at: /Users/oz/bowling/bowling_test.py

[Bash(cd /Users/oz/bowling && python3 -m pytest bowling_test.py -v 2>&1)]
  error: Exit code 1

Tutor: Two tests have wrong expected values — both are test bugs, not implementation bugs. Let me trace them:

- **`test_one_strike`**: `[10, 7, 3, 2, 0] + [0]*15` = 20 rolls, but that game legitimately ends in 19 (strike uses 1 roll, not 2). Need `[0]*14`.
- **`test_all_strikes_in_first_nine_then_open_tenth`**: Frame 8 bonus = 10+2=12 and frame 9 = 2+3=5, so 7×30+22+15+5 = **252**, not 257.

[Edit(/Users/oz/bowling/bowling_test.py)]
--- before
def test_one_strike():
    # Frame 1: 10 strike, bonus=7+3=10  →  20
    # Frame 2: 7+3 spare, bonus=2       →  12 ... wait, let's be careful
    # Frame 2: 7+3 spare                →  12 (spare: 10+2)
    # Frame 3: 2+0                      →   2
    # Frames 4–10: zeros                →   0
    rolls = [10, 7, 3, 2, 0] + [0] * 15
    assert score(rolls) == 30
--- after
def test_one_strike():
    # Frame 1: 10 strike, bonus=7+3=10  →  20
    # Frame 2: 7+3 spare,  bonus=2      →  12
    # Frame 3: 2+0                      →   2
    # Frames 4–10: zeros                →   0
    # Total: 34
    # Valid game = 19 rolls (1 strike + 8×2 + 2 open 10th)
    rolls = [10, 7, 3, 2, 0] + [0] * 14
    assert score(rolls) == 34
  The file /Users/oz/bowling/bowling_test.py has been updated successfully.

[Edit(/Users/oz/bowling/bowling_test.py)]
--- before
def test_all_strikes_in_first_nine_then_open_tenth():
    rolls = [10] * 9 + [2, 3]
    # Frames 1–8: each strike looks ahead; frame 9 looks at 10,2,3
    # Frame 1–7: 10+10+10=30 each → 7*30=210
    # Frame 8: 10+10+2=22
    # Frame 9: 10+2+3=15
    # Frame 10: 2+3=5
    assert score(rolls) == 257
--- after
def test_all_strikes_in_first_nine_then_open_tenth():
    rolls = [10] * 9 + [2, 3]
    # Frame 1–7: 10+10+10=30 each → 7×30 = 210
    # Frame 8:   10+10+2  = 22
    # Frame 9:   10+2+3   = 15
    # Frame 10:  2+3      =  5
    # Total: 252
    assert score(rolls) == 252
  The file /Users/oz/bowling/bowling_test.py has been updated successfully.

[Bash(cd /Users/oz/bowling && python3 -m pytest bowling_test.py -v 2>&1)]
  ============================= test session starts ==============================
  platform darwin -- Python 3.14.4, pytest-9.0.3, pluggy-1.6.0 -- /Users/oz/dev/ai-pair-proto/eval/.venv/bin/python3
  cachedir: .pytest_cache
  rootdir: /Users/oz/bowling
  plugins: anyio-4.13.0
  collecting ... collected 25 items
  
  bowling_test.py::test_gutter_game PASSED                                 [  4%]
  bowling_test.py::test_all_ones PASSED                                    [  8%]
  bowling_test.py::test_one_spare PASSED                                   [ 12%]
  bowling_test.py::test_spare_in_last_frame PASSED                         [ 16%]
  bowling_test.py::test_one_strike PASSED                                  [ 20%]
  … (23 more lines)

Tutor: **25/25 passing.** Here's a walkthrough of everything that was built.

---

## `bowling.py` — the implementation

### `score(rolls)` — the scorer

```
Frames 1–9  ──►  i tracks position in rolls list
                 ┌─ strike (rolls[i] == 10)     → total += 10 + next 2;  i += 1
                 ├─ spare  (two rolls sum to 10) → total += 10 + next 1;  i += 2
                 └─ open                         → total += two rolls;    i += 2

Frame 10    ──►  sum(rolls[i:])   (fill balls are already in the list,
                                   no separate bonus look-ahead needed)
```

### `_validate(rolls)` — the guard

Runs the same frame-walk as the scorer, but only to track `i`, checking:

| Check | Why |
|---|---|
| Any roll `< 0` or `> 10` | Impossible pin count |
| Frames 1–9: two-ball sum `> 10` | Can't knock down more than exist |
| `i >= len(rolls)` mid-walk | Game recorded before it ended |
| 10th-frame strike: `i+2 >= len(rolls)` | Missing one or both fill balls |
| 10th-frame strike, 2nd ball not a strike: `second + third > 10` | Invalid fill pair |
| 10th-frame spare: `i+2 >= len(rolls)` | Missing the fill ball |
| `i < len(rolls)` at end | Extra rolls after game ended |

### Key 10th-frame subtlety
When the 10th-frame first ball is a **strike** and the **second is also a strike**, the third ball is unconstrained (0–10). But if the second is *not* a strike, `second + third ≤ 10` — they share a lane rack.

```python
if second != 10 and second + third > 10:
    raise ValueError("Pin count exceeds pins on the lane")
```

### Student

I see the setup and full walkthrough. Before I ask my first question: I want to make sure I understand what's been handed to me. Let me check the actual implementation in `bowling.py` that was created:

```bash
cat /Users/oz/bowling/bowling.py
```

I'm curious to see the full `score()` and `_validate()` functions that were written. From your summary I can see the logic, but I want to read the actual code and then ask about any parts I don't fully grasp yet.

---

## Turn 2

### Tutor

[Read(/Users/oz/bowling/bowling.py)]
  1	"""Ten-pin bowling scorer (Exercism)."""
  2	
  3	
  4	def score(rolls: list[int]) -> int:
  5	    """Return the total score for a completed bowling game.
  6	
  7	    Args:
  8	        rolls: Pin counts in delivery order, including 10th-frame fill balls.
  9	
  10	    Returns:
  11	        Final score (0–300).
  12	
  … (83 more lines)

Tutor: There it is — all 95 lines. A few landmarks to orient yourself:

- **Line 16** — validation runs first, before any scoring math touches the list.
- **Lines 22–31** — the frames 1–9 loop. The variable `i` is a cursor that moves through `rolls`; a strike only advances it by 1 (one delivery), a spare or open frame advances it by 2.
- **Line 35** — the entire 10th-frame score is just `sum(rolls[i:])`. Whatever is left in the list from `i` onward — two or three balls — gets added directly, with no bonus look-ahead.
- **Lines 53–64** — validation mirrors the scorer's loop exactly, but its only job is to move `i` and check for illegal states.
- **Lines 72–91** — the 10th-frame validation branches into three cases: strike first, spare first, open first.
- **Line 93** — the final fence: if `i` hasn't consumed the whole list, there were extra rolls.

Ask away about any line or concept whenever you're ready.

### Student

Thanks for the orientation. Let me start by reading the actual code so I can see how it all fits together:

[Bash(cd /Users/oz/bowling && cat bowling.py)]

Actually, wait — the output got truncated in your last message. Could you show me the full file without the ellipsis? I want to see the complete `_validate()` function and how the 10th-frame cases are actually implemented, so I can ask real questions about the logic rather than guessing from the summary.

---

## Turn 3

### Tutor

Tutor: The full file was shown in my last message — all 95 lines, nothing truncated. Here it is again, unbroken:

```python
"""Ten-pin bowling scorer (Exercism)."""


def score(rolls: list[int]) -> int:
    """Return the total score for a completed bowling game.

    Args:
        rolls: Pin counts in delivery order, including 10th-frame fill balls.

    Returns:
        Final score (0–300).

    Raises:
        ValueError: If the roll sequence is illegal or the game is incomplete.
    """
    _validate(rolls)

    total = 0
    i = 0  # current position in the rolls list

    # ── Frames 1–9 ──────────────────────────────────────────────────────────
    for _ in range(9):
        if rolls[i] == 10:                          # strike
            total += 10 + rolls[i + 1] + rolls[i + 2]
            i += 1
        elif rolls[i] + rolls[i + 1] == 10:         # spare
            total += 10 + rolls[i + 2]
            i += 2
        else:                                        # open frame
            total += rolls[i] + rolls[i + 1]
            i += 2

    # ── Frame 10 ─────────────────────────────────────────────────────────────
    # No separate bonus look-ahead needed: fill balls are already in the list.
    total += sum(rolls[i:])

    return total


# ── Validation ───────────────────────────────────────────────────────────────

def _validate(rolls: list[int]) -> None:
    """Raise ValueError for any illegal roll sequence."""

    # Every individual delivery must be 0–10.
    for r in rolls:
        if r < 0 or r > 10:
            raise ValueError(f"Pin count exceeds pins on the lane: {r}")

    i = 0

    # Frames 1–9
    for _ in range(9):
        if i >= len(rolls):
            raise ValueError("Score cannot be taken until the end of the game")

        if rolls[i] == 10:          # strike — one delivery, next frame
            i += 1
        else:
            if i + 1 >= len(rolls):
                raise ValueError("Score cannot be taken until the end of the game")
            if rolls[i] + rolls[i + 1] > 10:
                raise ValueError("Pin count exceeds pins on the lane")
            i += 2

    # Frame 10 — at least the first delivery must exist.
    if i >= len(rolls):
        raise ValueError("Score cannot be taken until the end of the game")

    first = rolls[i]

    if first == 10:                 # strike → two fill balls required
        if i + 2 >= len(rolls):
            raise ValueError("Score cannot be taken until the end of the game")
        second, third = rolls[i + 1], rolls[i + 2]
        # If second ball is NOT a strike, second + third must fit on the lane.
        if second != 10 and second + third > 10:
            raise ValueError("Pin count exceeds pins on the lane")
        i += 3
    else:
        if i + 1 >= len(rolls):     # need at least the second delivery
            raise ValueError("Score cannot be taken until the end of the game")
        second = rolls[i + 1]
        if first + second > 10:
            raise ValueError("Pin count exceeds pins on the lane")
        if first + second == 10:    # spare → one fill ball required
            if i + 2 >= len(rolls):
                raise ValueError("Score cannot be taken until the end of the game")
            i += 3
        else:                       # open 10th — no fill balls allowed
            i += 2

    if i < len(rolls):
        raise ValueError("Cannot roll after game is over")
```

That's the complete file. What would you like to dig into?

### Student

Okay, now I can see the whole thing. Let me trace through a concrete example to make sure I understand the frame-walking logic.

Let's say I have a simple game: `[5, 4, 3, 6, 10, 0, 0, 2, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3]`

Let me walk through what happens:

- **Frame 1**: `rolls[0]=5, rolls[1]=4` → not a strike, not a spare (5+4=9) → score is 9, `i` moves from 0 to 2
- **Frame 2**: `rolls[2]=3, rolls[3]=6` → spare (3+6=10) → score is 10 + `rolls[4]=10` → 20, `i` moves from 2 to 4
- **Frame 3**: `rolls[4]=10` → strike → score is 10 + `rolls[5]=0` + `rolls[6]=0` → 10, `i` moves from 4 to 5
- **Frame 4**: `rolls[5]=0, rolls[6]=0` → score is 0, `i` moves from 5 to 7
- ... and so on

But here's my first real question: **In frame 3, when we look ahead for the strike bonus, we grab `rolls[5]` and `rolls[6]`, which are both 0. But what if one of those "next two rolls" is actually a fill ball in the 10th frame?** 

Like, if I had a strike in frame 9, I'd look at `rolls[i+1]` and `rolls[i+2]`. If those happen to be the 10th-frame first and second deliveries, that still works, right? The fill balls are already in the list, so I'm not double-counting or anything?

---

## Turn 4

### Tutor

Tutor: Your question is exactly the right one to ask — and the answer is yes, it works correctly and intentionally. But first, a small correction to your trace: **frame 2 is not a spare**.

```
rolls[2] + rolls[3]  =  3 + 6  =  9   ← open frame, not 10
```

That example game would also fail `_validate` later (frame 7 has `5+6=11`), but set that aside — your conceptual question about frame 9 striking into the 10th frame is the important one.

---

### Why the look-ahead into frame 10 is correct, not a bug

Take a cleaner example: 8 open frames, a strike in frame 9, then a spare + fill in frame 10.

```
rolls = [0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0,  10,  7, 3, 5]
index:   0 1  2 3  4 5  6 7  8 9 10 11 12 13 14 15   16  17 18 19
         ──────────── frames 1–8 ────────────────     f9  ── f10 ──
```

The scorer loop reaches frame 9 with `i=16`:

```python
rolls[16] == 10   # strike
total += 10 + rolls[17] + rolls[18]   # 10 + 7 + 3 = 20
i = 17
```

Then frame 10:

```python
total += sum(rolls[17:])   # 7 + 3 + 5 = 15
```

**`rolls[17]` and `rolls[18]` are used twice** — once as the strike bonus for frame 9, and again as part of the frame 10 sum. That is the correct answer in real bowling. Those two deliveries genuinely count for both:

| Frame | What it scores |
|---|---|
| Frame 9 (strike) | `10 + 7 + 3 = 20` |
| Frame 10 (spare + fill) | `7 + 3 + 5 = 15` |
| **Total** | **35** |

The list stores each delivery **once**, but the arithmetic visits some of them twice — and that's by design, not a bug. The rule "a strike scores 10 plus the next two deliveries" exists precisely to reward you for what you do on those *same* balls.

The `sum(rolls[i:])` shortcut for frame 10 works because by the time the loop exits, `i` is pointing at whatever 10th-frame balls remain. Whether that's 2 or 3 balls, they all get summed without any special-casing.

### Student

Ah, that makes sense! The double-counting is intentional — it's the *bonus* structure of bowling itself, not a quirk of the code. Each delivery gets added once to the list, but strategically positioned deliveries (like those that follow a strike) get counted again as part of the bonus.

That's elegant. So the fill balls being "already in the list" is the key insight: we don't have to fetch them separately or worry about running out of rolls — they're just sitting there waiting to be summed.

Now I have a follow-up about the 10th-frame validation, because that's the trickiest part:

```python
if first == 10:                 # strike → two fill balls required
    if i + 2 >= len(rolls):
        raise ValueError("Score cannot be taken until the end of the game")
    second, third = rolls[i + 1], rolls[i + 2]
    # If second ball is NOT a strike, second + third must fit on the lane.
    if second != 10 and second + third > 10:
        raise ValueError("Pin count exceeds pins on the lane")
    i += 3
```

I understand the rule: if the 10th frame starts with a strike, you get two bonus balls. And if the second of those isn't a strike, then second + third can't exceed 10 (they share a rack).

**But why is the check `second != 10`?** I get that if second IS 10, the third ball can be 0–10 freely. But in the code, we're only checking the sum when `second != 10`. What if `second == 10` and `third == 10`? Isn't that valid? Or am I misunderstanding what the condition is doing?

---

## Turn 5

### Tutor

Tutor: You've understood it correctly — `second == 10, third == 10` (the perfect 10th frame) is completely valid, and the code already handles it. Here's why the condition is written that way.

### The physical reason: pin resets

After a strike, all 10 pins are reset. This happens **each time** a strike is bowled in the 10th frame:

| What happened | Pins available for the next ball |
|---|---|
| `first == 10` (strike) | Fresh rack — 10 pins for `second` |
| `second == 10` (strike again) | Fresh rack — 10 pins for `third` |
| `second != 10` (some pins left standing) | Only `10 - second` pins remain for `third` |

So the constraint `second + third <= 10` only applies in the **last** row. When `second == 10`, the rack resets and `third` can independently be 0–10.

### What the condition is doing

```python
if second != 10 and second + third > 10:
    raise ValueError(...)
```

Read it as two separate guards combined:

```
Is this a "shared rack" situation?  →  second != 10
AND did they knock down too many?   →  second + third > 10
```

Both must be true to raise. If `second == 10`, the first condition short-circuits to `False`, the check is skipped entirely, and `third` is left to the earlier per-roll guard (`r > 10`) that already ran over every value in the list.

### Tracing your specific example

`first=10, second=10, third=10` — the three-strike 10th frame:

```python
second != 10   →  False        # short-circuits here
# sum check never runs
i += 3                         # advances past all three balls ✓
```

`first=10, second=10, third=7` — also valid, same path, no check triggered.

`first=10, second=7, third=4`:

```python
second != 10   →  True
second + third →  11 > 10      # both True → raises ✓
```

So the condition isn't "allow 10+10" as a special case — it's "only enforce the shared-rack constraint when the rack actually *is* shared."

### Student

Got it — that makes perfect sense. The pins reset after each strike, so `second == 10` is the signal that a fresh rack appeared. The condition elegantly captures that physical reality.

Okay, one more thing I want to trace through carefully. In the validation loop for frames 1–9, there's this pattern:

```python
for _ in range(9):
    if i >= len(rolls):
        raise ValueError("Score cannot be taken until the end of the game")

    if rolls[i] == 10:          # strike — one delivery, next frame
        i += 1
    else:
        if i + 1 >= len(rolls):
            raise ValueError("Score cannot be taken until the end of the game")
        if rolls[i] + rolls[i + 1] > 10:
            raise ValueError("Pin count exceeds pins on the lane")
        i += 2
```

I see that for a strike, we only check `i >= len(rolls)` before accessing `rolls[i]`, and then we increment `i += 1`. But for a non-strike (spare or open), we check `i + 1 >= len(rolls)` before accessing both `rolls[i]` and `rolls[i+1]`.

**Why don't we check `i + 1 >= len(rolls)` after the strike case, too?** Like, after a strike in frame 9, couldn't we run out of rolls before reaching frame 10? Or does that check happen later?

---

## Turn 6

### Tutor

Tutor: Excellent observation — this is a real asymmetry in the code and it's worth understanding exactly why it's safe.

### The short answer

The check is deferred, not missing. For frames 1–8 it lands at the **top of the next iteration**; for frame 9 it lands at the **first line after the loop**.

```python
# after the loop:
if i >= len(rolls):              # ← catches "strike in frame 9, then nothing"
    raise ValueError("Score cannot be taken until the end of the game")

first = rolls[i]
```

### Why the asymmetry exists

A strike frame and a non-strike frame need different amounts of information to *classify and validate themselves*:

| Frame type | Rolls needed to know what it is | Rolls needed for scoring bonus |
|---|---|---|
| Strike | 1 (`rolls[i]`) | 2 more (handled by scorer, not validator) |
| Spare / open | 2 (`rolls[i]` and `rolls[i+1]`) | 1 more (spare only) |

For a non-strike frame, the code **must** read `rolls[i+1]` right now — it can't even decide "spare or open?" without it, let alone check `first + second > 10`. So the bounds check `i+1 >= len(rolls)` is an immediate necessity.

For a strike, `rolls[i]` alone is enough to finish the frame. There's nothing more to check *about this frame*. The next thing the validator needs is `rolls[i]` of the **next** frame — and that check happens exactly where it always does: at the top of the next iteration.

### Tracing the "strike on frame 9, then nothing" case

```python
rolls = [10] * 9   # nine strikes, then the game stops
```

- Frames 1–8: loop runs 8 times, `i` moves to 8. ✓ each start-of-iteration check passes.
- Frame 9 (9th iteration): `i=8 < 9` ✓, `rolls[8]==10`, `i += 1` → `i=9`.
- Loop ends.
- **Post-loop**: `i=9 >= len(rolls)=9` → `raise ValueError("...end of the game")` ✓

So the gap is real, but it's closed by the guard that immediately follows the loop. The loop's job is to walk 9 frames; the post-loop guard is the entry fee for frame 10.

### Student

Perfect — that's the key insight I was missing. The bounds check for frame 10's first ball happens **right after the loop exits**, not inside it. The strike case doesn't need to look ahead within frames 1–9 because a strike is self-contained; the validator only needs to know `rolls[i]` to classify it.

And then once the loop is done, `i` is pointing at where frame 10 should start, and we immediately check `if i >= len(rolls)` before trying to read `first = rolls[i]`. Clean.

Let me ask one last thing about the actual **scoring** logic (not validation), because I want to make sure I see why it doesn't have the same paranoia:

```python
for _ in range(9):
    if rolls[i] == 10:                          # strike
        total += 10 + rolls[i + 1] + rolls[i + 2]
        i += 1
    elif rolls[i] + rolls[i + 1] == 10:         # spare
        total += 10 + rolls[i + 2]
        i += 2
    else:                                        # open frame
        total += rolls[i] + rolls[i + 1]
        i += 2
```

The validator already ran and passed, so we know the rolls are valid. But when we do `rolls[i + 1]` and `rolls[i + 2]` inside the scorer, we're **not checking bounds** — we're just assuming those indices exist. That's safe because `_validate()` already guaranteed it, right? 

Like, if validation passed, we know:
- Every frame 1–9 has enough rolls to be classified and scored.
- Frame 10 exists and is complete (whether 2 or 3 balls).
- There are no extra rolls after frame 10.

So by the time we reach the scorer, we can safely assume any index we try to access will exist?

---

## Turn 7

### Tutor

Tutor: Your conclusion is right, but the mechanism is slightly more subtle than "validation checked each look-ahead." It's worth being precise about what validation actually guarantees.

### What validation checks explicitly

| Situation | What `_validate` checks |
|---|---|
| Non-strike frame (1–9) | `rolls[i]` and `rolls[i+1]` both exist, sum ≤ 10 |
| Strike frame (1–9) | `rolls[i]` exists — nothing more |
| Frame 10 entry | `rolls[i]` exists |
| Frame 10 (strike) | `rolls[i+1]` and `rolls[i+2]` exist, constraint on their sum |
| Frame 10 (spare) | `rolls[i+2]` exists |
| Frame 10 (open) | `rolls[i+1]` exists, sum ≤ 10 |

Notice: validation **never** explicitly checks that a strike in frames 1–8 has valid look-ahead indices `i+1` and `i+2`.

### Why the scorer is still safe — structural completeness

Validation guarantees the list has the right *global* shape. As a consequence, any look-ahead the scorer performs is implicitly safe. The chain of reasoning:

- **Strike in frames 1–7**: `rolls[i+1]` is the next frame's first ball. Validation verified the next frame starts. `rolls[i+2]` is either the second ball of that frame, or the frame after it — both guaranteed present because validation walked all 9 frames and confirmed frame 10 exists.
- **Strike in frame 8**: `rolls[i+1]` is frame 9's first ball, `rolls[i+2]` is frame 9's second ball or frame 10's first — both guaranteed by the full walk.
- **Strike in frame 9**: `rolls[i+1]` is frame 10's first ball, `rolls[i+2]` is frame 10's second ball. The 10th-frame block verified both exist (the `i+2 >= len(rolls)` guard for the strike case).

So the guarantee isn't "I checked each look-ahead" — it's "I verified the list has a complete, legal 10-frame game, and a complete legal game necessarily contains every index the scorer will touch."

### The design contract

```
_validate(rolls)    ← establishes: "this is a complete, legal game"
                         ↓
score loop          ← relies on: "therefore all indices are safe"
```

The scorer has zero defensive checks because it's written to run only after that contract is established. If you ever called the scoring logic directly without `_validate`, it could raise an `IndexError` on a short list. The leading `_validate(rolls)` on line 16 is the only thing making the naked index accesses correct.

### Student

Ah, that's the key distinction I was conflating. Validation doesn't check *every* look-ahead explicitly — it walks the frames and verifies the global structure, which *implies* that all the indices the scorer will touch must exist.

It's a contract: validation says "this list is a complete, legal game," and the scorer says "okay, I trust that and won't do bounds checks myself."

That makes sense and it's efficient — we only validate once, upfront.

Now I'm satisfied with the logic. Let me actually run through one more concrete example with my own hand to make sure the whole thing clicks. Let me trace a perfect game (all strikes):

```
rolls = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
```

That's 9 strikes in frames 1–9, then frame 10 with a strike and two fill balls (both strikes). Total should be 300.

**Validation** (just the key checks):
- Frame 1: `i=0`, `rolls[0]==10`, `i+=1` → `i=1` ✓
- Frame 2: `i=1`, `rolls[1]==10`, `i+=1` → `i=2` ✓
- ... (frames 3–8 same)
- Frame 9: `i=8`, `rolls[8]==10`, `i+=1` → `i=9` ✓
- Post-loop: `i=9 < len(rolls)=12` ✓, `first=rolls[9]==10`
- 10th-frame strike: `i+2=11 < len(rolls)=12` ✓, `second=rolls[10]==10` (skip sum check), `i+=3` → `i=12` ✓
- Final: `i=12 >= len(rolls)=12` ✓ (no extra rolls)

**Scoring**:
- Frame 1: `rolls[0]==10`, `total += 10 + rolls[1] + rolls[2] = 10+10+10 = 30`, `i=1`
- Frame 2: `rolls[1]==10`, `total += 10 + rolls[2] + rolls[3] = 30`, `i=2`
- ... (frames 3–8 same, each adds 30)
- Frame 9: `rolls[8]==10`, `total += 10 + rolls[9] + rolls[10] = 10+10+10 = 30`, `i=9`
- Frame 10: `total += sum(rolls[9:]) = sum([10,10,10]) = 30`
- **Total: 9×30 + 30 = 300** ✓

Perfect. I think I've got it. The code is clean and correct. I don't have any more questions — I understand the frame walk, the validation structure, the 10th-frame special cases, and why the scorer can trust its indices.

<done/>

---

**Run end:** done after 7 turn(s) in 408.2s
