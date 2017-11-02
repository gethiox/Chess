from math import inf as infinity
from typing import TYPE_CHECKING, Type, Sequence

from app.sides import White, Black
from interface.piece import Piece

if TYPE_CHECKING:
    from interface.move import Move
    from interface.position import Position
    from interface.board import Board


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

    def available_moves(self, board: Type['Board'], position: Type['Position']) -> Sequence[Type['Move']]:
        raise NotImplemented


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

    def available_moves(self, board: Type['Board'], position: Type['Position']) -> Sequence[Type['Move']]:
        raise NotImplemented


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

    def available_moves(self, board: Type['Board'], position: Type['Position']) -> Sequence[Type['Move']]:
        raise NotImplemented


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

    def available_moves(self, board: Type['Board'], position: Type['Position']) -> Sequence[Type['Move']]:
        raise NotImplemented


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

    def available_moves(self, board: Type['Board'], position: Type['Position']) -> Sequence[Type['Move']]:
        raise NotImplemented


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

    def available_moves(self, board: Type['Board'], position: Type['Position']) -> Sequence[Type['Move']]:
        raise NotImplemented


str_map = {
    'k': King,
    'q': Queen,
    'r': Rook,
    'b': Bishop,
    'n': Knight,
    'p': Pawn,
}


def from_str(piece: str) -> Type['Piece']:  # TODO: Use another solution
    """ 
    Method designed to return Piece object from given one-letter string.
    Needed only for processing FEN board-state format.
    """
    if piece.lower() not in ('k', 'q', 'r', 'b', 'n', 'p'):
        raise ValueError('"%s" not defined as Chess piece.', piece)
    return str_map[piece.lower()](White) if piece.isupper() else str_map[piece.lower()](Black)
