#!/usr/bin/env python3
from argparse import ArgumentParser
from time import time, sleep

from src.app.move import StandardMove
from src.app.pieces import from_str, King
from src.app.player import Player
from src.app.position import StandardPosition
from src.app.variants import Normal
from src.cli import board_rendererer
from src.exceptions.variant import NotAValidMove
from src.interface.game import Game


def generate_moves(str_moves):
    for str_move in str_moves:
        source = StandardPosition.from_str(str_move[0:2])
        destination = StandardPosition.from_str(str_move[2:4])
        promotion_char = str_move[4:]
        if promotion_char:
            yield StandardMove(source=source, destination=destination,
                               promotion=from_str(promotion_char, initialized=False))
        else:
            yield StandardMove(source=source, destination=destination)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--silent', dest='silent', action='store_true',
                        help='return only average time statistics')
    parser.add_argument('--count', dest='count', action='store_true',
                        help='Count available moves, Very inefficient')
    parser.add_argument('-s', '--sleep', dest='sleep', type=float, default=0.0,
                        help='set sleep time between each move')
    parser.add_argument(dest='moves', nargs='*',
                        help='UCI move notation, each parameter is a move (eg. ./example.py e2e4 e7e5)')
    return parser.parse_args()


def get_stats(variant):
    return (
        "\n"
        "            FEN: {fen}\n"
        "      last move: {move}\n"
        "   move counter: {moves}\n"
        "        on move: {on_move}\n"
        "       in check: {check}\n"
        "available moves: {available_moves}\n"
        " winner side(s): {game_status}\n"
        "    explanation: {desc}\n"
        "\ncaptured pieces: (by side)\n{pocket}\n"
        "".format(
            fen=str(variant),
            move=variant.last_move,
            moves=variant.moves,
            on_move=variant.on_move,
            check=variant.is_check,
            available_moves=len(variant.all_available_moves()) if args.count else 'Disabled',
            game_status=variant.game_state[0],
            desc=variant.game_state[1],
            pocket='\n'.join(
                ['    %s: %s' % (side.name, ', '.join([piece.name for piece in pocket]) if pocket else None)
                 for side, pocket
                 in variant.pocket.items()]
            )
        )
    )


