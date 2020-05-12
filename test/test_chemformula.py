import unittest
from decimal import Decimal

from chemformula import *
from measurement import moles, liters, InvalidUnitError, grams, milli


class ChemicalFormulaTestCase(unittest.TestCase):

    def test_composition_NaHCO3(self):
        actual = composition('NaHCO3')
        expected = Component(1, 'Na', Decimal('27.37'))
        self.assertEqual(expected, actual[0])
        expected = Component(1, 'H', Decimal('1.20'))
        self.assertEqual(expected, actual[1])
        expected = Component(1, 'C', Decimal('14.30'))
        self.assertEqual(expected, actual[2])
        expected = Component(3, 'O', Decimal('57.14'))
        self.assertEqual(expected, actual[3])

    def test_composition_CO2(self):
        actual = composition('CO2')
        expected = Component(1, 'C', Decimal('27.29'))
        self.assertEqual(expected, actual[0])
        expected = Component(2, 'O', Decimal('72.71'))
        self.assertEqual(expected, actual[1])




if __name__ == '__main__':
    unittest.main()
