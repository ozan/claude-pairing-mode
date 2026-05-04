# exercism-pangram

- Condition: `learning`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:05:05

## Initial prompt

Exercism 'Pangram': write `is_pangram(text)` that returns True iff the input contains every letter of the alphabet at least once (case-insensitive).

---

## Turn 1

### Tutor

Tutor: ```python
def is_pangram(text: str) -> bool:
    return set("abcdefghijklmnopqrstuvwxyz").issubset(text.lower())
```

**How it works, step by step:**

| Step | What happens |
|------|--------------|
| `text.lower()` | Normalises case so `'A'` and `'a'` count as the same letter |
| `set(...)` on the result | Builds the set of *unique* characters actually present |
| `{"a","b",…,"z"}.issubset(…)` | Returns `True` only when every one of the 26 letters appears in that set |

**Why `issubset` over alternatives:**
- More readable than `len(set(text.lower()) & set(alpha)) == 26`
- Short-circuits — Python stops as soon as it finds a missing letter
- Works on any iterable, so no intermediate list is needed

**Quick mental tests:**

```python
is_pangram("The quick brown fox jumps over the lazy dog")  # True  ✓
is_pangram("Hello, World!")                                # False ✓ (missing most letters)
is_pangram("")                                             # False ✓
is_pangram("abcdefghijklmnopqrstuvwxyz")                  # True  ✓
```

### Student

Thanks for walking through this! I think I understand the logic, but let me make sure I've got it straight.

So when we call `text.lower()`, we're converting everything to lowercase so the comparison is case-insensitive. Then `set("abcdefghijklmnopqrstuvwxyz")` creates a set with all 26 letters. And `issubset()` checks whether that set of all 26 letters is contained within the lowercased text.

One thing I want to clarify though — when we do `set("abcdefghijklmnopqrstuvwxyz").issubset(text.lower())`, aren't we creating a set from the string literal, not from the lowercased text? I'm a bit confused about which set is being checked against which.

Actually, wait — I think I see it now. The set of 26 letters is on the left, and we're checking if it's a subset of the lowercased text. But doesn't `text.lower()` return a string, not a set? How does `issubset()` work with a string argument?

---

## Turn 2

### Tutor

Tutor: Great self-correction! You've got the direction right. Let me clear up the string-vs-set question:

**`issubset()` accepts any iterable, not just a set.**

When you pass a string, Python iterates over its characters automatically — exactly as if you'd written `set(text.lower())` yourself:

```python
# These two are equivalent:
set("abc").issubset("abcde")       # string passed directly ✓
set("abc").issubset(set("abcde"))  # explicitly a set      ✓
```

Internally Python just needs something it can loop over to check membership. A string is iterable (character by character), so it qualifies.

---

**Visualising the direction** — this is the key thing to hold onto:

```
set("abcdefghijklmnopqrstuvwxyz").issubset(text.lower())
│                                │
└── the 26 letters               └── the characters in the text
    ("does this fit inside…?")       ("…this pool?")
```

`A.issubset(B)` asks: *"Is every element of A also found in B?"*

So the question is: *"Is every one of the 26 alphabet letters found somewhere in the text?"* — which is exactly the pangram definition.

---

**A common gotcha** — the reverse call means something completely different:

```python
# WRONG for pangram — asks "is every char in the text a letter?"
set(text.lower()).issubset(set("abcdefghijklmnopqrstuvwxyz"))
```

That would return `False` for `"The quick brown fox..."` because of the spaces and punctuation. Keeping the 26-letter set on the **left** is what makes the logic correct.

### Student

Ah, that makes total sense now! So `issubset()` works with strings because it can iterate through them character by character. I was overthinking it — Python handles the conversion automatically.

And yeah, I can see why the order matters. If we flipped it around and asked "is everything in the text a letter?" we'd fail as soon as we hit a space or punctuation mark, which isn't what we want. We specifically need "do all 26 letters exist somewhere in this text?" — which is what we get by putting the alphabet set on the left.

Let me trace through one example to make sure I've got it:
- Input: `"The quick brown fox jumps over the lazy dog"`
- `text.lower()` → `"the quick brown fox jumps over the lazy dog"`
- Python checks: does this string contain `'a'`? Yes. `'b'`? Yes. ... `'z'`? Yes.
- All 26 letters found → `True`

Perfect. That's clear now. I think the solution is solid!

<done/>

---

**Run end:** done after 2 turn(s) in 27.3s
