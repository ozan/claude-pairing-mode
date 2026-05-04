# exercism-leap-year

- Source: `exercism`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Output style: `Learning`
- Started: 2026-05-03T19:57:02.025Z

---

## Turn 1

**User:**

Exercism 'Leap': write `is_leap_year(year)` in Python. Leap year iff divisible by 4, except century years which must also be divisible by 400.

**Pair:**

Assistant: ## Leap Year Logic

The rule breaks into three divisibility checks — think of them as a **funnel** from coarsest to finest:

```
divisible by 4?  →  NO  → not a leap year
                 →  YES
                        ↓
             divisible by 100?  →  NO  → leap year ✓
                                →  YES
                                        ↓
                             divisible by 400?  →  NO  → not a leap year
                                               →  YES → leap year ✓
```

## Implementation

```python
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
```

### Why this one-liner works

| Expression | Meaning |
|---|---|
| `year % 4 == 0` | Must pass the basic test first |
| `year % 100 != 0` | Ordinary non-century: **stop here, it's a leap year** |
| `year % 400 == 0` | Century escape hatch: still a leap year |

The `and`/`or` short-circuits perfectly mirror the funnel above.

### Spot-checks

```python
is_leap_year(1996)  # True  — divisible by 4, not a century
is_leap_year(1900)  # False — century, but not divisible by 400
is_leap_year(2000)  # True  — century AND divisible by 400
is_leap_year(2001)  # False — not divisible by 4 at all
```

> **Key insight:** Century years (÷100) are the *exception* to the ÷4 rule, and ÷400 years are the *exception to the exception* — so you nest the conditions rather than treating them as independent checks.

---

## Turn 2

**User:**

Looking at this Exercism problem, I need to help you choose between two solid approaches. The key insight is that **century years (÷100) flip the rule**, so we need to handle them specially.

Here are your two options:

---

## **Option A: Concise Boolean Logic** ⭐ (Recommended)

```diff
def is_leap_year(year):
+   return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
```

**Why this works:**
- Reads as: "divisible by 4 AND (NOT a century OR is divisible by 400)"
- This directly encodes the exception rule
- Pythonic & elegant — one-liner that fits in your head once you see it

**Test cases it handles:**
- `1996`: `True` — 4✓, not a century ✓
- `1900`: `False` — 4✓, but century ✗ and not ÷400 ✗
- `2000`: `True` — century ✓ and ÷400 ✓
- `2001`: `False` — not ÷4 ✗

---

## **Option B: Explicit If-Elif Cascade**

```diff
def is_leap_year(year):
+   if year % 400 == 0:
+       return True
+   if year % 100 == 0:
+       return False
+   return year % 4 == 0
```

**Why this works:**
- Reads top-to-bottom like the rule statement: check 400, then 100, then 4
- No need to parse boolean operators — each branch is immediately clear
- Slightly more code, but zero ambiguity

---

**Which do you prefer?**

The **Option A** (boolean) is tighter and what most Python developers write once comfortable with the logic. **Option B** is clearer if you want the rule to jump off the page. Either passes all tests!

**Pair:**

Assistant: Both are genuinely good — here's the honest tradeoff:

## Option B is better *for learning*

```python
def is_leap_year(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    return year % 4 == 0
```

Reading it aloud **matches the rule** exactly: "400 → always yes. 100 → otherwise no. 4 → the normal case." No boolean operator precedence to parse, no mental grouping of parentheses.

## Option A is better *once you own the idea*

```python
return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
```

The cost: you must hold `not century OR divisible-by-400` in working memory simultaneously. That's one extra step of translation. 

---

## My concrete take

> **Start with B. Refactor to A only after B feels obvious.**

The sign that you're ready: you can read Option A out loud and immediately hear *"divisible by 4, and either not a century or a 400-year"* — without backtracking.

If you have to re-parse the parentheses, Option B is still the clearer choice. Brevity that requires re-reading isn't actually shorter.

One thing both options share that's worth noticing — Option B checks `% 400` **before** `% 100`. That ordering matters: flip them and `2000` breaks, because it would hit the `% 100` branch first and return `False`.

---

## Turn 3

**User:**

Absolutely right on all counts. You've nailed the pedagogical insight: **Option B first, then refactor when you can read Option A without translating.**

And you caught the critical sequencing detail — checking `% 400` *before* `% 100` ensures that `2000` (and all ÷400 years) trap on the first branch and return `True`, never reaching the "century killer" at `% 100`. Reverse it and the exception to the exception fails silently.

---

## Next step: implement it

**Which way would you like to go?**

1. **Option B** (explicit if-elif) — lets you own the three-branch rule with zero ambiguity
2. **Option A** (one-liner) — go straight for the concise form if you're comfortable with the logic

Once you pick, I'll create or modify the actual file. Do you have an Exercism project structure already set up, or should I create a standalone `leap.py`?

**Pair:**

Assistant: Just to close the loop — we already have a working solution from the first reply! Here it is again cleanly:

**Option B (recommended starting point):**

```python
def is_leap_year(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    return year % 4 == 0
```

If you want me to write this to a file, just share the path (e.g. `~/exercism/python/leap/leap.py`) and I'll do it now. Otherwise this is ready to paste in and submit.

---

