from roman_numerals import to_roman

def test_to_roman():
    # Boundaries
    assert to_roman(1) == 'I'
    assert to_roman(3999) == 'MMMCMXCIX'

    # All 6 subtractive pairs
    assert to_roman(4) == 'IV'
    assert to_roman(9) == 'IX'
    assert to_roman(40) == 'XL'
    assert to_roman(90) == 'XC'
    assert to_roman(400) == 'CD'
    assert to_roman(900) == 'CM'

    # Mid-range composites
    assert to_roman(1994) == 'MCMXCIV'
    assert to_roman(58) == 'LVIII'

if __name__ == '__main__':
    test_to_roman()
    print('All tests passed')
