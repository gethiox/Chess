import re
from abc import ABCMeta, abstractmethod
from typing import Optional

from app.pieces import StandardPosition

location_regex = re.compile(r'^(?P<file>[a-zA-Z]+)(?P<rank>[0-9]+)$')


class Side(metaclass=ABCMeta):
    @property
    @abstractmethod
    def name(self) -> str:
        """return defined side name"""
        pass

    @property
    @abstractmethod
    def char(self) -> str:
        """return defined one-char side name"""
        pass

    @property
    @abstractmethod
    def capitalize(self) -> bool:
        """
        Return True if Piece char representation should be capitalized
        Should be implemented only for FEN boards representation purpose
        """
        pass

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, Side):
            return self.name == other.name


class Piece(metaclass=ABCMeta):
    def __init__(self, side: Side):
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

    @property
    def side(self) -> Side:
        return self.__side

    def __repr__(self):
        return '%s %s' % (self.side, self.name)

    def __str__(self):
        return self.char.upper() if self.side.capitalize else self.char.lower()

    def __eq__(self, other):
        if isinstance(other, Piece):
            return isinstance(other, type(self)) and other.side == self.side

    def __ne__(self, other):
        if isinstance(other, Piece):
            return not (isinstance(other, type(self)) and other.side == self.side)
        return True


class Position(metaclass=ABCMeta):
    def __repr__(self):
        return '<Position: %s>' % self

    @abstractmethod
    def __str__(self):
        """Should be implemented for converting position to string purpose if possible, eg. 'e4'"""
        pass

    @abstractmethod
    def __iter__(self):
        """Should be implemented for converting to sequence purpose where first value is a X coordinate, second Y etc."""
        pass

    @abstractmethod
    def __getitem__(self, item):
        """Should be implemented for index access purpose (object[index]). 0 for X, 1 for Y, 2 for Z etc."""
        pass


class Move:  # TODO: Next to abstract? fix constructor
    """
    Two Position aggregator with optional pawn promotion information
    """

    def __init__(self, a: StandardPosition, b: StandardPosition, promotion: Optional[Piece] = None):
        self.__a = a
        self.__b = b
        self.__promotion = promotion

    @property
    def a(self):
        return self.__a

    @property
    def b(self):
        return self.__b

    @property
    def promotion(self):
        return self.__promotion

    def __repr__(self):
        if self.__promotion:
            return 'Move: %s to %s with promotion to %s' % (self.__a, self.__b, self.__promotion.name)
        else:
            return 'Move: %s to %s' % (self.__a, self.__b)

    def __str__(self):
        if self.__promotion:
            return '%s%s%s' % (self.__a, self.__b, self.__promotion.char)
        else:
            return '%s%s' % (self.__a, self.__b)
