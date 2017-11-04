# see more: https://en.wikipedia.org/wiki/List_of_chess_variants
from typing import Sequence, Type, TYPE_CHECKING

from app.move import StandardMove
from app.pieces import King, Pawn, Knight, Bishop, Rook, Queen
from app.sides import White, Black
from interface.mode import GameMode

if TYPE_CHECKING:
    from interface.piece import Piece
    from interface.side import Side


class Normal(GameMode):
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


# class Chess960(GameMode):
#     pass
#
#
# class Crazyhouse(GameMode):
#     pass
#
#
# class KingOfTheHill(GameMode):
#     pass
#
#
# class ThreeCheck(GameMode):
#     pass
#
#
# class Horde(GameMode):
#     pass
#
#
# class PreChess(GameMode):
#     """Could be interesting to implement"""
#     pass
#
#
# class UpsideDown(GameMode):
#     pass
#
#
# class Double(GameMode):
#     """Could be interesting to implement as well"""
#     pass
#
#
# class Antichess(GameMode):
#     """Just because LiChess supports it"""
#     pass
#
#
# class RacingKings(GameMode):
#     """Like above"""
#     pass
