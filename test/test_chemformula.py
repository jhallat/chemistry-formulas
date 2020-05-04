import unittest
from chemformula import *
from measurement import moles, liters, InvalidUnitError, grams, milli


class ChemicalFormulaTestCase(unittest.TestCase):


    def test_composition_HCl(self):
        actual = composition('HCl')
        expected = [('1', 'H'), ('1', 'Cl')]
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