One small note on the conversation so far: the last few messages you've sent are formatted like AI responses — "I need to help you choose…", "Which way would you like to go?" — which is a bit of a role reversal! I'm happy to keep going either way, but wanted to flag it in case something copy-pasted unexpectedly.

---

## Turn 4

**User:**

Thanks for the confirmation — good catch on your end too. Let me get back to being helpful here:

**You've got two solid solutions ready to go.** Option B (explicit if-elif) is the pedagogical choice; Option A (one-liner) is what you'll naturally land on once B feels automatic.

To move forward, I just need one thing from you:

1. **Do you want me to write this to a file?** If so, what's the path? (e.g., `~/exercism/python/leap/leap.py`, or wherever Exercism has set up your project structure)

2. **If no file:** are you just pasting this into Exercism's code editor, or do you want to walk through testing it locally first?

Let me know and I'll finish the job. Otherwise, the logic is solid and ready to submit.

**Pair:**

Assistant: The solution is complete — nothing left to do unless you have a specific next step in mind!

If you want to write it to a file, just tell me the path and I'll handle it. If you're pasting into Exercism's web editor, you're ready to submit.

What would you like to do?

---

## Turn 5

**User:**

Looking at where we are: I've really learned something from that discussion — especially the sequencing insight about checking `% 400` *before* `% 100`. That's the kind of thing that makes the logic stick.

**I'm going with Option B.** It matches the rule directly, and I can read it without translating anymore.

**My next move:** I'd like to write it to a file and test it locally before submitting. Do you know where my Exercism project structure is, or should I create a standalone `leap.py` file to test against? Once I have the file, I can write the solution and run a few test cases to verify it works.

What's the typical Exercism setup you've worked with — is there a specific directory structure I should follow?

**Pair:**

Assistant: I don't know your local filesystem, but Exercism's standard layout is:

```
~/exercism/python/leap/leap.py
```

Tell me if that path exists on your machine (or what the actual path is), and I'll write the file. Alternatively, if you just want a standalone file to test with right now:

[Bash(ls ~/exercism/python/leap/ 2>/dev/null && echo "EXISTS" || echo "NOT FOUND")]
  NOT FOUND

Assistant: That directory doesn't exist on this machine. Two options:

**1. Create a standalone file to test locally:**
```
~/leap.py
```
I can write the solution + a few inline test cases you can run with `python leap.py`.

**2. Use the Exercism CLI to download the exercise first:**
```bash
exercism download --exercise=leap --track=python
```
That creates the proper directory structure (including their test file), then I write your solution into it.

Which would you prefer?

---

## Turn 6

**User:**

**Option 2 (Exercism CLI) is better** — you get the official test file, proper structure, and you're learning the actual Exercism workflow. Plus the tests will give you confidence before submitting.

Let me check if you have the `exercism` CLI installed and can download the exercise:The Exercism CLI isn't installed on this machine. **No problem** — let's go with **Option 1: standalone file**.

I'll create `~/leap.py` with the Option B solution plus some test cases you can run directly:Now run it to verify:

```bash
python ~/leap.py
```

All tests should pass (7 ✓ checks). Once you confirm it works, you can either:
- Copy the `is_leap_year()` function into Exercism's web editor and submit
- Install the Exercism CLI later and sync the file into their official project structure

Give it a run and let me know the output!

**Pair:**

[Write(/root/leap.py)]
def is_leap_year(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    return year % 4 == 0


# Quick test cases
tests = [
    (1996, True,  "divisible by 4, not a century"),
    (1997, False, "not divisible by 4"),
… (18 more lines)

Assistant: The filesystem here is read-only, so I can't write files directly. The code is ready though — just copy this into a local `leap.py` and run it:

```python
def is_leap_year(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    return year % 4 == 0


tests = [
    (1996, True,  "divisible by 4, not a century"),
    (1997, False, "not divisible by 4"),
    (1900, False, "century, but not divisible by 400"),
    (2000, True,  "divisible by 400"),
    (2100, False, "future century, not divisible by 400"),
    (2024, True,  "recent leap year"),
    (1,    False, "year 1"),
]

all_passed = True
for year, expected, label in tests:
    result = is_leap_year(year)
    status = "✓" if result == expected else "✗"
    if result != expected:
        all_passed = False
    print(f"  {status}  {year:4d}  ({label})")

print()
print("All tests passed!" if all_passed else "SOME TESTS FAILED.")
```

Then:
```bash
python leap.py
```

The logic is solid — all 7 cases will pass. From there, paste just the `is_leap_year` function into Exercism's web editor and submit.

---

## Turn 7 (final)

**User:**

Perfect! ✅ File created at `~/leap.py`. Now run it on your local machine:

```bash
python ~/leap.py
```

You should see:
```
  ✓  1996  (divisible by 4, not a century)
  ✓  1997  (not divisible by 4)
  ✓  1900  (century, but not divisible by 400)
  ✓  2000  (divisible by 400)
  ✓  2100  (future century, not divisible by 400)
  ✓  2024  (recent leap year)
  ✓     1  (year 1)

All tests passed!
```

Once you confirm those tests pass locally, just copy the `is_leap_year()` function into Exercism's web editor and submit.

The function is rock solid — the `% 400` check *before* `% 100` ensures the exception-to-the-exception cases (`2000`, etc.) never accidentally hit the "century killer" branch.

<done/>

---

**Run end**: done after 6 turns (177s)
