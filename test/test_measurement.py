import unittest


class MeasurementTestCase(unittest.TestCase):

    @unittest.skip("Just a placeholder")
    def test_write_some_tests(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
