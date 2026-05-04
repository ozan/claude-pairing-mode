ones = [
    "", "one", "two", "three", "four", "five",
    "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen"
]
tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

def sub_hundred(n):
    if n < 20:
        return ones[n]
    return tens[n // 10] + ("-" + ones[n % 10] if n % 10 else "")

def number_to_words(n):
    if n == 1000:
        return "one thousand"
    if n >= 100:
        rest = n % 100
        return ones[n // 100] + " hundred" + (" and " + sub_hundred(rest) if rest else "")
    return sub_hundred(n)

def letter_count(s):
    return sum(1 for c in s if c.isalpha())

print(sum(letter_count(number_to_words(n)) for n in range(1, 1001)))
