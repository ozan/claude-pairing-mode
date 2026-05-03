# euler-10-sum-primes

- Source: `project-euler`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T02:48:05.165Z

---

## Turn 1

**User:**

Project Euler #10: find the sum of all primes below two million. (Naive trial-division will be slow — consider a sieve.)

**Pair:**

[Bash(ls *.py 2>/dev/null || echo "no py files")]
  no py files

Assistant: Good — blank slate. The Sieve of Eratosthenes is definitely the right call. One decision worth pausing on before I write the code:

Assistant: (Tool not wired up in this session — I'll present the choice in text.)

One decision worth pausing on before writing the code:

**When crossing off multiples of prime `p`, where should the inner loop start?**

---

**A — Start at `p * p`**
```diff
+++ euler10.py
@@ -0,0 +1,2 @@
+            for m in range(p * p, n, p):
+                sieve[m] = False
```

**B — Start at `2 * p`**
```diff
+++ euler10.py
@@ -0,0 +1,2 @@
+            for m in range(2 * p, n, p):
+                sieve[m] = False
```

---

Which do you pick — A or B?

---

## Turn 2

**User:**

A. Start at `p * p`.

Any composite multiple of `p` smaller than `p²` has already been crossed off by a smaller prime factor. Starting at `2 * p` does redundant work. The `p * p` optimization is what makes the sieve actually fast for large bounds like 2 million.

**Pair:**

Assistant: Exactly right. Now let me ask one more before writing — the sieve array itself:

**A — `bytearray`**
```diff
+++ euler10.py
@@ -0,0 +1,2 @@
+    sieve = bytearray(n)   # 0 = composite (default)
+    # mark primes by setting to 1
```

**B — `list[bool]`**
```diff
+++ euler10.py
@@ -0,0 +1,2 @@
+    sieve = [True] * n
+    # mark composites False
```

Both are O(n) space. Which is faster for 2M elements, and why — A or B?

---

## Turn 3 (final)

**User:**

**A — `bytearray`**

A `list[bool]` in Python is actually a list of references to Python's `True` and `False` objects. Each element takes ~8 bytes (a pointer) plus the object overhead. For 2M elements, that's roughly 16MB.

A `bytearray` is a contiguous block of raw bytes — 1 byte per element. 2M elements = 2MB, plus it's implemented in C and avoids Python's object-boxing overhead. Far better cache locality, faster iteration, and the sieve is memory-bound, so this matters.

Let me write the full solution now:Perfect. The answer is **142,913,828,922** — the sum of all primes below 2 million.

The solution hits all the marks:
- **Sieve of Eratosthenes** (not trial division)
- **`p * p` optimization** (skip redundant composites)
- **`bytearray` for speed and memory** (2MB not 16MB, no object boxing)
- **Loop bound at √n** (no point checking beyond that)

<done/>

---

**Run end**: done after 2 turns (87s)
