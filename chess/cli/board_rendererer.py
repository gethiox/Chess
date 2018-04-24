from typing import List

from chess.app.board import StandardBoard
from chess.app.position import StandardPosition


class Colors:
    SCHEMA_24BIT = '\033[%s;2;%s;%s;%sm'

    FOREGROUND = '38'
    BACKGROUND = '48'

    END = '\033[0m'

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'

    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    YELLOW_BGD = '\033[43m'


class Colorize:
    @staticmethod
    def colorize_24bit(string, rgb):
        return Colors.SCHEMA_24BIT % (Colors.BACKGROUND, rgb[0], rgb[1], rgb[2]) + string + Colors.END

    @staticmethod
    def red(string):
        return '{}{}{}'.format(Colors.FAIL, string, Colors.END)

    @staticmethod
    def yellow(string):
        return '{}{}{}'.format(Colors.WARNING, string, Colors.END)

    @staticmethod
    def green(string):
        return '{}{}{}'.format(Colors.OKGREEN, string, Colors.END)

    @staticmethod
    def blue(string):
        return '{}{}{}'.format(Colors.OKBLUE, string, Colors.END)

    @staticmethod
    def yellow_bgd(string):
        return '{}{}{}'.format(Colors.YELLOW_BGD, string, Colors.END)


def tiny(board: StandardBoard, description: bool = True):
    board_str = ''

    rank_counter = 7
    while rank_counter >= 0:
        file_counter = 0
        while file_counter <= 7:
            piece = board.array[file_counter][rank_counter]
            if piece:
                board_str += piece.fen
            else:
                board_str += '.'
            if file_counter < 7:
                board_str += ' '
            file_counter += 1
        if rank_counter > 0:
            board_str += '\n'
        rank_counter -= 1
    return board_str


INFO_COLOR = (10, 40, 140)
WARN_COLOR = (100, 40, 10)


def normal(board: StandardBoard,
           description: bool = True,
           colorize: bool = True,
           info_fields: List[StandardPosition] = None,
           warn_fields: List[StandardPosition] = None):
    info_array = [(pos.file, pos.rank) for pos in info_fields] if info_fields else []
    warn_array = [(pos.file, pos.rank) for pos in warn_fields] if warn_fields else []

    if description:
        if colorize:
            board_str = '+-{}-+-{}-+-{}-+-{}-+-{}-+-{}-+-{}-+-{}-+\n'.format(
                Colorize.green('A'), Colorize.green('B'), Colorize.green('C'), Colorize.green('D'),
                Colorize.green('E'), Colorize.green('F'), Colorize.green('G'), Colorize.green('H')
            )
        else:
            board_str = '+-A-+-B-+-C-+-D-+-E-+-F-+-G-+-H-+\n'
    else:
        board_str = '+---+---+---+---+---+---+---+---+\n'

    rank_counter = 7
    while rank_counter >= 0:
        if description:
            if colorize:
                board_str += Colorize.green('%d' % (rank_counter + 1))
            else:
                board_str += '%d' % (rank_counter + 1)
        else:
            board_str += '|'
        file_counter = 0
        while file_counter <= 7:
            piece = board.array[file_counter][rank_counter]
            if piece:
                field = ' %s ' % piece.fen

                if colorize:
                    field = Colorize.red(field) if piece.fen.islower() else Colorize.yellow(field)
            else:
                field = '   '

            if colorize and (file_counter, rank_counter) in info_array:
                board_str += Colorize.colorize_24bit(field, INFO_COLOR)
            elif colorize and (file_counter, rank_counter) in warn_array:
                board_str += Colorize.colorize_24bit(field, WARN_COLOR)
            else:
                board_str += field

            if file_counter < 7:
                board_str += '|'
            file_counter += 1
        if description:
            if colorize:
                board_str += Colorize.green('%d' % (rank_counter + 1))
            else:
                board_str += '%d' % (rank_counter + 1)
        else:
            board_str += '|'
        if rank_counter > 0:
            board_str += '\n+---+---+---+---+---+---+---+---+\n'
        rank_counter -= 1

    if description:
        if colorize:
            board_str += '\n+-{}-+-{}-+-{}-+-{}-+-{}-+-{}-+-{}-+-{}-+'.format(
                Colorize.green('A'), Colorize.green('B'), Colorize.green('C'), Colorize.green('D'),
                Colorize.green('E'), Colorize.green('F'), Colorize.green('G'), Colorize.green('H')
            )
        else:
            board_str += '\n+-A-+-B-+-C-+-D-+-E-+-F-+-G-+-H-+'
    else:
        board_str += '\n+---+---+---+---+---+---+---+---+'
    return board_str
