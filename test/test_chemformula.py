import unittest
from chemformula import *
from measurement import moles, liters, InvalidUnitError, grams, milli


class ChemicalFormulaTestCase(unittest.TestCase):

    def test_round_to_sig_digits(self):
        actual = round_to_sig_digits(1.1119, 4)
        self.assertEqual(Decimal('1.112'), actual)

    def test_round_to_sig_digits_leading_zeros(self):
        actual = round_to_sig_digits(0.000147, 2)
        self.assertEqual(Decimal('0.00015'), actual)

    def test_round_to_sig_digits_before_decimal(self):
        actual = round_to_sig_digits(22345.34, 2)
        self.assertEqual(Decimal('22000'), actual)

    def test_round_last_decimal(self):
        actual = round_last(1.1119)
        self.assertEqual(Decimal('1.112'), actual)

    def test_round_last_decimal_2(self):
        actual = round_last(1.9999)
        self.assertEqual(Decimal('2.000'), actual)

    def test_round_last_decimal_3(self):
        actual = round_last(9.9999)
        self.assertEqual(Decimal('10.00'), actual)

    def test_round_last_integer(self):
        actual = round_last(2225)
        self.assertEqual(Decimal('2230'), actual)

    def test_round_last_decimal_zero(self):
        actual = round_last(Decimal('1.1110'))
        self.assertEqual(Decimal('1.111'), actual)

    def test_round_last_decimal_zero(self):
        actual = round_last('1.1110')
        self.assertEqual(Decimal('1.111'), actual)

    def test_round_last_integer_zero(self):
        actual = round_last(2220)
        self.assertEqual(Decimal('2200'), actual)

    def test_composition_HCl(self):
        actual = composition('HCl')
        expected = [('1', 'H'), ('1', 'Cl')]
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
