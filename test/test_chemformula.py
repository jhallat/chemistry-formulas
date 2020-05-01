import unittest
from chemformula import *

class MyTestCase(unittest.TestCase):

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

    def test_molar_mass_K2CrO4(self):
        actual = molar_mass('K2CrO4')
        self.assertEqual(Measurement(Decimal('194.19'),'g/mol'), actual)

    def test_molar_mass_C12H12O11(self):
        actual = molar_mass('C12H22O11')
        self.assertEqual(Measurement(Decimal('342.29'), 'g/mol'), actual)

    def test_moles_from_grams_K2CrO4(self):
        actual = moles_from_grams(212, 'K2CrO4')
        self.assertEqual(Measurement(Decimal('1.09'), 'mol'), actual)

    def test_molarity_by_grams(self):
        actual = molarity(Decimal('1.20'), Decimal('2.50'))
        self.assertEqual(Measurement(Decimal('0.480'), 'mol/L'), actual)


    def test_molarity_by_gram_measurement(self):
        actual = molarity(Measurement(Decimal('1.20'), 'mol'), Measurement(Decimal('2.50'), 'L'))
        self.assertEqual(Measurement(Decimal('0.480'), 'mol/L'), actual)

    def test_molarity_invalid_unit_exception(self):
        with self.assertRaises(InvalidUnitError):
            molarity(Measurement(Decimal('1.20'), 'g'), Measurement(Decimal('2.50'), 'L'))


if __name__ == '__main__':
    unittest.main()
