import unittest

from app.board import StandardBoard
from app.pieces import King, Queen, Rook
from app.position import StandardPosition
from app.sides import White, Black


class BoardTestCase(unittest.TestCase):
    def test_board_get_put_remove_piece(self):
        board = StandardBoard()
        old_piece = board.put_piece(
            piece=Rook(White),  # TODO: Understand the difference between Type[Something] and Something (typehints)
            position=StandardPosition.from_str('e4')
        )
        self.assertEqual(old_piece, None)
        print(board.get_piece(StandardPosition.from_str('e3')))
        print(Rook(White))
        self.assertNotEqual(
            board.get_piece(StandardPosition.from_str('e3')),
            Rook(White)
        )
        self.assertEqual(
            board.get_piece(StandardPosition.from_str('e4')),
            Rook(White)
        )

        old_piece = board.put_piece(
            piece=Queen(Black),
            position=StandardPosition.from_str('e4')
        )
        self.assertEqual(old_piece, Rook(White))
        self.assertEqual(
            board.get_piece(StandardPosition.from_str('e4')),
            Queen(Black)
        )

        old_piece = board.remove_piece(StandardPosition.from_str('e4'))
        self.assertEqual(
            board.get_piece(StandardPosition.from_str('e4')),
            None
        )
        self.assertEqual(old_piece, Queen(Black))

    def test_read_fenstring(self):
        board = StandardBoard()
        board.put_piece(piece=King(White),
                        position=StandardPosition.from_str('e1'))
        self.assertEqual(board.get_fen(), '8/8/8/8/8/8/8/4K3')

        board.put_piece(piece=King(Black),
                        position=StandardPosition.from_str('e8'))
        self.assertEqual(board.get_fen(), '4k3/8/8/8/8/8/8/4K3')

        board.put_piece(piece=Queen(White),
                        position=StandardPosition.from_str('d1'))
        board.put_piece(piece=Queen(Black),
                        position=StandardPosition.from_str('d8'))
        self.assertEqual(board.get_fen(), '3qk3/8/8/8/8/8/8/3QK3')

        board.put_piece(piece=Rook(White),
                        position=StandardPosition.from_str('a1'))
        board.put_piece(piece=Rook(White),
                        position=StandardPosition.from_str('h1'))
        board.put_piece(piece=Rook(Black),
                        position=StandardPosition.from_str('a8'))
        board.put_piece(piece=Rook(Black),
                        position=StandardPosition.from_str('h8'))

        self.assertEqual(board.get_fen(), 'r2qk2r/8/8/8/8/8/8/R2QK2R')

    def test_write_fenstring(self):
        board = StandardBoard()
        board.set_fen('8/8/8/8/8/8/8/4K3')
        self.assertEqual(board.get_piece(position=StandardPosition.from_str('e1')), King(White))
        self.assertEqual(board.get_piece(position=StandardPosition.from_str('e8')), None)

        board.set_fen('4k3/8/8/8/8/8/8/4K3')
        self.assertEqual(board.get_piece(position=StandardPosition.from_str('e1')), King(White))
        self.assertEqual(board.get_piece(position=StandardPosition.from_str('e8')), King(Black))
        self.assertNotEqual(board.get_piece(position=StandardPosition.from_str('e8')), King(White))
        self.assertNotEqual(board.get_piece(position=StandardPosition.from_str('e8')), Rook(Black))