moves = [
    'e2e4', 'e7e5', 'g1f3', 'b8c6', 'f1b5', 'a7a6', 'b5c6', 'd7c6', 'e1g1', 'f7f6', 'd2d4', 'e5d4', 'f3d4', 'f8d6',
    'c1e3', 'g8e7', 'd1h5', 'e7g6', 'f2f4', 'e8g8', 'c2c3', 'g6e7', 'h5e2', 'c6c5', 'd4b3', 'b7b6', 'b3d2', 'a6a5',
    'b1a3', 'c8a6', 'a3c4', 'e7c6', 'f1f3', 'd8e8', 'f3h3', 'a8d8', 'a2a4', 'f8f7', 'b2b3', 'g7g6', 'a1f1', 'd6f8',
    'h3f3', 'f7d7', 'e4e5', 'f8g7', 'd2e4', 'f6f5', 'e4f2', 'e8e6', 'f3g3', 'd8e8', 'e3c1', 'c6d8', 'h2h4', 'd8f7',
    'g3e3', 'h7h5', 'f2h3', 'f7h6', 'h3g5', 'e6d5', 'e2f3', 'd7d8', 'f3d5', 'd8d5', 'e3e1', 'd5d3', 'f1f3', 'd3d8',
    'c4a3', 'h6g4', 'c3c4', 'a6b7', 'f3h3', 'e8e7', 'a3b5', 'g7h6', 'h3g3', 'h6g5', 'h4g5', 'g8f7', 'g3h3', 'b7e4',
    'b5c3', 'f7e6', 'e1d1', 'e7d7', 'd1d7', 'd8d7', 'g1f1', 'e4c2', 'c3d5', 'c7c6', 'h3c3', 'c2e4', 'd5e3', 'g4e5',
    'f4e5', 'f5f4', 'f1e2', 'f4e3', 'g2g3', 'e4f5', 'c3e3', 'f5g4', 'e2f2', 'd7d1', 'e3c3', 'e6e5', 'c3e3', 'e5f5',
    'e3e1', 'd1d3', 'c1f4', 'g4d1', 'f4c7', 'd3d2', 'f2e3', 'd2d4', 'c7b6', 'd1b3', 'e1c1', 'd4e4', 'e3f2', 'b3c4',
    'c1c3', 'f5g4', 'b6a5', 'e4e2', 'f2g1', 'c4d5', 'a5c7', 'e2a2', 'c3c5', 'a2a4', 'c5a5', 'a4c4', 'c7d6', 'g4g5',
    'g1f2', 'g5f5', 'a5a8', 'c4c2', 'f2e3', 'g6g5', 'e3d3', 'd5e4', 'd3e3', 'c2c3', 'e3e2', 'c3d3', 'a8a5', 'f5g6',
    'd6c7', 'd3d7', 'a5a7', 'e4d5', 'c7b8', 'd7d8', 'b8c7', 'd8e8', 'e2f2', 'e8f8', 'f2e3', 'h5h4', 'g3h4', 'g5h4',
    'a7a4', 'g6h5', 'a4f4', 'f8a8', 'f4d4', 'a8a3', 'e3f2', 'a3a2', 'f2e3', 'h4h3', 'd4d2', 'a2a7', 'c7h2', 'a7f7',
    'd2d3', 'h5g5', 'd3d1', 'f7d7', 'd1g1', 'g5h5', 'g1g3', 'd5e6', 'g3f3', 'h5g5', 'h2f4', 'g5h4', 'f4h2', 'e6d5',
    'f3f4', 'h4g5', 'f4f1', 'd7e7', 'e3f2', 'g5h5', 'f1d1', 'e7f7', 'f2e3', 'f7f3', 'e3e2', 'f3f5', 'd1d4', 'h5g5',
    'h2c7', 'c6c5', 'c7d8', 'g5g6', 'd4g4', 'g6f7', 'g4h4', 'd5g2', 'd8c7', 'f7e6', 'h4a4', 'e6d5', 'c7h2', 'f5f7',
    'a4h4', 'c5c4', 'h2g1', 'g2f1', 'e2d2', 'f7f3', 'g1b6', 'f3d3', 'd2c2', 'f1g2', 'h4h5', 'd5e4', 'b6c7', 'g2f3',
    'h5h8', 'f3d1', 'c2c1', 'c4c3', 'h8b8', 'e4f3', 'b8g8', 'f3f2', 'c7b6', 'f2e2', 'g8e8', 'e2f3', 'e8f8', 'f3g4',
    'f8g8', 'g4f5', 'g8f8', 'f5g6', 'f8g8', 'g6f7', 'g8g1', 'd1b3', 'g1f1', 'f7g6', 'f1g1', 'g6f5', 'g1f1', 'f5g4',
    'f1g1', 'g4h4', 'b6f2', 'h4h5', 'g1h1', 'h5g4', 'h1g1', 'g4f4', 'g1h1', 'h3h2', 'f2c5', 'f4g3', 'c5b4', 'g3g2',
    'h1e1', 'h2h1q', 'e1h1', 'g2h1', 'b4c3', 'd3c3', 'c1b2', 'c3d3', 'b2a3', 'h1g2', 'a3b4', 'g2f3', 'b4b5', 'b3d5',
    'b5c5', 'f3e4', 'c5b5', 'd3c3', 'b5a5', 'c3b3', 'a5a4', 'e4d4', 'a4a5', 'd4c5', 'a5a4', 'b3b2', 'a4a3', 'b2a2'
]

