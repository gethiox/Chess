# see more: https://en.wikipedia.org/wiki/List_of_chess_variants

from abc import abstractmethod
from time import time

from domain.pieces import Side


class GameMode:
    """
    Generic Game Mode class
    """
    start_time = None

    @property
    @abstractmethod
    def on_move(self) -> Side:
        """ REQUIRED
        :return: Side
        """
        return NotImplemented

    def start_game(self):
        self.start_time = time()

    @abstractmethod
    def game_state(self):
        """ REQUIRED
        method return game state which depends on specific rules for every game mode.
        Look into "Normal" game mode class for inspirations (if is even implemented right now)
        :return: not_yet_started OR on_move_side OR winner_side
        """
        raise NotImplemented


class Normal(GameMode):
    pass


class Chess960(GameMode):
    pass


class Crazyhouse(GameMode):
    pass


class KingOfTheHill(GameMode):
    pass


class ThreeCheck(GameMode):
    pass


class Horde(GameMode):
    pass


class PreChess(GameMode):
    """Could be interesting to implement"""
    pass


class UpsideDown(GameMode):
    pass


class Double(GameMode):
    """Could be interesting to implement as well"""
    pass


class Antichess(GameMode):
    """Just because LiChess supports it"""
    pass


class RacingKings(GameMode):
    """Like above"""
    pass
