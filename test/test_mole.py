import unittest
from decimal import Decimal

from measurement import Measurement, MOLES, LITERS, moles, liters, InvalidUnitError, GRAMS, milli, grams
from mole import molar_mass, moles_from_grams, molarity, grams_in_solution, molarity_of_solution, moles_in_solution, \
    volume_from_solution
from scinotation import Scinot


class MoleTestCase(unittest.TestCase):

    def test_molar_mass_K2CrO4(self):
        actual = molar_mass('K2CrO4')
        self.assertEqual(Measurement(Decimal('194.19'),'g/mol'), actual)

    def test_molar_mass_C12H12O11(self):
        actual = molar_mass('C12H22O11')
        self.assertEqual(Measurement(Decimal('342.29'), 'g/mol'), actual)

    def test_moles_from_grams_K2CrO4(self):
        actual = moles_from_grams(212, 'K2CrO4')
        expected = Measurement(Scinot("1.09x10^0"), MOLES)
        self.assertEqual(expected, actual)

    def test_molarity_by_grams(self):
        actual = molarity(Decimal('1.20'), Decimal('2.50'))
        self.assertEqual(Measurement(Decimal('0.480'), MOLES/LITERS), actual)


    def test_molarity_by_gram_measurement(self):
        actual = molarity(Measurement(Decimal('1.20'), 'mol'), Measurement(Decimal('2.50'), 'L'))
        expected = Measurement(Scinot('4.80x10^-1'), MOLES/LITERS)
        self.assertEqual(expected, actual)

    def test_molarity_with_convienience_methods(self):
        actual = molarity(moles('1.20'), liters('2.50'))
        self.assertEqual(Measurement(Decimal('0.480'), MOLES/LITERS), actual)

    def test_molarity_invalid_unit_exception(self):
        with self.assertRaises(InvalidUnitError):
            molarity(Measurement(Decimal('1.20'), 'g'), Measurement(Decimal('2.50'), 'L'))

    def test_unit_mul_liters_and_molarity(self):
        actual = LITERS * (MOLES / LITERS)
        self.assertEqual(MOLES, actual)

    def test_unit_mul_liters_and_molarity_and_molar_mass(self):
        actual = LITERS * (MOLES / LITERS) * (GRAMS / MOLES)
        self.assertEqual(GRAMS, actual)

    def test_grams_for_tenth_mole_one_liter_K2CrO4(self):
        actual = grams_in_solution(molarity('0.1000'), molar_mass('K2CrO4'), liters('1.00'))
        self.assertEqual(Measurement(Decimal('19.4'), GRAMS), actual)

    def test_grams_for_12mole_tenth_liter_HCl(self):
        actual = grams_in_solution(molarity('12.0'), molar_mass('HCl'), liters('0.100'))
        expected = Measurement(Scinot('4.38x10^1'), GRAMS)
        self.assertEqual(expected, actual)


    def test_molarity_for_20g_of_K2CrO4_in_1L(self):
        actual = molarity_of_solution(grams('20.0'), molar_mass('K2CrO4'), liters('1.00'))
        expected = Measurement(Scinot('1.03x10^-1'), MOLES/LITERS)
        self.assertEqual(expected, actual)

    def test_moles_in_25ml_12mol_solution(self):
        actual = moles_in_solution(molarity('12.0'), milli(liters('25.0')))
        self.assertEqual(Measurement(Decimal('0.300'), MOLES), actual)

    def test_volume_for_1mole_in_12molar_solution(self):
        actual = volume_from_solution(moles('1.00'), molarity('12.0'))
        expected = Measurement(Decimal('0.0833'), LITERS)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
