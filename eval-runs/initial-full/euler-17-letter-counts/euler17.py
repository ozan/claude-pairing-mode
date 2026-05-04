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
    t, o = divmod(n, 10)
    return tens[t] + ("-" + ones[o] if o else "")

def number_to_words(n):
    if n == 1000:
        return "one thousand"
    if n >= 100:
        h, remainder = divmod(n, 100)
        base = ones[h] + " hundred"
        if remainder:                          # <-- the key guard
            base += " and " + below_hundred(remainder)
        return base
    return below_hundred(n)

def letter_count(s):
    return sum(c.isalpha() for c in s)

total = sum(letter_count(number_to_words(n)) for n in range(1, 1001))
print(total)

# spot-check a few
for n in [1, 12, 21, 99, 100, 115, 342, 1000]:
    print(f"{n:4d} -> {number_to_words(n)!r:40s}  ({letter_count(number_to_words(n))} letters)")
