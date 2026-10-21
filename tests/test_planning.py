from fractions import Fraction
import pytest
from app.core.planning import Allocation, parse_tokens, percent_label


@pytest.mark.parametrize('text', ['', '-1', '1.5', '1e6', '12,34', '１２', '+1'])
def test_invalid_tokens(text):
    with pytest.raises(ValueError):
        parse_tokens(text)


def test_exact_large_totals_and_overflow():
    capacity = 10**80
    plan = Allocation(capacity, capacity - 1, 5)
    assert plan.planned == capacity + 4
    assert plan.unallocated == -4 and plan.excess == 4
    assert sum(plan.segments(801)) == 801
    assert plan.segments(801)[2] == 0
    assert parse_tokens(f'{capacity:,}') == capacity
    assert percent_label(Fraction(1, 200)) == '0.01%'


def test_empty_exact_fit_and_invalid_capacity():
    assert Allocation(128000, 0, 8000).unallocated == 120000
    assert Allocation(10, 8, 2).segments(100) == (80, 20, 0)
    assert Allocation(10, 12, 0).segments(100) == (100, 0, 0)
    with pytest.raises(ValueError):
        Allocation(0, 0, 0)
    with pytest.raises(ValueError):
        parse_tokens('0', 1)
