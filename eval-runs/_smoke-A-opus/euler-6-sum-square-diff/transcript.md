# euler-6-sum-square-diff

- Source: `project-euler`
- Difficulty: `easy`
- Pair model: `claude-opus-4-7`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T02:34:31.669Z

---

## Turn 1

**User:**

Project Euler #6: find the difference between the square of the sum and the sum of the squares of the first 100 natural numbers.

**Pair:**

Assistant: Two natural approaches here:

**A. Loop and accumulate** — walk `1..n` once, summing `i` and `i*i`, then return `s*s - sq`. O(n).

**B. Closed-form** — use Gauss's sum `n(n+1)/2` and the square-pyramidal number `n(n+1)(2n+1)/6`. O(1).

For n=100 the runtime is identical, but B is worth knowing: it solves the same problem for n=10^18 instantly. Which would you like? I'll default to the closed-form unless you'd rather see the loop.

[Write(euler6.py)]
def solve(n: int) -> int:
    s = n * (n + 1) // 2
    sq = n * (n + 1) * (2 * n + 1) // 6
    return s * s - sq


print(solve(100))


[Bash(python3 euler6.py)]
  25164150

Assistant: Answer: **25,164,150**.

A quick check on why the integer division is safe: `n(n+1)` is always even (consecutive integers), so `//2` is exact. And exactly one of `n`, `n+1`, `2n+1` is divisible by 3, so `//6` is exact too. Worth keeping in mind any time you reach for `//` — it's only equivalent to true division when you can prove divisibility.

---

## Turn 2 (final)

**User:**

Oh, nice! I went with B without fully thinking through it, but that explanation about divisibility makes a lot of sense. I'll definitely keep that in mind — I used `//` before without really verifying that the division would be exact, so that's a good catch.

The closed-form approach is elegant too. I can see how it scales instantly to huge numbers, whereas the loop would just grind.

Thanks for walking through both options and the math behind it. This was a good refresher on Gauss's formula and the square-pyramidal number.

<done/>

---

**Run end**: done after 1 turn (35s)
