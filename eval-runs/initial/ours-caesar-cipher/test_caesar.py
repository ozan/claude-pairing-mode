from caesar import encode, decode


def test_encode_basic():
    assert encode("Hello", 3) == "Khoor"

def test_decode_basic():
    assert decode("Khoor", 3) == "Hello"

def test_roundtrip():
    assert decode(encode("Hello, World!", 7), 7) == "Hello, World!"

def test_lowercase_preserved():
    assert encode("abc", 1) == "bcd"

def test_uppercase_preserved():
    assert encode("ABC", 1) == "BCD"

def test_wrap_around_lower():
    assert encode("xyz", 3) == "abc"

def test_wrap_around_upper():
    assert encode("XYZ", 3) == "ABC"

def test_non_letters_unchanged():
    assert encode("a1b2c3!", 5) == "f1g2h3!"

def test_zero_shift():
    assert encode("test", 0) == "test"

def test_full_rotation():
    assert encode("test", 26) == "test"

def test_rot13_self_inverse():
    assert encode(encode("Hello", 13), 13) == "Hello"

def test_negative_shift():
    assert encode("def", -3) == "abc"
