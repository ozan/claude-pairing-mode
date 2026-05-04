# euler-17-letter-counts

- Source: `project-euler`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:31:21.746Z

---

## Turn 1

**User:**

Project Euler #17: if all numbers from 1 to 1000 inclusive are written out in British English (e.g. 342 = 'three hundred and forty-two'), how many letters are used in total? (Spaces and hyphens don't count.)

**Pair:**

Assistant: ## Solution

I'll work through this systematically, building up from small numbers.

### Letter counts for building blocks

**Ones (1–9):** one(3), two(3), three(5), four(4), five(4), six(3), seven(5), eight(5), nine(4) → **sum = 36**

**Teens (10–19):** ten(3), eleven(6), twelve(6), thirteen(8), fourteen(8), fifteen(7), sixteen(7), seventeen(9), eighteen(8), nineteen(8) → **sum = 70**

**Tens words (20–90):** twenty(6), thirty(6), forty(5), fifty(5), sixty(5), seventy(7), eighty(6), ninety(6) → **sum = 46**

---

### 1–99

| Range | Calculation | Subtotal |
|-------|-------------|----------|
| 1–9 | 36 | 36 |
| 10–19 | 70 | 70 |
| 20–99 | Each tens word appears 10×: 46×10 = 460; ones digits (1–9) appear once per decade (×8): 36×8 = 288 | 748 |
| **Total 1–99** | | **854** |

---

### 100–999

For each century X (1–9), we have 100 numbers:
- **X00** = "X hundred" → `ones[X]` + 7 letters
- **X01–X99** = "X hundred **and** Y" → `ones[X]` + 7 + 3 + `letters(Y)` each

Summing across all 100 numbers in century X:
```
100 × ones[X] + 7 + 99×(7+3) + sum(1–99)
= 100 × ones[X] + 7 + 990 + 854
= 100 × ones[X] + 1851
```

Across all 9 centuries:
```
100 × 36  +  9 × 1851
=  3,600  +  16,659  =  20,259
```

---

### 1000

"one thousand" = 3 + 8 = **11**

---

### Grand Total

| Range | Letters |
|-------|---------|
| 1–99 | 854 |
| 100–999 | 20,259 |
| 1000 | 11 |
| **Total** | **21,124** |

The answer is **21,124**.

---

## Turn 2 (final)

**User:**

Great! You've worked through the logic systematically. Let me verify this answer by implementing it as code:Perfect! ✓ The code confirms your manual solution:

**Answer: 21,124**

### Verification breakdown:
- **1–99:** 854 letters
- **100–999:** 20,259 letters  
- **1000:** 11 letters ("one thousand")

The example also confirms the counting method: 342 = "three hundred and forty-two" = 5 + 7 + 3 + 5 + 3 = **23 letters** ✓

Your mathematical reasoning was spot-on—breaking down each century into its 100-number pattern and calculating the formula `100 × ones[X] + 1851` is elegant. The code validates every number 1–1000 and arrives at the same answer.

<done/>

---

**Run end**: done after 1 turn (67s)
