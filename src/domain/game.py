from abc import ABCMeta, abstractmethod
from functools import lru_cache
from typing import Tuple, Optional

from domain.pieces import Move, Piece, Side, StandardPosition


class GameMode(metaclass=ABCMeta):
    @abstractmethod
    def init_board_state(self) -> str:
        """
        Sets Board init state for this game mode
        :return FEN strong of part with board only
        """
        pass

    @abstractmethod
    def assert_move(self, move: Move) -> bool:
        """
        Assert if given move in current game state and game mode is legal
        :param move: Move type
        :return: bool, positive if given move is legal
        """
        pass

    @property
    @abstractmethod
    def pieces(self) -> Tuple[Piece]:
        """
        :return: Tuple of Pieces supported with implemented GameMode
        """
        pass

    @property
    @abstractmethod
    def sides(self) -> Tuple[Side]:
        """
        :return: tuple of players sides
        """
        pass

    @lru_cache(maxsize=1)
    def __pieces_dict(self):
        d = {}
        for piece in self.pieces:
            d.update({piece.char: piece})
        return d

    @lru_cache(maxsize=1)
    def __sides_dict(self):
        d = {}
        for side in self.sides:
            d.update({side.char: side})
        return d


class Board(metaclass=ABCMeta):
    """
    Base board object
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Board type name
        """
        pass

    @abstractmethod
    def _get_piece(self, position: StandardPosition) -> Optional[Piece]:
        """
        Get Piece on given Position
        :param position: Position object
        :return: Piece on given Position
        """
        pass

    @abstractmethod
    def _put_piece(self, piece, position: StandardPosition) -> Optional[Piece]:
        """
        Put Piece on given Position
        :param piece: Just any kind of Piece
        :param position: Position object
        :return: Piece that was standing before putting new (None if none)
        """
        pass

    @abstractmethod
    def _remove_piece(self, position: StandardPosition) -> Optional[Piece]:
        """
        Remove Piece from given Position
        :param position: Position object
        :return: Piece that are removed (None if none)
        """
        pass

    @abstractmethod
    def set_fen(self, board_fen: str):
        """
        Sets board state from FEN
        :param board_fen: string, min 15 letters (ranks separated by slash)
        """
        pass

    @abstractmethod
    def get_fen(self) -> str:
        """
        :return: FEN representation of board state
        """
        pass

    def __repr__(self):
        return "<%s>" % self.name

    def __str__(self):
        return self.name
