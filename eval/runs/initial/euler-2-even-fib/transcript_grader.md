# euler-2-even-fib

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:02:26

## Initial prompt

Project Euler #2: find the sum of the even-valued Fibonacci numbers whose values do not exceed four million.

---

## Turn 1

### Tutor

Tutor: Good classic problem. Before we write code, a question on approach:

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Even-only recurrence
Every 3rd Fibonacci number is even (2, 8, 34, 144, …), and they satisfy their own recurrence: `E(n) = 4·E(n−1) + E(n−2)`. Iterate that directly — no filtering needed.

[B] Generate all, filter evens
Generate the full Fibonacci sequence up to 4M, keep only the even terms, and sum them.

(Reply with A or B, or ask a follow-up question.)

Tutor: Which approach do you want to go with?

### Student

I think I'd like to go with **A** — the even-only recurrence.

I haven't seen that pattern before (that every 3rd Fibonacci number is even), and I'm curious how that works. Plus, it sounds more efficient since we're not generating numbers we'll just throw away. Can you walk me through why that recurrence `E(n) = 4·E(n−1) + E(n−2)` gives us the even Fibonacci numbers?

---

## Turn 2

### Tutor

Tutor: Great choice. Let me walk through the two key insights.

**Why every 3rd Fibonacci number is even**

Look at the sequence mod 2:

```
F:      1  1  2  3  5  8  13  21  34 …
mod 2:  O  O  E  O  O  E   O   O   E …
```

The parity pattern `O, O, E` repeats forever — because `O+O=E`, `O+E=O`, `E+O=O`, and we're back to `O, O`. So F₃, F₆, F₉, … are always even.

**Why E(n) = 4·E(n−1) + E(n−2)**

Let E(n) = F(3k). We want to express F(3k+3) in terms of F(3k) and F(3k−3). Two steps:

1. Expand forward by 3 using F(n+1) = F(n) + F(n−1):
   ```
   F(3k+3) = 3·F(3k) + 2·F(3k−1)
   ```

2. Eliminate F(3k−1) — it's not an even-Fib term, so we express it using neighbors:
   ```
   F(3k)   = F(3k−1) + F(3k−2)
   F(3k−2) = F(3k−1) − F(3k−3)
   → 2·F(3k−1) = F(3k) + F(3k−3)
   ```

Substitute back:
```
F(3k+3) = 3·F(3k) + F(3k) + F(3k−3)
         = 4·F(3k) + F(3k−3)
```

That's the recurrence. Now let's write the solution:

[Bash(ls euler2.py 2>/dev/null && echo "exists" || echo "new")]
  new

[Write(euler2.py)]
def solve(limit=4_000_000):
    a, b = 2, 8  # First two even Fibonacci numbers
    total = 0
    while a <= limit:
        total += a
        a, b = b, 4 * b + a
    return total

print(solve())

  File created successfully at: euler2.py

[Bash(python euler2.py)]
  4613732

Tutor: **4,613,732** — and we only iterated through 11 terms instead of ~33.

The swap trick `a, b = b, 4*b + a` is worth noting: Python evaluates the right-hand side fully before any assignment, so you don't need a temp variable to avoid clobbering `b` before using it in `4*b + a`. Many languages would require `tmp = a; a = b; b = 4*b + tmp`.

### Student

Ah, that makes sense! I followed the algebra — especially how you had to eliminate F(3k−1) by expressing it in terms of the even-Fib neighbors. That's clever.

And thanks for the note about the tuple unpacking. I was actually wondering whether we'd need a temp variable there, so it's good to know Python handles that automatically.

Let me just verify the logic once more by hand:
- Start: a=2, b=8
- Next: a=8, b=4·8+2=34
- Next: a=34, b=4·34+8=144
- And so on...

Yep, that's matching the even Fibonacci terms: 2, 8, 34, 144, ... And we sum them all until we exceed 4 million. The output 4,613,732 looks right.

This was a nice lesson in recognizing patterns in sequences — I wouldn't have thought to look for a separate recurrence for just the even terms. Thanks for walking through that!

<done/>

---

**Run end:** done after 2 turn(s) in 58.3s
