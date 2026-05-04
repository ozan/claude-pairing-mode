# exercism-bowling

- Source: `exercism`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:39:24.467Z

---

## Turn 1

**User:**

Exercism 'Bowling': implement a 10-pin bowling scorer. Track frames, handle strikes (next two rolls bonus), spares (next roll bonus), and the special 10th-frame bonus rolls. Return the final score from a list of rolls.

**Pair:**

Assistant: Bowling is a great exercise — the 10th frame is where most implementations get tangled. I'll use Python. Let me start with the most consequential design decision.

OPTIONS:
[A] Roll-index loop
```diff
+++ bowling.py
@@ -0,0 +1,12 @@
+def score(rolls):
+    total = 0
+    i = 0
+    for frame in range(10):
+        if rolls[i] == 10:          # strike
+            total += 10 + rolls[i+1] + rolls[i+2]
+            i += 1
+        elif rolls[i] + rolls[i+1] == 10:  # spare
+            total += 10 + rolls[i+2]
+            i += 2
+        else:
+            total += rolls[i] + rolls[i+1]
+            i += 2
+    return total
```

[B] Build-frames-first
```diff
+++ bowling.py
@@ -0,0 +1,16 @@
+def score(rolls):
+    frames, i = [], 0
+    for _ in range(9):             # first 9 frames
+        if rolls[i] == 10:
+            frames.append(rolls[i:i+3])
+            i += 1
+        else:
+            frames.append(rolls[i:i+2])
+            i += 2
+    frames.append(rolls[i:i+3])    # 10th frame (up to 3 rolls)
+    total = 0
+    for f in frames:
+        total += sum(f)
+    return total
```

(Reply with A or B, or ask a follow-up question.)

Assistant: Which structure do you want to build on — **A** or **B**?

---

## Turn 2

**User:**

I'll go with **B** — build-frames-first.

Here's my reasoning: the 10th frame is fundamentally different from frames 1–9 (no bonuses *beyond* it), so separating frame construction from scoring keeps that difference explicit. Option A's roll-index loop tempts you to treat all 10 frames the same way, which is where the 10th-frame bugs hide.

That said, I notice Option B's scoring logic is incomplete — it just sums each frame's raw rolls, but `score()` needs to account for bonuses (next 2 rolls for a strike, next 1 for a spare). Should we build on that structure now and add the scoring pass that does the lookahead?

**Pair:**

Assistant: Your reasoning about explicitness is fair — but I want to push back gently on one thing: option A handles the 10th frame *correctly without special-casing it* precisely because the bonus rolls for a strike/spare in frame 9 naturally "spill into" frame 10's rolls. That's the insight, not a hidden bug. Anyway — you spotted the real flaw, so let's fix it.

Here's a subtlety worth thinking about. The bug is in frame *construction*, not scoring. The scoring pass is `sum(f)` — that's fine if the slices are right. The question is where to put the fix:

OPTIONS:
[A] Fix slice at construction
```diff
+++ bowling.py
@@ -4,7 +4,9 @@
     for _ in range(9):
         if rolls[i] == 10:
             frames.append(rolls[i:i+3])
             i += 1
+        elif rolls[i] + rolls[i+1] == 10:  # spare
+            frames.append(rolls[i:i+3])    # include bonus roll
+            i += 2
         else:
-            frames.append(rolls[i:i+2])
+            frames.append(rolls[i:i+2])
             i += 2
```

Scoring stays `sum(sum(f) for f in frames)`.

[B] Separate scoring pass
```diff
+++ bowling.py
@@ -11,5 +11,10 @@
     frames.append(rolls[i:i+3])    # 10th frame
-    total = 0
-    for f in frames:
-        total += sum(f)
-    return total
+    total, j = 0, 0
+    for k, f in enumerate(frames[:9]):
+        if f[0] == 10:            total += 10 + rolls[j+1] + rolls[j+2]; j+=1
+        elif sum(f) == 10:        total += 10 + rolls[j+2]; j+=2
+        else:                     total += sum(f); j+=2
+    total += sum(frames[9])
+    return total
```

(Reply with A or B, or ask a follow-up question.)

Assistant: **A** or **B**?

---

## Turn 3 (final)

**User:**

I'll go with **A** — fix slice at construction.

Here's my reasoning: once the frame slices are built correctly (even with their "overlap" for bonus rolls), the scoring becomes trivial — just `sum(sum(f) for f in frames)`. And trivial code is harder to get wrong.

Option B requires maintaining two indices in parallel (`k` for frames, `j` for rolls), and increments to both need to stay in sync. That's the classic source of off-by-one errors. The bonus logic is explicit, which is educational, but the parallel indexing introduces fragility.

Option A's overlapping slices might look odd at first — the same roll appears in two frames' slices — but that's actually *correct for bowling*. A roll serves as a bonus for one frame and a base roll for the next. By including all three rolls (strike + 2 bonuses) in the frame's slice, we're baking in the scoring rule, and the `sum()` at the end just works.

Let me apply Option A and add validation to catch invalid input:Let me check the working directory and navigate to the bowling problem:Let me create the bowling problem from scratch:Now let me write the solution with Option A:Now let's test it with some bowling scenarios:Perfect! All tests pass. Let me trace through one more complex scenario to show how the overlapping slices work correctly:Excellent trace! Notice how the overlapping works correctly:

- **Frame 1** (strike): `[10, 3, 7]` = 20 (strike + 2 bonus rolls from the next frame)
- **Frame 2** (spare): `[3, 7, 5]` = 15 (the 3 and 7 form the spare, 5 is the bonus)
- **Frame 3** (open): `[5, 0]` = 5 (no bonus)
- Rest are zeros

Rolls `[3, 7]` appear in *both* Frame 1 and Frame 2's slices — but that's correct! They're the "bonus rolls" for Frame 1 and the "base rolls" for Frame 2. By summing all frames, each roll contributes to the right frames according to bowling rules.

The beauty of Option A: once the frame slices are built correctly, the scoring is just `sum(sum(f) for f in frames)` — trivial code that can't hide bugs.

<done/>

---

**Run end**: done after 2 turns (170s)
