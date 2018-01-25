from math import inf as infinity

from app.sides import White, Black
from interface.piece import Piece, Movement, MoveDescription, CaptureDescription


class King(Piece):
    char = "k"

    @property
    def points(self):
        return infinity

    @property
    def name(self):
        return "King"

    @property
    def movement(self) -> 'Movement':
        return Movement(
            move_descriptions=[
                MoveDescription(vector=(0, 1), any_direction=True, distance=1, capture_break=True),
                MoveDescription(vector=(1, 1), any_direction=True, distance=1, capture_break=True),
            ],
        )


class Queen(Piece):
    char = "q"

    @property
    def points(self) -> int:
        return 9

    @property
    def name(self) -> str:
        return "Queen"

    @property
    def movement(self) -> 'Movement':
        return Movement(
            move_descriptions=[
                MoveDescription(vector=(0, 1), any_direction=True, distance=infinity, capture_break=True),
                MoveDescription(vector=(1, 1), any_direction=True, distance=infinity, capture_break=True),
            ],
        )


class Rook(Piece):
    char = 'r'

    @property
    def points(self) -> int:
        return 5

    @property
    def name(self) -> str:
        return "Rook"

    @property
    def movement(self) -> 'Movement':
        return Movement(
            move_descriptions=[
                MoveDescription(vector=(0, 1), any_direction=True, distance=infinity, capture_break=True),
            ],
        )


class Bishop(Piece):
    char = 'b'

    @property
    def points(self) -> int:
        return 3

    @property
    def name(self) -> str:
        return 'Bishop'

    @property
    def movement(self) -> 'Movement':
        return Movement(
            move_descriptions=[
                MoveDescription(vector=(1, 1), any_direction=True, distance=infinity, capture_break=True),
            ],
        )


class Knight(Piece):
    char = "n"

    @property
    def points(self) -> int:
        return 3

    @property
    def name(self) -> str:
        return "Knight"

    @property
    def movement(self) -> 'Movement':
        return Movement(
            move_descriptions=[
                MoveDescription(vector=(1, 2), any_direction=True, distance=1, capture_break=False),
            ],
        )


class Pawn(Piece):
    char = "p"

    @property
    def points(self) -> int:
        return 1

    @property
    def name(self) -> str:
        return "Pawn"

    @property
    def movement(self) -> 'Movement':
        return Movement(
            move_descriptions=[
                MoveDescription(vector=(0, 1), any_direction=False, distance=1, capture_break=True),
            ],
            capture_descriptions=[
                CaptureDescription(vector=(1, 1), any_direction=False, distance=1, capture_break=False),
                CaptureDescription(vector=(-1, 1), any_direction=False, distance=1, capture_break=False),
            ]
        )


str_map = {
    'k': King,
    'q': Queen,
    'r': Rook,
    'b': Bishop,
    'n': Knight,
    'p': Pawn,
}


def from_str(piece: str, initialized=True) -> 'Piece':  # TODO: Use another solution
    """
    Method designed to return Piece object from given one-letter string.
    Needed only for processing FEN board-state format.
    """
    if piece.lower() not in ('k', 'q', 'r', 'b', 'n', 'p'):
        raise ValueError('"%s" not defined as Chess piece.' % piece)
    if initialized:
        return str_map[piece.lower()](White) if piece.isupper() else str_map[piece.lower()](Black)
    return str_map[piece.lower()]
