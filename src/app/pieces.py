from math import inf as infinity

from domain.pieces import Piece, Side


class King(Piece):
    @property
    def char(self):
        return "k"

    @property
    def points(self):
        return infinity

    @property
    def name(self):
        return "King"


class Queen(Piece):
    @property
    def points(self) -> int:
        return 9

    @property
    def char(self) -> str:
        return "q"

    @property
    def name(self) -> str:
        return "Queen"


class Rook(Piece):
    @property
    def points(self) -> int:
        return 5

    @property
    def char(self) -> str:
        return 'r'

    @property
    def name(self) -> str:
        return "Rook"


class Bishop(Piece):
    @property
    def points(self) -> int:
        return 3

    @property
    def char(self) -> str:
        return 'b'

    @property
    def name(self) -> str:
        return 'Bishop'


class Knight(Piece):
    @property
    def points(self) -> int:
        return 3

    @property
    def char(self) -> str:
        return "n"

    @property
    def name(self) -> str:
        return "Knight"


class Pawn(Piece):
    @property
    def points(self) -> int:
        return 1

    @property
    def char(self) -> str:
        return "p"

    @property
    def name(self) -> str:
        return "Pawn"


class WhiteSide(Side):
    @property
    def char(self):
        return "w"

    @property
    def name(self) -> str:
        return "White"

    @property
    def capitalize(self) -> bool:
        return True


class BlackSide(Side):
    @property
    def char(self):
        return "b"

    @property
    def name(self) -> str:
        return "Black"

    @property
    def capitalize(self) -> bool:
        return False


White = WhiteSide()
Black = BlackSide()

str_map = {
    'k': King,
    'q': Queen,
    'r': Rook,
    'b': Bishop,
    'n': Knight,
    'p': Pawn,
}


def from_str(piece: str) -> Piece:
    """
    Method designed to return Piece object from given one-letter string.
    Needed only for processing FEN board-state format.
    """
    if piece.lower() not in ('k', 'q', 'r', 'b', 'n', 'p'):
        raise ValueError('"%s" not defined as Chess piece.', piece)
    return str_map[piece.lower()](White) if piece.isupper() else str_map[piece.lower()](Black)
