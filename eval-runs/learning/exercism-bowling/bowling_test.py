import pytest
from bowling import score


# ── Scoring ──────────────────────────────────────────────────────────────────

class TestScoring:
    def test_all_zeros(self):
        assert score([0] * 20) == 0

    def test_no_strikes_or_spares(self):
        # 6+3 per frame × 10 = 90
        assert score([6, 3] * 10) == 90

    def test_spare_followed_by_zeros(self):
        # frame 1: spare (10) + 0 bonus; rest all zeros → 10
        assert score([6, 4, 0, 0] + [0] * 16) == 10

    def test_roll_after_spare_counts_twice(self):
        # frame 1: spare bonus = 3 → 13; frame 2: 3+6=9; rest zero → 22
        assert score([6, 4, 3, 6] + [0] * 16) == 22

    def test_consecutive_spares(self):
        # frame 1: spare, bonus=5 → 10+5=15
        # frame 2: spare, bonus=3 → 10+3=13
        # frame 3: 3+0=3; rest zero → total 31
        assert score([5, 5, 5, 5, 3, 0] + [0] * 14) == 31

    def test_spare_in_last_frame_one_bonus_roll(self):
        # nine open frames of 3+6=9 each → 81; last frame: spare + 7 = 17 → 98
        assert score([3, 6] * 9 + [5, 5, 7]) == 98

    def test_strike_earns_ten_points(self):
        # frame 1 strike, bonus 0+0 → 10; rest zeros → 10
        assert score([10, 0, 0] + [0] * 16) == 10

    def test_rolls_after_strike_counted_twice(self):
        # frame 1 strike, bonus 3+6 → 19; frame 2: 3+6=9; rest zero → 28
        assert score([10, 3, 6] + [0] * 16) == 28

    def test_consecutive_strikes(self):
        # frame 1: 10+10+10=30; frame 2: 10+10+0=20; frame 3: 10+0+0=10; rest zero → 60
        # 3 strikes (3 rolls) + 7 open frames of 0,0 (14 rolls) = 17 rolls total
        assert score([10, 10, 10, 0, 0] + [0] * 12) == 60

    def test_strike_in_last_frame_two_bonus_rolls(self):
        assert score([0, 0] * 9 + [10, 7, 1]) == 18

    def test_spare_after_strike_bonus_not_applied_again(self):
        # last frame: 10 + 7/3 = 20 (the spare is not double-counted)
        assert score([0, 0] * 9 + [10, 7, 3]) == 20

    def test_two_strikes_in_last_frame(self):
        assert score([0, 0] * 9 + [10, 10, 7]) == 27

    def test_perfect_game(self):
        # twelve strikes → 300
        assert score([10] * 12) == 300

    def test_last_frame_all_strikes(self):
        # nine strikes + three strikes in 10th
        assert score([10] * 11 + [10]) == 300

    def test_spare_with_no_bonus_rolls_in_ninth_frame(self):
        # spare in frame 9, bonus = first roll of frame 10
        assert score([0, 0] * 8 + [5, 5, 3, 0]) == 16

    def test_all_fives(self):
        # each pair 5+5=spare, bonus=5 → 15 per frame for 9 frames = 135
        # 10th: 5+5+5 = 15 → 150
        assert score([5, 5] * 9 + [5, 5, 5]) == 150


# ── Invalid inputs ───────────────────────────────────────────────────────────

class TestInvalidInputs:
    def test_negative_roll(self):
        with pytest.raises(ValueError):
            score([-1, 0] + [0] * 18)

    def test_pin_count_exceeds_10(self):
        with pytest.raises(ValueError):
            score([11] + [0] * 19)

    def test_sum_of_frame_exceeds_10(self):
        with pytest.raises(ValueError):
            score([6, 5] + [0] * 18)

    def test_too_many_rolls(self):
        with pytest.raises(ValueError):
            score([0] * 21)

    def test_too_few_rolls(self):
        with pytest.raises(ValueError):
            score([0] * 19)

    def test_spare_then_too_many_bonus_rolls(self):
        with pytest.raises(ValueError):
            score([0, 0] * 9 + [5, 5, 7, 3])

    def test_strike_then_too_many_bonus_rolls(self):
        with pytest.raises(ValueError):
            score([0, 0] * 9 + [10, 7, 3, 2])

    def test_open_10th_with_bonus_roll(self):
        with pytest.raises(ValueError):
            score([0, 0] * 9 + [3, 3, 1])

    def test_bonus_roll_exceeds_10_after_strike(self):
        with pytest.raises(ValueError):
            score([0, 0] * 9 + [10, 11, 0])

    def test_bonus_rolls_exceed_10_unless_second_is_strike(self):
        # second ball 6, third ball 5: 6+5>10, invalid
        with pytest.raises(ValueError):
            score([0, 0] * 9 + [10, 6, 5])

    def test_two_bonus_rolls_after_strike_can_themselves_be_spare(self):
        # second 7, third 3 → 7+3=10 (a spare in bonus rolls): VALID
        assert score([0, 0] * 9 + [10, 7, 3]) == 20
