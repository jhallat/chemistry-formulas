import unittest
from scinotation import Scinot

class ScientificNotationTest(unittest.TestCase):

    def test_parse_full(self):
        number = Scinot('2.33x10^23')
        self.assertEqual('2', number._integral)
        self.assertEqual('33', number._decimal)
        self.assertEqual('23', number._exponent)

    def test_parse_small_decimal(self):
        number = Scinot('0.0120')
        self.assertEqual('1', number._integral)
        self.assertEqual('20', number._decimal)
        self.assertEqual('-2', number._exponent)

    def test_multiplication(self):
        number_one = Scinot('2.44x10^2')
        number_two = Scinot('3.1x10^1')
        product = number_one * number_two
        self.assertEqual('7', product._integral)
        self.assertEqual('6', product._decimal)
        self.assertEqual('3', product._exponent)

    def test_equals(self):
        number_one = Scinot('1.54x10^2')
        number_two = Scinot('1.54x10^2')
        self.assertTrue(number_one == number_two)

    def test_not_equals(self):
        number_one = Scinot('1.54x10^2')
        number_two = Scinot('1.53x10^2')
        self.assertFalse(number_one == number_two)

    def test_subtraction(self):
        number_one = Scinot('5.00x10^0')
        number_two = Scinot('2.61x10^0')
        number_three = Scinot('6.57x10^-1')
        actual = number_one - number_two - number_three
        expected = Scinot('1.73x10^0')
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
