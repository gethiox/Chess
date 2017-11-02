from unittest import TestCase

from app.game import StandardBoard
from app.pieces import King, Queen, Rook
from app.position import StandardPosition
from app.sides import White, Black


class BoardTestCase(TestCase):
    def board_get_put_remove_piece_test(self):
        board = StandardBoard()
        old_piece = board._put_piece(
            piece=Rook(White),
            position=StandardPosition('e4')
        )
        self.assertEqual(old_piece, None)
        print(board._get_piece(StandardPosition('e3')))
        print(Rook(White))
        self.assertNotEqual(
            board._get_piece(StandardPosition('e3')),
            Rook(White)
        )
        self.assertEqual(
            board._get_piece(StandardPosition('e4')),
            Rook(White)
        )

        old_piece = board._put_piece(
            piece=Queen(Black),
            position=StandardPosition('e4')
        )
        self.assertEqual(old_piece, Rook(White))
        self.assertEqual(
            board._get_piece(StandardPosition('e4')),
            Queen(Black)
        )

        old_piece = board._remove_piece(StandardPosition('e4'))
        self.assertEqual(
            board._get_piece(StandardPosition('e4')),
            None
        )
        self.assertEqual(old_piece, Queen(Black))

    def read_fenstring_test(self):
        board = StandardBoard()
        board._put_piece(piece=King(White),
                         position=StandardPosition('e1'))
        self.assertEqual(board.get_fen(), '8/8/8/8/8/8/8/4K3')

        board._put_piece(piece=King(Black),
                         position=StandardPosition('e8'))
        self.assertEqual(board.get_fen(), '4k3/8/8/8/8/8/8/4K3')

        board._put_piece(piece=Queen(White),
                         position=StandardPosition('d1'))
        board._put_piece(piece=Queen(Black),
                         position=StandardPosition('d8'))
        self.assertEqual(board.get_fen(), '3qk3/8/8/8/8/8/8/3QK3')

        board._put_piece(piece=Rook(White),
                         position=StandardPosition('a1'))
        board._put_piece(piece=Rook(White),
                         position=StandardPosition('h1'))
        board._put_piece(piece=Rook(Black),
                         position=StandardPosition('a8'))
        board._put_piece(piece=Rook(Black),
                         position=StandardPosition('h8'))

        self.assertEqual(board.get_fen(), 'r2qk2r/8/8/8/8/8/8/R2QK2R')

    def write_fenstring_test(self):
        board = StandardBoard()
        board.set_fen('8/8/8/8/8/8/8/4K3')
        self.assertEqual(board._get_piece(position=StandardPosition('e1')), King(White))
        self.assertEqual(board._get_piece(position=StandardPosition('e8')), None)

        board.set_fen('4k3/8/8/8/8/8/8/4K3')
        self.assertEqual(board._get_piece(position=StandardPosition('e1')), King(White))
        self.assertEqual(board._get_piece(position=StandardPosition('e8')), King(Black))
        self.assertNotEqual(board._get_piece(position=StandardPosition('e8')), King(White))
        self.assertNotEqual(board._get_piece(position=StandardPosition('e8')), Rook(Black))
