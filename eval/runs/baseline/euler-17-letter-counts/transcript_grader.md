# euler-17-letter-counts

- Condition: `baseline`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T20:52:53

## Initial prompt

Project Euler #17: if all numbers from 1 to 1000 inclusive are written out in British English (e.g. 342 = 'three hundred and forty-two'), how many letters are used in total? (Spaces and hyphens don't count.)

---

## Turn 1

### Tutor

Tutor: ## Solving Project Euler #17

Let me count letter by letter, group by group.

### Letter counts for key words

| Word | Letters | | Word | Letters |
|------|---------|---|------|---------|
| one | 3 | | ten | 3 |
| two | 3 | | eleven | 6 |
| three | 5 | | twelve | 6 |
| four | 4 | | thirteen | 8 |
| five | 4 | | fourteen | 8 |
| six | 3 | | fifteen | 7 |
| seven | 5 | | sixteen | 7 |
| eight | 5 | | seventeen | 9 |
| nine | 4 | | eighteen | 8 |
| | | | nineteen | 8 |
| twenty | 6 | thirty | 6 | forty | 5 |
| fifty | 5 | sixty | 5 | seventy | 7 |
| eighty | 6 | ninety | 6 | | |
| **hundred** | **7** | **and** | **3** | **thousand** | **8** |

---

### Group 1–9
`3+3+5+4+4+3+5+5+4 = `**36**

### Group 10–19
`3+6+6+8+8+7+7+9+8+8 = `**70**

### Group 20–99
- **Tens digits** (each tens-word appears 10 times): `(6+6+5+5+5+7+6+6) × 10 = 46 × 10 =` **460**
- **Units digits** (digits 1–9 each appear once per decade, 8 decades): `36 × 8 =` **288**
- Subtotal: **748**

### Running total 1–99: `36 + 70 + 748 =` **854**

---

### Group 100–999

**"X hundred" prefix** (each appears 100 times for X00–X99):

| X | letters | ×100 |
|---|---------|------|
| one hundred | 10 | 1000 |
| two hundred | 10 | 1000 |
| three hundred | 12 | 1200 |
| four hundred | 11 | 1100 |
| five hundred | 11 | 1100 |
| six hundred | 10 | 1000 |
| seven hundred | 12 | 1200 |
| eight hundred | 12 | 1200 |
| nine hundred | 11 | 1100 |
| **Total** | **99** | **9900** |

**"and"** appears for X01–X99 (99 per hundred, 9 hundreds):
`99 × 9 × 3 =` **2673**

**The 1–99 tail** repeats once per hundred (9 times):
`854 × 9 =` **7686**

Subtotal 100–999: `9900 + 2673 + 7686 =` **20259**

---

### 1000
"one thousand" = `3 + 8 =` **11**

---

### Grand Total

| Range | Letters |
|-------|---------|
| 1–99 | 854 |
| 100–999 | 20,259 |
| 1000 | 11 |
| **Total** | **21,124** |

## **Answer: 21,124**

### Student

Thanks for walking through that! I'm going to work through this myself to make sure I understand it.

Let me start by verifying your letter counts for the basic words. I'll spot-check a few:
- "one" = o-n-e = 3 ✓
- "twenty" = t-w-e-n-t-y = 6 ✓
- "hundred" = h-u-n-d-r-e-d = 7 ✓

OK, those look right.

Now let me trace through your logic for groups 1–9 and 10–19. I'm counting:
- 1–9: one through nine = 3+3+5+4+4+3+5+5+4 = 36 ✓
- 10–19: ten through nineteen = 3+6+6+8+8+7+7+9+8+8 = 70 ✓

For 20–99, I want to make sure I follow the breakdown:
- Each tens word (twenty, thirty, ..., ninety) appears 10 times: 46 × 10 = 460 ✓
- The units 1–9 appear once per decade, across 8 decades: 36 × 8 = 288 ✓
- Total for 20–99: 748 ✓

So 1–99 = 854. Good.

Now for 100–999, I'm following your structure. For the "X hundred" prefix, let me verify one entry:
- "three hundred" = 3+5 (three) + 7 (hundred) = 12 letters, appears 100 times = 1200 ✓

And "and" appears in numbers like 101, 102, ..., 199, 201, ..., 999 (but not 100, 200, ..., 900). So that's 99 instances per hundred × 9 hundreds × 3 letters = 2673 ✓

Then the 1–99 pattern repeats 9 times: 854 × 9 = 7686 ✓

100–999 = 9900 + 2673 + 7686 = 20259 ✓

And 1000 = "one thousand" = 3 + 8 = 11 ✓

**Grand total: 854 + 20259 + 11 = 21124**

I think I've got it. This breakdown makes sense — breaking it into the digit groups and being careful about when "and" appears is the key. Thanks for the detailed walkthrough!

<done/>

---

**Run end:** done after 1 turn(s) in 39.6s
