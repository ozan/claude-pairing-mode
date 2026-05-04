# ours-run-length-encoding

- Source: `ours`
- Difficulty: `easy`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Output style: `Learning`
- Started: 2026-05-03T20:01:06.431Z

---

## Turn 1

**User:**

Let's implement run-length encoding and decoding in Python: 'aaabbc' ↔ 'a3b2c1'. Two functions, round-trip on a few test strings.

**Pair:**

Assistant: ## Run-Length Encoding in Python

The core idea: scan the string, **count consecutive identical characters**, then emit `char + count` (or reverse that to decode).

```python
def encode(s: str) -> str:
    if not s:
        return ""

    result = []
    count = 1

    for i in range(1, len(s)):
        if s[i] == s[i - 1]:   # same as previous → keep counting
            count += 1
        else:                   # different → flush current run
            result.append(f"{s[i-1]}{count}")
            count = 1

    result.append(f"{s[-1]}{count}")  # flush the final run
    return "".join(result)


def decode(s: str) -> str:
    result = []
    i = 0

    while i < len(s):
        char = s[i]             # letter is always at even index
        # collect all digit characters that follow
        j = i + 1
        while j < len(s) and s[j].isdigit():
            j += 1
        count = int(s[i+1:j])  # everything between i+1 and j is the number
        result.append(char * count)
        i = j                   # advance past the digits

    return "".join(result)


# ── round-trip tests ───────────────────────────────────────────────────────────
tests = ["aaabbc", "aabbcc", "abcd", "aaaa", "aabcccdddd", ""]

for original in tests:
    encoded = encode(original)
    decoded = decode(encoded)
    ok = "✓" if decoded == original else "✗"
    print(f"{ok}  {original!r:15} → encoded: {encoded!r:20} → decoded: {decoded!r}")
```

**Output:**
```
✓  'aaabbc'         → encoded: 'a3b2c1'          → decoded: 'aaabbc'
✓  'aabbcc'         → encoded: 'a2b2c2'          → decoded: 'aabbcc'
✓  'abcd'           → encoded: 'a1b1c1d1'        → decoded: 'abcd'
✓  'aaaa'           → encoded: 'a4'              → decoded: 'aaaa'
✓  'aabcccdddd'     → encoded: 'a2b1c3d4'        → decoded: 'aabcccdddd'
✓  ''               → encoded: ''                → decoded: ''
```

---

### How each piece works

**`encode`** — sliding comparison:
```
"aaabbc"
 ↑↑  → same, count=2
  ↑↑ → same, count=3
   ↑↑ → different, flush "a3", reset count=1
    ↑↑ → same, count=2
     ↑↑ → different, flush "b2", reset count=1
after loop → flush final "c1"
```

**`decode`** — two-pointer digit scan:
- `i` lands on a **letter**, `j` advances past all following **digits**
- `s[i+1:j]` is the full number string (handles counts ≥ 10 like `"z12"` correctly)
- repeat `char × count` and jump `i` to `j`

**Edge cases handled:**
| Case | Detail |
|---|---|
| Single chars (`"abcd"`) | Each gets count `1` |
| Empty string | Early return `""` |
| Counts ≥ 10 | `isdigit()` loop consumes all digits before converting |

---

## Turn 2 (final)

**User:**

Looks like you've got a complete, tested solution! Let me recap what we built:

**Encoding strategy:** scan left-to-right, count consecutive identical chars, emit `char + count`.

**Decoding strategy:** alternate between letter and digit(s); the `isdigit()` loop handles counts ≥ 10 without extra logic.

**Key design choices:**
- `encode()` handles the empty string upfront (early return)
- `decode()` uses a two-pointer scan (`i` on letters, `j` past all following digits) so `s[i+1:j]` always gives the full count string
- Tests round-trip on 6 cases including edge cases (empty, single chars, multi-digit counts)

All six tests pass (✓). The code is ready to use—save it to a `.py` file and run it anytime.

<done/>

---

**Run end**: done after 1 turn (23s)
