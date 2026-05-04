# exercism-bowling

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:41:56

## Initial prompt

Exercism 'Bowling': implement a 10-pin bowling scorer. Track frames, handle strikes (next two rolls bonus), spares (next roll bonus), and the special 10th-frame bonus rolls. Return the final score from a list of rolls.

---

## Turn 1

### Tutor

Tutor: Let's build this up step by step. First, a foundational question about how we iterate through the rolls:

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Pre-split into frames
Parse `rolls` into a list of frame objects/tuples first, then iterate frames to sum scores. Feels structured and "clean" upfront.

[B] Roll-index traversal
Keep rolls as a flat list, walk it with an integer index. Each frame advances the index by 1 (strike) or 2 (otherwise). Bonus rolls are just `rolls[i+1]`, `rolls[i+2]`.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach do you prefer for the main scoring loop — **A** (parse into frames first) or **B** (flat list + index)?

### Student

I think I'll go with **B** — flat list + index.

My reasoning: since strikes advance the index differently than other frames, and the 10th frame has special rules about bonus rolls, it feels like the index-based approach will let me handle those variable step sizes more naturally. I can just increment the index by 1 or 2 depending on what I rolled, and look ahead with `rolls[i+1]` or `rolls[i+2]` when I need bonuses.

Pre-parsing into frames seems like it might force me to do a lot of conditional logic upfront to figure out frame boundaries, especially with the 10th frame being weird. With approach B, I can handle the frame logic and bonuses in one pass.

Shall we start coding?

---

## Turn 2

### Tutor

Tutor: Exactly right — great reasoning. Let's write the skeleton with frames 1–9 handled, then tackle the 10th frame.

[Bash(ls bowling.py 2>/dev/null || echo "not found")]
  not found

[Write(bowling.py)]
def score(rolls):
    total = 0
    i = 0  # index into rolls list

    for frame in range(9):
        if rolls[i] == 10:          # strike
            total += 10 + rolls[i + 1] + rolls[i + 2]
            i += 1
        elif rolls[i] + rolls[i + 1] == 10:  # spare
            total += 10 + rolls[i + 2]
            i += 2
        else:                        # open frame
… (7 more lines)
  File created successfully at: bowling.py

Tutor: Frames 1–9 are done. Now the 10th frame. The special rule is: a strike earns 2 bonus rolls, a spare earns 1 — but crucially, those bonus balls are *part of* the 10th frame's score, not a lookahead into a future frame. How should we score it?

OPTIONS:
[A] Sum remaining rolls
```diff
+++ bowling.py
@@ -14,3 +14,3 @@
-    # 10th frame: ???
+    # 10th frame: sum whatever rolls remain
+    total += sum(rolls[i:])
```
For a valid game, `rolls[i:]` is exactly the 10th frame's 2 or 3 rolls.

[B] Explicit strike/spare check
```diff
+++ bowling.py
@@ -14,3 +14,7 @@
-    # 10th frame: ???
+    if rolls[i] == 10 or rolls[i] + rolls[i + 1] == 10:
+        total += rolls[i] + rolls[i + 1] + rolls[i + 2]
+    else:
+        total += rolls[i] + rolls[i + 1]
```
Mirrors the logic used for frames 1–9.

(Reply with A or B, or ask a follow-up question.)

Tutor: **A** or **B** for the 10th frame?

### Student

I'll go with **A** — sum remaining rolls.

Here's my thinking: in a valid game, if we've correctly consumed all the rolls for frames 1–9, then `rolls[i:]` will be *exactly* the 10th frame's rolls (either 2 or 3 depending on strike/spare). It's simpler, less error-prone, and doesn't duplicate the strike/spare logic.

Option B works too, but it feels like we're re-checking conditions we already validated while building frames 1–9. If the input is valid, A just trusts that and gets the job done in one line.

Let's fill in the rest and test it!

---

## Turn 3

### Tutor

Tutor: Spot on. Let me apply that now.

[Edit(bowling.py)]
--- before
    # 10th frame: ???
--- after
    # 10th frame: sum whatever rolls remain
    total += sum(rolls[i:])
  The file bowling.py has been updated successfully.

Tutor: The scorer is functionally complete for valid games. Before writing tests — one more real decision: Exercism expects `ValueError` for invalid input. Where should that logic live?

