from datetime import datetime
from typing import Type, Tuple, TYPE_CHECKING, List

from app.sides import White, Black

if TYPE_CHECKING:
    from interface.move import Move
    from interface.board import Board
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
        self.__variant = variant

        self.__start_time = None
        self.__create_time = datetime.now()

        self.__moves = 0
        self.__half_moves = 0
        self.__moves_history = []

    @property
    def moves_history(self) -> List[Type['Move']]:
        return self.__moves_history

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

    @property
    def on_move(self) -> Type['Side']:
        sides = tuple(self.__players.keys())
        return sides[self.__half_moves % len(self.players)]

    def move(self, move: Type['Move']):
        if not self.variant.assert_move(move):
            raise ValueError("Move not allowed")
        piece = self.board.remove_piece(position=move.source)
        self.board.put_piece(piece=piece, position=move.destination)
        self.moves_history.append(move)

    def start_game(self):
        self.__start_time = datetime.now()

    def game_state(self) -> Type['Side']:

        """
        method return game state which depends on specific rules for every game mode.
        Look into "Normal" game mode class for inspirations (if is even implemented right now)
        :return: not_yet_started OR on_move_side OR winner_side
        """
        pass
