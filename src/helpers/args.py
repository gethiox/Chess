import argparse

def parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--help', action='help', help='Show Help')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-n', '--normal', dest='human', action='store_true',
                       help='Hunam vs Computer (chess engine required)')
    group.add_argument('-a', '--auto', dest='auto', action='store_true',
                       help='Computer vs Computer (chess engine required)')

    group.add_argument('-h', '--host', dest='host', metavar='<ip>', default=None,
                       help='Host a network game')
    group.add_argument('-j', '--join', dest='join', metavar='<ip>', default=None,
                       help='Join a network game')

    parser.add_argument('-p', '--port', dest='port', metavar='<port>', type=int, default=5678,
                        help='Destination Port')
    parser.add_argument('-s', '--stock', dest='stock', metavar='./stockfish', type=str, default='./src/helpers/stockfish',
                        help='Path to the Stockfish binary')

    args = parser.parse_args()
    return args