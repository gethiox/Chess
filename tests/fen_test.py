import sys, pytest
sys.path.append('./')
from chess import *
from src.exceptions import *

# http://chess.stackexchange.com/questions/1482/how-to-know-when-a-fen-position-is-legal
# start position - 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 1 0'

game = Chess()


def test_board_size():
    # Too many rows
    with pytest.raises(WrongBoardSize):
        game.set_position('k7/8/K7/8/8/8/8/8/8')

    # Too few rows
    with pytest.raises(WrongBoardSize):
        game.set_position('k7/8/K7/8/8/8/8')

    # Too many columns in some row
    with pytest.raises(WrongBoardSize):
        game.set_position('k7/8/K7/8/ppppppppp/8/8')

    with pytest.raises(WrongBoardSize):
        game.set_position('k7/8/K7/8/9/8/8')

    with pytest.raises(WrongBoardSize):
        game.set_position('k7/8/K7/8/p4p3/8/8')

    # Too few columns in some row
    with pytest.raises(WrongBoardSize):
        game.set_position('k7/8/K7/8/ppppppp/8/8')

    with pytest.raises(WrongBoardSize):
        game.set_position('k7/8/K7/8/7/8/8')

    # Correct size
    assert game.set_position('K7/8/k7/8/8/8/8/8') == True


def test_kings_count():
    # Any kings here
    with pytest.raises(KingsCount):
        game.set_position('8/8/8/8/8/8/8/8')

    # Missed black king
    with pytest.raises(KingsCount):
        game.set_position('K7/8/8/8/8/8/8/8')

    # Missed white king
    with pytest.raises(KingsCount):
        game.set_position('k7/8/8/8/8/8/8/8')

    # More than one black king
    with pytest.raises(KingsCount):
        game.set_position('k1k5/8/K7/8/8/8/8/8')

    # More than one white king
    with pytest.raises(KingsCount):
        game.set_position('K1K5/8/k7/8/8/8/8/8')


def test_kings_position():
    # kings are touching each other
    with pytest.raises(IllegalPosition):
        game.set_position('kK6/8/8/8/8/8/8/8/8')


def test_check_side():
    # black checked while white on move
    with pytest.raises(IllegalPosition):
        game.set_position('k7/8/KN6/8/8/8/8/8 w - - 1 0')

    # white checked while black on move
    with pytest.raises(IllegalPosition):
        game.set_position('K7/8/kn6/8/8/8/8/8 b - - 1 0')


def test_check_count():
    # black checked more than 2 times
    with pytest.raises(IllegalPosition):
        game.set_position('8/8/k6R/8/KNB5/8/8/8')

    # white checked more than 2 times
    with pytest.raises(IllegalPosition):
        game.set_position('8/8/K6r/8/knb5/8/8/8')


def test_pawns_position():
    # pawns on the last lines
    with pytest.raises(IllegalPosition):
        game.set_position('P7/8/k1K5/8/8/8/8/8')

    with pytest.raises(IllegalPosition):
        game.set_position('p7/8/k1K5/8/8/8/8/8')

    with pytest.raises(IllegalPosition):
        game.set_position('8/8/k1K5/8/8/8/8/P7')

    with pytest.raises(IllegalPosition):
        game.set_position('8/8/k1K5/8/8/8/8/p7')


def test_pawns_count():
    # too many black pawns
    with pytest.raises(IllegalPosition):
        game.set_position('k7/pppppppp/p7/8/8/8/PPPPPPPP/K7')

    # too white black pawns
    with pytest.raises(IllegalPosition):
        game.set_position('k7/pppppppp/8/8/8/P7/PPPPPPPP/K7')


def test_en_passant():
    raise Exception


def test_promoted_pieces():
    raise Exception


def test_pawn_formation():
    raise Exception
