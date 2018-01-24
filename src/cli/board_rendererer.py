from app.board import StandardBoard


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Colorize:
    @staticmethod
    def red(string):
        return '{}{}{}'.format(Colors.FAIL, string, Colors.ENDC)

    @staticmethod
    def yellow(string):
        return '{}{}{}'.format(Colors.WARNING, string, Colors.ENDC)

    @staticmethod
    def green(string):
        return '{}{}{}'.format(Colors.OKGREEN, string, Colors.ENDC)

    @staticmethod
    def blue(string):
        return '{}{}{}'.format(Colors.OKBLUE, string, Colors.ENDC)


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


def normal(board: StandardBoard, description: bool = True, colorize: bool = True):
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
                board_str += Colorize.green('%d ' % (rank_counter + 1))
            else:
                board_str += '%d ' % (rank_counter + 1)
        else:
            board_str += '| '
        file_counter = 0
        while file_counter <= 7:
            piece = board.array[file_counter][rank_counter]
            if piece:
                if colorize:
                    board_str += Colorize.red(piece.fen) if piece.fen.islower() else Colorize.yellow(piece.fen)
                else:
                    board_str += piece.fen
            else:
                board_str += ' '
            if file_counter < 7:
                board_str += ' | '
            file_counter += 1
        if description:
            if colorize:
                board_str += Colorize.green(' %d' % (rank_counter + 1))
            else:
                board_str += ' %d' % (rank_counter + 1)
        else:
            board_str += ' |'
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
