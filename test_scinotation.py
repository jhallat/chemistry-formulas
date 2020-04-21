import unittest
from scinotation import ScientificNotation

class ScientificNotationTest(unittest.TestCase):

    def test_parse_full(self):
        number = ScientificNotation('2.33x10^23')
        self.assertEqual('2', number.integral)
        self.assertEqual('33', number.decimal)
        self.assertEqual('23', number.exponent)

    def test_multiplication(self):
        number_one = ScientificNotation('2.44x10^2')
        number_two = ScientificNotation('3.1x10^1')
        product = number_one * number_two
        self.assertEqual('7', product.integral)
        self.assertEqual('6', product.decimal)
        self.assertEqual('3', product.exponent)

    def test_equals(self):
        number_one = ScientificNotation('1.54x10^2')
        number_two = ScientificNotation('1.54x10^2')
        self.assertTrue(number_one == number_two)

    def test_not_equals(self):
        number_one = ScientificNotation('1.54x10^2')
        number_two = ScientificNotation('1.53x10^2')
        self.assertFalse(number_one == number_two)

if __name__ == '__main__':
    unittest.main()
