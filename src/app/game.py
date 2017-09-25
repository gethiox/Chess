from string import digits

from app.cli_board import tiny_rendererer
from app.pieces import from_str


class Board:
    """
    Board only stores list of Pieces and unfortunately not of their positions
    Positions are hold by Pieces themselves just because it is interesting to implement it that way.
    It is just my retarded project, what did you even expect from it?
    """

    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]

    def render(self):
        tiny_rendererer(self.board)

    def set_fen(self, board_fen: str):
        """
        Sets board state from FEN
        :param board_fen: string, min 15 letters (ranks separated by slash)
        """

        y = 7
        for rank in board_fen.split('/'):
            x = 0
            for piece in rank:
                if piece not in digits:
                    self.board[x][y] = from_str(piece)
                    x += 1
                else:
                    for i in range(int(piece)):
                        x += 1
            y -= 1

    def get_fen(self) -> str:
        """
        :return: FEN representation of board state
        """
        board_fen = ''

        # Here we go into C programming style

        no_pieces_counter = 0
        y = 7
        while y >= 0:
            x = 0
            while x <= 7:
                piece = self.board[x][y]
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

    def _clear(self):
        """Should be not used but here you go, just for you"""
        self.board = [[None for _ in range(8)] for _ in range(8)]

    def __repr__(self):
        return '<Board: %s>' % self.get_fen()

    def __str__(self):
        return self.get_fen()


class Chess:
    def __init__(self):
        self.board = Board()

    def new_game(self):
        self.board.set_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
