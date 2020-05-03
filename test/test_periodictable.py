import unittest

from periodictable import PeriodicTable


class PeriodicTableTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.periodictable = PeriodicTable()

    def test_accessing_symbol_map_of_periodic_table_not_allowed(self):
        with self.assertRaises(AttributeError):
            table = self.periodictable.table_symbol
            print(table)

    def test_accessing_number_map_of_periodic_table_not_allowed(self):
        with self.assertRaises(AttributeError):
            table = self.periodictable.table_number

    def test_writing_symbol_map_of_periodic_table_not_allowed(self):
        with self.assertRaises(AttributeError):
            self.periodictable.table_symbol = {}

    def test_writing_number_map_of_periodic_table_not_allowed(self):
        with self.assertRaises(AttributeError):
            self.periodictable.table_number = {}

    def test_deleting_symbol_map_of_periodic_table_not_allowed(self):
        with self.assertRaises(AttributeError):
            del(self.periodictable.table_symbol)

    def test_deleting_number_map_of_periodic_table_not_allowed(self):
        with self.assertRaises(AttributeError):
            del(self.periodictable.table_number)

    def test_return_hydrogen_by_atomic_number(self):
        hydrogen = self.periodictable.search('1')
        self.assertEqual(hydrogen.symbol, 'H')

    def test_return_hydrogen_by_atomic_number_as_int(self):
        hydrogen = self.periodictable.search(1)
        self.assertEqual(hydrogen.symbol, 'H')

    def test_return_hydrogen_by_symbol(self):
        hydrogen = self.periodictable.search('H')
        self.assertEqual(hydrogen.symbol, 'H')



if __name__ == '__main__':
    unittest.main()
