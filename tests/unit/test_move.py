import pytest

from chess.app.move import StandardMove
from chess.app.pieces import Queen
from chess.app.position import StandardPosition


def test_init_move():
    a_pos = StandardPosition((0, 0))
    b_pos = StandardPosition((0, 1))

    move = StandardMove(source=a_pos, destination=b_pos)
    assert move.source == a_pos
    assert move.destination == b_pos
    assert move.promotion is None

    move = StandardMove(source=a_pos, destination=b_pos, promotion=Queen)
    assert move.source == a_pos
    assert move.destination == b_pos
    assert move.promotion == Queen

    with pytest.raises(ValueError, message="Source and destination should be not the same field"):
        StandardMove(source=StandardPosition((0, 0)), destination=StandardPosition((0, 0)))


def test_init_move_from_uci():
    move = StandardMove.from_str('e2e4')
    assert move.source == StandardPosition((4, 1))
    assert move.destination == StandardPosition((4, 3))
    assert move.promotion is None

    move = StandardMove.from_str('a7a8q')
    assert move.source == StandardPosition((0, 6))
    assert move.destination == StandardPosition((0, 7))
    assert move.promotion == Queen

    # cases based on wrong length
    bad_moves = ['a', 'e2', 'e2e', 'e2e4qq', 'sadnhjfegesj']
    # edge cases, depended on proper UCI syntax and position ranges
    bad_moves += ['eeee', 'e234', '4123f', 'qqqqq']

    for move_str in bad_moves:
        with pytest.raises(ValueError, message='Not a proper UCI format should be declined'):
            StandardMove.from_str(move_str)
