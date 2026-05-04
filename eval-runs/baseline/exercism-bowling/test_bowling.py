"""Tests for the bowling scorer, mirroring the Exercism test suite."""

import pytest
from bowling import BowlingGame, score


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def play(rolls: list[int]) -> BowlingGame:
    g = BowlingGame()
    for p in rolls:
        g.roll(p)
    return g


# ---------------------------------------------------------------------------
# Basic scoring
# ---------------------------------------------------------------------------

class TestBasicScoring:
    def test_all_gutters(self):
        assert score([0] * 20) == 0

    def test_all_ones(self):
        assert score([1] * 20) == 20

    def test_open_game(self):
        # 3+6, 3+6, 3+6, 3+6, 3+6, 3+6, 3+6, 3+6, 3+6, 3+6 => 90
        assert score([3, 6] * 10) == 90


# ---------------------------------------------------------------------------
# Spare scoring
# ---------------------------------------------------------------------------

class TestSpares:
    def test_spare_followed_by_zeros(self):
        # frame 1: spare (5+5), next roll bonus 0 => 10
        # rest: gutter => total 10
        rolls = [5, 5, 0] + [0] * 17
        assert score(rolls) == 10

    def test_spare_bonus_is_next_roll(self):
        # frame 1: spare (5+5), next roll 3 => 13
        # frame 2: 3+0 => 3
        # rest zeros
        rolls = [5, 5, 3, 0] + [0] * 16
        assert score(rolls) == 16

    def test_consecutive_spares(self):
        # frame1: 5+5=spare, bonus=5 => 15
        # frame2: 5+5=spare, bonus=5 => 15
        # frame3: 5+0 => 5
        # rest zeros
        rolls = [5, 5, 5, 5, 5, 0] + [0] * 14
        assert score(rolls) == 35

    def test_spare_in_last_frame(self):
        rolls = [0] * 18 + [7, 3, 7]   # 10th-frame spare + fill
        assert score(rolls) == 17


# ---------------------------------------------------------------------------
# Strike scoring
# ---------------------------------------------------------------------------

class TestStrikes:
    def test_strike_followed_by_zeros(self):
        rolls = [10, 0, 0] + [0] * 16
        assert score(rolls) == 10

    def test_strike_bonus_is_next_two_rolls(self):
        # frame1: strike, bonus=3+4 => 17
        # frame2: 3+4 => 7
        # rest zeros
        rolls = [10, 3, 4] + [0] * 16
        assert score(rolls) == 24

    def test_perfect_game(self):
        # 12 strikes => 300
        assert score([10] * 12) == 300

    def test_two_consecutive_strikes(self):
        # frame1: strike, bonus=10+3 => 23
        # frame2: strike, bonus=3+0 => 13
        # frame3: 3+0 => 3
        # frames 4-10: zeros
        # rolls used: 1+1+2+14 = 18 total
        rolls = [10, 10, 3, 0] + [0] * 14
        assert score(rolls) == 39

    def test_strike_in_last_frame(self):
        rolls = [0] * 18 + [10, 7, 3]   # 10th-frame strike + 2 fill rolls
        assert score(rolls) == 20

    def test_strike_then_spare_in_last_frame(self):
        rolls = [0] * 18 + [10, 3, 7]
        assert score(rolls) == 20


# ---------------------------------------------------------------------------
# Mixed / realistic games
# ---------------------------------------------------------------------------

class TestRealistic:
    def test_heart_break(self):
        # 11 strikes then 9 in the last fill roll
        rolls = [10] * 11 + [9]
        assert score(rolls) == 299

    def test_all_spares(self):
        # each frame: 5+5 spare, fill roll 5 at the end
        rolls = [5, 5] * 10 + [5]
        assert score(rolls) == 150

    def test_sample_game(self):
        # Exercism's canonical sample game
        # 1+4, 4+5, 6+4(spare), 5+5(spare), 10(strike), 0+1, 7+3(spare),
        # 6+4(spare), 10(strike), 2+8(spare)+6
        rolls = [1, 4, 4, 5, 6, 4, 5, 5, 10, 0, 1, 7, 3, 6, 4, 10, 2, 8, 6]
        assert score(rolls) == 133


# ---------------------------------------------------------------------------
# Validation — invalid rolls
# ---------------------------------------------------------------------------

class TestInvalidRolls:
    def test_negative_pins(self):
        with pytest.raises(ValueError):
            play([-1])

    def test_pins_exceed_10(self):
        with pytest.raises(ValueError):
            play([11])

    def test_two_rolls_exceed_10_in_frame(self):
        with pytest.raises(ValueError):
            play([6, 5])

    def test_roll_after_game_over(self):
        g = play([0] * 20)
        with pytest.raises(ValueError):
            g.roll(0)

    def test_roll_after_perfect_game(self):
        g = play([10] * 12)
        with pytest.raises(ValueError):
            g.roll(0)


# ---------------------------------------------------------------------------
# Validation — incomplete game / score before done
# ---------------------------------------------------------------------------

class TestIncompleteGame:
    def test_score_before_any_rolls(self):
        with pytest.raises(ValueError):
            BowlingGame().score()

    def test_score_after_partial_game(self):
        g = play([1, 2, 3])
        with pytest.raises(ValueError):
            g.score()


# ---------------------------------------------------------------------------
# 10th-frame edge cases
# ---------------------------------------------------------------------------

class TestTenthFrame:
    def test_open_10th_no_bonus(self):
        rolls = [0] * 18 + [3, 4]
        assert score(rolls) == 7

    def test_no_extra_roll_after_open_10th(self):
        g = play([0] * 18 + [3, 4])
        with pytest.raises(ValueError):
            g.roll(0)

    def test_double_strike_fill_resets_lane(self):
        # Two strikes in 10th frame — fill ball can be up to 10.
        rolls = [0] * 18 + [10, 10, 10]
        assert score(rolls) == 30

    def test_strike_then_non_strike_fill_limited(self):
        # After 10, 3 in the 10th, fill ball must be ≤ 7.
        with pytest.raises(ValueError):
            score([0] * 18 + [10, 3, 8])

    def test_spare_fill_resets_lane(self):
        # After spare in 10th, fill ball can be up to 10.
        rolls = [0] * 18 + [7, 3, 10]
        assert score(rolls) == 20

    def test_two_rolls_exceed_10_in_10th_no_strike(self):
        with pytest.raises(ValueError):
            score([0] * 18 + [6, 5])
