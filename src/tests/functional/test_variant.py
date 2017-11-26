from unittest import TestCase

from app.move import StandardMove
from app.player import Player
from app.position import StandardPosition
from app.sides import Black
from app.variants import Normal
from cli import board_rendererer
from exceptions.variant import CausesCheck
from interface.game import Game


class MyTestCase(TestCase):
    def setUp(self):
        self.game = Game(Player('White Player'), Player('Black Player'), Normal())
        self.variant = self.game.variant

    def test_some(self):
        board_rendererer.tiny(self.variant.board)
        print()
        for move in self.moves_from_str(['f2f3', 'e7e6', 'g2g4', 'd8h4']):
            status = self.variant.move(move)
            if status:
                print('Move execution %s ok' % move)
            else:
                print('Move execution %s failed' % move)

            board_rendererer.tiny(self.variant.board)
            print(
                "\n"
                "half move: {half}\n"
                "move: {moves}\n"
                "on move: {on_move}\n"
                "last move: {last_move}\n"
                "available moves: {available_moves}\n"
                "game status: {game_status}\n"
                "".format(half=self.variant.half_moves,
                          moves=self.variant.moves,
                          on_move=self.variant.on_move,
                          last_move=self.variant.last_move,
                          available_moves=len(self.variant.all_available_moves()),
                          game_status=self.variant.game_state)
            )
        self.assertEqual(
            self.variant.game_state, {Black}
        )

    def test_CausesCheck(self):
        self.game.move(self.move_from_str('e2e3'))
        self.game.move(self.move_from_str('e7e6'))
        self.game.move(self.move_from_str('d1h5'))

        with self.assertRaises(CausesCheck):
            self.game.move(self.move_from_str('f7f6'))

    def moves_from_str(self, moves_str):
        for move_str in moves_str:
            yield StandardMove(
                StandardPosition.from_str(move_str[:2]),
                StandardPosition.from_str(move_str[-2:])
            )

    def move_from_str(self, move_str: str):
        return StandardMove(
            StandardPosition.from_str(move_str[:2]),
            StandardPosition.from_str(move_str[2:])
        )
