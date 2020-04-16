import unittest
from scinotation import ScientificNotation

class ScientificNotationTest(unittest.TestCase):

    def test_parse_full(self):
        number = ScientificNotation('2.33x10^23')
        self.assertEqual('2', number.integral)
        self.assertEqual('33', number.decimal)
        self.assertEqual('23', number.exponent)

if __name__ == '__main__':
    unittest.main()
