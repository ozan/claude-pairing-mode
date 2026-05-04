# euler-17-letter-counts

- Source: `project-euler`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Output style: `Learning`
- Started: 2026-05-03T19:59:58.973Z

---

## Turn 1

**User:**

Project Euler #17: if all numbers from 1 to 1000 inclusive are written out in British English (e.g. 342 = 'three hundred and forty-two'), how many letters are used in total? (Spaces and hyphens don't count.)

**Pair:**

Assistant: ## Project Euler #17

Let me build up the count layer by layer.

---

### Layer 1 — Units (1–9)

| Word | Letters |
|------|---------|
| one, two, six | 3 each |
| four, five, nine | 4 each |
| three, seven, eight | 5 each |

**Sum = 3+3+5+4+4+3+5+5+4 = 36**

---

### Layer 2 — Teens (10–19)

ten(3) + eleven(6) + twelve(6) + thirteen(8) + fourteen(8) + fifteen(7) + sixteen(7) + seventeen(9) + eighteen(8) + nineteen(8)

**Sum = 70**

---

### Layer 3 — Tens (20–99)

Each tens-word appears **10 times** (once for the round number, once each with units 1–9):

| Word | Letters | ×10 |
|------|---------|-----|
| twenty, thirty | 6 | 60, 60 |
| forty, fifty, sixty | 5 | 50, 50, 50 |
| seventy | 7 | 70 |
| eighty, ninety | 6 | 60, 60 |

Tens-words total: **460**

Each unit word (1–9) appears once in each of the 8 decades (20s–90s):
36 × 8 = **288**

**20–99 total = 748**

---

### Running total: 1–99 = 36 + 70 + 748 = **854**

---

### Layer 4 — Hundreds (100–999)

For each of the 9 centuries (100–999), you get:

| Component | Letters | Count |
|-----------|---------|-------|
| Hundreds-digit word (one–nine, ×100 each) | 36 total | ×100 → **3,600** |
| "hundred" (7 letters) | 7 | 9×100 → **6,300** |
| "and" (3 letters, for X01–X99 only) | 3 | 9×99 → **2,673** |
| The full 1–99 tail (once per century) | 854 | ×9 → **7,686** |

**100–999 total = 3,600 + 6,300 + 2,673 + 7,686 = 20,259**

---

### Layer 5 — 1000

"**one thousand**" → `onethousand` = **11 letters**

---

### Grand Total

| Range | Letters |
|-------|---------|
| 1–99 | 854 |
| 100–999 | 20,259 |
| 1000 | 11 |
| **Total** | **21,124** |

---

## Turn 2 (final)

**User:**

Great! Let me verify this answer by coding it up—that's the most reliable way to check.Perfect! ✓

The computation confirms my manual breakdown:

- **1–9**: 36 letters
- **10–19**: 70 letters  
- **20–99**: 748 letters
- **1–99**: 854 letters
- **100–999**: 20,259 letters
- **1000**: 11 letters

**Answer: 21,124 letters**

The spot checks confirm the logic is right:
- `342` = "threehundredandfortytwo" = 23 letters ✓
- `100` = "onehundred" = 10 letters (no "and" for round hundreds) ✓
- `101` = "onehundredandone" = 16 letters (the "and" only appears for non-zero remainders) ✓

<done/>

---

**Run end**: done after 1 turn (56s)
