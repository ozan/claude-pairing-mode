# exercism-bowling

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:52:22

## Initial prompt

Exercism 'Bowling': implement a 10-pin bowling scorer. Track frames, handle strikes (next two rolls bonus), spares (next roll bonus), and the special 10th-frame bonus rolls. Return the final score from a list of rolls.

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Tutor: Good — let's build this in Python. The Exercism interface uses a class with `roll(pins)` and `score()` methods.

First key decision — how does `score()` compute the total?

OPTIONS:
[A] Accumulate score during roll()
Track a running total and pending bonus multipliers as each `roll()` arrives. `score()` just returns the accumulated value.

[B] Replay rolls list in score()
`roll()` appends to a list. `score()` walks through all 10 frames with an index pointer, computing bonuses by peeking ahead in the list.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach do you prefer?

### Student

I think I'll go with **B** — replay rolls in `score()`.

Here's my reasoning: strikes and spares both need us to look ahead at future rolls to calculate bonuses. With option A, we'd have to somehow defer or guess those bonuses when we don't know what's coming next. With option B, once all the rolls are recorded, we can walk through the frames cleanly and peek ahead whenever we need to, without any guessing.

It feels like it separates concerns better too — `roll()` just records what happened, and `score()` handles all the logic of figuring out what each frame is worth.

---

## Turn 2

### Tutor

Tutor: Exactly right — clean separation, and the look-ahead is trivial once all rolls exist. Great instinct.

Now the tricky part: the 10th frame. After a strike or spare you get bonus rolls, but they're scored differently than frames 1–9. How should `score()` treat frame 10?

OPTIONS:
[A] Special-case frame 10
Loop over frames 0–8 with the standard logic, then handle frame 10 outside the loop: sum whatever bonus balls were thrown without applying the strike/spare bonus formula.

[B] Uniform formula all 10 frames
Run the same strike/spare/normal logic for all 10 frames. The 10th frame's bonus balls land at `rolls[i+1]` and `rolls[i+2]` just like any other frame — the formula naturally picks them up.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which feels right to you?

### Student

I think **B** — uniform formula for all 10 frames.

My reasoning: if the 10th frame's bonus rolls are just sitting in the `rolls` list at predictable indices, then the same strike/spare logic should just work. A strike in frame 10 means I add the next two rolls as a bonus, and those next two rolls exist in the list. A spare means I add the next one roll. It's the same rule.

Option A would require me to write different code paths and remember which rules apply where. Option B means I write the logic once and trust it works consistently. That feels safer and less error-prone.

The only thing I need to be careful about is that in frame 10, those bonus rolls might not be "real frames" — they're just extra rolls — but that shouldn't matter for the *formula* itself. The formula just looks at indices and sums pins.

---

## Turn 3

### Tutor

Tutor: Spot on — you've identified exactly why it works. The "bonus rolls" aren't a conceptual exception, just more list entries.

Now let's talk about validation. Exercism expects errors for things like too many pins, rolling after the game ends, or calling `score()` on an incomplete game. Where does that logic live?

OPTIONS:
[A] Validate eagerly in roll()
Track frame state as rolls arrive. Raise immediately if a roll is out of bounds, a frame exceeds 10 pins, or the game is already over.

[B] Validate lazily in score()
Let `roll()` append blindly. When `score()` replays the list, check for invalid sequences and raise if anything looks wrong.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which do you prefer?

### Student

I'll go with **A** — validate eagerly in `roll()`.

Here's my thinking: if someone calls `roll(15)` or tries to roll after the game is over, they should know immediately that something is wrong. Waiting until `score()` is called feels like hiding the error and making the bug harder to track down. Plus, if validation happens early, the caller can fix their mistake right away instead of building up a whole invalid rolls list.

Also, validating in `roll()` means I can track state as I go — like keeping track of whether I'm still in frame 1 or already past frame 10 — which is natural to do incrementally. If I wait until `score()`, I'd have to reconstruct that state from scratch, which seems wasteful and more complex.

The only tricky part is making sure my state tracking in `roll()` is correct and doesn't get confused. But that feels like the right place to be careful rather than punting to later.

---

## Turn 4

### Tutor

Tutor: Exactly right on all counts. "Fix errors close to where they occur" is a reliable principle.

We've made all the key decisions. Let me write the implementation — I'll inline the interesting bits as we go.

[Glob(bowling.py)]
  No files found

[Write(bowling.py)]
class BowlingGame:
    def __init__(self):
        self._rolls = []
        self._current_frame = 0   # 0-indexed (0–9)
        self._roll_in_frame = 0   # which roll within the current frame
        self._game_done = False

    def roll(self, pins):
        if self._game_done:
            raise Exception("Cannot roll after game is over")
        if pins < 0:
            raise Exception("Negative pins not allowed")
