class WrongMoveOrder(Exception):
    """
    raised when tried execute move of side that not supposed to
    """
    pass


class NoPiece(Exception):
    """
    raised when any piece on board with given position
    """
    pass


class NotAValidMove(Exception):
    """
    generic exception raised when requested move is not allowed by variant implementation
    """
    pass


class CausesCheck(NotAValidMove):
    """
    raised when move attempt causes check from other side(s)
    """
    pass


class NotAValidPromotion(NotAValidMove):
    """
    raised when someone want to promote Pawn to a Pawn in standard chess variant for example
    """
    pass


class NotAValidPosition(Exception):
    """
    generic exception raised when requested position is against the rules 
    """


class MissingKing(NotAValidPosition):
    """
    raised when some King is missing on board
    """
    pass


class TooManyKings(NotAValidPosition):
    """
    raised when too many Kings on board (eg. greater or equal 2)
    """
    pass


class PawnOnWrongRank(NotAValidPosition):
    """
    raised when position with pawn on first/last rank is tried to establish 
    """
    pass


class GameIsOver(Exception):
    """
    raised when game ended by rules but someone still want to do a move
    """
    pass
