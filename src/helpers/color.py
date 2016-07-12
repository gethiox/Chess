PURPLE = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
END = '\033[0m'


def purple(msg):
    return PURPLE + msg + END


def blue(msg):
    return BLUE + msg + END


def green(msg):
    return GREEN + msg + END


def yellow(msg):
    return YELLOW + msg + END


def red(msg):
    return RED + msg + END


def bold(msg):
    return BOLD + msg + END


def underline(msg):
    return UNDERLINE + msg + END