# euler-2-even-fib

- Condition: `learning`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:06:18

## Initial prompt

Project Euler #2: find the sum of the even-valued Fibonacci numbers whose values do not exceed four million.

---

## Turn 1

### Tutor

[Bash(python3 -c "
a, b = 1, 1
total = 0
while b <= 4_000_000:
    if b % 2 == 0:
        total += b
    a, b = b, a + b
print(total)
"
)]
  4613732

Tutor: ## Answer: **4,613,732**

---

### How it works

**The Fibonacci sequence** starts `1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, …`

The even terms follow a neat pattern — **every 3rd Fibonacci number is even**:

| Term | Value | Even? |
|------|-------|-------|
| F₃   | 2     | ✅ |
| F₆   | 8     | ✅ |
| F₉   | 34    | ✅ |
| …    | …     | … |
| F₃₃  | 3,524,578 | ✅ (last ≤ 4M) |
| F₃₆  | 14,930,352 | ✅ (exceeds 4M — stop) |

### Why every 3rd term is even

It comes down to parity (odd = O, even = E):

```
O + O = E   ← position 3
O + E = O   ← position 4
E + O = O   ← position 5
O + O = E   ← position 6  (pattern repeats every 3)
```

The parity pattern **O, O, E** repeats forever.

### The code

```python
a, b = 1, 1
total = 0
while b <= 4_000_000:
    if b % 2 == 0:        # is this term even?
        total += b
    a, b = b, a + b       # advance the sequence
print(total)              # → 4,613,732
```

> **Key idea:** advance `a, b` simultaneously using tuple unpacking — no temp variable needed, and both update in a single step.

### Student

Thanks for walking through this! That parity pattern explanation is really helpful — I can see now why every 3rd Fibonacci number is even. That's a cool mathematical insight.

I have a quick question about the code itself: when we do `a, b = b, a + b`, does Python evaluate the right side (`b, a + b`) completely before assigning to the left side (`a, b`)? I want to make sure we're not accidentally using the updated value of `b` when computing `a + b`.

---

## Turn 2

### Tutor

Tutor: Yes, exactly right — Python **fully evaluates the entire right-hand side first**, then assigns. This is guaranteed by the language.

### What actually happens step-by-step

```python
a, b = 1, 1   # starting state

a, b = b, a + b
#      ^  ^^^
#      |   └─ uses original a (1) and original b (1) → 2
#      └───── uses original b (1)
#
# right side evaluates to the tuple (1, 2)
# THEN: a = 1, b = 2
```

You can verify this with the `dis` module, which shows Python's bytecode:

```python
import dis
dis.dis("a, b = b, a + b")
```
```
LOAD_NAME   b        # push b onto stack
LOAD_NAME   a        # push a onto stack
LOAD_NAME   b        # push b onto stack
BINARY_OP   +        # compute a + b, push result
BUILD_TUPLE 2        # bundle into (b, a+b) ← both from original values
UNPACK_SEQUENCE 2    # unpack the tuple
STORE_NAME  a        # a = first element
STORE_NAME  b        # b = second element
```

Both `b` and `a + b` are **loaded and computed before any store happens**.

### The bug you'd get without this guarantee

If Python assigned left-to-right *eagerly* (like some languages do), you'd need a temp variable:

```python
# what you'd have to write in an eager-assignment language:
temp = a + b
a = b
b = temp
```

Because Python uses tuple semantics, the one-liner is safe and idiomatic. The right side builds a complete, immutable snapshot of the values you need, and only then does the unpacking write anything.

### Student

Ah, that makes sense! So Python builds the whole tuple first — `(1, 2)` in that example — and then unpacks and assigns. That's the safety net.

I think I've got it now. The solution is clean and works, and I understand why the code doesn't accidentally step on itself. The parity pattern is a nice bonus insight, but the core loop is straightforward: generate Fibonacci numbers, add the even ones to the total, stop when we exceed 4 million.

Thanks for breaking down the tuple unpacking — that's a useful pattern to keep in mind for swaps and simultaneous updates.

<done/>

---

**Run end:** done after 2 turn(s) in 32.4s
