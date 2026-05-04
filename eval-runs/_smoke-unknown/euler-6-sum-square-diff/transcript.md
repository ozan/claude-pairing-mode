# euler-6-sum-square-diff

- Source: `project-euler`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T03:51:40.403Z

---

## Turn 1

**User:**

Project Euler #6: find the difference between the square of the sum and the sum of the squares of the first 100 natural numbers.

**Pair:**

Thinking: The user wants to solve Project Euler Problem #6. Let me think about this:
  
  - Sum of squares: 1² + 2² + ... + 100²
  - Square of sum: (1 + 2 + ... + 100)²
  - Find the difference: (sum)² - (sum of squares)
  
  There are two approaches:
  1. Brute force: compute both with loops
  2. Use mathematical formulas:
     - Sum of first n natural numbers: n(n+1)/2
     - Sum of squares: n(n+1)(2n+1)/6
  
  The mathematical formula approach is O(1) vs O(n) for the loop approach. 
  
  I'll present both solutions to show the contrast between a straightforward iterative approach and an elegant mathematical one, then let the user choose which direction they'd prefer to explore.

Assistant: Good classic problem. Before writing any code — which approach do you want to take?

OPTIONS:
[A] Loop it out
```diff
+++ euler6.py
@@ -0,0 +1,6 @@
+n = 100
+sum_of_squares = sum(i*i for i in range(1, n+1))
+square_of_sum = sum(range(1, n+1)) ** 2
+print(square_of_sum - sum_of_squares)
```

[B] Closed-form formulas
```diff
+++ euler6.py
@@ -0,0 +1,6 @@
+n = 100
+square_of_sum = (n * (n + 1) // 2) ** 2
+sum_of_squares = n * (n + 1) * (2*n + 1) // 6
+print(square_of_sum - sum_of_squares)
```
Uses Σk = n(n+1)/2 and Σk² = n(n+1)(2n+1)/6.

(Reply with A or B, or ask a follow-up question.)

Thinking: The tool isn't available. Let me just proceed with the implementation. I'll present the two options as text and ask the user.

Assistant: Let me present two approaches:

**Option A — Loop it out:**
```python
n = 100
sum_of_squares = sum(i*i for i in range(1, n+1))
square_of_sum = sum(range(1, n+1)) ** 2
print(square_of_sum - sum_of_squares)
```

**Option B — Closed-form formulas:**
```python
n = 100
square_of_sum = (n * (n + 1) // 2) ** 2
sum_of_squares = n * (n + 1) * (2*n + 1) // 6
print(square_of_sum - sum_of_squares)
```
Uses `Σk = n(n+1)/2` and `Σk² = n(n+1)(2n+1)/6`.

Which do you prefer?

---

## Turn 2

**User:**

I think I'll go with **Option B** — the formulas approach. Option A is straightforward enough that I can write it myself pretty easily, but I'm curious about those summation formulas. I've seen `Σk = n(n+1)/2` before but never really *used* it in code. 

Can you go ahead with Option B and maybe walk me through why those formulas work as we implement? That way I'll actually build some intuition for them instead of just copy-pasting.

**Pair:**

Thinking: The user wants to go with Option B (closed-form formulas) and wants to understand why the formulas work. Let me write the file and explain the intuition behind both formulas.
  
  Let me first check if the file exists.

Assistant: Great choice. Let me write the file, then walk through both formulas.

[Glob(euler6.py)]
  No files found

[Write(euler6.py)]
n = 100
square_of_sum = (n * (n + 1) // 2) ** 2
sum_of_squares = n * (n + 1) * (2*n + 1) // 6
print(square_of_sum - sum_of_squares)


[Bash(python euler6.py)]
  error: Exit code 127

[Bash(python3 euler6.py)]
  25164150

Assistant: **25,164,150** ✓ (matches the known answer.)

---

### Why `Σk = n(n+1)/2`

This one has a beautiful proof attributed to Gauss (as a schoolboy). Write the sum forwards and backwards, then add them together:

```
  1  +  2  +  3  + ... + 100
100  + 99  + 98  + ... +   1
─────────────────────────────
101  + 101 + 101 + ... + 101   ← 100 pairs, each summing to 101
```

So `2 × sum = 100 × 101`, meaning `sum = 100 × 101 / 2 = 5050`. In general: `n(n+1)/2`.

In code: `n * (n + 1) // 2` — the `//` is just integer division since one of `n` or `n+1` is always even.

---

### Why `Σk² = n(n+1)(2n+1)/6`

This one is less obvious. One way to see it: imagine you're building a 3D staircase of unit cubes — layer 1 has 1 cube, layer 2 has 4, layer 3 has 9, etc. You can pack *six* such staircases together to exactly fill an `n × (n+1) × (2n+1)` rectangular box. That's the geometric proof.

A more algebraic intuition: notice you can write `k² = k(k-1) + k`. The term `k(k-1)` counts pairs, and there's a telescoping pattern that collapses into that `n(n+1)(2n+1)/6` form.

---

The real payoff in code is that both expressions are **O(1)** — it doesn't matter if `n` is 100 or 10 billion. The loop version is O(n) and becomes noticeably slow. Euler problems often have this structure: brute force works for small inputs, but the *intended* insight is a mathematical shortcut.

Want to verify the formula against the loop for a small `n` to build confidence in it?

---

## Turn 3 (final)

**User:**

Actually, I feel pretty good about it now. The Gauss pairing trick makes `Σk` click for me — that's a pattern I can actually remember. And the geometric intuition for the squares formula (the staircase packing into a box) gives me enough of a handle to trust it.

The code works, the answer checks out, and I get *why* these formulas are faster than loops for large n. That's exactly what I wanted to learn here.

<done/>

---

**Run end**: done after 2 turns (51s)
