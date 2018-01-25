from string import digits
from typing import Optional, Tuple, TYPE_CHECKING, List, Dict

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
        self.__pieces: Dict['StandardPosition', 'Piece'] = {}

    @property
    def array(self) -> List[List[Optional['Piece']]]:
        array = [[None for _ in range(self.ranks)] for _ in range(self.files)]
        for position, piece in self.__pieces.items():
            array[position.file][position.rank] = piece

        return array

    @property
    def size(self) -> Tuple[int, int]:
        return self.__files, self.__ranks

    @property
    def files(self) -> int:
        return self.__files

    @property
    def ranks(self) -> int:
        return self.__ranks

    def get_piece(self, position: 'StandardPosition') -> Optional['Piece']:
        """
        Get Piece on given Position
        :param position: Position object
        :return: Piece on given Position
        """
        try:
            return self.__pieces[position]
        except KeyError:
            return None

    def put_piece(self, piece: 'Piece', position: StandardPosition) -> Optional['Piece']:
        """
        Put Piece on given Position
        :param piece: Just any kind of Piece
        :param position: Position object
        :return: Piece that was standing before putting new (None if none)
        """

        try:
            current = self.__pieces[position]
        except KeyError:
            current = None
        self.__pieces[position] = piece
        return current

    def remove_piece(self, position: StandardPosition) -> Optional['Piece']:
        """
        Remove Piece from given Position
        :param position: Position object
        :return: Piece that are removed (None if none)
        """

        try:
            current = self.__pieces.pop(position)
        except KeyError:
            current = None
        return current

    def set_fen(self, board_fen: str):
        # TODO: validate input string
        """
        Sets board state from FEN
        :param board_fen: string, min 15 letters (ranks separated by slash)
        """
        if self.files != 8 or self.ranks != 8:  # FEN is not supported on other-sized board than 8x8
            raise NotImplemented

        pieces_tmp: Dict['StandardPosition', 'Piece'] = {}

        rank_counter = self.ranks - 1
        for rank in board_fen.split('/'):
            file_counter = 0
            for piece in rank:
                if piece not in digits:
                    position_object = StandardPosition((file_counter, rank_counter))
                    piece_object = from_str(piece)
                    pieces_tmp.update({position_object: piece_object})
                    file_counter += 1
                else:
                    for i in range(int(piece)):
                        file_counter += 1
            rank_counter -= 1

        self.__pieces = pieces_tmp

    def get_fen(self) -> str:
        """
        :return: FEN representation of board state
        """
        if self.files != 8 or self.ranks != 8:  # FEN is not supported on other-sized board than 8x8
            raise NotImplemented

        board_fen = ''

        no_pieces_counter = 0
        rank_counter = self.ranks - 1
        while rank_counter >= 0:
            file_counter = 0
            while file_counter <= self.files - 1:
                piece = self.array[file_counter][rank_counter]
                if piece:
                    if no_pieces_counter > 0:
                        board_fen += str(no_pieces_counter)
                        no_pieces_counter = 0
                    board_fen += piece.fen
                else:
                    no_pieces_counter += 1
                file_counter += 1
            if no_pieces_counter > 0:
                board_fen += str(no_pieces_counter)
                no_pieces_counter = 0
            if rank_counter > 0:
                board_fen += '/'
            rank_counter -= 1

        return board_fen

    @property
    def pieces(self) -> List[Tuple['StandardPosition', 'Piece']]:
        pieces = []
        for position, piece in self.__pieces.items():
            pieces.append((position, piece))
        # sorting list by piece value helps a lot for move availability validation, king are checked at first
        # in most popular "check" positions king is able to make a move and break rest of pieces validation.
        return sorted(pieces, key=lambda x: x[1].points, reverse=True)

    def find_pieces(self, requested_piece: Optional['Piece']) -> List[Tuple['StandardPosition', 'Piece']]:
        pieces = []
        for position, piece in self.__pieces.items():
            if requested_piece == piece:
                pieces.append(
                    (position, piece)
                )
        return pieces

    def validate_position(self, position: StandardPosition) -> bool:
        if self.files > position.file >= 0 and self.ranks > position.rank >= 0:
            return True
        return False

    def __hash__(self):
        return hash(tuple((position, piece) for position, piece in self.__pieces.items()))
