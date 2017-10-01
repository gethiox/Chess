from string import digits

from app.cli_board import tiny_rendererer
from app.pieces import from_str


class Board:
    """
    Base board object, used to create variable-size boards
    """

    def __init__(self, size_x: int = 8, size_y: int = 8):  # 8x8 as standard size of chess board
        self.__size_x = size_x
        self.__size_y = size_y

        self.board = [[None for _ in range(self.size[1])] for _ in range(self.size[0])]

    @property
    def size(self) -> tuple:
        return self.__size_x, self.__size_y

    def render(self):
        # TODO: More rendererers, if more than one will appear then refactor
        # TODO: Re/move CLI renderer from this object, it is not supposed to be there
        tiny_rendererer(self.board)

    def set_fen(self, board_fen: str):  # TODO: validate input string
        """
        Sets board state from FEN
        :param board_fen: string, min 15 letters (ranks separated by slash)
        """
        board_tmp = [[None for _ in range(self.size[1])] for _ in range(self.size[0])]

        # thumbs up for more AVR-Based code like this, maybe assembly inside Python?

        y = self.size[1] - 1
        for rank in board_fen.split('/'):
            x = 0
            for piece in rank:
                if piece not in digits:
                    board_tmp[x][y] = from_str(piece)
                    x += 1
                else:
                    for i in range(int(piece)):
                        x += 1
            y -= 1

        self.board = board_tmp

    def get_fen(self) -> str:
        """
        :return: FEN representation of board state
        """
        board_fen = ''

        # Here we go into C programming style

        no_pieces_counter = 0
        y = self.size[1] - 1
        while y >= 0:
            x = 0
            while x <= self.size[0] - 1:
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

    def __repr__(self):
        return '<Board: %s>' % self.get_fen()

    def __str__(self):
        return self.get_fen()


class Chess:
    def __init__(self):
        self.board = Board()

    def new_game(self):
        self.board.set_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
