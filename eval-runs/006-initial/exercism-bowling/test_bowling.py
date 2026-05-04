import pytest
from bowling import BowlingGame


def make_game(rolls):
    g = BowlingGame()
    for r in rolls:
        g.roll(r)
    return g


def test_gutter_game():
    g = make_game([0] * 20)
    assert g.score() == 0


def test_all_ones():
    g = make_game([1] * 20)
    assert g.score() == 20


def test_spare_in_first_frame():
    # 5+5 spare, then 3, rest gutter
    g = make_game([5, 5, 3] + [0] * 17)
    assert g.score() == 16  # 10+3 + 3 + 0*17


def test_strike_in_first_frame():
    # strike, then 3+4, rest gutter
    g = make_game([10, 3, 4] + [0] * 16)
    assert g.score() == 24  # 10+3+4 + 3+4 + 0*16


def test_perfect_game():
    # 12 strikes
    g = make_game([10] * 12)
    assert g.score() == 300


def test_tenth_frame_spare():
    g = make_game([0] * 18 + [5, 5, 7])
    assert g.score() == 17  # 10+7 = 17 for 10th, rest 0


def test_tenth_frame_three_strikes():
    g = make_game([0] * 18 + [10, 10, 10])
    assert g.score() == 30


def test_score_before_game_over_raises():
    g = BowlingGame()
    g.roll(5)
    with pytest.raises(Exception, match="end of the game"):
        g.score()


def test_too_many_rolls_raises():
    g = make_game([0] * 20)
    with pytest.raises(Exception, match="Game is already over"):
        g.roll(1)


def test_negative_pins_raises():
    g = BowlingGame()
    with pytest.raises(Exception):
        g.roll(-1)


def test_pins_over_10_raises():
    g = BowlingGame()
    with pytest.raises(Exception):
        g.roll(11)


def test_frame_pins_over_10_raises():
    g = BowlingGame()
    g.roll(6)
    with pytest.raises(Exception):
        g.roll(5)


def test_tenth_frame_strike_then_invalid_bonus():
    # 10, 6, 5 is invalid: after a strike, second=6 leaves 4 pins, can't knock 5
    g = BowlingGame()
    for r in [0] * 18 + [10, 6]:
        g.roll(r)
    with pytest.raises(Exception):
        g.roll(5)


def test_tenth_frame_strike_then_valid_bonus():
    # 10, 6, 4 is valid: second=6, third=4 (spare on the mini-frame)
    g = make_game([0] * 18 + [10, 6, 4])
    assert g.score() == 20  # 10+6+4 = 20


def test_tenth_frame_double_strike_then_any():
    # 10, 10, 7 is valid: after two strikes, fresh 10 pins for third
    g = make_game([0] * 18 + [10, 10, 7])
    assert g.score() == 27


def test_typical_game():
    # Famous example: 20+14+10+5+5+... let's use the Exercism standard
    # rolls: [3,6, 6,3, 10, 8,1, 10, 10, 9,0, 7,3, 4,4, 10, 9,0]
    # Actually let's compute manually:
    # Frame 1: 3+6 = 9
    # Frame 2: 6+3 = 9
    # Frame 3: strike 10+8+1 = 19
    # Frame 4: 8+1 = 9
    # Frame 5: strike 10+10+9 = 29
    # Frame 6: strike 10+9+0 = 19
    # Frame 7: 9+0 = 9
    # Frame 8: 7+3 spare = 10+4 = 14
    # Frame 9: 4+4 = 8
    # Frame 10: strike 10+9+0 = 19
    # Total: 9+9+19+9+29+19+9+14+8+19 = 144
    g = make_game([3, 6, 6, 3, 10, 8, 1, 10, 10, 9, 0, 7, 3, 4, 4, 10, 9, 0])
    assert g.score() == 144
