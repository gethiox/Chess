from string import digits
from typing import List, Optional

from app.cli_board import tiny_rendererer
from app.pieces import from_str
from domain.pieces import Piece
from domain.pieces import Position


class Board:
    """
    Board only stores list of Pieces and unfortunately not of their positions
    Positions are hold by Pieces themselves just because it is interesting to implement it that way.
    It is just my retarded project, what did you even expect from it?
    """

    def __init__(self, pieces: Optional[List[Piece]] = None):
        if pieces:
            self.pieces = pieces
        else:
            self.pieces = []

    def render(self):
        tiny_rendererer(self._array())

    def set_fen(self, board_fen: str):
        pieces = []

        y = 7
        for rank in board_fen.split('/'):
            x = 0
            for piece in rank:
                if piece not in digits:
                    pieces.append(from_str(piece, Position((x, y))))
                    x += 1
                else:
                    for i in range(int(piece)):
                        x += 1
            y -= 1

        self.pieces = pieces

    def get_fen(self) -> str:
        """
        :return: FEN representation of board state
        """
        arr = self._array()
        board_fen = ''

        # Here we go into C programming style

        no_pieces_counter = 0
        y = 7
        while y >= 0:
            x = 0
            while x <= 7:
                piece = arr[x][y]
                if piece:
                    if no_pieces_counter > 0:
                        board_fen += str(no_pieces_counter)
                        no_pieces_counter = 0
                    board_fen += str(piece)
                else:
                    no_pieces_counter += 1
                x += 1
            if no_pieces_counter > 0:
                board_fen += str(no_pieces_counter)
                no_pieces_counter = 0
            if y > 0:
                board_fen += '/'
            y -= 1

        # Pretty easy to understand

        return board_fen

    def _array(self) -> List[List[Optional[Piece]]]:
        """
        Dynamically generated two-dimensional board array
        :return: 8x8 board array
        """
        arr = [[None for _ in range(8)] for _ in range(8)]

        for piece in self.pieces:
            x, y = tuple(piece.position)
            arr[x][y] = piece

        return arr

    def __repr__(self):
        return '<Board: %s>' % self.get_fen()

    def __str__(self):
        return self.get_fen()


class Chess:
    def __init__(self):
        self.board = Board()

    def new_game(self):
        self.board.set_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