… (64 more lines)
  File created successfully at: bowling.py

Tutor: Good. Let me run a quick sanity check on a few key cases before we review:

[Bash(python3 -c "
from bowling import BowlingGame

# Perfect game: 12 strikes = 300
g = BowlingGame()
for _ in range(12):
    g.roll(10)
print('Perfect game:', g.score())   # expect 300

# All spares + 5: each frame = 15, 10th frame = 15
g = BowlingGame()
for _ in range(21):
    g.roll(5)
print('All spares:', g.score())     # expect 150

# Gutter game: 20 zeros = 0
g = BowlingGame()
for _ in range(20):
    g.roll(0)
print('Gutter game:', g.score())    # expect 0

# Mixed: strike + spare + ... simple case
g = BowlingGame()
g.roll(10)  # frame 1 strike
g.roll(3); g.roll(6)  # frame 2: 9
for _ in range(8):  # frames 3-9: gutter
    g.roll(0); g.roll(0)
g.roll(0); g.roll(0)  # frame 10: gutter
print('Strike then 3/6:', g.score())  # 10+3+6 + 9 + 0*8 = 28

# Validation: too many pins in a frame
try:
    g = BowlingGame()
    g.roll(6); g.roll(5)
except Exception as e:
    print('Frame > 10 caught:', e)

# Validation: roll after game over
try:
    g = BowlingGame()
    for _ in range(20):
        g.roll(0)
    g.roll(1)
except Exception as e:
    print('Roll after game caught:', e)

# score() on incomplete game
try:
    g = BowlingGame()
    g.roll(5)
    g.score()
except Exception as e:
    print('Incomplete game caught:', e)
"
)]
  error: Exit code 1

Tutor: The code is fine — my test had the wrong roll count. `range(8)` extended into the 10th frame and completed it, then I tried to roll again. Let me fix the test and verify properly:

[Bash(python3 -c "
from bowling import BowlingGame

# Perfect game: 12 strikes = 300
g = BowlingGame()
for _ in range(12):
    g.roll(10)
print('Perfect game:', g.score())   # 300

# All spares + 5
g = BowlingGame()
for _ in range(21):
    g.roll(5)
print('All spares:', g.score())     # 150

# Gutter game
g = BowlingGame()
for _ in range(20):
    g.roll(0)
print('Gutter game:', g.score())    # 0

# Strike in frame 1, 3/6 in frame 2, zeros elsewhere (7 more frames + 10th)
g = BowlingGame()
g.roll(10)            # frame 1: strike
g.roll(3); g.roll(6) # frame 2: 9 (bonus: 3+6=9, frame total = 10+9=19)
for _ in range(7):   # frames 3-9: zeros
    g.roll(0); g.roll(0)
g.roll(0); g.roll(0) # frame 10: zeros
print('Strike then 3/6:', g.score())  # 19 + 9 + 0 = 28

# Spare in frame 1
g = BowlingGame()
g.roll(6); g.roll(4) # frame 1: spare
g.roll(3); g.roll(0) # frame 2: 3 (bonus to spare)
for _ in range(7):
    g.roll(0); g.roll(0)
g.roll(0); g.roll(0)
print('Spare then 3:', g.score())  # (10+3) + 3 + 0 = 16

# Validation: frame exceeds 10
try:
    g = BowlingGame()
    g.roll(6); g.roll(5)
except Exception as e:
    print('Frame > 10:', e)

# Validation: negative pins
try:
    g = BowlingGame()
    g.roll(-1)
except Exception as e:
    print('Negative pins:', e)

# Validation: roll after game over
try:
    g = BowlingGame()
    for _ in range(20): g.roll(0)
    g.roll(1)
except Exception as e:
    print('After game over:', e)

# Validation: score on incomplete game
try:
    g = BowlingGame()
    g.roll(5)
    g.score()
except Exception as e:
    print('Incomplete game:', e)

# 10th frame: spare earns one bonus roll
g = BowlingGame()
for _ in range(9): g.roll(0); g.roll(0)
g.roll(7); g.roll(3); g.roll(8)  # spare + bonus 8
print('10th frame spare:', g.score())  # 0*9 + (10+8) = 18

# 10th frame: validate no 3rd roll without strike/spare
try:
    g = BowlingGame()
    for _ in range(9): g.roll(0); g.roll(0)
    g.roll(3); g.roll(4)   # normal frame in 10th
    g.roll(1)              # should raise
except Exception as e:
    print('10th no bonus roll:', e)
"
)]
  Perfect game: 300
  All spares: 150
  Gutter game: 0
  Strike then 3/6: 28
  Spare then 3: 16
  Frame > 10: Pin count exceeds pins on the lane
  Negative pins: Negative pins not allowed
  After game over: Cannot roll after game is over
  Incomplete game: Score cannot be taken until the end of the game
  10th frame spare: 18
  10th no bonus roll: Cannot roll after game is over

