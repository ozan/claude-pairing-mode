# exercism-allergies

- Source: `exercism`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T02:53:42.668Z

---

## Turn 1

**User:**

Exercism 'Allergies': allergens encode as bitfield flags in a single int score (eggs=1, peanuts=2, shellfish=4, ... cats=128). Write `is_allergic_to(score, allergen)` and `allergies(score)` returning the list of allergens.

**Pair:**

Thinking: Let me think about this problem. The Allergies problem on Exercism involves a bitfield where each allergen is assigned a power of 2:
  
  - eggs = 1 (2^0)
  - peanuts = 2 (2^1)
  - shellfish = 4 (2^2)
  - strawberries = 8 (2^3)
  - tomatoes = 16 (2^4)
  
  
  - chocolate = 32 (2^5)
  - pollen = 64 (2^6)
  - cats = 128 (2^7)
  
  So `is_allergic_to(score, allergen)` checks if the bit for that allergen is set in score, and `allergies(score)` returns all allergens whose bits are set. I'm deciding between representing these as a list of tuples with names and bit values, or using an Enum with powers of 2 as values.
  
  Actually, Python's `IntFlag` enum is the most idiomatic approach here—it's specifically designed for bitfield flags and handles iteration and containment checks elegantly, whereas a plain dict would require more manual work.

Assistant: Good problem — it's a clean bitfield exercise. Before writing any code, let me ask about the data model since it shapes everything else.

Thinking: The tool isn't available as an MCP tool right now. Let me just proceed with the implementation and present options differently. I'll just write the code directly with a good explanation.
  
  Actually, let me think about what to do. The tool failed, so I'll just present the options in text and proceed with the implementation.
  
  Let me just explain both options and ask the user which they prefer, or just proceed with the better option.

Assistant: The tool isn't available right now, so let me just lay out the two approaches and my take:

**Option A — plain dict + bitwise**
```python
ALLERGENS = {'eggs': 1, 'peanuts': 2, ..., 'cats': 128}
is_allergic_to = lambda score, allergen: bool(score & ALLERGENS[allergen])
allergies = lambda score: [a for a, bit in ALLERGENS.items() if score & bit]
```

**Option B — `IntFlag` enum** (looks like the "right" tool for bitfields, but has a gotcha: `IntFlag(score)` for a score > 255 produces an unnamed remainder bit that leaks into iteration — confusing for external input you don't control)

I'll go with Option A. Let me write the file:

[Bash(ls allergies.py 2>/dev/null && echo exists || echo missing)]
  missing

[Write(allergies.py)]
ALLERGENS = {
    'eggs':         1,
    'peanuts':      2,
    'shellfish':    4,
    'strawberries': 8,
    'tomatoes':     16,
    'chocolate':    32,
    'pollen':       64,
    'cats':         128,
}


… (7 more lines)

Assistant: Let's verify it works:

[Bash(python3 - <<'EOF'
from allergies import is_allergic_to, allergies

# score 0 → nothing
assert allergies(0) == []

# score 1 → eggs only
assert allergies(1) == ['eggs']
assert is_allergic_to(1, 'eggs') is True
assert is_allergic_to(1, 'cats') is False

# score 255 → all allergens
all_8 = allergies(255)
assert set(all_8) == {'eggs','peanuts','shellfish','strawberries','tomatoes','chocolate','pollen','cats'}

# score > 255 — upper bits silently ignored
assert allergies(257) == ['eggs']   # 256 is bit 8, not in our map

print("All assertions passed ✓")
EOF)]
  All assertions passed ✓

Assistant: All good. A few things worth noting:

- **`score & bit`** is the core operation — it masks out everything except the one bit we care about. Non-zero means "set".
- **Scores > 255** are handled gracefully: any unknown high bits simply don't match anything in `ALLERGENS`, so they're silently ignored. This is why I avoided `IntFlag` — `IntFlag(257)` would surface a mysterious unnamed bit in its iteration.
- The dict preserves insertion order (Python 3.7+), so `allergies()` returns allergens in the canonical low-to-high-bit order, which matches Exercism's expected output.

Want to add tests, or move on to another problem?

---

## Turn 2 (final)

**User:**

I think we're good! The code works and handles the edge cases well (especially the > 255 bit silently being ignored rather than confusing things). I got what I needed out of this — understanding why the plain dict + bitwise approach is cleaner than `IntFlag` here, and seeing how the bit masking actually works.

I'll skip adding a full test suite and definitely won't pivot to a new problem. This one's done.

<done/>

---

**Run end**: done after 1 turn (44s)
