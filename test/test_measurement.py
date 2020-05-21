import unittest

from measurement import grams


class MeasurementTestCase(unittest.TestCase):

    def test_subtraction(self):
        value_one = grams('5.00')
        value_two = grams('2.61x10^0')
        value_three = grams('6.57x10^-1')
        actual = value_one - value_two - value_three
        expected = grams('1.73x10^0')
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
