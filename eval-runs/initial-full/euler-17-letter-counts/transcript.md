# euler-17-letter-counts

- Source: `project-euler`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T08:25:32.236Z

---

## Turn 1

**User:**

Project Euler #17: if all numbers from 1 to 1000 inclusive are written out in British English (e.g. 342 = 'three hundred and forty-two'), how many letters are used in total? (Spaces and hyphens don't count.)

**Pair:**

Assistant: Fun one. Before writing any code, let me ask you a design question about the number-to-words logic.

Assistant: The `propose_options` tool isn't loading, so let me just ask this directly before writing any code — it's a real trap in this problem.

**Quick question:** In British English, "three hundred and forty-two" has an "and", but what about "three hundred" exactly? Should the "and" appear there too?

The answer is **no** — exact multiples of 100 (100, 200, ..., 900) don't use "and". A common bug is unconditionally appending `" and " + remainder_words` without checking if the remainder is non-zero. Let's make sure we get that right.

Let me build the solution:

[Bash(ls euler17* 2>/dev/null || echo "no file yet")]
  no file yet

[Write(euler17.py)]
ones = [
    "", "one", "two", "three", "four", "five",
    "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen",
]
tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

def below_hundred(n):
    """Return words for 1–99."""
    if n < 20:
        return ones[n]
… (24 more lines)

[Bash(python3 euler17.py)]
  21124
     1 -> 'one'                                     (3 letters)
    12 -> 'twelve'                                  (6 letters)
    21 -> 'twenty-one'                              (9 letters)
    99 -> 'ninety-nine'                             (10 letters)
   100 -> 'one hundred'                             (10 letters)
   115 -> 'one hundred and fifteen'                 (20 letters)
   342 -> 'three hundred and forty-two'             (23 letters)
  1000 -> 'one thousand'                            (11 letters)

Assistant: **Answer: 21124**

The spot-checks look right — "three hundred and forty-two" = 23 letters (matching the problem statement), and "one hundred" has no "and".

A few design decisions worth noting:

- **`divmod`** is idiomatic for splitting hundreds/tens/ones — cleaner than separate `//` and `%`.
- The hyphen in "forty-two" is excluded from the count automatically because `c.isalpha()` skips it — no need for a separate strip step.
- **The `if remainder:` guard** is the crux. Without it, "one hundred" becomes "one hundred and " — 3 extra phantom "and"s × 9 hundreds = 27 letters of error (actually more, since only exact-hundred multiples are affected, but the direction is clear).

Want to dig into any part of this, or move on to another problem?

---

## Turn 2 (final)

**User:**

Looks good. The spot checks all verify — "three hundred and forty-two" is indeed 23 letters, and "one hundred" correctly has no "and". 

The key insight you flagged (`if remainder:`) is really the crux. I can see how it's easy to mess up — without that guard, you'd be adding phantom " and " to every 100, 200, 300, etc., which would definitely throw off the final count.

The `divmod` approach for splitting the number is clean too. And using `c.isalpha()` to filter means hyphens and spaces are automatically excluded — no special handling needed.

I'm confident 21124 is right. The logic handles all the cases:
- Below 20 (special names)
- 20–99 (tens + ones with hyphen)
- 100–999 (hundreds + "and" + remainder, conditional)
- 1000 (special case)

<done/>

---

**Run end**: done after 1 turn (74s)
