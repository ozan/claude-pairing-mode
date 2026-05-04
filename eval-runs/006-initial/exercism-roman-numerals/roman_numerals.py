# All 13 value→symbol pairs in descending order.
# Subtractive forms (CM, CD, XC, XL, IX, IV) sit naturally alongside additive ones.
VALUES = [
    (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
    (100,  'C'), (90,  'XC'), (50,  'L'), (40,  'XL'),
    (10,   'X'), (9,   'IX'), (5,   'V'), (4,   'IV'),
    (1,    'I'),
]


def to_roman(n: int) -> str:
    """Convert an integer 1–3999 to a Roman numeral string."""
    result = ''
    for value, numeral in VALUES:
        while n >= value:
            result += numeral
            n -= value
    return result


if __name__ == '__main__':
    tests = {
        1: 'I', 4: 'IV', 9: 'IX', 14: 'XIV', 40: 'XL',
        58: 'LVIII', 90: 'XC', 399: 'CCCXCIX', 400: 'CD',
        900: 'CM', 1994: 'MCMXCIV', 3999: 'MMMCMXCIX',
    }
    for n, expected in tests.items():
        got = to_roman(n)
        status = '✓' if got == expected else f'✗ expected {expected}'
        print(f'{n:>4} → {got:<12} {status}')
