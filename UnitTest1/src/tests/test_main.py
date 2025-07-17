import pytest
from src.main import sum, is_greater_than, pair


def test_sum():
    assert sum(2, 4) ==  6


def test_is_greater_than():
    assert is_greater_than(10, 2)


@pytest.mark.parametrize(
    "input_x, input_y, expected",
    [
        (5, 1, 6),
        (6, sum(4, 2), 12),
        (sum(19, 1), 15, 35),
        (-7, 10, sum(-7, 10))
    ]
)
def test_sum_params(input_x, input_y, expected):
    assert sum(input_x, input_y) == expected

@pytest.mark.parametrize(
    "num, expected",
    [
        (2, True),
        (4, True),
        (0, True),
        (-2, True),
        (1, False),
        (3, False),
        (-1, False),
        (999, True)
    ]
)
def test_pair_parametrizado(num, expected):
    assert pair(num) == expected
