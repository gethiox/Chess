from typing import List, Optional

from domain.pieces import Piece


def tiny_rendererer(board_array: List[List[Optional[Piece]]]):
    # TODO: inject Board object, add support for variable board size

    board_str = ''

    rank_counter = 7
    while rank_counter >= 0:
        file_counter = 0
        while file_counter <= 7:
            piece = board_array[file_counter][rank_counter]
            if piece:
                board_str += str(piece)
            else:
                board_str += '.'
            if file_counter < 7:
                board_str += ' '
            file_counter += 1
        if rank_counter > 0:
            board_str += '\n'
        rank_counter -= 1
    print(board_str)
