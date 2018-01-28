from chess.app.pieces import Rook, Knight, Bishop, Queen, King, Pawn
from chess.app.position import StandardPosition
from chess.app.sides import Black, White
from chess.app.variants.classic import Normal


class UpsideDown(Normal):
    @property
    def name(self):
        return "Upside Down"

    def init_board_state(self):
        """
        Set board start position for classic chess variant
        """
        self.board.put_piece(piece=Rook(Black), position=StandardPosition((0, 0)))
        self.board.put_piece(piece=Rook(Black), position=StandardPosition((7, 0)))
        self.board.put_piece(piece=Knight(Black), position=StandardPosition((1, 0)))
        self.board.put_piece(piece=Knight(Black), position=StandardPosition((6, 0)))
        self.board.put_piece(piece=Bishop(Black), position=StandardPosition((2, 0)))
        self.board.put_piece(piece=Bishop(Black), position=StandardPosition((5, 0)))
        self.board.put_piece(piece=Queen(Black), position=StandardPosition((3, 0)))
        self.board.put_piece(piece=King(Black), position=StandardPosition((4, 0)))

        for i in range(8):
            self.board.put_piece(piece=Pawn(Black), position=StandardPosition((i, 1)))

        for i in range(8):
            self.board.put_piece(piece=Pawn(White), position=StandardPosition((i, 6)))

        self.board.put_piece(piece=Rook(White), position=StandardPosition((0, 7)))
        self.board.put_piece(piece=Rook(White), position=StandardPosition((7, 7)))
        self.board.put_piece(piece=Knight(White), position=StandardPosition((1, 7)))
        self.board.put_piece(piece=Knight(White), position=StandardPosition((6, 7)))
        self.board.put_piece(piece=Bishop(White), position=StandardPosition((2, 7)))
        self.board.put_piece(piece=Bishop(White), position=StandardPosition((5, 7)))
        self.board.put_piece(piece=Queen(White), position=StandardPosition((3, 7)))
        self.board.put_piece(piece=King(White), position=StandardPosition((4, 7)))

        return self.board.get_fen()