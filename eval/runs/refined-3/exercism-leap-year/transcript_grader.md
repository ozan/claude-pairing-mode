# exercism-leap-year

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-05T07:51:22

## Initial prompt

Exercism 'Leap': write `is_leap_year(year)` in Python. Leap year iff divisible by 4, except century years which must also be divisible by 400.

---

## Turn 1

### Tutor

Tutor: Good Exercism problem — the logic is simple but the ordering has an interesting wrinkle. Before I write anything, let me ask:

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Check 400 first
```diff
+++ leap.py
@@ -0,0 +1,2 @@
+def is_leap_year(year):
+    return year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)
```

[B] Check 4 first
```diff
+++ leap.py
@@ -0,0 +1,2 @@
+def is_leap_year(year):
+    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
```

(Reply with A or B, or ask a follow-up question.)

Tutor: Which ordering do you prefer — and does the order even matter here?

### Student

Good question! Let me think through this...

Both should give the same answer, right? Since the logic is equivalent — just written in different orders. Let me trace through a couple cases mentally:

- Year 2000 (divisible by 400): Both return True ✓
- Year 1900 (divisible by 100 but not 400): Both return False ✓
- Year 2004 (divisible by 4 but not 100): Both return True ✓
- Year 2001 (not divisible by 4): Both return False ✓

So functionally they're the same. But efficiency-wise... option [B] checks `year % 4 == 0` first, which will be false most of the time (75% of years aren't leap years), so it short-circuits early. Option [A] always checks the more expensive `year % 400 == 0` first.

I'd go with **[B]** — it's more efficient because it eliminates most non-leap-years immediately with the divisible-by-4 check.

Does that reasoning make sense?

---

## Turn 2

### Tutor

Tutor: Exactly right. You nailed the short-circuit argument — `% 4` filters out 75% of years in one cheap check. For modulo arithmetic the wall-clock difference is noise, but the *habit* of ordering conditions by elimination power pays off when conditions are expensive (DB queries, regex, I/O).

[Write(leap.py)]
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

  File created successfully at: leap.py

Tutor: Done. One line, three modulo checks, correct for all four cases you traced. 

The rule reads almost like prose: *"divisible by 4, and either not a century year or divisible by 400."* That's the spec translated directly — no branching, no edge-case special cases scattered across `if`/`elif`. Worth noticing that keeping the logic in a single boolean expression also makes it trivially testable: you can fuzz it against a table of known leap years without worrying about which branch you're hitting.

### Student

That's really helpful context. I see what you mean — keeping it as one expression makes the logic transparent and testable. I can see how that's better than something like:

```python
if year % 400 == 0:
    return True
if year % 100 == 0:
    return False
if year % 4 == 0:
    return True
return False
```

Even though that would work, it's scattered across multiple branches and harder to verify at a glance.

I appreciate you pointing out the short-circuit ordering too — that's a pattern I'll try to remember when writing conditions. Check the cheap/likely-to-fail thing first, so you don't waste cycles on expensive checks.

The solution makes sense and I feel confident about it. Let me verify once more against the spec:
- Divisible by 4 → leap (unless century)
- Century year divisible by 400 → leap
- Everything else → not leap

Yep, the expression covers all three cases. 

<done/>

---

**Run end:** done after 2 turn(s) in 43.2s
