import string, random
from caesar import encode, decode

# --- explicit boundary cases (spec documentation) ---

def test_basic():    assert encode('Hello, World!', 13) == 'Uryyb, Jbeyq!'
def test_case():     assert encode('abc', 1) == 'bcd'
def test_wrap():     assert encode('xyz', 3) == 'abc'
def test_upper():    assert encode('XYZ', 3) == 'ABC'
def test_nonalpha(): assert encode('a1!', 1) == 'b1!'
def test_shift26():  assert encode('Hello', 26) == 'Hello'
def test_neg():      assert encode('bcd', -1) == 'abc'

def test_decode():
    assert decode(encode('Secret msg 42!', 7), 7) == 'Secret msg 42!'

# --- property: encode/decode are inverses across random inputs ---

def test_roundtrip():
    for _ in range(200):
        text = ''.join(random.choices(string.printable, k=40))
        shift = random.randint(-100, 100)
        assert decode(encode(text, shift), shift) == text
