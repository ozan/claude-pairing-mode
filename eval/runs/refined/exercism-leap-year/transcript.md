# exercism-leap-year

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:40:25

## Initial prompt

Exercism 'Leap': write `is_leap_year(year)` in Python. Leap year iff divisible by 4, except century years which must also be divisible by 400.

---

## Turn 1

### Tutor

Thinking: The user wants to write a `is_leap_year(year)` function in Python for the Exercism "Leap" exercise. This is a classic problem with an interesting implementation choice worth exploring.
  
  Let me think about the options:
  
  The rule is:
  - Divisible by 4 → leap year
  - EXCEPT century years (divisible by 100) → NOT a leap year
  - UNLESS also divisible by 400 → IS a leap year
  
  So: `year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)`
  
  There's also the option of using Python's `calendar.isleap()`, but that's cheating for an exercise.
  
  
  I'm considering two logically equivalent approaches with different short-circuit behavior. Option A checks divisibility by 400 first, which fails quickly for most years, then checks divisibility by 4. Option B reverses this, checking divisibility by 4 first, which also eliminates most non-leap years early on.
  
  While both are O(1) operations with negligible performance differences, Option B aligns better with the problem's natural logic flow: first checking the base leap year rule (divisible by 4), then handling the century exceptions (divisible by 100 but not 400).

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

Thinking: Now let me propose the two options for the implementation of `is_leap_year`. I'll present two logically equivalent but structurally different boolean expressions.
  
  Option A: Check divisibility by 4 first (most years aren't divisible by 4, so this short-circuits early for ~75% of years)
  `return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)`
  
  Option B: Check divisibility by 400 first
  `return year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)`
  
  
  Both approaches are logically correct, but Option A has a performance advantage since the majority of years fail the initial divisibility-by-4 check and exit immediately, whereas Option B's divisibility-by-400 check fails for nearly all years before falling through to the more complex compound condition. 100` != 0 passes → 2 checks
  - For century non-leap years (~0.75%): `% 4` passes, `% 100` == 0 fails first part, `% 400` != 0 → 3 checks
  - For years divisible by 400 (~0.25%): `% 4` passes, `% 100` == 0 fails first part, `% 400` == 0 passes → 3 checks
  
  Option A wins on average since three-quarters of years short-circuit after just one check, though honestly the performance difference is negligible since both approaches are constant time. The real value here is showing how the boolean logic structure affects efficiency.
  
  I'll go with Option A as my recommendation since checking divisibility by 4 first makes the most pedagogical sense.

Tutor: Both these one-liners are logically correct — which would you prefer?

OPTIONS:
[A] 400-first order
```diff
+++ leap.py
@@ -0,0 +1,2 @@
+def is_leap_year(year):
+    return year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)
```

[B] 4-first order
```diff
+++ leap.py
@@ -0,0 +1,2 @@
+def is_leap_year(year):
+    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
```

(Reply with A or B, or ask a follow-up question.)

PRIVATE: best=B
PRIVATE: rationale=Option B checks % 4 first, which eliminates ~75% of all years in a single modulo — Python short-circuits `and`, so those years never reach the century checks. Option A checks % 400 first, which only fires for 1-in-400 years, meaning almost every call falls through to the full compound check. Both are O(1) and the real-world difference is tiny, but B mirrors the natural reading of the rule ("must be divisible by 4, and then...") and is marginally more efficient due to short-circuit evaluation order.

Tutor: Which feels right to you?

### Student

I need to think through both of these carefully.

Let me trace through a few test cases mentally:

**Option A** (400-first): `year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)`
- Year 2000: 2000 % 400 == 0 → True ✓
- Year 1900: 1900 % 400 != 0, then check (1900 % 4 == 0 and 1900 % 100 != 0) → (True and False) → False ✓
- Year 2004: 2004 % 400 != 0, then check (2004 % 4 == 0 and 2004 % 100 != 0) → (True and True) → True ✓

**Option B** (4-first): `year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)`
- Year 2000: 2000 % 4 == 0 and (2000 % 100 != 0 or 2000 % 400 == 0) → True and (False or True) → True ✓
- Year 1900: 1900 % 4 == 0 and (1900 % 100 != 0 or 1900 % 400 == 0) → True and (False or False) → False ✓
- Year 2004: 2004 % 4 == 0 and (2004 % 100 != 0 or 2004 % 400 == 0) → True and (True or False) → True ✓

Both work logically. But **I'd pick Option B** because it feels more intuitive to me: "divisible by 4, *except* when divisible by 100, *unless* also divisible by 400." It reads left-to-right in the order the rules are stated in the problem. Option A feels like it's checking the exception first, which is less natural to my brain.

---

## Turn 2

### Tutor

Thinking: The user picked Option B, which is my best recommendation. I should express brief agreement and apply the changes.

Tutor: Exactly right — and that's the stronger reason to prefer it over the performance angle. The `% 4` check also happens to short-circuit away ~75% of years immediately, but the readability argument stands on its own.

Let me write the file:

[Write(leap.py)]
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

  File created successfully at: leap.py

Tutor: Done. One line, three modulo checks, mirrors the rule statement exactly.

Your trace was thorough — you hit all the interesting cases: the 400-year exception (2000), the plain century non-leap (1900), and a regular leap (2004). The only other edge worth knowing: year 1 is not a leap year, and this handles it correctly since `1 % 4 != 0`.

### Student

Thanks! That's really helpful. I appreciate you pointing out that year 1 case — it's good to know the logic handles those edge cases naturally without needing special handling.

I feel like I've got a solid understanding now: the rule itself tells you the structure of the condition, and Option B just translates it directly into code. That's a much better principle than trying to optimize prematurely or pick the "cleverest" version.

<done/>

---

**Run end:** done after 2 turn(s) in 45.6s
