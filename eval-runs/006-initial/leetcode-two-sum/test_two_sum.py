from two_sum import two_sum


def test_happy_path():
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]


def test_answer_not_at_start():
    assert two_sum([3, 2, 4], 6) == [1, 2]


def test_self_match_guard():
    # Two distinct indices with the same value — should match [0,1], not [0,0]
    assert two_sum([3, 3], 6) == [0, 1]


def test_negative_numbers():
    assert two_sum([-1, -2, -3, -4, -5], -8) == [2, 4]


def test_mixed_signs():
    assert two_sum([-3, 4, 3, 90], 0) == [0, 2]
