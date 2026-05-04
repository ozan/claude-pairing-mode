# euler-10-sum-primes

- Condition: `regular`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:03:24

## Initial prompt

Project Euler #10: find the sum of all primes below two million. (Naive trial-division will be slow — consider a sieve.)

---

## Turn 1

### Tutor

Tutor: Good choice — Sieve of Eratosthenes is the right tool. Before I write it, there's one detail worth getting right on the first try:

[ToolSearch({"query": "select:mcp__pairing__propose_options", "max_results": 1})]
  (no output)

OPTIONS:
[A] Start marking at p²
```diff
+++ euler10.py
@@ -0,0 +1,10 @@
+LIMIT = 2_000_000
+sieve = bytearray([1]) * LIMIT
+sieve[0] = sieve[1] = 0
+
+for p in range(2, int(LIMIT**0.5) + 1):
+    if sieve[p]:
+        sieve[p*p::p] = bytearray(len(sieve[p*p::p]))
+
+print(sum(i for i, v in enumerate(sieve) if v))
```

[B] Start marking at 2p
```diff
+++ euler10.py
@@ -0,0 +1,10 @@
+LIMIT = 2_000_000
+sieve = bytearray([1]) * LIMIT
+sieve[0] = sieve[1] = 0
+
+for p in range(2, int(LIMIT**0.5) + 1):
+    if sieve[p]:
+        sieve[2*p::p] = bytearray(len(sieve[2*p::p]))
+
+print(sum(i for i, v in enumerate(sieve) if v))
```

(Reply with A or B, or ask a follow-up question.)

Tutor: When the inner loop marks multiples of `p` — where should it start?

### Student

I need to think through this one.

If we start marking at `2*p`, we'd be marking `2p, 3p, 4p, ...` as composite.

But if we start at `p*p`, we'd be marking `p², p²+p, p²+2p, ...` as composite.

The key insight is that any composite multiple of `p` that's smaller than `p²` would have already been marked by a smaller prime. For example, if `p = 5`, then `2·5 = 10` was already marked when we processed `p = 2` (since `10 = 2·5`). But `5² = 25` hasn't been marked yet — it can only be factored as `5·5`.

So starting at `p²` is more efficient because we skip marking things that are already marked.

I'll go with **A**.

---

## Turn 2

### Tutor

Tutor: Exactly right — that's the core invariant of the sieve: when you reach prime `p`, every composite below `p²` already has a prime factor smaller than `p`, so it's been marked. `p²` is the first *new* work.

Let me write the file:

[Write(euler10.py)]
LIMIT = 2_000_000
sieve = bytearray([1]) * LIMIT
sieve[0] = sieve[1] = 0

for p in range(2, int(LIMIT**0.5) + 1):
    if sieve[p]:
        sieve[p*p::p] = bytearray(len(sieve[p*p::p]))

print(sum(i for i, v in enumerate(sieve) if v))

  File created successfully at: euler10.py

[Bash(python euler10.py)]
  142913828922

Tutor: **142,913,828,922** — correct answer.

A couple of implementation notes worth knowing:

- **`bytearray` over `list`**: uses 1 byte per element instead of 28 bytes (Python int object overhead), so ~2 MB instead of ~56 MB for this problem.
- **`sieve[p*p::p] = bytearray(...)`**: slice assignment in one C-level operation — much faster than a Python `for` loop zeroing elements one at a time.
- **Outer loop to `√LIMIT`**: by the same argument you just made — any composite above `√LIMIT` must have a prime factor *below* `√LIMIT`, so it's already been caught.

### Student

That makes sense! I appreciate the clarity on those three points:

1. **`bytearray`** — I hadn't thought about the memory difference, but that's a huge win at scale. 2 MB vs 56 MB is the kind of thing that could make the difference between a solution that runs smoothly and one that thrashes.

2. **Slice assignment** — that's elegant. Instead of looping and setting individual indices, we're doing one vectorized operation. Python's doing the heavy lifting under the hood.

3. **Loop bound** — that ties back perfectly to what we just discussed. Once you're past `√LIMIT`, every composite has already been marked by a smaller prime factor.

The solution ran instantly and gave the right answer. I feel like I understand *why* each piece is there now, not just that it works. Thanks for walking through the reasoning before jumping to code — that really helped.

<done/>

---

**Run end:** done after 2 turn(s) in 43.0s
