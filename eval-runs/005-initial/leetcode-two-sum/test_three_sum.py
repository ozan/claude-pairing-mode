from three_sum import three_sum

def test_standard():
    assert sorted(three_sum([-1, 0, 1, 2, -1, -4])) == [[-1, -1, 2], [-1, 0, 1]]

def test_all_same():
    assert three_sum([0, 0, 0]) == [[0, 0, 0]]

def test_many_duplicates():
    # Only one unique triplet despite four zeros
    assert three_sum([0, 0, 0, 0]) == [[0, 0, 0]]

def test_no_solution():
    assert three_sum([1, 2, 3]) == []

def test_empty():
    assert three_sum([]) == []
