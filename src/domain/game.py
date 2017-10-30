from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Optional, Sequence, Type, Tuple

from app.game import Player
from app.pieces import Move, Black, White
from domain.pieces import Piece, Side, Position


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
    def pieces(self) -> Sequence[Type[Piece]]:
        """
        :return: Tuple of Pieces supported with implemented GameMode
        """
        pass

    @property
    @abstractmethod
    def sides(self) -> Sequence[Type[Side]]:
        """
        :return: tuple of players sides
        """
        pass


class Game(metaclass=ABCMeta):
    """
    Generic Game logic base class
    """

    def __init__(self, player1: Player, player2: Player, mode: Type[GameMode]):
        self.__players = {
            White: player1,
            Black: player2,
        }
        self.mode = mode

        self.__start_time = None
        self.__create_time = datetime.now()

        self.__moves = 0
        self.__half_moves = 0

    @property
    def players(self) -> Tuple[Player, ...]:
        return tuple(player for _, player in self.__players.items())

    @property
    def start_time(self) -> datetime:
        return self.__start_time

    @property
    def creation_date(self) -> datetime:
        return self.__create_time

    @property
    def on_move(self) -> Type[Side]:
        sides = tuple(self.__players.keys())
        return sides[self.__half_moves % len(self.players)]

    def start_game(self):
        self.__start_time = datetime.now()

    @abstractmethod
    def game_state(self) -> Type[Side]:
        """ 
        method return game state which depends on specific rules for every game mode.
        Look into "Normal" game mode class for inspirations (if is even implemented right now)
        :return: not_yet_started OR on_move_side OR winner_side
        """
        pass


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

    @property
    @abstractmethod
    def array(self):
        """
        Read-only, direct access to the board array
        :return: n-dimensional array
        """  # TODO: maybe make not only read-only

    @abstractmethod
    def _get_piece(self, position: Type[Position]) -> Optional[Type[Piece]]:
        """
        Get Piece on given Position
        :param position: Position object
        :return: Piece on given Position
        """
        pass

    @abstractmethod
    def _put_piece(self, piece, position: Type[Position]) -> Optional[Type[Piece]]:
        """
        Put Piece on given Position
        :param piece: Just any kind of Piece
        :param position: Position object
        :return: Piece that was standing before putting new (None if none)
        """
        pass

    @abstractmethod
    def _remove_piece(self, position: Type[Position]) -> Optional[Type[Piece]]:
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
        return "<%s Board>" % self.name

    def __str__(self):
        return self.name
