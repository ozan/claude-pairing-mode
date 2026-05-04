# exercism-leap-year

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:40:25

## Initial prompt

Exercism 'Leap': write `is_leap_year(year)` in Python. Leap year iff divisible by 4, except century years which must also be divisible by 400.

---

## Turn 1

### Tutor

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

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
