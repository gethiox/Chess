from unittest import TestCase

from app.move import StandardMove
from app.player import Player
from app.position import StandardPosition
from app.sides import Black
from app.variants import Normal
from cli import board_rendererer
from interface.game import Game


class MyTestCase(TestCase):
    def setUp(self):
        self.game = Game(Player('White Player'), Player('Black Player'), Normal())
        self.variant = self.game.variant

    def test_some(self):
        board_rendererer.tiny(self.variant.board)
        print()
        for move in self.generate_moves(['f2f3', 'e7e6', 'g2g4', 'd8h4']):
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
                          available_moves=len(self.variant.all_available_moves),
                          game_status=self.variant.game_state)
            )
        self.assertEqual(
            self.variant.game_state, {Black}
        )

    def generate_moves(self, str_moves):
        for str_move in str_moves:
            yield StandardMove(StandardPosition(str_move[:2]), StandardPosition(str_move[-2:]))