OPTIONS:
[A] Validate inside score()
Add `if` checks inline — e.g. `if rolls[i] < 0 or rolls[i] > 10: raise ValueError(...)` — woven into the existing loop.

[B] Separate validate() function
Write a `_validate(rolls)` that raises on bad input, called at the top of `score()` before any scoring logic runs.

(Reply with A or B, or ask a follow-up question.)

Tutor: **A** (inline) or **B** (separate `_validate`)?

### Student

I'll go with **B** — separate `_validate()` function.

My reasoning: validation is conceptually distinct from scoring. If I mix it into the loop with option A, the scoring logic gets harder to read and reason about. Plus, if validation fails early, I want to catch it *before* we start accumulating a score.

A separate function also makes it easier to test validation independently, and if the rules change later (or we need to add more checks), there's a clear place to put them.

Let's write the validator — what invalid cases should we check for? Invalid roll values (negative or over 10)? Frame totals exceeding 10 (except in the 10th)? Wrong number of rolls?

---

## Turn 4

### Tutor

Tutor: Good instincts — all three categories matter. The per-roll bounds (`< 0`, `> 10`) and frame totals are straightforward. The tricky one is detecting the wrong roll count, because it depends on the actual rolls (strikes collapse frames, 10th-frame bonus rolls are conditional). How should we check it?

OPTIONS:
[A] Range check on len(rolls)
A valid game has between 12 and 21 rolls, so just check:
```diff
+++ bowling.py
@@ -0,0 +1,3 @@
+def _validate(rolls):
+    if not (12 <= len(rolls) <= 21):
+        raise ValueError("wrong number of rolls")
```

[B] Walk frames, check exhaustion
Simulate the frame walk inside `_validate`. After consuming all 10 frames, check `i == len(rolls)` — too many or too few both raise.
```diff
+++ bowling.py
@@ -0,0 +1,4 @@
+def _validate(rolls):
+    i = _walk_frames(rolls)   # raises on bad pin counts too
+    if i != len(rolls):
+        raise ValueError("wrong number of rolls")
```

(Reply with A or B, or ask a follow-up question.)

Tutor: **A** or **B**?

### Student

I'll go with **B** — walk frames and check exhaustion.

Here's why: option A is a quick bounds check, but it's loose. A game could have 15 rolls but still be invalid if, say, someone rolled an 11 in frame 3. Option B actually simulates the frame consumption, so it catches *both* structural errors (wrong count) *and* logical errors (invalid pin counts) in one pass.

Also, if we're already walking through the frames to validate pin counts, we might as well verify that we've consumed *exactly* the right number of rolls at the end. It's more thorough and doesn't require separate logic.

Should we refactor the scoring loop into a helper like `_walk_frames()` so both `_validate()` and `score()` can use it? Or keep them separate for now?

---

## Turn 5

### Tutor

Tutor: Good question — worth pausing on before we write the code.

OPTIONS:
[A] Shared _walk_frames() helper
Extract the frame-walking into one function used by both `_validate()` and `score()`. No duplicated loop logic.

[B] Keep them separate
`_validate()` has its own walk (pin checks + exhaustion). `score()` keeps its own loop. ~10 lines of similar-but-not-identical code in two places.

(Reply with A or B, or ask a follow-up question.)

Tutor: **A** or **B** — keep them separate or share the walking logic?

### Student

I'll go with **A** — shared `_walk_frames()` helper.

My reasoning: if I keep them separate, I'm duplicating the frame-walking logic (the strike/spare/open frame detection, the index increments). That's a maintenance headache — if I find a bug in how frames are consumed, I'd have to fix it in two places.

A shared helper means one source of truth for "how do we walk through frames?" Then `_validate()` can use it to check the walk is exhaustive, and `score()` uses it to accumulate points. Both trust the same logic.

The only thing I need to be careful about: the helper should return the final index (or maybe the list of frame structures?), so both callers can do what they need with it.

Should we have `_walk_frames()` return just the final index, or should it yield/return frame data that both functions can use?

---

## Turn 6

### Tutor

Tutor: Good — you've talked yourself to the right place. Now the specific shape of `_walk_frames`:

