from valid_parentheses import is_valid

def test_valid_simple():
    assert is_valid("()") is True

def test_valid_mixed():
    assert is_valid("()[]{}") is True

def test_valid_nested():
    assert is_valid("{[()]}") is True

def test_invalid_mismatch():
    assert is_valid("(]") is False

def test_invalid_unclosed_openers():
    assert is_valid("((") is False

def test_invalid_closer_only():
    assert is_valid(")") is False

def test_empty_string():
    assert is_valid("") is True
