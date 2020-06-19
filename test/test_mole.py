from decimal import Decimal

import pytest

from src.chemistry.measurement import Measurement, MOLES, LITERS, moles, liters, InvalidUnitError, GRAMS, milli, grams
from src.chemistry.mole import molar_mass, moles_from_grams, molarity, grams_in_solution, molarity_of_solution, moles_in_solution, \
    volume_from_solution, mass, molecules_in_mass
from src.chemistry.scinotation import Scinot


def test_molar_mass_K2CrO4():
    actual = molar_mass('K2CrO4')
    assert Measurement(Decimal('194.19'),'g/mol') == actual

def test_molar_mass_C12H12O11():
    actual = molar_mass('C12H22O11')
    assert Measurement(Decimal('342.29'), 'g/mol') == actual

def test_molar_mass_H2O2():
     actual = molar_mass('H2O2')
     expected = Measurement(Scinot('3.4014x10^1'), GRAMS / MOLES)
     assert expected == actual

def test_moles_from_grams_K2CrO4():
    actual = moles_from_grams(212, 'K2CrO4')
    expected = Measurement(Scinot("1.09x10^0"), MOLES)
    assert expected == actual

def test_molarity_by_grams():
    actual = molarity(Decimal('1.20'), Decimal('2.50'))
    assert Measurement(Decimal('0.480'), MOLES/LITERS) == actual


def test_molarity_by_gram_measurement():
    actual = molarity(Measurement(Decimal('1.20'), 'mol'), Measurement(Decimal('2.50'), 'L'))
    expected = Measurement(Scinot('4.80x10^-1'), MOLES/LITERS)
    assert expected == actual

def test_molarity_with_convienience_methods():
    actual = molarity(moles('1.20'), liters('2.50'))
    assert Measurement(Decimal('0.480'), MOLES/LITERS) == actual

def test_molarity_invalid_unit_exception():
    with pytest.raises(InvalidUnitError):
        molarity(Measurement(Decimal('1.20'), 'g'), Measurement(Decimal('2.50'), 'L'))

def test_unit_mul_liters_and_molarity():
    actual = LITERS * (MOLES / LITERS)
    assert MOLES == actual

def test_unit_mul_liters_and_molarity_and_molar_mass():
    actual = LITERS * (MOLES / LITERS) * (GRAMS / MOLES)
    assert GRAMS == actual

def test_grams_for_tenth_mole_one_liter_K2CrO4():
    actual = grams_in_solution(molarity('0.1000'), molar_mass('K2CrO4'), liters('1.00'))
    assert Measurement(Decimal('19.4'), GRAMS) == actual

def test_grams_for_12mole_tenth_liter_HCl():
    actual = grams_in_solution(molarity('12.0'), molar_mass('HCl'), liters('0.100'))
    expected = Measurement(Scinot('4.38x10^1'), GRAMS)
    assert expected == actual


def test_molarity_for_20g_of_K2CrO4_in_1L():
    actual = molarity_of_solution(grams('20.0'), molar_mass('K2CrO4'), liters('1.00'))
    expected = Measurement(Scinot('1.03x10^-1'), MOLES/LITERS)
    assert expected == actual

def test_moles_in_25ml_12mol_solution():
    actual = moles_in_solution(molarity('12.0'), milli(liters('25.0')))
    assert Measurement(Decimal('0.300'), MOLES) == actual

def test_volume_for_1mole_in_12molar_solution():
    actual = volume_from_solution(moles('1.00'), molarity('12.0'))
    expected = Measurement(Decimal('0.0833'), LITERS)
    assert expected == actual

def test_mass_of_S():
    actual = mass('S')
    expected = Measurement(Scinot('5.325x10^-23'), GRAMS)
    assert expected == actual

def test_mass_of_H2O2():
    actual = mass('H2O2')
    expected = Measurement(Scinot('5.648x10^-23'), GRAMS)
    assert expected == actual

def test_molecules_in_1gram_S():
    actual = molecules_in_mass('S', grams('1.000'))
    expected = Measurement(Scinot('1.878x10^22'), 'atoms')
    assert expected == actual

def test_molecules_in_1gram_H2O2():
    actual = molecules_in_mass('H2O2', grams('1.00'))
    expected = Measurement(Scinot('1.77x10^22'), 'atoms')
    assert expected == actual

