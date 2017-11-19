from typing import TYPE_CHECKING

from interface.move import Move

if TYPE_CHECKING:
    from app.position import StandardPosition


class StandardMove(Move):
    """
    Two Position aggregator with optional pawn promotion information
    """

    @property
    def source(self) -> 'StandardPosition':
        return self._source

    @property
    def destination(self) -> 'StandardPosition':
        return self._destination

    @property
    def promotion(self):
        return self._promotion
