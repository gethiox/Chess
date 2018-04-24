from typing import Tuple, Optional, Set, Type, TYPE_CHECKING

from chess.app.pieces import King, Queen, Rook, Bishop, Knight
from chess.app.position import StandardPosition
from chess.app.sides import Black, White
from chess.app.variants.classic import Normal

if TYPE_CHECKING:
    from chess.interface.side import Side


class RacingKings(Normal):
    @property
    def name(self):
        return "Racing Kings"

    def init_board_state(self):
        self.board.put_piece(King(Black), StandardPosition.from_str('a2'))
        self.board.put_piece(Queen(Black), StandardPosition.from_str('a1'))
        self.board.put_piece(Rook(Black), StandardPosition.from_str('b2'))
        self.board.put_piece(Rook(Black), StandardPosition.from_str('b1'))
        self.board.put_piece(Bishop(Black), StandardPosition.from_str('c2'))
        self.board.put_piece(Bishop(Black), StandardPosition.from_str('c1'))
        self.board.put_piece(Knight(Black), StandardPosition.from_str('d2'))
        self.board.put_piece(Knight(Black), StandardPosition.from_str('d1'))

        self.board.put_piece(King(White), StandardPosition.from_str('h2'))
        self.board.put_piece(Queen(White), StandardPosition.from_str('h1'))
        self.board.put_piece(Rook(White), StandardPosition.from_str('g2'))
        self.board.put_piece(Rook(White), StandardPosition.from_str('g1'))
        self.board.put_piece(Bishop(White), StandardPosition.from_str('f2'))
        self.board.put_piece(Bishop(White), StandardPosition.from_str('f1'))
        self.board.put_piece(Knight(White), StandardPosition.from_str('e2'))
        self.board.put_piece(Knight(White), StandardPosition.from_str('e1'))

        return self.board.get_fen()

    @property
    def game_state(self) -> Tuple[Optional[Set[Type['Side']]], Optional[str]]:
        # find kings position and return winner if king is standing on the eight rank
        kings = []
        for side in self.sides:
            king_pos, piece = self.board.find_pieces(King(side))[0]
            kings.append((king_pos, piece))

        for king_pos, piece in kings:
            if king_pos.rank == 7:
                return {piece.side}, 'king ends the race'

        # else return winner by standard chess rule
        return super(RacingKings, self).game_state