# another nice move sequence
# moves = [
#     'e2e4', 'e7e5', 'g1f3', 'b8c6', 'f1b5', 'a7a6', 'b5c6', 'd7c6', 'e1g1', 'f7f6', 'd2d4', 'e5d4', 'f3d4', 'f8d6',
#     'c1e3', 'g8e7', 'd1h5', 'e7g6', 'f2f4', 'e8g8', 'c2c3', 'g6e7', 'h5e2', 'c6c5', 'd4b3', 'b7b6', 'b3d2', 'a6a5',
#     'b1a3', 'c8a6', 'a3c4', 'e7c6', 'f1f3', 'd8e8', 'f3h3', 'a8d8', 'a2a4', 'f8f7', 'b2b3', 'g7g6', 'a1f1', 'd6f8',
#     'h3f3', 'f7d7', 'e4e5', 'f8g7', 'd2e4', 'f6f5', 'e4f2', 'e8e6', 'f3g3', 'd8e8', 'e3c1', 'c6d8', 'h2h4', 'd8f7',
#     'g3e3', 'h7h5', 'f2h3', 'f7h6', 'h3g5', 'e6d5', 'e2f3', 'd7d8', 'f3d5', 'd8d5', 'e3e1', 'd5d3', 'f1f3', 'd3d8',
#     'c4a3', 'h6g4', 'c3c4', 'a6b7', 'f3h3', 'e8e7', 'a3b5', 'g7h6', 'h3g3', 'h6g5', 'h4g5', 'g8f7', 'b5c3', 'f7e6',
#     'e1f1', 'b7e4', 'c3b5', 'e4c6', 'g3h3', 'c6b5', 'c4b5', 'e7d7', 'f1e1', 'd7d4', 'g1f1', 'd4b4', 'h3c3', 'd8d7',
#     'g2g3', 'd7h7', 'f1g2', 'h5h4', 'e1h1', 'h4h3', 'h1h3', 'h7h3', 'g2h3', 'g4f2', 'h3g2', 'f2e4', 'c3d3', 'c5c4',
#     'b3c4', 'b4c4', 'c1e3', 'c4a4', 'g2f3', 'a4c4', 'e3d4', 'c4c1', 'd4e3', 'c1f1', 'f3g2', 'f1b1', 'g2f3', 'a5a4',
#     'g3g4', 'e4c5', 'd3d8', 'b1b3', 'g4f5', 'e6f5', 'd8f8', 'f5e6', 'f4f5', 'e6e5', 'f5g6', 'c5e6', 'f8e8', 'e5d6',
#     'e8d8', 'd6e7', 'd8c8', 'b3b5', 'g6g7', 'e6g7', 'c8c7', 'e7f8', 'c7c8', 'f8f7', 'c8c7', 'f7g8', 'c7c8', 'g8h7',
#     'c8c7', 'b5b3', 'f3e4', 'h7g6', 'c7c6', 'g6h5', 'e3b6', 'b3b4', 'b6d4', 'h5g5', 'e4d3', 'g7f5', 'd4c3', 'b4b3',
#     'c6c5', 'b3a3', 'd3c4', 'g5f4', 'c4b4', 'a3a2', 'c5c8', 'f5e3', 'c8f8', 'f4e4', 'f8e8', 'e4f3', 'e8f8', 'f3e2',
#     'f8d8', 'a2c2', 'c3d4', 'c2d2', 'b4a4', 'e2d1', 'a4b4', 'e3c2', 'b4c3', 'c2d4', 'd8d4', 'd2d4', 'c3d4'
# ]

if __name__ == "__main__":
    args = parse_args()
    if args.moves:
        moves = args.moves

    game = Game(Player('White Player'), Player('Black Player'), Normal())
    variant = game.variant

    if not args.silent:
        board_str = board_rendererer.normal(variant.board)
        print(board_str)

        t_p_start = time()
        stats = get_stats(variant=variant)
        t_p_stop = time()

        collection_time = t_p_stop - t_p_start
        print(stats)
        print('\n (     game statistic collection time: {:.5f} )\n'.format(collection_time))

    g_start = time()
    validation_list, collection_list = [], []
    for move in generate_moves(moves):
        if args.sleep:
            sleep(args.sleep)
        try:
            t_start = time()
            variant.move(move)
            t_stop = time()
        except NotAValidMove as err:
            print(err)
            print('%s is not a valid move, game state not changed\n' % move)
            continue

        t_p_start = time()
        stats = get_stats(variant=variant)
        t_p_stop = time()

        validation_time = t_stop - t_start
        collection_time = t_p_stop - t_p_start

        if not args.silent:
            board_str = board_rendererer.normal(
                variant.board,
                info_fields=[variant.last_move.source, variant.last_move.destination],
                warn_fields=[x[0] for x in variant.board.find_pieces(King(variant.on_move))] if variant.is_check else []
            )
            print(board_str)
            print(stats)
            print(' ( move validation and execution time: {:.5f} )\n'
                  ' (     game statistic collection time: {:.5f} )\n'.format(validation_time, collection_time))

        validation_list.append(validation_time)
        collection_list.append(collection_time)

    g_stop = time()
    print('    all moves execution time: {:.4f}, {:d} moves in total, {:.4f} seconds on move'.format(
        g_stop - g_start, len(moves), (g_stop - g_start) / len(moves)))
    print('     slowest validation time: {:.4f} fastest: {:.4f}'.format(max(validation_list), min(validation_list)))
    print('slowest data collection time: {:.4f} fastest: {:.4f}'.format(max(collection_list), min(collection_list)))
