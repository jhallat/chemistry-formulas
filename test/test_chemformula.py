import unittest
from decimal import Decimal

from chemformula import *
from measurement import moles, liters, InvalidUnitError, grams, milli
from scinotation import Scinot


class ChemicalFormulaTestCase(unittest.TestCase):

    def test_composition_NaHCO3(self):
        actual = composition('NaHCO3')
        expected = Component(1, 'Na', grams('0.2737'), Decimal('27.37'))
        self.assertEqual(expected, actual[0])
        expected = Component(1, 'H', grams('0.01200'), Decimal('1.20'))
        self.assertEqual(expected, actual[1])
        expected = Component(1, 'C', grams('0.1430'), Decimal('14.30'))
        self.assertEqual(expected, actual[2])
        expected = Component(3, 'O', grams('0.5714'), Decimal('57.14'))
        self.assertEqual(expected, actual[3])

    def test_composition_CO2(self):
        actual = composition('CO2')
        expected = Component(1, 'C', grams('0.2729'), Decimal('27.29'))
        self.assertEqual(expected, actual[0])
        expected = Component(2, 'O', grams('0.7271'), Decimal('72.71'))
        self.assertEqual(expected, actual[1])

    def test_amount_of_iron_in_limonite(self):
        actual = composition('Fe2O3*[3/2]H2O', grams(Scinot('1.0000x10^6')))
        expected = Component(2, 'Fe', grams(Scinot('5.9820x10^5')), Decimal('59.82'))
        self.assertEqual(expected, actual[0])


    def test_formula_of_Sn_and_O(self):
        elements = [('Sn', Decimal('78.8')),
                    ('O', Decimal('21.2'))]
        actual = formula_from_percent(elements)
        expected = "SnO2"
        self.assertEqual(expected, actual)

    def test_formula_of_K_Cr_O(self):
        elements = [('K', Decimal('26.6')),
                    ('Cr', Decimal('35.4')),
                    ('O', Decimal('38.0'))]
        actual = formula_from_percent(elements)
        expected = "K2Cr2O7"
        self.assertEqual(expected, actual)

    def test_formula_of_C_H_O(self):
        elements = [('C', grams('2.61')),
                    ('H', grams('0.658')),
                    ('O', grams('1.73'))]
        actual = formula_from_mass(elements)
        expected = "C2H6O"
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
