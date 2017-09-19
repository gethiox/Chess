from typing import Union, List

from src.domain.pieces import Piece


class Board:
    """
    Board only stores list of Pieces and unfortunately not of their positions
    Positions are hold by Pieces themselves just because it is interesting to implement it that way.
    It is just my retarded project, what did you even expect from it?
    """

    def __init__(self, pieces: Union[List[Piece], None] = None):
        if pieces:
            self.pieces = pieces
        else:
            self.pieces = []

    def array(self) -> List[List[Union[Piece, None]]]:
        """
        Dynamically generated two-dimensional board array
        :return: 8x8 board array
        """
        arr = [[None for _ in range(8)] for _ in range(8)]

        for piece in self.pieces:
            x, y = tuple(piece.position)
            arr[x][y] = piece

        return arr

    def fen(self) -> str:
        arr = self.array()
        board_fen = ''

        # Here we go into C programming style

        x, y = 0, 7
        no_pieces_counter = 0
        while y >= 0:
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
            x = 0
            y -= 1

        # Pretty easy to understand

        return board_fen

    def __repr__(self):
        return '<Board: %s>' % self.fen()

    def __str__(self):
        return self.fen()


class Chess:
    pass  # TODO

