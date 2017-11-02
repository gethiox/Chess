from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Type, Tuple

from domain.mode import GameMode
from domain.player import Player
from domain.side import Side


class Game(metaclass=ABCMeta):
    """
    Generic Game logic base class
    """

    def __init__(self, player1: Player, player2: Player, mode: Type[GameMode]):
        self.__players = [
            player1,
            player2,
        ]
        self.mode = mode

        self.__start_time = None
        self.__create_time = datetime.now()

        self.__moves = 0
        self.__half_moves = 0

    @property
    def players(self) -> Tuple[Player, ...]:
        return tuple(player for _, player in self.__players.items())

    @property
    def start_time(self) -> datetime:
        return self.__start_time

    @property
    def creation_date(self) -> datetime:
        return self.__create_time

    @property
    def on_move(self) -> Type[Side]:
        sides = tuple(self.__players.keys())
        return sides[self.__half_moves % len(self.players)]

    def start_game(self):
        self.__start_time = datetime.now()

    @abstractmethod
    def game_state(self) -> Type[Side]:
        """
        method return game state which depends on specific rules for every game mode.
        Look into "Normal" game mode class for inspirations (if is even implemented right now)
        :return: not_yet_started OR on_move_side OR winner_side
        """
        pass
