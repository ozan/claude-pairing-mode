# exercism-hamming

- Source: `exercism`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T02:51:52.555Z

---

## Turn 1

**User:**

Exercism 'Hamming': write `distance(a, b)` returning the number of positions at which two equal-length DNA strands differ. Raise on length mismatch.

**Pair:**

Thinking: The user wants to solve the Exercism 'Hamming' problem - implementing a `distance(a, b)` function that calculates the Hamming distance between two DNA strands. Let me think about this and present a good teaching opportunity.
  
  Let me think about what options would be instructive here. The core of this problem is comparing characters at each position. There are a few approaches:
  
  1. Using `zip` with a generator expression: `sum(c1 != c2 for c1, c2 in zip(a, b))`
  2. Using `enumerate` and indexing: `sum(1 for i, c in enumerate(a) if b[i] != c)`
  
  
  The `zip` approach is more Pythonic and cleaner, but there's an important edge case: `zip` silently truncates to the shorter sequence, so I need to validate that both strands have equal length before comparing them. The key teaching moment here is deciding between the elegant `zip` approach versus other iteration methods, and making sure to handle the length validation upfront.
  
  Writing the solution... I'm realizing the key pedagogical issue here: using `zip` without an explicit length check silently truncates mismatched strings, which is a subtle trap that beginners often miss. The most instructive approach would be to show a correct implementation that validates equal lengths upfront, then contrasts it with what happens when you rely on `zip` alone. I see the bug now—when `b` is longer than `a`, `zip` silently truncates to match `a`'s length, so the length check passes even though the strands are actually mismatched. This would return 0 instead of raising an error, which is a real problem. Let me structure this as a teaching example by showing both approaches side by side.

Assistant: Good Exercism problem — there's a neat Pythonic trick here worth thinking about. Quick question before I write it:

OPTIONS:
[A] zip + length check
```diff
+++ hamming.py
@@ -0,0 +1,6 @@
+def distance(a, b):
+    pairs = list(zip(a, b))
+    if len(pairs) != len(a):
+        raise ValueError("Strands must be of equal length")
+    return sum(c1 != c2 for c1, c2 in pairs)
```

[B] explicit len + zip
```diff
+++ hamming.py
@@ -0,0 +1,6 @@
+def distance(a, b):
+    if len(a) != len(b):
+        raise ValueError("Strands must be of equal length")
+    return sum(c1 != c2 for c1, c2 in zip(a, b))
```

(Reply with A or B, or ask a follow-up question.)

Thinking: The tool isn't available. Let me just implement the solution directly.

Assistant: Quick question before I write it — which of these two approaches do you prefer?

**Option A — zip + length check via pairs:**
```python
def distance(a, b):
    pairs = list(zip(a, b))
    if len(pairs) != len(a):
        raise ValueError("Strands must be of equal length")
    return sum(c1 != c2 for c1, c2 in pairs)
```

**Option B — explicit `len` check upfront:**
```python
def distance(a, b):
    if len(a) != len(b):
        raise ValueError("Strands must be of equal length")
    return sum(c1 != c2 for c1, c2 in zip(a, b))
```

Both use `zip` for iteration — but there's a subtle correctness difference. Which would you pick?

---

## Turn 2

**User:**

I need help with the Exercism Hamming problem. I understand the requirements — count differences between two DNA strands, raise an error if they're different lengths — but I'm not sure about the cleanest way to check the length condition alongside the comparison.

Should I validate lengths upfront with a simple `len()` check, or use `zip` and infer the length from the pairs it produces? I know `zip` truncates silently, which seems risky, but I want to understand the tradeoff.

What would you suggest?

**Pair:**

Thinking: The user is asking about the two approaches I was presenting. They've already articulated the tradeoff well - they know zip truncates silently. Let me explain the bug in Option A clearly and recommend Option B, then implement it.
  
  The key insight: Option A has a real bug. `zip("AC", "ACG")` produces `[('A','A'), ('C','C')]` - length 2 - and `len(a)` is also 2, so the check passes silently. It only catches the case where `b` is *shorter* than `a`, not when `b` is *longer*.
  
  
  Now I'll write out the solution with Option B, which properly handles both directions.

Assistant: You've already spotted the key issue. The `zip`-based check has a real bug — it only catches mismatches in *one direction*.

Try it mentally: `a = "AC"`, `b = "ACG"`. `zip` produces `[('A','A'), ('C','C')]` — length 2. And `len(a)` is also 2. The check passes silently, you get `0` back, no error raised. It only fires when `b` is *shorter* than `a`.

Upfront `len()` check is unambiguously correct and clearer to read. Here's the full implementation:

[Glob(hamming.py)]
  No files found

[Write(hamming.py)]
def distance(a, b):
    if len(a) != len(b):
        raise ValueError("Strands must be of equal length")
    return sum(c1 != c2 for c1, c2 in zip(a, b))


Assistant: A couple of things worth noting:

- **`sum()` over booleans** — `c1 != c2` yields `True`/`False`, and Python bools are ints (`True == 1`), so `sum()` just counts the mismatches. Clean and idiomatic.
- **`zip` is safe here** — because by the time we reach it, we've already guaranteed equal lengths, so its truncation behaviour is a non-issue.

The general lesson: don't try to infer a precondition from a side-effect of a data structure (like zip's output length) when you can just check the precondition directly. It's clearer and avoids subtle asymmetry bugs like the one above.

---

## Turn 3 (final)

**User:**

Got it — that's a really clear explanation. I see the bug now: `zip` only catches the mismatch when `b` is *shorter*, not when it's *longer*. Checking lengths upfront is way simpler and removes that asymmetry.

And I like the lesson about not inferring preconditions from side effects. That's a good habit to build.

The implementation looks right to me — `sum(c1 != c2 for c1, c2 in zip(a, b))` is elegant once the lengths are guaranteed equal. Let me make sure this passes the test cases mentally:

- `distance("AG", "CT")` → lengths match, compare pairs → 2 (both differ) ✓
- `distance("AG", "ACG")` → `len(2) != len(3)` → raises ✓  
- `distance("", "")` → lengths match, no pairs → 0 ✓

Thanks for breaking down the subtle bug — that's exactly the kind of thing I'd miss if I tried to be too clever with `zip`.

<done/>

---

**Run end**: done after 2 turns (67s)
