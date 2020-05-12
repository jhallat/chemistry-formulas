import unittest
from decimal import Decimal

from formulaparser import parse_formula


class FormulaParserTestCase(unittest.TestCase):

    def test_parse_formula_HCl(self):
        actual = parse_formula('HCl')
        expected = [(Decimal('1.000'), 'H'), (Decimal('1.000'), 'Cl')]
        self.assertEqual(actual, expected)

    def test_parse_formula_Fe2O3_combined_with_H2O(self):
        actual = parse_formula('Fe2O3*[3/2]H2O')
        expected = [(Decimal('2.000'), 'Fe'), (Decimal('4.500'), 'O'), (Decimal('3.000'), 'H')]
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
