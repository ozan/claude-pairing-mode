# euler-6-sum-square-diff

- Source: `project-euler`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Output style: `Learning`
- Started: 2026-05-03T19:59:31.189Z

---

## Turn 1

**User:**

Project Euler #6: find the difference between the square of the sum and the sum of the squares of the first 100 natural numbers.

**Pair:**

Assistant: ## Project Euler #6

**Two quantities to find:**

### 1. Sum of squares — $\sum_{i=1}^{n} i^2 = \frac{n(n+1)(2n+1)}{6}$

$$\frac{100 \times 101 \times 201}{6} = \frac{2{,}030{,}100}{6} = 338{,}350$$

### 2. Square of sum — $\left(\sum_{i=1}^{n} i\right)^2 = \left(\frac{n(n+1)}{2}\right)^2$

$$\left(\frac{100 \times 101}{2}\right)^2 = 5050^2 = 25{,}502{,}500$$

### Difference

$$25{,}502{,}500 - 338{,}350 = \boxed{25{,}164{,}150}$$

---

**Why is the square of sum so much larger?** The cross terms. When you expand $(1+2+\cdots+100)^2$, you get every $i^2$ term *plus* every $2ij$ term ($i \neq j$) — and those $\binom{100}{2} = 4{,}950$ cross terms are what the difference captures. It's a tidy illustration of why $(a+b)^2 \neq a^2 + b^2$.

---

## Turn 2

**User:**

Great problem! Let me give you two approaches to implement this. The math is straightforward, but we can solve it in different ways:

---

## Option A: Direct mathematical formulas
Use the closed-form formulas for sum of integers and sum of squares. Very fast, very clear intent.

```typescript
const n = 100;

// Square of sum: (n(n+1)/2)^2
const sumOfInts = (n * (n + 1)) / 2;
const squareOfSum = sumOfInts ** 2;

// Sum of squares: n(n+1)(2n+1)/6
const sumOfSquares = (n * (n + 1) * (2 * n + 1)) / 6;

const difference = squareOfSum - sumOfSquares;
console.log(difference); // 25164150
```

**Why pick this**: It's O(1), mathematically elegant, and shows you understand the formulas. Great for interviews.

---

## Option B: Explicit loops
Build both sums step-by-step with loops. Slightly more code, but makes the calculation transparent — you can see exactly what's being summed.

```typescript
const n = 100;

let sumOfInts = 0;
let sumOfSquares = 0;

for (let i = 1; i <= n; i++) {
  sumOfInts += i;
  sumOfSquares += i * i;
}

const squareOfSum = sumOfInts ** 2;
const difference = squareOfSum - sumOfSquares;
console.log(difference); // 25164150
```

**Why pick this**: It's explicit and debuggable — you can add logging to watch the sums build. Better for learning what's really happening.

---

**Which appeals to you?** Pick A for the math elegance, or B if you'd like to see the sums accumulate step-by-step. Or tell me if you'd like a variation (e.g., functional style with `reduce`, or a different language).

**Pair:**

Assistant: Both work perfectly — here's my honest take on the tradeoff:

**Lean toward B for this problem specifically.** The loop version makes the *structure* of the problem visible: you're literally accumulating two different things over the same range, then comparing them. That mirrors how Euler framed it, and it's easy to sanity-check by pausing at `i = 3` mentally (sum=6, squareOfSum=36, sumOfSquares=14, diff=22 ✓).

Option A is production-ideal for large `n`, but for `n = 100` the O(1) vs O(n) distinction is noise — and the formula `n*(n+1)*(2*n+1)/6` requires prior knowledge to read, not just logic to follow.

---

**A third option worth knowing** — functional style with `Array.from`:

```typescript
const range = Array.from({ length: 100 }, (_, i) => i + 1);

const sum = range.reduce((a, b) => a + b, 0);
const sumOfSquares = range.reduce((a, b) => a + b ** 2, 0);

console.log(sum ** 2 - sumOfSquares); // 25164150
```

This reads almost like the problem statement itself: *"here's the range, here's the sum, here's the sum of squares."* The tradeoff is it allocates an array — fine here, wasteful at scale.

---

**Rule of thumb across Euler problems:**

| Situation | Reach for |
|---|---|
| Small, fixed `n` | Loops or functional — clarity wins |
| Large or variable `n` | Closed-form formulas |
| Prototyping | Whatever you can write fastest |

---

## Turn 3 (final)

**User:**

You're right — Option B really does expose the problem structure. Let me implement it:

```typescript
const n = 100;

let sumOfInts = 0;
let sumOfSquares = 0;

for (let i = 1; i <= n; i++) {
  sumOfInts += i;
  sumOfSquares += i * i;
}

const squareOfSum = sumOfInts ** 2;
const difference = squareOfSum - sumOfSquares;

console.log(`Sum of integers: ${sumOfInts}`);
console.log(`Square of sum: ${squareOfSum}`);
console.log(`Sum of squares: ${sumOfSquares}`);
console.log(`Difference: ${difference}`);
```

Let me test this:Perfect! **✓ 25,164,150** — matches our math exactly.

**What I learned from this choice:**

1. **Clarity > complexity at small scale** — With `n = 100`, even if Option B were O(n²), you'd never notice. The loop reads like the problem itself.

2. **The debugging advantage is real** — If I'd gotten the wrong answer, I could sprinkle a `console.log` at `i = 1, 2, 3` and spot the bug instantly. The formula approach would have left me staring at algebra.

3. **Intermediate values are free** — I get to print out `sumOfInts` (5050) and `sumOfSquares` (338,350) directly. With Option A, you'd have to re-derive them mentally or compute them separately to verify.

The functional approach (with `Array.from`) would've been elegant too, but it allocates memory unnecessarily here — and the loop version is already as readable.

<done/>

---

**Run end**: done after 2 turns (52s)
