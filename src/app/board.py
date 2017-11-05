from string import digits
from typing import Optional, Tuple, Sequence, TYPE_CHECKING

from app.pieces import from_str
from app.position import StandardPosition
from interface.board import Board

if TYPE_CHECKING:
    from interface.piece import Piece


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
        # TODO: Use legit arrays from numpy but maybe it is not necessary

    @property
    def array(self) -> Sequence[Sequence[Optional['Piece']]]:
        return self.__board_array

    @property
    def size(self) -> Tuple[int, int]:
        return self.__files, self.__ranks

    @property
    def files(self) -> int:
        return self.__files

    @property
    def ranks(self) -> int:
        return self.__ranks

    def _get_piece(self, position: StandardPosition) -> Optional['Piece']:
        """
        Get Piece on given Position
        :param position: Position object
        :return: Piece on given Position
        """
        current = self.__board_array[position.file][position.rank]
        return current

    def _put_piece(self, piece: 'Piece', position: StandardPosition) -> Optional['Piece']:
        """
        Put Piece on given Position
        :param piece: Just any kind of Piece
        :param position: Position object
        :return: Piece that was standing before putting new (None if none)
        """
        current = self.__board_array[position.file][position.rank]
        self.__board_array[position.file][position.rank] = piece
        return current

    def _remove_piece(self, position: StandardPosition) -> Optional['Piece']:
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
        """
        Sets board state from FEN
        :param board_fen: string, min 15 letters (ranks separated by slash)
        """
        if self.files != 8 or self.ranks != 8:  # FEN is not supported on other-sized board than 8x8
            raise NotImplemented

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
        """
        :return: FEN representation of board state
        """
        if self.files != 8 or self.ranks != 8:  # FEN is not supported on other-sized board than 8x8
            raise NotImplemented

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