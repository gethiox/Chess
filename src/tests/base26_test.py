from unittest import TestCase

from app.pieces import StandardPosition


class MyTestCase(TestCase):
    def read_test(self):
        pos = StandardPosition((0, 0))
        self.assertEqual(str(pos), 'a1')

        pos = StandardPosition((0, 7))
        self.assertEqual(str(pos), 'a8')

        pos = StandardPosition((7, 7))
        self.assertEqual(str(pos), 'h8')

        pos = StandardPosition((7, 0))
        self.assertEqual(str(pos), 'h1')

    def write_test(self):
        pos = StandardPosition('a1')
        self.assertEqual(tuple(pos), (0, 0))

        pos = StandardPosition('a8')
        self.assertEqual(tuple(pos), (0, 7))

        pos = StandardPosition('h8')
        self.assertEqual(tuple(pos), (7, 7))

        pos = StandardPosition('h1')
        self.assertEqual(tuple(pos), (7, 0))

    def read_above_standard_test(self):
        pos = StandardPosition((25, 99))
        self.assertEqual(str(pos), 'z100')  # 'b1 means the same as ab1 just like decimals - 001 == 1'

        pos = StandardPosition((26, 99))
        self.assertEqual(str(pos), 'ba100')

        pos = StandardPosition((51, 99))
        self.assertEqual(str(pos), 'bz100')

        pos = StandardPosition((52, 99))
        self.assertEqual(str(pos), 'ca100')

        pos = StandardPosition((676, 99))
        self.assertEqual(str(pos), 'baa100')

    def write_above_standard_test(self):
        pos = StandardPosition('z100')
        self.assertEqual(tuple(pos), (25, 99))

        pos = StandardPosition('ba100')
        self.assertEqual(tuple(pos), (26, 99))

        pos = StandardPosition('bz100')
        self.assertEqual(tuple(pos), (51, 99))

        pos = StandardPosition('ca100')
        self.assertEqual(tuple(pos), (52, 99))

        pos = StandardPosition('baa100')
        self.assertEqual(tuple(pos), (676, 99))
