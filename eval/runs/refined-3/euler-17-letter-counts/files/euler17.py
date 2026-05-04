ones = ['','one','two','three','four','five','six','seven',
        'eight','nine','ten','eleven','twelve','thirteen',
        'fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
tens = ['','','twenty','thirty','forty','fifty',
        'sixty','seventy','eighty','ninety']

def say_below_100(n):
    if n < 20:
        return ones[n]   # ones[0] == '' covers n=0
    return tens[n//10] + ('-' + ones[n%10] if n%10 else '')

def number_to_words(n):
    if n == 1000:
        return 'one thousand'
    if n >= 100:
        remainder = n % 100
        tail = ' and ' + say_below_100(remainder) if remainder else ''
        return ones[n//100] + ' hundred' + tail
    return say_below_100(n)

print(sum(len(number_to_words(n).replace(' ','').replace('-','')) for n in range(1, 1001)))
