# euler-2-even-fib

- Condition: `baseline`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T20:52:09

## Initial prompt

Project Euler #2: find the sum of the even-valued Fibonacci numbers whose values do not exceed four million.

---

## Turn 1

### Tutor

[Bash(python3 -c "
a, b = 1, 1
total = 0
while a <= 4_000_000:
    if a % 2 == 0:
        total += a
    a, b = b, a + b

print(f'Answer: {total:,}')
"
)]
  Answer: 4,613,732

Tutor: **Answer: 4,613,732**

---

Here's how it works:

**Algorithm** — iterate through Fibonacci numbers, accumulate any that are even:
```python
a, b = 1, 1
total = 0
while a <= 4_000_000:
    if a % 2 == 0:
        total += a
    a, b = b, a + b   # advance: next = current + previous
```

**The even Fibonacci numbers ≤ 4,000,000** (every 3rd term is even):

| # | Value |
|---|-------|
| F(3) | 2 |
| F(6) | 8 |
| F(9) | 34 |
| F(12) | 144 |
| F(15) | 610 |
| F(18) | 2,584 |
| F(21) | 10,946 |
| F(24) | 46,368 |
| F(27) | 196,418 |
| F(30) | 832,040 |
| F(33) | **3,524,578** |

**Sum = 4,613,732** ✓

> **Why every 3rd term?** The parity pattern of Fibonacci numbers is `odd, odd, even, odd, odd, even, …` — since odd+odd=even and even+odd=odd, the even values recur with period 3.

### Student

Thanks for walking me through this! That's really clear. I can see how the solution works now:

1. We start with the first two Fibonacci numbers (both 1)
2. We loop while the current number doesn't exceed 4 million
3. We check if it's even and add it to our running total if it is
4. We advance to the next Fibonacci number by updating `a, b = b, a + b`

I especially like the insight about the parity pattern — it makes sense that the pattern repeats every 3 terms because of how odd and even numbers add together. That means in theory we could optimize by only checking every 3rd number, but the straightforward approach is already pretty fast and easy to understand.

The answer 4,613,732 checks out. I feel confident about this solution now.

<done/>

---

**Run end:** done after 1 turn(s) in 19.8s
