# exercism-acronym

- Condition: `learning`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:05:33

## Initial prompt

Exercism 'Acronym': given a phrase, return its acronym in uppercase. Treat hyphens as word separators; ignore other punctuation. e.g. 'Portable Network Graphics' → 'PNG'.

---

## Turn 1

### Tutor

Tutor: ## Approach

**Rules to implement:**
1. Split on **whitespace** and **hyphens** (both are word separators)
2. Take the **first alphabetic character** of each resulting segment
3. **Uppercase** everything; skip non-alpha leading chars

```python
import re

def abbreviate(words: str) -> str:
    parts = re.split(r"[\s\-]+", words)   # split on spaces & hyphens
    return "".join(
        next((c.upper() for c in part if c.isalpha()), "")
        for part in parts
    )
```

---

### How it works — step by step

| Input | After `re.split` | First-alpha-upper | Result |
|---|---|---|---|
| `"Portable Network Graphics"` | `["Portable","Network","Graphics"]` | P, N, G | **PNG** |
| `"Complementary metal-oxide semiconductor"` | `["Complementary","metal","oxide","semiconductor"]` | C, M, O, S | **CMOS** |
| `"First In, First Out"` | `["First","In,","First","Out"]` | F, I, F, O | **FIFO** |
| `"Halley's Comet"` | `["Halley's","Comet"]` | H, C | **HC** |
| `"Something - Under - Test"` | `["Something","","Under","","Test"]` | S, U, T | **SUT** |

### Key design decisions

- **`re.split(r"[\s\-]+")`** — the `+` collapses consecutive separators (e.g. `" - "`), so empty strings only arise from leading/trailing separators, which `next(..., "")` silently skips.
- **`next(c.upper() for c in part if c.isalpha(), "")`** — skips leading punctuation like `_` or `,` before grabbing the first real letter. The default `""` means fully-punctuation segments contribute nothing.
- No mutation, no loops with manual index tracking — one clean generator expression per part.

### Student

Thanks for walking me through this! I can see how the solution works now. Let me make sure I understand the key pieces:

1. **`re.split(r"[\s\-]+")`** splits on whitespace and hyphens, and the `+` means consecutive separators get treated as one break—so `" - "` doesn't create extra empty strings we'd have to worry about.

2. **`next((c.upper() for c in part if c.isalpha()), "")`** is the clever bit—it iterates through each character in a part, finds the first alphabetic one, uppercases it, and returns it. If there's no alphabetic character at all, it returns `""` instead of crashing.

3. The outer `"".join(...)` just concatenates all those first letters together.

Let me trace through one example to confirm I've got it:
- Input: `"First In, First Out"`
- After split: `["First", "In,", "First", "Out"]`
- For each part, grab first alpha: `F`, `I`, `F`, `O`
- Join: `"FIFO"` ✓

That makes sense. One question though—what happens if we pass an empty string or a string with no alphabetic characters at all? Would we just get an empty acronym back?

---

## Turn 2

### Tutor

Tutor: Your trace is exactly right, and your intuition on the edge cases is correct too — let's verify:

**Empty string `""`:**
```
re.split(r"[\s\-]+", "")  →  [""]
next(... for c in "" if c.isalpha(), "")  →  ""   # generator empty, hits default
"".join([""])  →  ""
```

**No alphabetic characters `"123 - 456"`:**
```
split  →  ["123", "456"]
next(...)  →  "",  ""   # no c.isalpha() ever fires, default "" each time
"".join(...)  →  ""
```

Both return `""` — no crash, no surprise. That's the whole point of the `""` default in `next()`. Without it:

```python
next(c.upper() for c in part if c.isalpha())
# raises StopIteration if no alpha char found
```

So the default acts as a **safe fallback** that also doubles as a no-op in the final `join`.

---

One subtle point worth noting — `re.split` on an empty string behaves a little oddly:

```python
re.split(r"[\s\-]+", "")    # → [""]   one empty string
re.split(r"[\s\-]+", "  ")  # → ["", ""]  two empty strings
```

But since every empty string produces `""` via `next`, it doesn't matter how many you get — `join` flattens them all away. The design is **robust by composition**, not by explicit guarding.

### Student

Ah, that's really helpful! I see now—the `""` default in `next()` is doing double duty: it's both a safety net *and* a way to handle edge cases elegantly. Since `"".join(["", "", ""])` just gives `""`, all those empty contributions disappear automatically.

I was worried there might be some weird off-by-one or trailing-character bug lurking in there, but the design just... sidesteps it by making empty contributions a no-op.

Let me verify my understanding one more time with a tricky case—what if someone passes `"---"` (just hyphens)?

```
re.split(r"[\s\-]+", "---")  →  ["", ""]   # leading/trailing empty from the separators
next(... for c in "" if c.isalpha(), "")  →  "",  ""
"".join(...)  →  ""
```

So that also returns `""` cleanly, right? No weird crash or leftover separator character.

I think I've got the full picture now. The solution is solid—it handles the main cases cleanly and the edge cases just fall out naturally from the design. Thanks for breaking down how `next()` with a default works; that pattern is really useful when you want to safely extract something from a generator without crashing.

<done/>

---

**Run end:** done after 2 turn(s) in 45.4s
