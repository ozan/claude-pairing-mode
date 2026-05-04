# euler-6-sum-square-diff

- Source: `project-euler`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T04:02:35.023Z

---

## Turn 1

**User:**

Project Euler #6: find the difference between the square of the sum and the sum of the squares of the first 100 natural numbers.

**Pair:**

Thinking: The user wants to solve Project Euler #6. Let me think about this problem first.
  
  The sum of squares of first n natural numbers: 1² + 2² + ... + n² = n(n+1)(2n+1)/6
  The square of sum of first n natural numbers: (1 + 2 + ... + n)² = (n(n+1)/2)²
  
  For n=100:
  - Sum of squares = 100 * 101 * 201 / 6 = 338350
  
  
  - Square of sum = (100 * 101 / 2)² = 5050² = 25502500
  - Difference = 25502500 - 338350 = 25164150
  
  I can show both a straightforward iterative approach and the elegant closed-form solution using these mathematical formulas, which makes for a nice comparison of efficiency.

Assistant: Good classic problem. Before we code it — two ways to approach this:

OPTIONS:
[A] Loop it out
```diff
+++ euler6.py
@@ -0,0 +1,7 @@
+n = 100
+sum_of_sq = sum(i*i for i in range(1, n+1))
+sq_of_sum = sum(range(1, n+1)) ** 2
+print(sq_of_sum - sum_of_sq)
```

[B] Closed-form formula
```diff
+++ euler6.py
@@ -0,0 +1,5 @@
+n = 100
+sq_of_sum = (n * (n + 1) // 2) ** 2
+sum_of_sq = n * (n + 1) * (2*n + 1) // 6
+print(sq_of_sum - sum_of_sq)
```

(Reply with A or B, or ask a follow-up question.)

Thinking: The tool isn't available. Let me just solve the problem directly. I'll present both approaches in my response.

Assistant: Two ways to approach this — worth thinking about before coding:

**Option A: Loop it out**
```python
n = 100
sum_of_sq = sum(i*i for i in range(1, n+1))
sq_of_sum = sum(range(1, n+1)) ** 2
print(sq_of_sum - sum_of_sq)
```

**Option B: Closed-form formula**
```python
n = 100
sq_of_sum = (n * (n + 1) // 2) ** 2
sum_of_sq = n * (n + 1) * (2*n + 1) // 6
print(sq_of_sum - sum_of_sq)
```

Which would you go with — and do you know where those formulas in B come from?

---

For what it's worth, both give the same answer. The loop is O(n), the formula is O(1). For n=100 it's trivial, but the formulas are genuinely worth knowing:

- **Sum of first n integers**: `n(n+1)/2` — Gauss's trick, pairs that each sum to n+1
- **Sum of first n squares**: `n(n+1)(2n+1)/6` — provable by induction

Let me run option B:

[Bash(python3 -c "
n = 100
sq_of_sum = (n * (n + 1) // 2) ** 2
sum_of_sq = n * (n + 1) * (2*n + 1) // 6
print(f'Square of sum: {sq_of_sum}')
print(f'Sum of squares: {sum_of_sq}')
print(f'Difference: {sq_of_sum - sum_of_sq}')
"
)]
  Square of sum: 25502500
  Sum of squares: 338350
  Difference: 25164150

Assistant: **Answer: `25164150`**

The square of the sum (5050²) dwarfs the sum of squares (338350) — the difference grows as O(n⁴) vs O(n³) and O(n²), so the gap explodes fast as n increases.

---

## Turn 2 (final)

**User:**

Ah, I see! So option B using the closed-form formulas was the way to go. That's really clean — I didn't know the sum-of-squares formula off the top of my head, but the induction proof makes sense once you think about it.

I like how the difference explodes like that. The square of the sum is just *so much larger* than the sum of squares because you're capturing all the cross-products when you expand (1+2+...+100)². That's a nice intuition to keep.

So 25164150 is the final answer. Should we write this to a file and call it done, or did you want to test it against something first?

<done/>

---

**Run end**: done after 1 turn (42s)
