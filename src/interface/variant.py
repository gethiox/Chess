from abc import ABCMeta, abstractmethod
from typing import Sequence, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from interface.move import Move
    from interface.piece import Piece
    from interface.side import Side


class Variant(metaclass=ABCMeta):
    @abstractmethod
    def init_board_state(self) -> str:
        """
        Sets Board init state for this game mode
        :return FEN strong of part with board only
        """
        pass

    @abstractmethod
    def assert_move(self, move: 'Move') -> bool:
        """
        Assert if given move in current game state and game mode is legal
        :param move: Move type
        :return: bool, positive if given move is legal
        """
        pass

    @property
    @abstractmethod
    def pieces(self) -> Sequence[Type['Piece']]:
        """
        :return: Tuple of Pieces supported with implemented GameMode
        """
        pass

    @property
    @abstractmethod
    def sides(self) -> Sequence[Type['Side']]:
        """
        :return: tuple of players sides
        """
        pass
