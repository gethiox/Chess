# see more: https://en.wikipedia.org/wiki/List_of_chess_variants
from typing import Sequence, Type, TYPE_CHECKING

from app.move import StandardMove
from app.pieces import King, Pawn, Knight, Bishop, Rook, Queen
from app.sides import White, Black
from interface.variant import Variant

if TYPE_CHECKING:
    from interface.piece import Piece
    from interface.side import Side


class Normal(Variant):
    def assert_move(self, move: StandardMove) -> bool:
        pass

    @property
    def sides(self) -> Sequence[Type['Side']]:
        return White, Black

    def init_board_state(self):
        pass

    @property
    def pieces(self) -> Sequence[Type['Piece']]:
        return King, Queen, Rook, Bishop, Knight, Pawn


# class Chess960(Variant):
#     pass
#
#
# class Crazyhouse(Variant):
#     pass
#
#
# class KingOfTheHill(Variant):
#     pass
#
#
# class ThreeCheck(Variant):
#     pass
#
#
# class Horde(Variant):
#     pass
#
#
# class PreChess(Variant):
#     """Could be interesting to implement"""
#     pass
#
#
# class UpsideDown(Variant):
#     pass
#
#
# class Double(Variant):
#     """Could be interesting to implement as well"""
#     pass
#
#
# class Antichess(Variant):
#     """Just because LiChess supports it"""
#     pass
#
#
# class RacingKings(Variant):
#     """Like above"""
#     pass
