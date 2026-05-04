"""Tests for the Exercism Bowling exercise.

Covers the functional `score()` API and the mutable `BowlingGame` class.
"""

import pytest
from bowling import BowlingGame, score


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _play(rolls: list[int]) -> BowlingGame:
    """Feed rolls into a BowlingGame and return it."""
    game = BowlingGame()
    for r in rolls:
        game.roll(r)
    return game


# ===========================================================================
# Basic / open-frame games
# ===========================================================================

class TestOpenFrames:
    def test_all_gutter_balls(self):
        assert score([0] * 20) == 0

    def test_all_ones(self):
        assert score([1] * 20) == 20

    def test_mixed_open_frames(self):
        # 10 frames: (3,6), (6,3), (5,4), (2,7), (1,8) × 2 = 45
        rolls = [3, 6, 6, 3, 5, 4, 2, 7, 1, 8,
                 3, 6, 6, 3, 5, 4, 2, 7, 1, 8]
        assert score(rolls) == 90

    def test_single_pin_each_roll(self):
        assert score([1] * 20) == 20


# ===========================================================================
# Spares
# ===========================================================================

class TestSpares:
    def test_spare_followed_by_zeros(self):
        # (5,5) spare → 10 + 3 = 13, then open (3,0), rest gutter
        rolls = [5, 5, 3, 0] + [0] * 16
        assert score(rolls) == 16

    def test_all_spares(self):
        # Each spare frame = 15, but 10th frame has 3 rolls.
        # Frames 1-9: (5,5) each → bonus = next roll = 5 → 15 each = 135
        # Frame 10:  (5,5,5) = 15 → total = 150
        rolls = [5, 5] * 10 + [5]
        assert score(rolls) == 150

    def test_spare_bonus_counts_only_next_roll(self):
        rolls = [5, 5, 7, 2] + [0] * 16
        assert score(rolls) == 26  # (10+7)=17 + 9 + 0*8 = 26

    def test_spare_in_last_frame(self):
        rolls = [0] * 18 + [7, 3, 5]
        assert score(rolls) == 15


# ===========================================================================
# Strikes
# ===========================================================================

class TestStrikes:
    def test_strike_followed_by_zeros(self):
        rolls = [10, 0, 0] + [0] * 16
        assert score(rolls) == 10

    def test_strike_bonus_is_two_next_rolls(self):
        rolls = [10, 3, 4] + [0] * 16
        assert score(rolls) == 24  # (10+3+4)=17 + 7 + 0*8

    def test_consecutive_strikes(self):
        # Strike scores:  10+(10+10)=30, 10+(10+4)=24, 10+(4+3)=17, (4+3)=7, rest 0
        # 3 strike rolls + 2 open rolls + 6 frames × 2 = 17 rolls total
        rolls = [10, 10, 10, 4, 3] + [0] * 12
        assert score(rolls) == 78

    def test_perfect_game(self):
        # 12 strikes → 300
        rolls = [10] * 12
        assert score(rolls) == 300

    def test_strike_in_last_frame(self):
        rolls = [0] * 18 + [10, 7, 3]
        assert score(rolls) == 20

    def test_two_strikes_in_last_frame(self):
        rolls = [0] * 18 + [10, 10, 7]
        assert score(rolls) == 27


# ===========================================================================
# 10th-frame bonus roll rules
# ===========================================================================

class TestTenthFrame:
    def test_open_10th_no_bonus(self):
        rolls = [0] * 18 + [3, 5]
        assert score(rolls) == 8

    def test_spare_10th_gets_one_bonus(self):
        rolls = [0] * 18 + [6, 4, 3]
        assert score(rolls) == 13

    def test_strike_10th_gets_two_bonus_rolls(self):
        rolls = [0] * 18 + [10, 4, 3]
        assert score(rolls) == 17

    def test_all_strikes_in_10th(self):
        rolls = [0] * 18 + [10, 10, 10]
        assert score(rolls) == 30

    def test_spare_then_strike_in_10th(self):
        rolls = [0] * 18 + [7, 3, 10]
        assert score(rolls) == 20


# ===========================================================================
# Score calculation — known totals
# ===========================================================================

class TestKnownScores:
    def test_wikipedia_example(self):
        # 12, spare in 9th and 10th frames, rest gutter
        rolls = [1, 4, 4, 5, 6, 4, 5, 5, 10, 0, 1,
                 7, 3, 6, 4, 10, 2, 8, 6]
        assert score(rolls) == 133

    def test_all_fives_with_spare(self):
        # Each pair is a spare (5+5), bonus = 5. 10th frame: 5,5,5.
        # Frames 1-9: 15 each = 135. Frame 10: 5+5+5 = 15. Total = 150.
        rolls = [5, 5] * 10 + [5]
        assert score(rolls) == 150


# ===========================================================================
# Validation errors
# ===========================================================================

class TestValidation:
    def test_negative_pins(self):
        with pytest.raises(ValueError):
            score([-1] + [0] * 19)

    def test_pins_over_10_in_frame(self):
        with pytest.raises(ValueError):
            score([11] + [0] * 19)

    def test_two_rolls_exceed_pins(self):
        with pytest.raises(ValueError):
            score([6, 5] + [0] * 18)

    def test_too_many_rolls_open_game(self):
        with pytest.raises(ValueError):
            score([0] * 21)

    def test_too_many_bonus_rolls_after_spare(self):
        with pytest.raises(ValueError):
            score([0] * 18 + [5, 5, 5, 5])

    def test_too_many_bonus_rolls_after_strike(self):
        with pytest.raises(ValueError):
            score([0] * 18 + [10, 10, 10, 10])

    def test_too_few_rolls(self):
        with pytest.raises(ValueError):
            score([0] * 19)

    def test_incomplete_game(self):
        with pytest.raises(ValueError):
            score([10] * 5)

    def test_second_bonus_roll_exceeds_pins_after_non_strike(self):
        # 10th frame: first roll is a strike → second + third may be spare/strike
        # but if second roll is not a strike, r2+r3 must not exceed 10
        with pytest.raises(ValueError):
            score([0] * 18 + [10, 5, 6])

    def test_bonus_roll_after_open_10th_not_allowed(self):
        with pytest.raises(ValueError):
            score([0] * 18 + [3, 5, 1])


# ===========================================================================
# BowlingGame class API
# ===========================================================================

class TestBowlingGameClass:
    def test_perfect_game(self):
        game = _play([10] * 12)
        assert game.score == 300

    def test_all_gutter_balls(self):
        game = _play([0] * 20)
        assert game.score == 0

    def test_score_before_game_over_raises(self):
        game = _play([0] * 10)
        with pytest.raises(ValueError):
            _ = game.score

    def test_roll_after_game_over_raises(self):
        game = _play([0] * 20)
        with pytest.raises(ValueError):
            game.roll(0)

    def test_invalid_roll_raises(self):
        game = BowlingGame()
        with pytest.raises(ValueError):
            game.roll(-1)

    def test_incremental_open_game(self):
        game = BowlingGame()
        for _ in range(10):
            game.roll(3)
            game.roll(5)
        assert game.score == 80

    def test_incremental_spare_game(self):
        game = BowlingGame()
        # Frames 1-9: (5,5), Frame 10: (5,5,3)
        for _ in range(9):
            game.roll(5)
            game.roll(5)
        game.roll(5)
        game.roll(5)
        game.roll(3)
        # Frames 1-9: 10+5 = 15 each → 135; Frame 10: 13 → 148
        assert game.score == 148

    def test_incremental_perfect_game(self):
        game = BowlingGame()
        for _ in range(12):
            game.roll(10)
        assert game.score == 300
