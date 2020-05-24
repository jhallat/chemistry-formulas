import pytest

from periodictable import PeriodicTable


@pytest.fixture
def periodictable():
    """Provides an instance of the Periodic Table"""
    return PeriodicTable()


def test_return_hydrogen_by_atomic_number(periodictable):
    hydrogen = periodictable['1']
    assert hydrogen.symbol == 'H'


def test_return_hydrogen_by_atomic_number_as_int(periodictable):
    hydrogen = periodictable[1]
    assert hydrogen.symbol == 'H'


def test_return_hydrogen_by_symbol(periodictable):
    hydrogen = periodictable['H']
    assert hydrogen.symbol == 'H'


def test_atomic_number_is_immutable(periodictable):
    hydrogen = periodictable['H']
    with pytest.raises(AttributeError):
        hydrogen.atomic_number = 2