from unittest import TestCase

from app.game import Board
from app.pieces import King, Queen, Rook
from domain.pieces import White, Black, Position


class BoardTestCase(TestCase):
    def read_fenstring_test(self):
        board = Board()
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
        board = Board()
        board.set_fen('8/8/8/8/8/8/8/4K3')
        self.assertEqual(board._get_piece(position=Position('e1')), King(White))
        self.assertEqual(board._get_piece(position=Position('e8')), None)

        board.set_fen('4k3/8/8/8/8/8/8/4K3')
        self.assertEqual(board._get_piece(position=Position('e1')), King(White))
        self.assertEqual(board._get_piece(position=Position('e8')), King(Black))
        self.assertNotEqual(board._get_piece(position=Position('e8')), King(White))
        self.assertNotEqual(board._get_piece(position=Position('e8')), Rook(Black))
