import pytest

from sample_code import inc_dec


@pytest.fixture
def sample_num():
    return int(1)


def test_increment():
    assert inc_dec.increment(3) == 4


def test_decrement(sample_num):
    assert inc_dec.decrement(3) == 2
    assert inc_dec.decrement(sample_num) == 0
