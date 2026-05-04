ONES = [
    '', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
    'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen',
    'seventeen', 'eighteen', 'nineteen',
]

TENS = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']


def say_below_20(n):
    """1–19"""
    return ONES[n]


def say_below_100(n):
    """1–99"""
    if n < 20:
        return say_below_20(n)
    tens, ones = divmod(n, 10)
    return TENS[tens] + ('-' + ONES[ones] if ones else '')


def say_below_1000(n):
    """1–999"""
    if n < 100:
        return say_below_100(n)
    hundreds, remainder = divmod(n, 100)
    base = ONES[hundreds] + ' hundred'
    if remainder:
        return base + ' and ' + say_below_100(remainder)
    return base


def say(n):
    if n == 1000:
        return 'one thousand'
    return say_below_1000(n)


def count_letters(s):
    return sum(c.isalpha() for c in s)


assert sum(count_letters(say(n)) for n in range(1, 6)) == 19, "spot-check failed"

total = sum(count_letters(say(n)) for n in range(1, 1001))
print(total)
