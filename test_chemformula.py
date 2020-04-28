import unittest
from chemformula import *

class MyTestCase(unittest.TestCase):

    def test_round_to_sig_digits(self):
        actual = round_to_sig_digits(1.1119, 4)
        self.assertEqual(Decimal('1.112'), actual)

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
        self.assertEqual(Decimal('2220'), actual)

if __name__ == '__main__':
    unittest.main()
