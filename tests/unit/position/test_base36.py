from unittest import TestCase

from chess.app.position import StandardPosition


class MyTestCase(TestCase):
    def test_read(self):
        pos = StandardPosition((0, 0))
        self.assertEqual(str(pos), 'a1')

        pos = StandardPosition((0, 7))
        self.assertEqual(str(pos), 'a8')

        pos = StandardPosition((7, 7))
        self.assertEqual(str(pos), 'h8')

        pos = StandardPosition((7, 0))
        self.assertEqual(str(pos), 'h1')

    def test_write(self):
        pos = StandardPosition.from_str('a1')
        self.assertEqual(tuple(pos), (0, 0))

        pos = StandardPosition.from_str('a8')
        self.assertEqual(tuple(pos), (0, 7))

        pos = StandardPosition.from_str('h8')
        self.assertEqual(tuple(pos), (7, 7))

        pos = StandardPosition.from_str('h1')
        self.assertEqual(tuple(pos), (7, 0))

    def test_read_above_standard(self):
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

    def test_write_above_standard(self):
        pos = StandardPosition.from_str('z100')
        self.assertEqual(tuple(pos), (25, 99))

        pos = StandardPosition.from_str('ba100')
        self.assertEqual(tuple(pos), (26, 99))

        pos = StandardPosition.from_str('bz100')
        self.assertEqual(tuple(pos), (51, 99))

        pos = StandardPosition.from_str('ca100')
        self.assertEqual(tuple(pos), (52, 99))

        pos = StandardPosition.from_str('baa100')
        self.assertEqual(tuple(pos), (676, 99))
