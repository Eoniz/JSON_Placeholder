from json_placeholder.utils.random import float_between, int_bewteen, one_of

import pytest


@pytest.mark.unit_tests
def test_one_of():
    values = ["foo", "bar"]
    value = one_of(values)
    assert value in values


@pytest.mark.unit_tests
def test_int_between():
    value = int_bewteen(0, 10)
    assert 0 <= value <= 10
    assert isinstance(value, int)


@pytest.mark.unit_tests
def test_float_between():
    value = float_between(0, 10)
    assert 0.0 <= value <= 10.0
    assert isinstance(value, float)
