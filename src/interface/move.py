from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from interface.piece import Piece
    from interface.position import Position


class Move(metaclass=ABCMeta):
    def __init__(self, source: 'Position', destination: 'Position', promotion: 'Piece' = None):
        self._source = source
        self._destination = destination
        self._promotion = promotion

    def __repr__(self):  # TODO: update for positions objects without support of converting to string
        if self._promotion:
            return 'Move: %s to %s with promotion to %s' % (self._source, self._destination, self._promotion.name)
        else:
            return 'Move: %s to %s' % (self._source, self._destination)

    def __str__(self):
        if self._promotion:
            # TODO: fix converting move with promotion to string (object holds uninitialized children of Piece)
            return '%s%s%s' % (self._source, self._destination, self._promotion.char)
        else:
            return '%s%s' % (self._source, self._destination)

    @property
    @abstractmethod
    def destination(self) -> Type['Position']:
        pass

    @property
    @abstractmethod
    def source(self) -> Type['Position']:
        pass

    @property
    @abstractmethod
    def promotion(self) -> Type['Piece']:
        pass
