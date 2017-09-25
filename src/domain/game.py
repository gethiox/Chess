from abc import ABCMeta

from domain.pieces import Move


class GameMoode(ABCMeta):
    def init_board_state(cls) -> str:
        """
        Sets Board init state for this game mode
        :return FEN strong of part with board only
        """
        pass

    def assert_move(cls, move: Move) -> bool:
        """
        Assert if given move in current game state and game mode is legal
        :param move: Move type
        :return: bool, positive if given move is legal
        """
        pass

    # TODO: TODO
