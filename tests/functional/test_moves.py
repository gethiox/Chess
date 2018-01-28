from unittest import TestCase

from chess.app.pieces import Pawn
from chess.app.player import Player
from chess.app.position import StandardPosition
from chess.app.sides import White, Black
from chess.app.variants.classic import Normal
from chess.interface.game import Game


class MyTestCase(TestCase):
    def setUp(self):
        self.game = Game(player1=Player('white player'), player2=Player('black player'), variant=Normal())
        for pos, _ in self.game.board.pieces:
            self.game.board.remove_piece(pos)

    def test_assert_empty_board(self):
        self.assertEqual(self.game.board.pieces, [])

    def test_white_pawn_two_moves(self):
        piece = Pawn(White)
        pos = StandardPosition.from_str('b2')
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
        pos = StandardPosition.from_str('b3')
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
        pos = StandardPosition.from_str('b4')
        self.game.board.put_piece(piece, pos)
        self.game.board.put_piece(Pawn(Black), StandardPosition.from_str('a5'))
        self.game.board.put_piece(Pawn(Black), StandardPosition.from_str('b5'))
        self.game.board.put_piece(Pawn(Black), StandardPosition.from_str('c5'))
        self.game.board.put_piece(Pawn(Black), StandardPosition.from_str('a4'))
        self.game.board.put_piece(Pawn(Black), StandardPosition.from_str('c4'))
        self.game.board.put_piece(Pawn(Black), StandardPosition.from_str('a3'))
        self.game.board.put_piece(Pawn(Black), StandardPosition.from_str('b3'))
        self.game.board.put_piece(Pawn(Black), StandardPosition.from_str('c3'))
        self.assertEqual(
            self._get_available_move_strings(pos),
            set()
        )
        self.assertEqual(
            self._get_available_capture_strings(pos),
            {'a5', 'c5'}
        )

    def _get_available_move_strings(self, pos):
        return {'{}'.format(x) for x in self.game.variant.standard_moves(pos) | self.game.variant.special_moves(pos)}

    def _get_available_capture_strings(self, pos):
        return {'{}'.format(x) for x in self.game.variant.standard_captures(pos)}
