from abc import ABCMeta, abstractmethod
from typing import Tuple
from functools import lru_cache

from domain.pieces import Move, Piece, Side


class GameMode(metaclass=ABCMeta):
    @abstractmethod
    def init_board_state(self) -> str:
        """
        Sets Board init state for this game mode
        :return FEN strong of part with board only
        """
        pass

    @abstractmethod
    def assert_move(self, move: Move) -> bool:
        """
        Assert if given move in current game state and game mode is legal
        :param move: Move type
        :return: bool, positive if given move is legal
        """
        pass

    @property
    @abstractmethod
    def pieces(self) -> Tuple[Piece]:
        """
        :return: Tuple of Pieces supported with implemented GameMode
        """
        pass

    @property
    @abstractmethod
    def sides(self) -> Tuple[Side]:
        """
        :return: tuple of players sides
        """
        pass

    @lru_cache(maxsize=1)
    def __pieces_dict(self):
        d = {}
        for piece in self.pieces:
            d.update({piece.char: piece})
        return d

    @lru_cache(maxsize=1)
    def __sides_dict(self):
        d = {}
        for side in self.sides:
            d.update({side.char: side})
        return d
