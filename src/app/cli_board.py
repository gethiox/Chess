from typing import List, Optional

from domain.pieces import Piece


def tiny_rendererer(board_array: List[List[Optional[Piece]]]):
    board_str = ''

    y = 7
    while y >= 0:
        x = 0
        while x <= 7:
            piece = board_array[x][y]
            if piece:
                board_str += str(piece)
            else:
                board_str += '.'
            if x < 7:
                board_str += ' '
            x += 1
        if y > 0:
            board_str += '\n'
        y -= 1
    print(board_str)


