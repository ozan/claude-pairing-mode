# euler-17-letter-counts

- Condition: `learning`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:06:50

## Initial prompt

Project Euler #17: if all numbers from 1 to 1000 inclusive are written out in British English (e.g. 342 = 'three hundred and forty-two'), how many letters are used in total? (Spaces and hyphens don't count.)

---

## Turn 1

### Tutor

Tutor: ## Approach

Break the problem into ranges, compute letter counts analytically rather than string-by-string.

---

### Building Blocks

| Range | Words | Letters |
|-------|-------|---------|
| **1–9** | one, two, three, four, five, six, seven, eight, nine | 3,3,5,4,4,3,5,5,4 → **sum = 36** |
| **10–19** | ten, eleven, twelve, thirteen, fourteen, fifteen, sixteen, seventeen, eighteen, nineteen | 3,6,6,8,8,7,7,9,8,8 → **sum = 70** |
| **Tens words** | twenty, thirty, forty, fifty, sixty, seventy, eighty, ninety | 6,6,5,5,5,7,6,6 → **sum = 46** |

---

### Sum for 1–99

**20–99:** Each decade word appears 10 times (e.g. "twenty" for 20–29), plus units 1–9 appear once each per decade (8 decades):

```
(46 × 10) + (8 × 36) = 460 + 288 = 748
```

**Total 1–99:**
```
36 + 70 + 748 = 854
```

---

### Sum for 100–999

For each century **X** (1–9), across all 100 numbers:
- Every number contributes `ones[X] + 7` for "**X** hundred"  
- The 99 non-round numbers also add 3 for "**and**"  
- The sub-100 tails 01–99 contribute the 1–99 sum (854)

```
Per century X = 100 × (ones[X] + 7) + 99 × 3 + 854
             = 100 × ones[X] + 700 + 297 + 854
             = 100 × ones[X] + 1851
```

Summing over X = 1–9:
```
100 × 36 + 9 × 1851 = 3600 + 16659 = 20259
```

---

### 1000

"one thousand" = 3 + 8 = **11**

---

### Grand Total

```
  1–99:    854
100–999: 20259
   1000:    11
─────────────
  Total: 21124
```

> **The answer is 21,124.**

**Spot-check:** "three hundred and forty-two" → three(5) + hundred(7) + and(3) + forty(5) + two(3) = **23 letters** ✓

### Student

Thanks for walking me through this! I really appreciate the structured breakdown. Let me make sure I understand the logic correctly before I code it up.

So the key insight is:
- Instead of generating strings for all 1000 numbers, we compute letter counts analytically by understanding the patterns (how many times each word appears, etc.)
- For 1–99, we handle the teens (10–19) separately since they don't follow the "tens + units" pattern
- For 100–999, we recognize that each century block (100–199, 200–299, etc.) follows the same structure: the "X hundred" prefix, the "and" connector (except for the round hundreds like 100, 200), and then the 1–99 pattern repeating
- Then just add 1000 separately

I think I've got it. Let me code this up:

```python
ones = {1:3, 2:3, 3:5, 4:4, 5:4, 6:3, 7:5, 8:5, 9:4}  # one–nine
teens = {10:3, 11:6, 12:6, 13:8, 14:8, 15:7, 16:7, 17:9, 18:8, 19:8}  # ten–nineteen
tens = {2:6, 3:6, 4:5, 5:5, 6:5, 7:7, 8:6, 9:6}  # twenty, thirty, ..., ninety

# 1–9: sum of ones
sum_1_to_9 = sum(ones.values())  # 36

# 10–19: sum of teens
sum_10_to_19 = sum(teens.values())  # 70

# 20–99: each tens word appears 10 times, plus units 1–9 once per decade (8 decades)
sum_20_to_99 = sum(tens.values()) * 10 + 8 * sum_1_to_9  # 46*10 + 8*36 = 748

# 1–99 total
sum_1_to_99 = sum_1_to_9 + sum_10_to_19 + sum_20_to_99  # 854

# 100–999: for each century X (1–9)
sum_100_to_999 = 0
for x in range(1, 10):
    # "X hundred" appears 100 times, plus "and" appears 99 times (not for round hundreds)
    per_century = 100 * (ones[x] + 7) + 99 * 3 + sum_1_to_99
    sum_100_to_999 += per_century

# 1000: "one thousand"
sum_1000 = 11  # one(3) + thousand(8)

# Total
total = sum_1_to_99 + sum_100_to_999 + sum_1000
print(total)
```

Let me trace through one century to verify:
- For X=3 (300–399): ones[3]=5 (three)
- Per century = 100*(5+7) + 99*3 + 854 = 1200 + 297 + 854 = 2351
- That matches the formula 100*5 + 1851 = 500 + 1851 = 2351 ✓

Running this should give 21124. Does this look right to you?

---

## Turn 2

### Tutor

Tutor: Your understanding is spot-on, and the code looks correct. Let me run it to confirm:

[Bash(python3 -c "
ones = {1:3, 2:3, 3:5, 4:4, 5:4, 6:3, 7:5, 8:5, 9:4}
teens = {10:3, 11:6, 12:6, 13:8, 14:8, 15:7, 16:7, 17:9, 18:8, 19:8}
tens = {2:6, 3:6, 4:5, 5:5, 6:5, 7:7, 8:6, 9:6}

sum_1_to_9 = sum(ones.values())
sum_10_to_19 = sum(teens.values())
sum_20_to_99 = sum(tens.values()) * 10 + 8 * sum_1_to_9
sum_1_to_99 = sum_1_to_9 + sum_10_to_19 + sum_20_to_99

sum_100_to_999 = 0
for x in range(1, 10):
    per_century = 100 * (ones[x] + 7) + 99 * 3 + sum_1_to_99
    sum_100_to_999 += per_century

sum_1000 = 11
total = sum_1_to_99 + sum_100_to_999 + sum_1000
print(total)
"
)]
  21124

Tutor: ✅ **21124** — confirmed.

Your summary of the key insights is exactly right. One small thing worth making explicit in case it trips you up later:

> **Why teens are special:** Numbers 13–19 look like they *should* decompose (e.g. "three-teen"), but they don't — "thirteen" is a single fused word, not "ten" + "three". So they need their own lookup table rather than being handled by the `tens + ones` formula used for 20–99.

Everything else in your code is clean. The `ones` dict does double duty — it defines letter counts for 1–9 on their own *and* gets reused as the "X hundred" prefix lookup for 100–999, which is a nice economy.

### Student

Perfect! That confirmation is really helpful. And yeah, that note about the teens is exactly the kind of gotcha I would have missed if I hadn't thought carefully about it — treating 13 as "ten + three" would have been a silent bug.

I'm satisfied with this solution. The analytical approach is much faster than string-building, and breaking it down into ranges made the logic actually manageable to understand and verify. The spot-checks (like verifying 342 and tracing through century 3) gave me confidence in the answer.

Thanks for the structured walkthrough and the confirmation!

<done/>

---

**Run end:** done after 2 turn(s) in 68.9s