OPTIONS:
[A] Yield frame score + next index
Generator yields `(frame_score, next_i)` per frame. `score()` sums the scores; `_validate()` checks the final `next_i == len(rolls)`.
```diff
+++ bowling.py
@@ -0,0 +1,5 @@
+# usage:
+# score():    sum(s for s, _ in _walk_frames(rolls))
+# validate(): _, i = last item; assert i == len(rolls)
+def _walk_frames(rolls):
+    # yields (frame_score, next_roll_index) for each frame
```

[B] Return only final index
Returns just `i` after consuming all 10 frames. `_validate()` checks `i == len(rolls)`, but `score()` still needs its own loop to accumulate totals.
```diff
+++ bowling.py
@@ -0,0 +1,3 @@
+def _walk_frames(rolls):
+    # returns final roll index after 10 frames
+    ...
```

(Reply with A or B, or ask a follow-up question.)

Tutor: **A** or **B**?

### Student

I'll go with **A** — yield frame score + next index.

Here's why: option B saves us the index check in validation, but we still have to duplicate the scoring logic in `score()`. With option A, `_walk_frames()` is a single source of truth for *both* how frames are consumed *and* how they're scored. `score()` just sums what the generator yields, and `_validate()` gets to verify the walk was exhaustive. No duplication.

Plus, a generator feels natural here — we're walking through frames one at a time, computing each one's score as we go. Very clean.

Let me write it out:

```python
def _walk_frames(rolls):
    """Yields (frame_score, next_roll_index) for each of 10 frames."""
    i = 0
    for frame in range(10):
        if frame < 9:
            # frames 1-9
            if rolls[i] == 10:  # strike
                score = 10 + rolls[i + 1] + rolls[i + 2]
                i += 1
            elif rolls[i] + rolls[i + 1] == 10:  # spare
                score = 10 + rolls[i + 2]
                i += 2
            else:  # open
                score = rolls[i] + rolls[i + 1]
                i += 2
        else:
            # frame 10: sum remaining
            score = sum(rolls[i:])
            i = len(rolls)
        yield (score, i)
```

Does that look right?

---

## Turn 7

### Tutor

Tutor: That looks correct. Let me trace through the perfect game to double-check: 12 strikes → frames 1–9 each yield `(30, i+1)`, frame 10 yields `sum([10,10,10])=30`, total = 300. ✓

One minor style note: `for frame in range(10)` with `if frame < 9` is a loop that knows its own index — that's a hint it could be `range(9)` + a separate block, but functionally it's fine. Let's keep it.

Now let's wire up `_validate()` and rewrite `score()` to use the generator. `_validate()` needs to check roll bounds, frame totals, and exhaustion. Let me write the complete file:

[Read(bowling.py)]
  1	def score(rolls):
  2	    total = 0
  3	    i = 0  # index into rolls list
  4	
  5	    for frame in range(9):
  6	        if rolls[i] == 10:          # strike
  7	            total += 10 + rolls[i + 1] + rolls[i + 2]
  8	            i += 1
  9	        elif rolls[i] + rolls[i + 1] == 10:  # spare
  10	            total += 10 + rolls[i + 2]
  11	            i += 2
  12	        else:                        # open frame
  … (8 more lines)

[Write(bowling.py)]
def _walk_frames(rolls):
    """Yields (frame_score, next_roll_index) for each of 10 frames."""
    i = 0
    for frame in range(10):
        if frame < 9:
            if rolls[i] == 10:                        # strike
                score = 10 + rolls[i + 1] + rolls[i + 2]
                i += 1
            elif rolls[i] + rolls[i + 1] == 10:       # spare
                score = 10 + rolls[i + 2]
                i += 2
            else:                                      # open
… (53 more lines)
  The file bowling.py has been updated successfully.

Tutor: Now let's run some tests to see if it holds up:

