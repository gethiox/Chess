from unittest import TestCase

from domain.pieces import Position


class MyTestCase(TestCase):
    def read_test(self):
        pos = Position((0, 0))
        self.assertEqual(str(pos), 'a1')

        pos = Position((0, 7))
        self.assertEqual(str(pos), 'a8')

        pos = Position((7, 7))
        self.assertEqual(str(pos), 'h8')

        pos = Position((7, 0))
        self.assertEqual(str(pos), 'h1')

    def write_test(self):
        pos = Position('a1')
        self.assertEqual(tuple(pos), (0, 0))

        pos = Position('a8')
        self.assertEqual(tuple(pos), (0, 7))

        pos = Position('h8')
        self.assertEqual(tuple(pos), (7, 7))

        pos = Position('h1')
        self.assertEqual(tuple(pos), (7, 0))

    def read_above_standard_test(self):
        pos = Position((25, 99))
        self.assertEqual(str(pos), 'z100')  # 'b1 means the same as ab1 just like decimals - 001 == 1'

        pos = Position((26, 99))
        self.assertEqual(str(pos), 'ba100')

        pos = Position((51, 99))
        self.assertEqual(str(pos), 'bz100')

        pos = Position((52, 99))
        self.assertEqual(str(pos), 'ca100')

        pos = Position((676, 99))
        self.assertEqual(str(pos), 'baa100')

    def write_above_standard_test(self):
        pos = Position('z100')
        self.assertEqual(tuple(pos), (25, 99))

        pos = Position('ba100')
        self.assertEqual(tuple(pos), (26, 99))

        pos = Position('bz100')
        self.assertEqual(tuple(pos), (51, 99))

        pos = Position('ca100')
        self.assertEqual(tuple(pos), (52, 99))

        pos = Position('baa100')
        self.assertEqual(tuple(pos), (676, 99))
