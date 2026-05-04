ones = [
    '', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
    'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen',
    'seventeen', 'eighteen', 'nineteen'
]
tens = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']

def spell(n):
    if n == 1000:
        return 'one thousand'
    if n >= 100:
        h, remainder = divmod(n, 100)
        # ??? hundred [and] remainder
        pass
    if n >= 20:
        t, o = divmod(n, 10)
        return tens[t] + ('-' + ones[o] if o else '')
    return ones[n]

total = sum(len(spell(n).replace(' ', '').replace('-', '')) for n in range(1, 1001))
print(total)
