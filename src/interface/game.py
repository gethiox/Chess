from datetime import datetime
from typing import Type, Tuple, TYPE_CHECKING

from app.sides import White, Black
from interface.move import Move

if TYPE_CHECKING:
    from interface.variant import Variant
    from app.player import Player
    from interface.side import Side


class Game:
    """
    Generic Game logic base class
    """

    def __init__(self, player1: 'Player', player2: 'Player', variant: 'Variant'):
        self.__players = {
            White: player1,
            Black: player2,
        }
        self.variant = variant
        self.variant.init_board_state()

        self.__start_time = None
        self.__create_time = datetime.now()

        self.__moves = 0
        self.__half_moves = 0

    @property
    def players(self) -> Tuple['Player', ...]:
        return tuple(player for _, player in self.__players.items())

    @property
    def start_time(self) -> datetime:
        return self.__start_time

    @property
    def creation_date(self) -> datetime:
        return self.__create_time

    @property
    def on_move(self) -> Type['Side']:
        sides = tuple(self.__players.keys())
        return sides[self.__half_moves % len(self.players)]

    def move(self, move: 'Move') -> bool:
        if self.variant.assert_move(move):
            piece = self.variant.board.remove_piece(move.source)
            self.variant.board.put_piece(piece, move.destination)
            return True
        return False

    def start_game(self):
        self.__start_time = datetime.now()

    def game_state(self) -> Type['Side']:
        """
        method return game state which depends on specific rules for every game mode.
        Look into "Normal" game mode class for inspirations (if is even implemented right now)
        :return: not_yet_started OR on_move_side OR winner_side
        """
        pass
