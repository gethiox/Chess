from unittest import TestCase

from app.game import StandardBoard
from app.pieces import King, Queen, Rook, White, Black
from domain.pieces import Position


class BoardTestCase(TestCase):
    def board_get_put_remove_piece_test(self):
        board = StandardBoard()
        old_piece = board._put_piece(
            piece=Rook(White),
            position=Position('e4')
        )
        self.assertEqual(old_piece, None)
        self.assertNotEqual(
            board._get_piece(Position('e3')),
            Rook(White)
        )
        self.assertEqual(
            board._get_piece(Position('e4')),
            Rook(White)
        )

        old_piece = board._put_piece(
            piece=Queen(Black),
            position=Position('e4')
        )
        self.assertEqual(old_piece, Rook(White))
        self.assertEqual(
            board._get_piece(Position('e4')),
            Queen(Black)
        )

        old_piece = board._remove_piece(Position('e4'))
        self.assertEqual(
            board._get_piece(Position('e4')),
            None
        )
        self.assertEqual(old_piece, Queen(Black))

    def read_fenstring_test(self):
        board = StandardBoard()
        board._put_piece(piece=King(White),
                         position=Position('e1'))
        self.assertEqual(board.get_fen(), '8/8/8/8/8/8/8/4K3')

        board._put_piece(piece=King(Black),
                         position=Position('e8'))
        self.assertEqual(board.get_fen(), '4k3/8/8/8/8/8/8/4K3')

        board._put_piece(piece=Queen(White),
                         position=Position('d1'))
        board._put_piece(piece=Queen(Black),
                         position=Position('d8'))
        self.assertEqual(board.get_fen(), '3qk3/8/8/8/8/8/8/3QK3')

        board._put_piece(piece=Rook(White),
                         position=Position('a1'))
        board._put_piece(piece=Rook(White),
                         position=Position('h1'))
        board._put_piece(piece=Rook(Black),
                         position=Position('a8'))
        board._put_piece(piece=Rook(Black),
                         position=Position('h8'))

        self.assertEqual(board.get_fen(), 'r2qk2r/8/8/8/8/8/8/R2QK2R')

    def write_fenstring_test(self):
        board = StandardBoard()
        board.set_fen('8/8/8/8/8/8/8/4K3')
        self.assertEqual(board._get_piece(position=Position('e1')), King(White))
        self.assertEqual(board._get_piece(position=Position('e8')), None)

        board.set_fen('4k3/8/8/8/8/8/8/4K3')
        self.assertEqual(board._get_piece(position=Position('e1')), King(White))
        self.assertEqual(board._get_piece(position=Position('e8')), King(Black))
        self.assertNotEqual(board._get_piece(position=Position('e8')), King(White))
        self.assertNotEqual(board._get_piece(position=Position('e8')), Rook(Black))
