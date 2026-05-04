ones = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven',
        'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen',
        'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
tens = ['', '', 'twenty', 'thirty', 'forty', 'fifty',
        'sixty', 'seventy', 'eighty', 'ninety']

def spell(n):
    if n == 1000: return 'onethousand'
    if n < 20:    return ones[n]
    if n < 100:   return tens[n // 10] + spell(n % 10)
    rest = spell(n % 100)
    return spell(n // 100) + 'hundred' + ('and' + rest if rest else '')

# Sanity checks
assert spell(1)    == 'one'
assert spell(12)   == 'twelve'
assert spell(20)   == 'twenty'
assert spell(100)  == 'onehundred'
assert spell(115)  == 'onehundredandfifteen'
assert spell(342)  == 'threehundredandfortytwo'
assert spell(1000) == 'onethousand'

answer = sum(len(spell(n)) for n in range(1, 1001))
print(answer)
