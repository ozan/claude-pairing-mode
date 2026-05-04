# exercism-bowling

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:52:22

## Initial prompt

Exercism 'Bowling': implement a 10-pin bowling scorer. Track frames, handle strikes (next two rolls bonus), spares (next roll bonus), and the special 10th-frame bonus rolls. Return the final score from a list of rolls.

---

## Turn 1

### Tutor

Thinking: The user wants to implement a bowling scorer for the Exercism Bowling exercise. Let me think about the key design decisions here.
  
  Key aspects of 10-pin bowling:
  1. 10 frames
  2. Strike: knock down all 10 pins on first roll → bonus = next 2 rolls
  3. Spare: knock down all 10 pins in 2 rolls → bonus = next 1 roll
  4. 10th frame special: if strike, get 2 more rolls; if spare, get 1 more roll
  5. Return total score
  
  Let me think about the main design decisions:
  
  1. **Language choice** - The user didn't specify. Exercism supports many languages. 
  
  I'll go with Python since it's widely used and the user didn't indicate otherwise.
  
  2. **Core algorithmic approach**: 
     - Option A: Iterate through frames, maintaining an index into the rolls list
     - Option B: Process rolls one at a time with state machine
  
  The frame-index approach is cleaner and more straightforward. The state machine approach can work but adds unnecessary complexity.
  
  3. **Validation**: The Exercism bowling exercise typically requires validation—raising errors for invalid roll sequences like negative pins, pins exceeding 10, or attempting to score after the game ends.
  
  Now I'm thinking through the key design decision: how to walk through the rolls to score frames. I could use a roll index that advances through the rolls list frame by frame, or build Frame objects to track rolls. The index-based approach is cleaner and more Pythonic. For Exercism's bowling, the standard pattern is to iterate through 10 frames, checking if each frame is a strike and advancing the roll index accordingly.
  
  Writing the scoring logic... I'm deciding between a functional approach with index-based iteration through the rolls array versus a class-based design with separate `roll()` and `score()` methods. The functional approach is cleaner for reasoning about the problem, so I'll go with collecting all rolls first, then iterating through frames to calculate the score.

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Thinking: Now let me think about the first key design decision for the bowling scorer. I'll use Python since it's not specified.
  
  The Exercism bowling exercise in Python typically uses a class with `roll()` and `score()` methods. The key first design question is about how to structure the scoring logic.
  
  The most fundamental algorithmic question is: how do we walk through the rolls to compute the score?
  
  **Option A**: Store all rolls in a list, then when `score()` is called, iterate through frames using an index pointer into the rolls list.
  
  **Option B**: Compute score incrementally as rolls come in - track frame state, running totals, etc. during `roll()` calls.
  
  
  Option A is cleaner because I can defer all the complexity to one place, whereas Option B requires managing pending bonuses for strikes and spares throughout the rolling process, which gets messy quickly.

Tutor: Good — let's build this in Python. The Exercism interface uses a class with `roll(pins)` and `score()` methods.

First key decision — how does `score()` compute the total?

OPTIONS:
[A] Accumulate score during roll()
Track a running total and pending bonus multipliers as each `roll()` arrives. `score()` just returns the accumulated value.

[B] Replay rolls list in score()
`roll()` appends to a list. `score()` walks through all 10 frames with an index pointer, computing bonuses by peeking ahead in the list.

(Reply with A or B, or ask a follow-up question.)

PRIVATE: best=B
PRIVATE: rationale=Option B (replay) is cleaner because the look-ahead for strike/spare bonuses is natural when you have all rolls available. With Option A, you need to track "pending bonus counts" (e.g., a strike means the next 2 rolls each count double), which requires careful state: bonus_rolls_remaining, multipliers per pending event, etc. The replay approach lets score() just say "if strike, add rolls[i+1]+rolls[i+2]" — simple index arithmetic. The incremental approach is tempting (feels more "real-time") but the state management gets messy, especially for back-to-back strikes where bonuses overlap.

Tutor: Which approach do you prefer?

### Student

