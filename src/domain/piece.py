from abc import ABCMeta, abstractmethod
from typing import Type, Sequence

from domain.board import Board
from domain.move import Move
from domain.position import Position
from domain.side import Side


class Piece(metaclass=ABCMeta):
    def __init__(self, side: Type[Side]):
        self.__side = side

    @property
    @abstractmethod
    def name(self) -> str:
        """return piece name starts with uppercase, eg. Pawn"""
        pass

    @property
    @abstractmethod
    def char(self) -> str:
        """return one lowercase letter representation of piece, eg. p"""
        pass

    @property
    @abstractmethod
    def points(self) -> int:
        """return int piece value representation, eg. 1"""
        pass

    @abstractmethod
    def available_moves(self, board: Type[Board], position: Type[Position]) -> Sequence[Type[Move]]:
        """return sequence of available Moves"""
        pass

    @property
    def side(self) -> Type[Side]:
        return self.__side

    def __repr__(self):
        return '<%s %s>' % (self.side, self.name)

    def __str__(self):
        return self.char.upper() if self.side.capitalize else self.char.lower()

    def __eq__(self, other):
        if isinstance(other, Piece):
            return isinstance(other, type(self)) and other.side == self.side

    def __ne__(self, other):
        if isinstance(other, Piece):
            return not (isinstance(other, type(self)) and other.side == self.side)
        return True
