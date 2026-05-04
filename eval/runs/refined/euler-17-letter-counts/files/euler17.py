ones  = ['', 'one', 'two', 'three', 'four', 'five',
          'six', 'seven', 'eight', 'nine']
teens = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen',
          'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
tens  = ['', '', 'twenty', 'thirty', 'forty', 'fifty',
          'sixty', 'seventy', 'eighty', 'ninety']


def words_under_100(n):
    if n < 10:
        return ones[n]
    elif n < 20:
        return teens[n - 10]
    else:
        t, o = tens[n // 10], ones[n % 10]
        return f"{t}-{o}" if o else t


def number_to_words(n):
    if n == 1000:
        return 'one thousand'
    elif n >= 100:
        h = ones[n // 100] + ' hundred'
        r = n % 100
        return h + ' and ' + words_under_100(r) if r else h
    else:
        return words_under_100(n)


# Spot-checks
for n in [1, 12, 20, 42, 100, 115, 300, 342, 1000]:
    print(f"{n:4d} -> {number_to_words(n)!r}")

# Final answer
total = sum(
    len(number_to_words(n).replace(' ', '').replace('-', ''))
    for n in range(1, 1001)
)
print(f"\nTotal letters (1–1000): {total}")
