import pytest
from evaluator import evaluate


# ── basic arithmetic ───────────────────────────────────────────────────────────

def test_addition():              assert evaluate("1 + 2")             == 3.0
def test_subtraction():           assert evaluate("5 - 3")             == 2.0
def test_multiplication():        assert evaluate("4 * 3")             == 12.0
def test_division():              assert evaluate("10 / 4")            == 2.5


# ── operator precedence ────────────────────────────────────────────────────────

def test_mul_before_add():        assert evaluate("3 + 4 * 2")         == 11.0
def test_mul_before_sub():        assert evaluate("10 - 2 * 3")        == 4.0
def test_div_before_add():        assert evaluate("8 + 6 / 2")         == 11.0
def test_div_before_sub():        assert evaluate("8 - 6 / 2")         == 5.0


# ── parentheses override precedence ───────────────────────────────────────────

def test_given_example():         assert evaluate("3 + 4 * (2 - 1)")   == 7.0
def test_parens_force_add_first():assert evaluate("(3 + 4) * 2")       == 14.0
def test_nested_parens():         assert evaluate("((2 + 3) * (1 + 1))")== 10.0
def test_deep_nesting():          assert evaluate("(((3)))")            == 3.0


# ── left-associativity ─────────────────────────────────────────────────────────

def test_left_assoc_sub():        assert evaluate("10 - 3 - 2")        == 5.0   # (10-3)-2
def test_left_assoc_div():        assert evaluate("24 / 4 / 2")        == 3.0   # (24/4)/2


# ── unary operators ────────────────────────────────────────────────────────────

def test_unary_minus():           assert evaluate("-3 + 5")             == 2.0
def test_unary_plus():            assert evaluate("+5 - 3")             == 2.0
def test_double_unary_minus():    assert evaluate("--3")                == 3.0
def test_unary_in_parens():       assert evaluate("(-3) * 4")           == -12.0
def test_unary_minus_times():     assert evaluate("-3 * -2")            == 6.0


# ── whitespace ─────────────────────────────────────────────────────────────────

def test_no_spaces():             assert evaluate("2+3*4")              == 14.0
def test_extra_spaces():          assert evaluate("  2  +  3  ")        == 5.0


# ── floats and scientific notation ────────────────────────────────────────────

def test_decimal():               assert evaluate("1.5 * 2")            == 3.0
def test_trailing_dot():          assert evaluate("2. + 1")             == 3.0
def test_scientific():            assert evaluate("1e2 + 0.5e1")        == 105.0
def test_negative_exponent():     assert evaluate("1e-1 * 10")          == pytest.approx(1.0)


# ── error cases ────────────────────────────────────────────────────────────────

def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        evaluate("1 / 0")

def test_unexpected_char():
    with pytest.raises(SyntaxError):
        evaluate("1 ^ 2")

def test_mismatched_paren_open():
    with pytest.raises(SyntaxError):
        evaluate("(1 + 2")

def test_mismatched_paren_close():
    with pytest.raises(SyntaxError):
        evaluate("1 + 2)")

def test_empty_parens():
    with pytest.raises(SyntaxError):
        evaluate("()")

def test_trailing_operator():
    with pytest.raises(SyntaxError):
        evaluate("1 +")
