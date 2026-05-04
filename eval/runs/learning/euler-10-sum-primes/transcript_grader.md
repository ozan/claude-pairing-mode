# euler-10-sum-primes

- Condition: `learning`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:06:32

## Initial prompt

Project Euler #10: find the sum of all primes below two million. (Naive trial-division will be slow — consider a sieve.)

---

## Turn 1

### Tutor

Tutor: ## Sieve of Eratosthenes

The key insight: trial division checks each number independently (O(n√n)), but the **Sieve of Eratosthenes** crosses off multiples in bulk — O(n log log n), which is nearly linear.

**How it works:**

```
Start: [T T T T T T T T T T ...]  (index = the number, T = "still prime?")
        0 1 2 3 4 5 6 7 8 9

Fix 0,1: not prime by definition.
p=2: mark 4, 6, 8, 10 … (every multiple of 2, starting at 2²=4)
p=3: mark 9, 12, 15 …   (start at 3²=9; 6 already crossed off)
p=5: mark 25, 30 …      (start at 5²=25)
… stop once p² ≥ limit
```

Whatever indices are still `True` at the end are prime. Sum them.

```python
def sum_primes_below(limit: int) -> int:
    # bytearray is fast and memory-efficient (1 byte per entry, not 28 like a Python bool)
    sieve = bytearray(b'\x01') * limit   # all True
    sieve[0] = sieve[1] = 0              # 0 and 1 are not prime

    for p in range(2, int(limit**0.5) + 1):
        if sieve[p]:                     # p is still prime
            # cross off p², p²+p, p²+2p, …  (multiples below p² already handled)
            sieve[p*p :: p] = bytes(len(sieve[p*p :: p]))

    return sum(i for i, is_prime in enumerate(sieve) if is_prime)

print(sum_primes_below(2_000_000))
```

```
142913828922
```

---

### Why each optimisation matters

| Choice | Why |
|---|---|
| `bytearray` instead of `list` | ~28× less memory; cache-friendly |
| Start crossing off at **p²** | All smaller multiples (2p, 3p…) already crossed off by smaller primes |
| Loop only up to **√limit** | Any composite ≤ limit has a factor ≤ √limit |
| Slice assignment `sieve[p*p::p] = bytes(…)` | Bulk C-speed write, no Python loop |

### Complexity vs. naive trial division

| Method | Time | For n = 2 000 000 |
|---|---|---|
| Trial division | O(n √n) | ~2.8 billion ops |
| Sieve of Eratosthenes | O(n log log n) | ~6 million ops |

The sieve runs in **under 0.1 s**; trial division would take **minutes**.

### Student

Thanks for walking me through this! I can see why the Sieve of Eratosthenes is so much faster than trial division for this problem.

Let me make sure I understand the key parts:

1. We use a `bytearray` where each index represents a number, and the value (0 or 1) tells us if it's prime
2. We start marking off multiples at `p²` because anything smaller would've already been crossed off by a smaller prime
3. We only loop up to `√limit` because any composite number must have at least one factor ≤ its square root
4. The slice assignment `sieve[p*p::p] = bytes(...)` efficiently marks all multiples of `p` at once

A couple of quick clarification questions:

- When we do `sieve[p*p :: p] = bytes(len(sieve[p*p :: p]))`, we're creating a bytes object filled with zeros (since `bytes(n)` creates n zero bytes), right? That's what marks them as "not prime"?
- Is there a reason we use `bytearray` instead of a regular list of bools, beyond just memory efficiency? Does it also affect speed?

Once I understand those details, I think I'm ready to try running this myself!

---

## Turn 2

### Tutor

Tutor: Both great observations — you've got it exactly right on both counts.

---

**`bytes(n)` → n zero bytes → "not prime"**

Yes, precisely:

```python
bytes(3)        # → b'\x00\x00\x00'  (three zero bytes)
bytearray(b'\x01') * 5  # → bytearray(b'\x01\x01\x01\x01\x01')  (five 1-bytes = "prime")
```

So the assignment `sieve[p*p::p] = bytes(len(sieve[p*p::p]))` is saying:
*"replace every pth slot starting at p² with a zero byte"* — i.e., mark them all composite.

---

**`bytearray` vs `list` — it's both memory AND speed**

A Python `list` stores *pointers* to Python objects. Even `True`/`False` are full Python objects:

```
list of bools        bytearray
┌──────────────┐     ┌───┐
│ ptr → True   │  8B │ 1 │  1B
│ ptr → False  │  8B │ 0 │  1B
│ ptr → True   │  8B │ 1 │  1B
│    …         │     │ … │
└──────────────┘     └───┘
  ~16 MB for 2M       2 MB for 2M
```

The speed win comes from two things:

1. **Cache locality** — 8× smaller data fits more easily in L1/L2 CPU cache; cache misses are the silent killer of tight loops
2. **Bulk slice assignment is C-speed** — `sieve[p*p::p] = bytes(...)` on a `bytearray` compiles down to something close to a C `memset` loop. On a `list`, Python would have to touch each pointer-sized slot individually through the interpreter

A quick benchmark to make it concrete:

```python
import timeit

N = 2_000_000

def sieve_bytearray():
    s = bytearray(b'\x01') * N
    s[0] = s[1] = 0
    for p in range(2, int(N**0.5) + 1):
        if s[p]:
            s[p*p::p] = bytes(len(s[p*p::p]))
    return sum(i for i, v in enumerate(s) if v)

def sieve_list():
    s = [True] * N
    s[0] = s[1] = False
    for p in range(2, int(N**0.5) + 1):
        if s[p]:
            s[p*p::p] = [False] * len(s[p*p::p])
    return sum(i for i, v in enumerate(s) if v)

print(timeit.timeit(sieve_bytearray, number=5))  # ~0.6 s
print(timeit.timeit(sieve_list,      number=5))  # ~1.5 s
```

Same algorithm, same answer — `bytearray` is roughly **2–3× faster** in practice just from those two effects. Go ahead and run it!

### Student

Ah, that makes total sense now! The memory layout difference is really eye-opening — I hadn't realized that a Python `list` stores pointers to objects rather than the values themselves. And the cache locality point clicks for me too; I've heard about that being a big deal in performance, but seeing it matter this much for the same algorithm is convincing.

Let me run the code to verify it works and see those timing differences myself:

```python
import timeit

N = 2_000_000

def sieve_bytearray():
    s = bytearray(b'\x01') * N
    s[0] = s[1] = 0
    for p in range(2, int(N**0.5) + 1):
        if s[p]:
            s[p*p::p] = bytes(len(s[p*p::p]))
    return sum(i for i, v in enumerate(s) if v)

def sieve_list():
    s = [True] * N
    s[0] = s[1] = False
    for p in range(2, int(N**0.5) + 1):
        if s[p]:
            s[p*p::p] = [False] * len(s[p*p::p])
    return sum(i for i, v in enumerate(s) if v)

# First verify both give the same answer
print("bytearray result:", sieve_bytearray())
print("list result:     ", sieve_list())

# Then time them
print("\nTiming (5 runs each):")
print("bytearray:", timeit.timeit(sieve_bytearray, number=5))
print("list:     ", timeit.timeit(sieve_list, number=5))
```

Running this should confirm that both produce the correct answer (142913828922) and show the speed difference. I'm ready to test it now — thanks for breaking down those low-level details!

<done/>

---

**Run end:** done after 2 turn(s) in 49.4s
