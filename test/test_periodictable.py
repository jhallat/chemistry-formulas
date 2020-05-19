import unittest

from periodictable import PeriodicTable


class PeriodicTableTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.periodictable = PeriodicTable()

    def test_return_hydrogen_by_atomic_number(self):
        hydrogen = self.periodictable['1']
        self.assertEqual(hydrogen.symbol, 'H')

    def test_return_hydrogen_by_atomic_number_as_int(self):
        hydrogen = self.periodictable[1]
        self.assertEqual(hydrogen.symbol, 'H')

    def test_return_hydrogen_by_symbol(self):
        hydrogen = self.periodictable['H']
        self.assertEqual(hydrogen.symbol, 'H')

    def test_atomic_number_is_immutable(self):
        hydrogen = self.periodictable['H']
        with self.assertRaises(AttributeError):
            hydrogen.atomic_number = 2


if __name__ == '__main__':
    unittest.main()
