# exercism-leap-year

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:00:32

## Initial prompt

Exercism 'Leap': write `is_leap_year(year)` in Python. Leap year iff divisible by 4, except century years which must also be divisible by 400.

---

## Turn 1

### Tutor

Thinking: The user wants to implement a `is_leap_year(year)` function in Python for the Exercism Leap exercise. Let me think about this and present two options - one correct and one with a subtle issue.
  
  The correct logic for leap year:
  - Divisible by 400 → leap year
  - Divisible by 100 (but not 400) → not a leap year
  - Divisible by 4 → leap year
  - Otherwise → not a leap year
  
  This can be expressed as:
  ```python
  return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
  
  
  ```
  
  Or equivalently:
  ```python
  return year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)
  ```
  
  A tempting alternative that looks wrong at first glance is actually correct due to Python's operator precedence - `and` binds tighter than `or`, so the expression naturally groups into the right logic.
  
  Let me work through some genuinely tricky variations to find a subtle bug...
  
  Testing different formulations... I found a genuinely wrong implementation: the condition for century years is inverted. When I test year 100, it incorrectly returns True because the divisibility-by-4 check passes, even though 100 isn't a leap year since it's not divisible by 400. The logic fails to properly exclude non-400-divisible century years. I see the issue now - century years that are divisible by 4 but not 400 still aren't leap years, and Option B fails to exclude them properly. Now I'm going to propose some alternative implementations to illustrate this distinction more clearly.

Tutor: Let me first load the options tool, then present this as a teaching moment — there's a classic trap here.

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Thinking: Now let me present the two options. I'll create the file with the `is_leap_year` function. Let me present two options:
  
  Option A (subtly wrong): 
  ```python
  return (year % 100 == 0 and year % 400 == 0) or year % 4 == 0
  ```
  This looks like it directly encodes the rules but is wrong because all century years are also divisible by 4, so the `year % 4 == 0` clause catches century non-leap years too.
  
  
  Option B (correct):
  ```python
  return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
  ```
  
  I'll randomize which is which - let me put the wrong one as A and correct as B, so best_letter is B.

Tutor: Which logic correctly implements the rule?

OPTIONS:
[A] Positive century check
```diff
+++ leap.py
@@ -0,0 +1,2 @@
+def is_leap_year(year):
+    return (year % 100 == 0 and year % 400 == 0) or year % 4 == 0
```

[B] Negative century check
```diff
+++ leap.py
@@ -0,0 +1,2 @@
+def is_leap_year(year):
+    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
```

(Reply with A or B, or ask a follow-up question.)

PRIVATE: best=B
PRIVATE: rationale=Option A looks like it directly encodes "century years divisible by 400 are leap years, OR divisible by 4 is a leap year." The trap: every century year (100, 200, 300...) is also divisible by 4, so the `year % 4 == 0` clause is always True for them — it overrides the century exclusion. year=100 returns True, which is wrong. Option B is correct: start with "must be div by 4", then the century exception gates out 100, 200, 300 etc., but lets 400 back through.

Tutor: Which do you prefer?

### Student

I need to think through this carefully because I want to make sure I understand the logic, not just guess.

Let me trace through both with some test cases:

**Option A:** `(year % 100 == 0 and year % 400 == 0) or year % 4 == 0`

- Year 2000 (century, divisible by 400): `(True and True) or True` = True ✓
- Year 1900 (century, NOT divisible by 400): `(True and False) or False` = False ✓
- Year 2004 (divisible by 4, not century): `(False and ...) or True` = True ✓
- Year 2001 (not divisible by 4): `(False and ...) or False` = False ✓

**Option B:** `year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)`

- Year 2000: `True and (False or True)` = True ✓
- Year 1900: `False and (True or False)` = False ✓
- Year 2004: `True and (True or ...)` = True ✓
- Year 2001: `False and (...)` = False ✓

They both seem to work on these cases... but I'm worried Option A has a subtle bug. Let me check year 2100:

- Option A: `(True and False) or False` = False ✓
- Option B: `False and (...)` = False ✓

Hmm, both still work. But reading Option A more carefully, the `or year % 4 == 0` at the end feels dangerous—it means any year divisible by 4 will return True, even if we already handled the century exception. 

I think **Option B** is better because it explicitly requires divisibility by 4 *first*, and then adds the century exception as a refinement. That feels like it's following the rule more directly: "divisible by 4, except century years which must be divisible by 400."

My answer is **B**.

---

## Turn 2

### Tutor

Thinking: The user traced through carefully and got it right. Let me confirm their analysis with a specific counterexample for Option A that they missed - year 100, 200, 300 (wait, they did check 1900 and 2100, both of which are divisible by 100 but not 400, and both got False correctly from both options).
  
  Wait, let me re-trace Option A with year 1900:
  
  
  Actually, I need to recalculate this. 1900 is divisible by 4 (1900 = 4 × 475), so when I evaluate the condition, the second part `1900 % 4 == 0` returns True, making the entire expression `False or True` evaluate to True. But the user said Option A returns False for 1900, which means they made an arithmetic error - 1900 is actually divisible by 4, so Option A would incorrectly return True when it should return False.

Tutor: Correct — and your intuition nailed it. But there's actually a bug hiding in your Option A trace that would have caught it red-handed. Look again at year **1900**:

```
Option A: (1900 % 100 == 0 and 1900 % 400 == 0) or 1900 % 4 == 0
           (True           and False            ) or True   ← 1900 ÷ 4 = 475 exactly!
         = False or True = True  ✗
```

1900 is divisible by 4, so Option A returns `True` — but 1900 was **not** a leap year. The `or year % 4 == 0` at the end undoes all the century logic, because every century year is also divisible by 4.

Your read of Option B is exactly right: it enforces divisibility-by-4 as the *gate*, then uses the century check as a refinement:

> "must be div by 4 — *and* (not a century year, *or* a 400-year)"

Writing it out now:

[Write(leap.py)]
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

  File created successfully at: leap.py

Tutor: Done. The key takeaway: when you see `A or B`, always ask "can B be true even when A is false?" Here, the century guard in the first clause is completely bypassed by the `year % 4 == 0` fallback — a classic short-circuit logic trap.

### Student

Oh wow, thank you for catching that! I actually *did* make the mistake in my trace—I wrote "False ✓" for 1900 under Option A when I should have computed it all the way through. Since 1900 *is* divisible by 4, that final `or year % 4 == 0` makes the whole thing True, which is wrong. I got lucky guessing B was better, but I didn't actually verify carefully enough.

That's a really helpful lesson: I need to trace through the *entire* expression, not stop early just because one part looks right. And your point about the `or` creating a bypass is spot-on—I can see now how that structure lets the century rule get trampled by the simpler divisible-by-4 check.

So the key insight with Option B is that it treats divisibility-by-4 as a necessary condition first (`year % 4 == 0 and ...`), which means century years have to pass through that gate. Then the second part refines it: "unless it's a century year, *or* it's divisible by 400."

I understand the logic now and why B is correct. Thanks for walking me through that—definitely going to be more careful about tracing all the way through boolean expressions from now on.

<done/>

---

**Run end:** done after 2 turn(s) in 57.4s
