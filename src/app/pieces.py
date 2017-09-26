from math import inf as infinity

from domain.pieces import Piece, White, Black


class King(Piece):
    name = 'King'
    char = 'k'
    points = infinity


class Queen(Piece):
    name = 'Queen'
    char = 'q'
    points = 9


class Rook(Piece):
    name = 'Rook'
    char = 'r'
    points = 5


class Bishop(Piece):
    name = 'Bishop'
    char = 'b'
    points = 3


class Knight(Piece):
    name = 'Knight'
    char = 'n'
    points = 3


class Pawn(Piece):
    name = 'Pawn'
    char = 'p'
    points = 1


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
