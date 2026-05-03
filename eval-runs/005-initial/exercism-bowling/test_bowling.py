from bowling import score
import pytest

def test_gutter_game():
    assert score([0] * 20) == 0

def test_perfect_game():
    assert score([10] * 12) == 300

def test_all_spares():
    assert score([5, 5] * 9 + [5, 5, 5]) == 150

def test_one_spare():
    assert score([5, 5, 3] + [0] * 17) == 16

def test_one_strike():
    assert score([10, 3, 4] + [0] * 16) == 24

def test_invalid_pin_count():
    with pytest.raises(ValueError):
        score([11, 0] * 10)

def test_negative_pins():
    with pytest.raises(ValueError):
        score([-1, 5] + [0] * 18)

def test_incomplete_game():
    with pytest.raises(ValueError):
        score([5] * 15)

def test_incomplete_spare():
    with pytest.raises(ValueError):
        score([5, 5] * 9 + [5])

def test_frame_exceeds_ten():
    with pytest.raises(ValueError):
        score([5, 6] + [0] * 18)

def test_tenth_strike_valid_bonus():
    # [10,10,5]: frame-10 strike, first bonus strike, second bonus 5 — valid
    assert score([0] * 18 + [10, 10, 5]) == 25

def test_tenth_strike_invalid_bonus():
    # [10, 5, 6]: first bonus not a strike, 5+6>10 — invalid
    with pytest.raises(ValueError):
        score([0] * 18 + [10, 5, 6])