[Bash(cd "$(pwd)" && python3 -c "
from bowling import score

# Perfect game
assert score([10]*12) == 300, 'perfect game'

# All gutter balls
assert score([0]*20) == 0, 'gutter game'

# All spares + 5 bonus
assert score([5, 5] * 10 + [5]) == 150, 'all spares'

# One strike in frame 1, open rest
rolls = [10, 3, 6] + [3, 6] * 8 + [3, 6]
assert score(rolls) == 10+3+6 + 3+6 + 7*9 + 9, f'got {score(rolls)}'

# Spare in 10th earns bonus
assert score([0,0]*9 + [7, 3, 5]) == 15, 'spare in 10th'

# Strike in 10th earns two bonus
assert score([0,0]*9 + [10, 3, 4]) == 17, 'strike in 10th'

# Validation: negative roll
try:
    score([-1] + [0]*19)
    assert False, 'should raise'
except ValueError:
    pass

# Validation: too many pins in a frame
try:
    score([6, 5] + [0]*18)
    assert False, 'should raise'
except ValueError:
    pass

print('All tests passed.')
"
)]
  error: Exit code 1

Tutor: The bug is in my test, not the code. I accidentally wrote `[10, 3, 6] + [3, 6] * 8 + [3, 6]` — that double-counts frame 2 (the rolls after the strike are frame 2, not extra). Let me fix:

[Bash(python3 -c "
from bowling import score

# Perfect game
assert score([10]*12) == 300, 'perfect game'

# All gutter balls
assert score([0]*20) == 0, 'gutter game'

# All spares + 5 bonus
assert score([5, 5] * 10 + [5]) == 150, 'all spares'

# Strike in frame 1, open rest: 19 + 8*9 + 9 = 100
rolls = [10] + [3, 6] * 9
assert score(rolls) == 100, f'strike frame 1: got {score(rolls)}'

# Spare in 10th earns bonus
assert score([0,0]*9 + [7, 3, 5]) == 15, 'spare in 10th'

# Strike in 10th earns two bonus
assert score([0,0]*9 + [10, 3, 4]) == 17, 'strike in 10th'

# Validation: negative roll
try:
    score([-1] + [0]*19)
    assert False
except ValueError:
    pass

# Validation: too many pins in a frame
try:
    score([6, 5] + [0]*18)
    assert False
except ValueError:
    pass

# Validation: too many rolls (extra ball after open 10th)
try:
    score([0]*21)
    assert False
except ValueError:
    pass

# Validation: too few rolls
try:
    score([0]*19)
    assert False
except ValueError:
    pass

print('All tests passed.')
"
)]
  All tests passed.

Tutor: All green. Here's the final file:

[Read(bowling.py)]
  1	def _walk_frames(rolls):
  2	    """Yields (frame_score, next_roll_index) for each of 10 frames."""
  3	    i = 0
  4	    for frame in range(10):
  5	        if frame < 9:
  6	            if rolls[i] == 10:                        # strike
  7	                score = 10 + rolls[i + 1] + rolls[i + 2]
  8	                i += 1
  9	            elif rolls[i] + rolls[i + 1] == 10:       # spare
  10	                score = 10 + rolls[i + 2]
  11	                i += 2
  12	            else:                                      # open
  … (53 more lines)

Tutor: Clean separation of concerns — `score()` is now a one-liner body. A few things worth noting about the structure you landed on:

- **`_walk_frames` is a generator** — `score()` lazy-evaluates it with a genexp. For 10 frames that's trivial, but the pattern scales.
- **`_validate` uses `rolls[i:]` for the 10th frame** — same `sum(rolls[i:])` insight you applied to scoring now works for validation too.
- **The 10th-frame strike check `r[1] != 10 and r[1] + r[2] > 10`** handles the case where both bonus balls are strikes (valid) vs. a non-strike followed by too many pins (invalid).

Want to stress-test an edge case, or is there anything in the validation logic you want to revisit?

### Student

I think we're in good shape. The logic is solid, the tests are passing, and the code is clean. Let me just make sure I understand that 10th-frame validation check you mentioned:

`r[1] != 10 and r[1] + r[2] > 10` — this means: "if the second bonus roll isn't a strike (i.e., it's a regular roll), then the second and third rolls can't sum to more than 10." That makes sense because if you roll a non-strike, the next roll has to respect the 10-pin limit for that "mini-frame." But if you *do* roll a strike on the second bonus, you get a fresh set of 10 pins for the third roll.

I feel like I understand the problem now, the code works, and there's nothing left to do. We've covered strikes, spares, open frames, the weird 10th-frame rules, and validation. Perfect game scores 300, gutter game scores 0, and all the edge cases pass.

<done/>

---

**Run end:** done after 7 turn(s) in 281.9s