Tutor: All cases pass. Now — one thing worth looking at closely before calling this done:

OPTIONS:
[A] Validation is complete
The current 10th-frame validation handles all cases. The code is ready.

[B] One edge case is missing
A strike in the 10th followed by two more rolls — what if the second ball knocks down 7 pins, then the third ball gets 4? That's 7+4 > 10 on a "fresh" set. Does the code catch it?

(Reply with A or B, or ask a follow-up question.)

Tutor: What do you think?

### Student

I think **B** — there's an edge case missing.

In the 10th frame, after a strike, you get two bonus rolls. Those two bonus rolls are treated as a *new frame* — if the first of those two rolls is itself a strike, the second roll starts fresh. But if the first roll is *not* a strike, then the first and second rolls together shouldn't exceed 10 pins.

So if I roll a strike in frame 10, then roll 7, then roll 4 — that's 7 + 4 = 11, which should fail. But if I roll a strike, then roll 10 (another strike), then roll anything, that's valid.

Similarly, after a spare in frame 10, you get one bonus roll, and that bonus roll can be anything (0–10).

Let me test this to see if the current code catches it:

```python
g = BowlingGame()
for _ in range(9): g.roll(0); g.roll(0)
g.roll(10)  # 10th frame: strike
g.roll(7); g.roll(4)  # bonus rolls: 7 + 4 = 11, should fail
print(g.score())
```

I suspect this will either pass incorrectly or error in a confusing way. Does the validation in the 10th frame check for that?

---

## Turn 5

### Tutor

Tutor: Good instinct — let's find out:

[Bash(python3 -c "
from bowling import BowlingGame

# strike → 7 → 4 (should FAIL: 7+4=11 on same set of pins)
try:
    g = BowlingGame()
    for _ in range(9): g.roll(0); g.roll(0)
    g.roll(10)
    g.roll(7); g.roll(4)
    print('WRONG: accepted strike/7/4, score =', g.score())
except Exception as e:
    print('Correctly rejected strike/7/4:', e)

# strike → 10 → 4 (should PASS: second strike resets pins)
try:
    g = BowlingGame()
    for _ in range(9): g.roll(0); g.roll(0)
    g.roll(10); g.roll(10); g.roll(4)
    print('Correctly accepted strike/strike/4, score =', g.score())
except Exception as e:
    print('WRONG: rejected strike/strike/4:', e)

# strike → 10 → 10 (perfect 10th frame - should PASS)
try:
    g = BowlingGame()
    for _ in range(9): g.roll(0); g.roll(0)
    g.roll(10); g.roll(10); g.roll(10)
    print('Correctly accepted 3 strikes in 10th, score =', g.score())
except Exception as e:
    print('WRONG: rejected 3 strikes in 10th:', e)
"
)]
  Correctly rejected strike/7/4: Pin count exceeds pins on the lane
  Correctly accepted strike/strike/4, score = 24
  Correctly accepted 3 strikes in 10th, score = 30

Tutor: The check was already there — `first == 10 and second != 10 and second + pins > 10`. It catches the case because after a 10th-frame strike, if the second ball *isn't* also a strike, the second and third balls share the same set of pins.

The three scenarios map cleanly to the validation branches:

| 10th-frame rolls | Rule |
|---|---|
| strike → non-strike → X | `second + X ≤ 10` enforced |
| strike → strike → X | pins reset again, any `X` 0–10 valid |
| spare → X | pins reset, any `X` 0–10 valid |

The implementation is solid. Here's a summary of what we built and the decisions behind it:

- **`roll()` appends to a list** — `score()` replays it, so look-ahead for bonuses is simple index arithmetic
- **Uniform formula across all 10 frames** — the 10th frame's bonus balls are just the next entries in the list; no special case in `score()`
- **Eager validation in `roll()`** — errors surface immediately at the bad input, not deferred to `score()`
- **State tracked in `roll()`**: current frame, roll-within-frame, and `_game_done` — which also drives the "roll after game over" guard

### Student

That's really helpful — I'm satisfied with how it all came together.

Looking back at the journey:
- We chose to replay rolls in `score()` so we could look ahead cleanly for bonuses
- We kept the 10th frame under the same formula instead of special-casing it, which turned out to be elegant
- We validated eagerly in `roll()` so errors surface right where they happen
- The 10th-frame validation handles the subtle case where a strike followed by a non-strike requires the two non-strike rolls to sum to ≤10, but a strike followed by another strike resets the pins

I feel like I understand *why* each piece works now, not just that it works. The code is clean and handles all the edge cases properly.

<done/>

---

**Run end:** done after 5 turn(s) in 280.5s
