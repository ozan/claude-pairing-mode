# ours-run-length-encoding

- Condition: `learning`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:07:40

## Initial prompt

Let's implement run-length encoding and decoding in Python: 'aaabbc' ↔ 'a3b2c1'. Two functions, round-trip on a few test strings.

---

## Turn 1

### Tutor

Tutor: ## Run-Length Encoding in Python

Here's the plan before writing a line:
- **Encode**: walk the string, count consecutive identical chars, emit `char+count`
- **Decode**: parse alternating char/number pairs, repeat each char by its count

```python
import re


def rle_encode(s: str) -> str:
    """Compress consecutive repeated characters: 'aaabbc' → 'a3b2c1'."""
    if not s:
        return ""

    result = []
    count = 1

    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            result.append(f"{s[i - 1]}{count}")
            count = 1

    result.append(f"{s[-1]}{count}")   # flush the final run
    return "".join(result)


def rle_decode(s: str) -> str:
    """Expand an RLE string back to its original: 'a3b2c1' → 'aaabbc'."""
    if not s:
        return ""

    # Each token is one letter followed by one or more digits
    tokens = re.findall(r"([a-zA-Z])(\d+)", s)
    return "".join(char * int(count) for char, count in tokens)


# ── round-trip tests ──────────────────────────────────────────────────────────

cases = [
    "aaabbc",        # basic mixed run
    "aabbccdd",      # all pairs
    "abcd",          # no repeats — every run is length 1
    "aaaa",          # single character, long run
    "",              # empty string edge case
    "aabbcccddddz",  # varied run lengths
]

for original in cases:
    encoded = rle_encode(original)
    decoded = rle_decode(encoded)
    status  = "✓" if decoded == original else "✗ MISMATCH"
    print(f"{status}  {original!r:20} → encoded: {encoded!r:20} → decoded: {decoded!r}")
```

**Output:**
```
✓  'aaabbc'             → encoded: 'a3b2c1'             → decoded: 'aaabbc'
✓  'aabbccdd'           → encoded: 'a2b2c2d2'           → decoded: 'aabbccdd'
✓  'abcd'               → encoded: 'a1b1c1d1'           → decoded: 'abcd'
✓  'aaaa'               → encoded: 'a4'                 → decoded: 'aaaa'
✓  ''                   → encoded: ''                   → decoded: ''
✓  'aabbcccddddz'       → encoded: 'a2b2c3d4z1'         → decoded: 'aabbcccddddz'
```

---

### Key design decisions

| Choice | Why |
|---|---|
| `range(1, len(s))` + flush after loop | One pass, no lookahead needed |
| `re.findall(r"([a-zA-Z])(\d+)")` | Handles multi-digit counts (e.g. `a12`) automatically |
| Returns `""` for `""` | Avoids an `IndexError` on `s[-1]` in the encoder |

A subtle gotcha: the **final run must be flushed after the loop** — a common off-by-one bug is emitting only the transitions and losing the last group entirely.

### Student

Thanks for walking me through this! I can see the logic is solid, and all the test cases pass. Let me trace through one example to make sure I understand the flow:

For `'aaabbc'`:
- **Encode**: start at index 1, `s[1]='a'` matches `s[0]='a'`, so count becomes 2. Then `s[2]='a'` matches, count becomes 3. Then `s[3]='b'` doesn't match `s[2]='a'`, so we emit `'a3'` and reset. Continue for `'b'` and `'c'`, and the final `result.append(f"{s[-1]}{count}")` catches the last `'c'`. We get `'a3b2c1'`. ✓

- **Decode**: the regex `r"([a-zA-Z])(\d+)"` pulls out `('a', '3')`, `('b', '2')`, `('c', '1')`, then we expand each one with `char * int(count)`. Back to `'aaabbc'`. ✓

One thing I want to confirm: in the encoder, why do we need that special handling of the final run? Is it because the loop condition `range(1, len(s))` means we stop one character short, so we'd lose tracking of whatever the last character was?

Also, I notice the regex only matches uppercase and lowercase letters — would this work if someone passed in numbers or special characters in the original string? Or is that outside the scope of this problem?

---

## Turn 2

### Tutor

Tutor: Your trace is exactly right! Let me answer both questions precisely.

---

### Why the final flush is needed

The loop only emits a token on **transitions** — when `s[i] != s[i-1]`. That means it emits the *previous* run the moment a new one begins. The last run, by definition, never triggers a transition (nothing comes after it), so it quietly accumulates in `count` and would be silently dropped without the post-loop append.

A concrete trace makes this vivid:

```
s = 'aaabbc'

i=1  'a'=='a'  count=2
i=2  'a'=='a'  count=3
i=3  'b'!='a'  → emit 'a3', reset count=1
i=4  'b'=='b'  count=2
i=5  'c'!='b'  → emit 'b2', reset count=1
                                          ← loop ends here, 'c1' never emitted!
post-loop append → emit 'c1'              ← this is the rescue line
```

The pattern generalises: **a string with N distinct runs will produce N−1 transitions**, so the loop always misses the last one.

---

### The digit/special-character problem

You've spotted a real limitation — there are actually **two separate issues**:

**1. The decoder's regex is too narrow**

`[a-zA-Z]` excludes `!`, `@`, digits, spaces, etc. This is a simple fix:

```python
# replace this
tokens = re.findall(r"([a-zA-Z])(\d+)", s)

# with this — matches any single non-digit character
tokens = re.findall(r"([^\d])(\d+)", s)
```

That covers punctuation, spaces, Unicode — anything that isn't itself a digit.

**2. Digits in the source cause genuine ambiguity**

This is deeper and not fixable with just a regex tweak. If the source contains digits, the encoded output is structurally ambiguous:

```
source:  '111'
encoded: '13'       ← is this "digit 1, count 3"? or the literal string "13"?

source:  'aaa111'
encoded: 'a313'     ← is the '3' part of 'a3', or the start of '31'?
```

The decoder has no way to tell where the count ends and the next character begins. The standard fixes are:

| Fix | Example format | Trade-off |
|---|---|---|
| Require a delimiter | `a:3,b:2,c:1` | Larger output, always unambiguous |
| Restrict source to non-digits | (current approach) | Simple, but limited alphabet |
| Escape digits in source first | `\x31` for `'1'` | Complex but fully general |

For the classic use-case — compressing text, DNA sequences, pixel colours — the letter-only restriction is perfectly fine and keeps the implementation clean.

### Student

Ah, that makes total sense! The final flush issue is a classic off-by-one trap — the loop only emits *when a transition happens*, so the last run just keeps accumulating in `count` and has nowhere to go unless we catch it after the loop ends. Thanks for the concrete trace; that really drives it home.

And the ambiguity problem with digits is a great real-world lesson. I can see why `'111'` → `'13'` creates chaos on decode — there's literally no way to parse it correctly without additional context. I like the three options you listed, and I agree that for typical text/DNA/image use cases, just sticking with letters is the right call. The restriction keeps the code simple and handles the actual problem domain.

So if we wanted to be slightly more general without getting into escaping, using `[^\d]` instead of `[a-zA-Z]` seems like a good middle ground — it handles punctuation and spaces, which might be nice for compressing things like `"   aaaa!!!!!"` without being overly complex.

That said, for the problem as stated — "implement run-length encoding and decoding" with the example `'aaabbc'` — the current solution is solid and passes all the round-trip tests. I think we're good here.

<done/>

---

**Run end:** done after 2 turn(s) in 56.1s
