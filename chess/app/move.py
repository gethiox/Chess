from chess.app.pieces import from_str
from chess.app.position import StandardPosition
from chess.interface.move import Move


class StandardMove(Move):
    """
    Two Position aggregator with optional pawn promotion information
    """

    @classmethod
    def from_str(cls, move_str: str):
        if len(move_str) == 4:
            return cls(StandardPosition.from_str(move_str[0:2]),
                       StandardPosition.from_str(move_str[2:4]))

        elif len(move_str) == 5:
            return cls(StandardPosition.from_str(move_str[0:2]),
                       StandardPosition.from_str(move_str[2:4]),
                       from_str(move_str[4], initialized=False))
        else:
            raise ValueError('Primitive move is described as 4-5 length string (without or with promotion)')

    @property
    def source(self) -> 'StandardPosition':
        return self._source

    @property
    def destination(self) -> 'StandardPosition':
        return self._destination

    @property
    def promotion(self):
        return self._promotion
