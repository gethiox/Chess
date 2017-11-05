# see more: https://en.wikipedia.org/wiki/List_of_chess_variants
from typing import Sequence, Type, TYPE_CHECKING

from app.move import StandardMove
from app.pieces import King, Pawn, Knight, Bishop, Rook, Queen
from app.position import StandardPosition
from app.sides import White, Black
from interface.variant import Variant

if TYPE_CHECKING:
    from interface.move import Move
    from interface.position import Position
    from interface.piece import Piece
    from interface.side import Side


class Normal(Variant):
    def assert_move(self, move: StandardMove) -> bool:
        return True  # TODO

    @property
    def sides(self) -> Sequence[Type['Side']]:
        return White, Black

    def init_board_state(self):
        self.board.put_piece(piece=Rook(White), position=StandardPosition((0, 0)))
        self.board.put_piece(piece=Rook(White), position=StandardPosition((7, 0)))
        self.board.put_piece(piece=Knight(White), position=StandardPosition((1, 0)))
        self.board.put_piece(piece=Knight(White), position=StandardPosition((6, 0)))
        self.board.put_piece(piece=Bishop(White), position=StandardPosition((2, 0)))
        self.board.put_piece(piece=Bishop(White), position=StandardPosition((5, 0)))
        self.board.put_piece(piece=Queen(White), position=StandardPosition((3, 0)))
        self.board.put_piece(piece=King(White), position=StandardPosition((4, 0)))

        for i in range(8):
            self.board.put_piece(piece=Pawn(White), position=StandardPosition((i, 1)))

        for i in range(8):
            self.board.put_piece(piece=Pawn(Black), position=StandardPosition((i, 6)))

        self.board.put_piece(piece=Rook(Black), position=StandardPosition((0, 7)))
        self.board.put_piece(piece=Rook(Black), position=StandardPosition((7, 7)))
        self.board.put_piece(piece=Knight(Black), position=StandardPosition((1, 7)))
        self.board.put_piece(piece=Knight(Black), position=StandardPosition((6, 7)))
        self.board.put_piece(piece=Bishop(Black), position=StandardPosition((2, 7)))
        self.board.put_piece(piece=Bishop(Black), position=StandardPosition((5, 7)))
        self.board.put_piece(piece=Queen(Black), position=StandardPosition((3, 7)))
        self.board.put_piece(piece=King(Black), position=StandardPosition((4, 7)))

        return self.board.get_fen()

    @property
    def pieces(self) -> Sequence[Type['Piece']]:
        return King, Queen, Rook, Bishop, Knight, Pawn

    def available_moves(self, position: Type['Position']) -> Sequence[Type['Move']]:
        pass  # TODO
        # moves = []
        # piece = self.board.get_piece(position)
        # if not piece:
        #     return moves
        #
        # for move_description in piece.movement.move:
        #     pass
        # for capture_description in piece.movement.capture:
        #     pass

    def attacked_fields(self, side: Type['Side']) -> Sequence[Type['Position']]:
        pass

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
