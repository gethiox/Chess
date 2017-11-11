from unittest import TestCase

from app.pieces import Pawn
from app.player import Player
from app.position import StandardPosition
from app.sides import White, Black
from app.variants import Normal
from interface.game import Game


class MyTestCase(TestCase):
    def setUp(self):
        self.game = Game(player1=Player('white player'), player2=Player('black player'), variant=Normal())
        for pos, _ in self.game.board.pieces.items():
            self.game.board.remove_piece(pos)

    def test_assert_empty_board(self):
        self.assertEqual(self.game.board.pieces, {})

    def test_white_pawn_two_moves(self):
        piece = Pawn(White)
        pos = StandardPosition('b2')
        self.game.board.put_piece(piece, pos)
        self.assertEqual(
            self._get_available_move_strings(pos),
            {'b3', 'b4'}
        )
        self.assertEqual(
            self._get_available_capture_strings(pos),
            set()
        )

    def test_white_pawn_one_move(self):
        piece = Pawn(White)
        pos = StandardPosition('b3')
        self.game.board.put_piece(piece, pos)
        self.assertEqual(
            self._get_available_move_strings(pos),
            {'b4'}
        )
        self.assertEqual(
            self._get_available_capture_strings(pos),
            set()
        )

    def test_white_pawn_capture_available(self):
        piece = Pawn(White)
        pos = StandardPosition('b4')
        self.game.board.put_piece(piece, pos)
        self.game.board.put_piece(Pawn(Black), StandardPosition('a5'))
        self.game.board.put_piece(Pawn(Black), StandardPosition('b5'))
        self.game.board.put_piece(Pawn(Black), StandardPosition('c5'))
        self.game.board.put_piece(Pawn(Black), StandardPosition('a4'))
        self.game.board.put_piece(Pawn(Black), StandardPosition('c4'))
        self.game.board.put_piece(Pawn(Black), StandardPosition('a3'))
        self.game.board.put_piece(Pawn(Black), StandardPosition('b3'))
        self.game.board.put_piece(Pawn(Black), StandardPosition('c3'))
        self.assertEqual(
            self._get_available_move_strings(pos),
            set()
        )
        self.assertEqual(
            self._get_available_capture_strings(pos),
            {'a5', 'c5'}
        )

    def _get_available_move_strings(self, pos):
        return {'{}'.format(x) for x in self.game.variant.available_moves(pos)}

    def _get_available_capture_strings(self, pos):
        return {'{}'.format(x) for x in self.game.variant.available_captures(pos)}