I think I'll go with **B** — replay rolls in `score()`.

Here's my reasoning: strikes and spares both need us to look ahead at future rolls to calculate bonuses. With option A, we'd have to somehow defer or guess those bonuses when we don't know what's coming next. With option B, once all the rolls are recorded, we can walk through the frames cleanly and peek ahead whenever we need to, without any guessing.

It feels like it separates concerns better too — `roll()` just records what happened, and `score()` handles all the logic of figuring out what each frame is worth.

---

## Turn 2

### Tutor

Thinking: The user picked B and gave excellent reasoning. They've clearly understood the key insight. Let me affirm briefly and move on to the next decision.
  
  Next decision: the 10th frame handling. This is where it gets tricky. The 10th frame has special rules:
  - If you get a strike in the 10th frame, you get 2 bonus rolls
  - If you get a spare in the 10th frame, you get 1 bonus roll
  - The scoring in the 10th frame is just the sum of all rolls (no "bonus" multiplier beyond what those extra rolls provide)
  
  
  Now I'm thinking through how to handle the 10th frame in the scoring logic. The question is whether to treat it as a special case after the main loop or find a way to integrate it into the same logic. For frames 1-9, a strike scores 10 plus the next two rolls, but the 10th frame works differently—those bonus rolls are just added directly to the frame's total without the multiplier effect. I'm realizing the 10th frame actually follows the same scoring formula as frames 1-9, so I can handle all frames uniformly with a single loop rather than special-casing the final frame—the bonus rolls are just naturally part of the rolls array.

Tutor: Exactly right — clean separation, and the look-ahead is trivial once all rolls exist. Great instinct.

Now the tricky part: the 10th frame. After a strike or spare you get bonus rolls, but they're scored differently than frames 1–9. How should `score()` treat frame 10?

OPTIONS:
[A] Special-case frame 10
Loop over frames 0–8 with the standard logic, then handle frame 10 outside the loop: sum whatever bonus balls were thrown without applying the strike/spare bonus formula.

[B] Uniform formula all 10 frames
Run the same strike/spare/normal logic for all 10 frames. The 10th frame's bonus balls land at `rolls[i+1]` and `rolls[i+2]` just like any other frame — the formula naturally picks them up.

(Reply with A or B, or ask a follow-up question.)

PRIVATE: best=B
PRIVATE: rationale=The standard replay formula (strike → +rolls[i+1]+rolls[i+2], spare → +rolls[i+2]) works identically for frame 10 because the "bonus rolls" the 10th frame earns are simply subsequent entries in the rolls list. The formula peeks ahead and grabs them the same way it would for frames 1–9. No special case needed. Option A is tempting because the 10th frame *feels* different (you bowl up to 3 balls instead of 2), but that difference is in validation/input, not in the scoring formula itself.

Tutor: Which feels right to you?

### Student

I think **B** — uniform formula for all 10 frames.

My reasoning: if the 10th frame's bonus rolls are just sitting in the `rolls` list at predictable indices, then the same strike/spare logic should just work. A strike in frame 10 means I add the next two rolls as a bonus, and those next two rolls exist in the list. A spare means I add the next one roll. It's the same rule.

Option A would require me to write different code paths and remember which rules apply where. Option B means I write the logic once and trust it works consistently. That feels safer and less error-prone.

The only thing I need to be careful about is that in frame 10, those bonus rolls might not be "real frames" — they're just extra rolls — but that shouldn't matter for the *formula* itself. The formula just looks at indices and sums pins.

---

## Turn 3

### Tutor

