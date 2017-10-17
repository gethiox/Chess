from string import digits
from typing import Optional

from app.cli_board import tiny_rendererer
from app.pieces import from_str
from domain.game import Board
from domain.pieces import Piece, StandardPosition


class StandardBoard(Board):
    """
    Standard chess board, used to create variable-sized two dimensional boards
    """

    @property
    def name(self) -> str:
        return "Standard Chess Board"

    def __init__(self, files: int = 8, ranks: int = 8):  # 8x8 as standard size of chess board
        self.__files = files
        self.__ranks = ranks
        self.__board_array = [[None for _ in range(self.ranks)] for _ in range(self.files)]

    @property
    def size(self) -> tuple:
        return self.__files, self.__ranks

    @property
    def files(self) -> int:
        return self.__files

    @property
    def ranks(self) -> int:
        return self.__ranks

    def render(self):
        # TODO: More rendererers, if more than one will appear then refactor
        # TODO: Re/move CLI renderer from this object, it is not supposed to be there
        tiny_rendererer(self.__board_array)

    def _get_piece(self, position: StandardPosition) -> Optional[Piece]:
        """
        Get Piece on given Position
        :param position: Position object
        :return: Piece on given Position
        """
        current = self.__board_array[position.file][position.rank]
        return current

    def _put_piece(self, piece: Piece, position: StandardPosition) -> Optional[Piece]:
        """
        Put Piece on given Position
        :param piece: Just any kind of Piece
        :param position: Position object
        :return: Piece that was standing before putting new (None if none)
        """
        current = self.__board_array[position.file][position.rank]
        self.__board_array[position.file][position.rank] = piece
        return current

    def _remove_piece(self, position: StandardPosition) -> Optional[StandardPosition]:
        """
        Remove Piece from given Position
        :param position: Position object
        :return: Piece that are removed (None if none)
        """
        current = self.__board_array[position.file][position.rank]
        self.__board_array[position.file][position.rank] = None
        return current

    def set_fen(self, board_fen: str):
        # TODO: validate input string
        # TODO: solve variable board problem, support it in some kind of way or disband
        """
        Sets board state from FEN
        :param board_fen: string, min 15 letters (ranks separated by slash)
        """
        board_tmp = [[None for _ in range(self.ranks)] for _ in range(self.files)]

        # thumbs up for more AVR-Based code like this, maybe assembly inside Python?

        rank_counter = self.ranks - 1
        for rank in board_fen.split('/'):
            file_counter = 0
            for piece in rank:
                if piece not in digits:
                    board_tmp[file_counter][rank_counter] = from_str(piece)
                    file_counter += 1
                else:
                    for i in range(int(piece)):
                        file_counter += 1
            rank_counter -= 1

        self.__board_array = board_tmp

    def get_fen(self) -> str:
        # TODO: solve variable board problem, support it in some kind of way or disband
        """
        :return: FEN representation of board state
        """
        board_fen = ''

        # Here we go into C programming style

        no_pieces_counter = 0
        rank_counter = self.ranks - 1
        while rank_counter >= 0:
            file_counter = 0
            while file_counter <= self.files - 1:
                piece = self.__board_array[file_counter][rank_counter]
                if piece:
                    if no_pieces_counter > 0:
                        board_fen += str(no_pieces_counter)
                        no_pieces_counter = 0
                    board_fen += str(piece)
                else:
                    no_pieces_counter += 1
                file_counter += 1
            if no_pieces_counter > 0:
                board_fen += str(no_pieces_counter)
                no_pieces_counter = 0
            if rank_counter > 0:
                board_fen += '/'
            rank_counter -= 1

        # Pretty easy to understand

        return board_fen


class Chess:
    def __init__(self):
        self.board = StandardBoard()

    def new_game(self):
        self.board.set_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
