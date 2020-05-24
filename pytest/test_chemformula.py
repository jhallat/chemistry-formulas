from decimal import Decimal

from chemformula import composition, Component, formula_from_percent, formula_from_mass, mol_formula_from_simple_formula
from measurement import grams
from scinotation import Scinot


def test_composition_NaHCO3():
    actual = composition('NaHCO3')
    expected = Component(1, 'Na', grams('0.2737'), Decimal('27.37'))
    assert expected == actual[0]
    expected = Component(1, 'H', grams('0.01200'), Decimal('1.20'))
    assert expected == actual[1]
    expected = Component(1, 'C', grams('0.1430'), Decimal('14.30'))
    assert expected == actual[2]
    expected = Component(3, 'O', grams('0.5714'), Decimal('57.14'))
    assert expected == actual[3]


def test_composition_CO2():
    actual = composition('CO2')
    expected = Component(1, 'C', grams('0.2729'), Decimal('27.29'))
    assert expected == actual[0]
    expected = Component(2, 'O', grams('0.7271'), Decimal('72.71'))
    assert expected == actual[1]


def test_amount_of_iron_in_limonite():
    actual = composition('Fe2O3*[3/2]H2O', grams(Scinot('1.0000x10^6')))
    expected = Component(2, 'Fe', grams(Scinot('5.9820x10^5')), Decimal('59.82'))
    assert expected == actual[0]


def test_formula_of_Sn_and_O():
    elements = [('Sn', Decimal('78.8')),
                ('O', Decimal('21.2'))]
    actual = formula_from_percent(elements)
    expected = "SnO2"
    assert expected == actual


def test_formula_of_K_Cr_O():
    elements = [('K', Decimal('26.6')),
                ('Cr', Decimal('35.4')),
                ('O', Decimal('38.0'))]
    actual = formula_from_percent(elements)
    expected = "K2Cr2O7"
    assert expected == actual


def test_formula_of_C_H_O():
    elements = [('C', grams('2.61')),
                ('H', grams('0.658')),
                ('O', grams('1.73'))]
    actual = formula_from_mass(elements)
    expected = "C2H6O"
    assert expected == actual

def test_mol_formula_of_vitamin_c():
    actual = mol_formula_from_simple_formula("C3H4O3", Decimal('180'))
    expected = "C6H8O6"
    assert expected == actual