Thinking: The user has excellent reasoning again. They've understood the key insight perfectly. Let me affirm and move to the next decision.
  
  Now let's think about what to build next. We have the core algorithm decided. Let me think about what the next interesting design decision would be.
  
  The next question could be about validation. The Exercism bowling exercise requires validation - you need to raise errors for:
  1. Negative pins or pins > 10 in a single roll
  2. Two rolls in a frame summing to more than 10 (unless it's the 10th frame with a strike)
  3. Rolling after the game is over
  4. Calling score() on an incomplete game
  
  Should we validate? And if so, where?
  
  
  I'm weighing whether to jump straight into validation or present the class structure first. The validation question itself is interesting because there's a real trade-off between eager validation in `roll()` as balls come in versus lazy validation in `score()` during replay. Eager validation catches errors immediately, which feels like the better approach.
  
  Though some validation is inherently stateful—like checking whether the game is already over—so it naturally belongs in `roll()` where you track game state. so you need some state tracking in `roll()` anyway.
  
  The real question is where validation happens: either I validate eagerly in `roll()` and raise errors immediately, or I defer all validation to `score()` and replay the rolls to catch problems. The first approach gives better error locality and user experience, so that's the way to go.

Tutor: Spot on — you've identified exactly why it works. The "bonus rolls" aren't a conceptual exception, just more list entries.

Now let's talk about validation. Exercism expects errors for things like too many pins, rolling after the game ends, or calling `score()` on an incomplete game. Where does that logic live?

OPTIONS:
[A] Validate eagerly in roll()
Track frame state as rolls arrive. Raise immediately if a roll is out of bounds, a frame exceeds 10 pins, or the game is already over.

[B] Validate lazily in score()
Let `roll()` append blindly. When `score()` replays the list, check for invalid sequences and raise if anything looks wrong.

(Reply with A or B, or ask a follow-up question.)

PRIVATE: best=A
PRIVATE: rationale=Eager validation in roll() gives immediate, precise feedback at the point of the bad input. If someone rolls 15 pins, you want to raise right then, not silently store it and only find out when score() is called. It also naturally catches "rolled after game is over" since you track game progress in roll(). The downside is you need some frame-tracking state in roll() — but you need that anyway to know when the game ends. Lazy validation in score() means errors surface at the wrong time, and you'd also have to re-derive frame structure during score() just for validation, which is redundant work alongside the scoring pass.

Tutor: Which do you prefer?

### Student

I'll go with **A** — validate eagerly in `roll()`.

Here's my thinking: if someone calls `roll(15)` or tries to roll after the game is over, they should know immediately that something is wrong. Waiting until `score()` is called feels like hiding the error and making the bug harder to track down. Plus, if validation happens early, the caller can fix their mistake right away instead of building up a whole invalid rolls list.

Also, validating in `roll()` means I can track state as I go — like keeping track of whether I'm still in frame 1 or already past frame 10 — which is natural to do incrementally. If I wait until `score()`, I'd have to reconstruct that state from scratch, which seems wasteful and more complex.

The only tricky part is making sure my state tracking in `roll()` is correct and doesn't get confused. But that feels like the right place to be careful rather than punting to later.

---

## Turn 4

### Tutor

Thinking: The user has made all three key design decisions:
  1. Replay approach in `score()`
  2. Uniform formula for all 10 frames
  3. Eager validation in `roll()`
  
  Now let me write the initial file. Let me think about the implementation.
  
  The class needs:
  - `__init__`: initialize state
  - `roll(pins)`: validate and record a roll
  - `score()`: replay and compute
  
  State needed for validation in `roll()`:
  - `self._rolls`: list of all rolls
  - Track whether the game is done
  - Track current frame and position within frame
  
  For tracking state in `roll()`, I need to know:
  
  
  - Which frame we're on (0-9)
  - Which roll within the frame (first or second)
  - Whether the game is over
  
  For the 10th frame, I need special handling: if it's a strike, allow 2 more rolls; if it's a spare, allow 1 more roll. Let me set up a state machine with instance variables to track the current frame, which roll we're on within that frame, and whether the game has finished.
  
  Defining the class structure...
  
  Now I'm implementing the roll validation logic that checks for invalid inputs like negative pins or exceeding the pin count, with special rules for frames before the 10th where consecutive rolls in the same frame can't exceed 10 pins total.
  
  For the 10th frame, the logic gets trickier—I need to allow a third roll only if the first roll was a strike or the first two rolls made a spare, then mark the game as complete.
  
  Simplifying the state representation...
  
  Writing the frame logic... I'm settling on just writing the implementation now since we've covered the main design decisions around frame handling and scoring logic. The validation for the 10th frame is complex with different rules than frames 1-9, but I think I have a clear enough picture to code it up.
  
  Writing the BowlingGame class... I'm realizing my approach to tracking the 10th frame needs adjustment. Now I'm implementing the scoring logic that handles strikes, spares, and regular frames by iterating through the rolls and calculating bonuses appropriately.
  
  The 10th frame is trickier because it allows bonus rolls if you get a strike or spare, and the validation rules change depending on what happened in previous rolls—if the first roll was a strike, pins reset for the second roll, and the third roll's constraints depend on whether the second was also a strike or not.
  
  I think the cleanest approach is to track the rolls taken in the 10th frame as a list and validate each new roll based on its position and the values of previous rolls.
  
  Implementing the validation logic... Writing the bowling game class... I'm realizing there's an issue with how I'm tracking the rolls—when I check `self._rolls[-1]` after appending, I need to be careful about whether that's actually the first roll of the current frame or something else. Let me reconsider the logic for frames 0-8 and make sure I'm accessing the right roll when validating the pin count.
  
  I think the cleanest approach is to track the first roll of the current frame separately as its own variable, rather than trying to reconstruct it from the rolls list. That way I can easily validate that two consecutive rolls in the same frame don't exceed 10 pins without getting confused about indices.
  
  Defining the class structure... I'm realizing the roll tracking is getting messy with the 10th frame logic, especially when handling strikes. Let me simplify by tracking the starting index of the 10th frame separately instead of trying to infer it from the roll history.
  
  Refining the tenth frame handler... Still writing validation logic...
  
  Now I'm thinking through the `score()` method and when it should be callable. The game ends either when `_game_over` is set to True or when all frames are complete, so I need to validate that the game is actually finished before allowing scoring. Writing the BowlingGame class... Continuing the validation logic for the 10th frame, then recording the roll and checking if the game ends after two or three rolls depending on whether a strike or spare was earned. After that, I'm implementing the scoring method that calculates the total points by iterating through frames and applying bonus multipliers for strikes and spares.
  
  Wait, I need to double-check the 10th frame validation—when checking the first roll, I'm looking at the last element in the rolls list, but the current roll hasn't been added yet, so that's actually pointing to the first roll of the 10th frame, which is what I want.
  
  Let me trace through the logic: in frames 0-8, when I'm on the second roll, `self._rolls[-1]` gives me the first roll of that frame. But in the 10th frame, the logic is different because I need to validate against the previous roll to determine what's allowed. The last appended roll was the first roll of the current frame (we appended it in the `else` branch when `roll_in_frame` was 0). So `self._rolls[-1]` is the first roll of the current frame. ✓
  
  This looks correct! But I realize there's still an issue: when `_roll_in_frame == 2` in the 10th frame, `self._rolls[-2]` and `self._rolls[-1]` might not be the first and second rolls of the 10th frame if... wait, they will be, because we're tracking `_roll_in_frame` which tells us exactly which roll in the 10th frame this is. If it's the 3rd roll (r==2), then the last two appended rolls must be the 1st and 2nd rolls of the 10th frame. ✓
  
  OK so this logic is correct. Let me also handle the `score()` completeness check more carefully. `_game_done` only gets set when the 10th frame finishes, so calling `score()` before that point will correctly raise an exception. For a perfect game with 12 strikes, the 10th frame would have three strikes in a row, and `_game_done` would be set after the third roll completes. The perfect game scores correctly at 300 points, with each of the first nine frames contributing 30 points and the tenth frame doing the same. I've settled on raising an error for incomplete games rather than silently handling them, and the `_game_done` flag manages that detection cleanly. I think I've covered the main design decisions, so I'm ready to write out the implementation. I'm realizing there's a potential issue with accessing future rolls in the `score()` method when we peek ahead for strikes and spares, but since we already validate that the game is complete before scoring, we're guaranteed to have all the rolls we need—the peek-ahead will always find rolls either later in the current frame or in the 10th frame's bonus rolls. The implementation should be solid, so I'll go ahead and write it out.

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

Thinking: There's a bug! After the strike in frame 1 and the 3/6 in frame 2, we play frames 3-9 (7 frames × 2 rolls = 14 rolls), but my loop says "8 frames" which would be 16 rolls. Let me recalculate.
  
  After frames 1 (strike, 1 roll) and 2 (3+6, 2 rolls), we're at frame 3 (index 2). We need frames 3-9 = 7 frames, plus frame 10. My loop does `for _ in range(8)` which is 8 frames × 2 rolls = 16 rolls for frames 3-10... that's too many.
  
  
  So the total should be 1 + 2 + 14 + 2 = 19 rolls, but my test is only providing 1 + 2 + 16 = 19 rolls total, which means I'm consuming too many rolls in the middle frames. I'm getting confused about the frame indexing here. Let me trace through this more carefully: frame 0 is the strike, frame 1 is the 3+6, then the loop handles frames 2 through 9 (which is actually the 10th frame). When `_current_frame` equals 9, that's when we should call `_roll_tenth_frame` instead of `_roll_normal_frame`. I'm tracing through the loop iterations to verify the tenth frame logic—when we reach frame 9 (the 10th frame), the code correctly calls `_roll_tenth_frame` instead of `_roll_normal_frame`, and subsequent rolls in that frame are handled by the tenth frame method rather than the normal frame logic.
  
  After working through the iterations, I realize the test itself is flawed, not the code. The loop uses `range(8)` which covers frames 2-9 (8 frames total), but that already includes the 10th frame, so the game finishes before those extra rolls outside the loop. I need to adjust the test to use `range(7)` for frames 2-8, then handle the 10th frame separately—that gives me 1 roll for the strike, 2 rolls for frame 1, 14 rolls for frames 2-8, and 2 rolls for frame 9, totaling 19 rolls instead.

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

PRIVATE: best=B
PRIVATE: rationale=After a 10th-frame strike, the pins are reset, so rolls 2 and 3 are on a fresh rack. If roll 2 is not itself a strike, roll 2 + roll 3 can't exceed 10. The current code only checks `first == 10 and second != 10 and second + pins > 10` which handles this — but it's worth verifying with an actual test since it's a subtle rule. A test of strike → 7 → 4 should raise, but strike → 10 → 4 (two strikes then 4) should be valid.

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

Thinking: The user wants to test if the current code catches the case of strike → 7 → 4 in the 10th frame. Let me check the code.
  
  In `_roll_tenth_frame`, when `r == 2` (third roll):
  ```python
  elif r == 2:
      first, second = self._rolls[-2], self._rolls[-1]
      if first != 10 and first + second != 10:
          raise Exception("Cannot roll after game is over")
      # strike then non-strike: second set of pins must be ≤ 10 - second
  
  
  ```
  
  Checking the validation logic...
  
  For strike → 7 → 4, the code checks if the first roll is 10 and the second isn't, then validates that the second plus third roll doesn't exceed 10. Since 7 + 4 = 11, this exceeds the limit and the exception gets raised. So it does catch this case correctly. Let me run the test to confirm.
  
  Actually, I need to trace through the 10th frame logic more carefully. After rolling a strike, then 7, we're at `_roll_in_frame = 2`. The validation checks if the first roll (10) isn't a strike and if first + second equals 10 — but since first is 10, that condition is false, so we skip the early termination. Then when the third roll (4) comes in, we check if second + third exceeds 10 pins, which it does, triggering the exception.

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

Thinking: The code handles all these cases correctly. The validation in `_roll_tenth_frame` when `r == 2` correctly checks:
  - `first == 10 and second != 10 and second + pins > 10` → catches strike/7/4 ✓
  - strike/strike/4 passes because `second == 10` → skip the check ✓
  - strike/strike/strike passes ✓
  
  The code is correct. Let me summarize the implementation to the user.

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
