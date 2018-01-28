from datetime import datetime
from typing import Type, Tuple, TYPE_CHECKING

from chess.app.sides import White, Black

if TYPE_CHECKING:
    from chess.interface.move import Move
    from chess.interface.board import Board
    from chess.interface.variant import Variant
    from chess.app.player import Player


class Game:
    """
    Generic Game logic base class
    """

    def __init__(self, player1: 'Player', player2: 'Player', variant: 'Variant'):
        self.__players = {
            White: player1,
            Black: player2,
        }
        self.__variant = variant

        self.__start_time = None
        self.__create_time = datetime.now()

    @property
    def board(self) -> Type['Board']:
        return self.__variant.board

    @property
    def variant(self):
        return self.__variant

    @property
    def players(self) -> Tuple['Player', ...]:
        return tuple(player for _, player in self.__players.items())

    @property
    def start_time(self) -> datetime:
        return self.__start_time

    @property
    def creation_date(self) -> datetime:
        return self.__create_time

    def move(self, move: Type['Move']) -> bool:
        return self.variant.move(move)

    def start_game(self):
        self.__start_time = datetime.now()
