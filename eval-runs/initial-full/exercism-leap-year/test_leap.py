import pytest
from leap import is_leap_year


@pytest.mark.parametrize("year, expected", [
    (1997, False),  # not divisible by 4
    (1996, True),   # divisible by 4, not a century year
    (1900, False),  # century year, not divisible by 400
    (2000, True),   # divisible by 400
    (2024, True),   # recent leap year
    (1800, False),  # another century non-leap
    (2100, False),  # future century non-leap
])
def test_is_leap_year(year, expected):
    assert is_leap_year(year) == expected
