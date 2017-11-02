from abc import ABCMeta, abstractmethod
from typing import Optional, TYPE_CHECKING, Type

if TYPE_CHECKING:
    from interface.piece import Piece
    from interface.position import Position


class Move(metaclass=ABCMeta):
    def __init__(self, a: Type['Position'], b: Type['Position'], promotion: Optional[Type['Piece']] = None):
        self.__a = a
        self.__b = b
        self.__promotion = promotion

    def __repr__(self):  # TODO: update for positions objects without support of converting to string
        if self.__promotion:
            return 'Move: %s to %s with promotion to %s' % (self.__a, self.__b, self.__promotion.name)
        else:
            return 'Move: %s to %s' % (self.__a, self.__b)

    def __str__(self):
        if self.__promotion:
            return '%s%s%s' % (self.__a, self.__b, self.__promotion.char)
        else:
            return '%s%s' % (self.__a, self.__b)

    @property
    @abstractmethod
    def b(self) -> Type['Position']:
        pass

    @property
    @abstractmethod
    def a(self) -> Type['Position']:
        pass

    @property
    @abstractmethod
    def promotion(self) -> Type['Piece']:
        pass
