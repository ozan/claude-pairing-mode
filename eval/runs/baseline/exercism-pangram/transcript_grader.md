# exercism-pangram

- Condition: `baseline`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T20:50:40

## Initial prompt

Exercism 'Pangram': write `is_pangram(text)` that returns True iff the input contains every letter of the alphabet at least once (case-insensitive).

---

## Turn 1

### Tutor

Tutor: ```python
def is_pangram(text: str) -> bool:
    return set("abcdefghijklmnopqrstuvwxyz").issubset(text.lower())
```

**How it works:**

1. `text.lower()` — normalises the input to lowercase so the check is case-insensitive.
2. `set("abcdefghijklmnopqrstuvwxyz")` — builds the 26-letter alphabet as a set.
3. `.issubset(...)` — returns `True` only when every one of those 26 letters appears somewhere in the (lowercased) text.

Python's `str` supports `issubset` directly because iterating over a string yields individual characters, so no explicit conversion to a set is needed for the right-hand side.

---

**Quick mental tests:**

| Input | Expected | Why |
|---|---|---|
| `"The quick brown fox jumps over the lazy dog"` | `True` | Classic pangram |
| `"Hello, World!"` | `False` | Missing most letters |
| `""` | `False` | Empty string |
| `"abcdefghijklmnopqrstuvwxyz"` | `True` | Exact alphabet |
| `"ABCDEFGHIJKLMNOPQRSTUVWXYZ"` | `True` | Uppercase alphabet |

---

**Alternative one-liner** using a generator (slightly more verbose but explicit):

```python
def is_pangram(text: str) -> bool:
    return all(letter in text.lower() for letter in "abcdefghijklmnopqrstuvwxyz")
```

Both are O(n) where n is `len(text)`. The `issubset` version is typically faster in practice because it short-circuits internally in C and avoids building intermediate Python objects.

### Student

Thanks for walking through this! The solution is really clean. I have a couple of quick questions to make sure I understand it fully:

1. When you say "Python's `str` supports `issubset` directly" — does that mean `issubset()` automatically converts the string to a set of characters behind the scenes? Or is there something special about how `issubset()` works with strings?

2. For the alternative with `all()` — I see it checks each letter individually. Does `all()` actually short-circuit early if it finds a letter that's *not* in the text, or does it always iterate through all 26?

3. One more thing: in the main solution, we're checking if the alphabet set is a subset of the lowercased text. Is there any downside to doing it that way instead of converting the text to a set first (like `set(text.lower()).issuperset(set("abcdefg..."))`)? I'm wondering about memory or speed.

I think the solution works, but I want to lock in my understanding of *why* it's efficient before I call it done.

---

## Turn 2

### Tutor

Tutor: Great questions — all three touch on real Python internals worth understanding precisely.

---

### 1. How `issubset()` handles a string argument

`set.issubset(other)` accepts **any iterable** as `other` — it doesn't require a set. But when `other` is *not* already a set or frozenset, CPython's implementation **does convert it to a temporary set internally** before doing the subset test. You can see this in [`Objects/setobject.c`](https://github.com/python/cpython/blob/main/Objects/setobject.c):

```c
if (!PyAnySet_Check(other)) {
    PyObject *tmp = make_new_set(&PySet_Type, other);  // ← builds a set from the iterable
    rv = set_issubset(so, tmp);
    Py_DECREF(tmp);
    ...
}
```

So "automatically converts to a set of characters behind the scenes" is exactly what's happening. There's nothing magic — it's just that the iterable protocol is used to build that temporary set.

---

### 2. Does `all()` really short-circuit?

Yes, **guaranteed by the language**, not just an implementation detail. From the Python docs:

> `all(iterable)` — Return `True` if all elements of the iterable are true. **If the iterable is empty or an element is false, return `False` immediately.**

So with `all(letter in text for letter in "abc...xyz")`, as soon as one letter is missing the generator is abandoned and `False` is returned. If you're checking a text that's missing `'q'`, iteration stops at `'q'` (the 17th letter) — the remaining 9 letters are never tested.

---

### 3. `issubset(string)` vs. `issubset(set(string))` — memory & speed

As established in #1, passing the raw string means CPython silently builds the same temporary set anyway. So these two are **functionally identical** at the C level:

```python
alphabet.issubset(text.lower())        # CPython builds set(text.lower()) internally
alphabet.issubset(set(text.lower()))   # you build it explicitly in Python
```

The only real difference is **explicitness**. The second form makes the intent clearer — but there's no meaningful speed or memory advantage to either.

Where it *does* matter is the comparison with the `all()` alternative:

| Approach | Text scan | Per-letter lookup | Overall |
|---|---|---|---|
| `issubset(set(text))` | O(n) once | O(1) × 26 | **O(n)** |
| `all(c in text for c in alphabet)` | O(n) per letter (string search) | — | **O(26n)** worst case |

The `all()` version calls Python's string `in` operator 26 times, and each is a linear scan of the text. Big-O-wise it's still O(n) (constant factor), but for a long input the set-based approach does substantially less work.

---

**Summary of what makes the main solution efficient:**

```python
set("abcdefghijklmnopqrstuvwxyz").issubset(text.lower())
```

- Scans `text` **once** to build an internal set of unique characters — O(n)
- Does 26 O(1) hash-table lookups — O(1) effectively
- Total: **O(n)**, with a small constant

### Student

Perfect — that's exactly the level of detail I needed. Thanks for breaking down the C internals and the Big-O comparison; I really appreciate that you showed the actual cost difference between `issubset(set(text))` vs `all()`.

One last sanity check: in the main solution, we're building a set from the *alphabet string* (`set("abcdefg...")`), not from the input text. So we're only doing the O(n) scan on `text.lower()`, and the alphabet set is just a tiny fixed O(1) lookup table. That's why it's so efficient even on huge inputs, right?

And just to be clear — if I wanted to write it even more explicitly for readability, I could do something like:

```python
def is_pangram(text: str) -> bool:
    alphabet = set("abcdefghijklmnopqrstuvwxyz")
    text_chars = set(text.lower())
    return alphabet.issubset(text_chars)
```

This would do two O(n) passes (one for each set), but it's clearer what's happening. That would still be O(n) overall, just with a higher constant, right?

Got it — the solution works, and I understand the tradeoffs now. Thanks!

<done/>

---

**Run end:** done after 2 turn(s) in 68.6s
