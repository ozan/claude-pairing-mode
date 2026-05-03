from container_water import max_area

def test_standard():
    # Classic LeetCode example: answer is 49 ([8, 7] at indices 1 and 8)
    assert max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49

def test_two_elements():
    assert max_area([1, 1]) == 1

def test_ascending():
    # Best is rightmost pair
    assert max_area([1, 2, 3, 4, 5]) == 6  # min(2,5)*3 or min(1,5)*4=4... actually min(2,4)*3=6

def test_equal_heights():
    assert max_area([5, 5, 5, 5]) == 15  # min(5,5)*3
