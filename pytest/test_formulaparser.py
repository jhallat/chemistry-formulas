import unittest
from decimal import Decimal

from formulaparser import parse_formula


def test_parse_formula_HCl():
    actual = parse_formula('HCl')
    expected = [(Decimal('1.000'), 'H'), (Decimal('1.000'), 'Cl')]
    assert actual == expected

def test_parse_formula_Fe2O3_combined_with_H2O():
    actual = parse_formula('Fe2O3*[3/2]H2O')
    expected = [(Decimal('2.000'), 'Fe'), (Decimal('3.000'), 'O'), [(Decimal('3.000'), 'H'), (Decimal('1.500'), 'O')]]
    assert expected == actual

