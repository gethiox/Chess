from app.board import StandardBoard


def tiny(board: StandardBoard):
    # TODO: add support for variable board size
    board_str = ''

    rank_counter = 7
    while rank_counter >= 0:
        file_counter = 0
        while file_counter <= 7:
            piece = board.array[file_counter][rank_counter]
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
    return board_str


def normal(board: StandardBoard):
    # TODO: add support for variable board size
    board_str = '+---+---+---+---+---+---+---+---+\n'

    rank_counter = 7
    while rank_counter >= 0:
        board_str += '| '
        file_counter = 0
        while file_counter <= 7:
            piece = board.array[file_counter][rank_counter]
            if piece:
                board_str += str(piece)
            else:
                board_str += ' '
            if file_counter < 7:
                board_str += ' | '
            file_counter += 1
        board_str += ' |'
        if rank_counter > 0:
            board_str += '\n+---+---+---+---+---+---+---+---+\n'
        rank_counter -= 1
    board_str += '\n+---+---+---+---+---+---+---+---+'
    return board_str
