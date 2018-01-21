#!/usr/bin/env python3
from argparse import ArgumentParser
from time import time, sleep

from app.move import StandardMove
from app.pieces import from_str
from app.player import Player
from app.position import StandardPosition
from app.variants import Normal
from cli import board_rendererer
from exceptions.variant import NotAValidMove
from interface.game import Game


def generate_moves(str_moves):
    for str_move in str_moves:
        source = StandardPosition.from_str(str_move[0:2])
        destination = StandardPosition.from_str(str_move[2:4])
        promotion_char = str_move[4:]
        if promotion_char:
            yield StandardMove(source=source, destination=destination,
                               promotion=from_str(promotion_char), initialized=False)
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
    return ("\n"
            "FEN: {fen}\n"
            "executed/last move: {move}\n"
            "move count: {moves}\n"
            "on move: {on_move}\n"
            "in check: {check}\n"
            "available moves: {available_moves}\n"
            "winner side(s): {game_status}\n"
            "captured pieces: (by side)\n{pocket}\n"
            "game state description: {desc}\n"
            "".format(fen=str(variant),
                      move=variant.last_move,
                      moves=variant.moves,
                      on_move=variant.on_move,
                      check=variant.is_check,
                      available_moves=len(variant.all_available_moves()) if args.count else None,
                      game_status=variant.game_state[0],
                      desc=variant.game_state[1],
                      pocket='\n'.join(
                          ['    %s' % str({side.name: [piece.name for piece in pocket]})
                           for side, pocket
                           in variant.pocket.items()])
                      )
            )


moves = ['d2d4', 'd7d5', 'g1f3', 'b8c6', 'e2e3', 'g8f6', 'f3e5', 'c6e5', 'd4e5', 'f6d7', 'd1d5', 'e7e6', 'd5e4', 'f8e7',
         'f1e2', 'f7f5', 'e5f6', 'd7f6', 'e4c4', 'a7a6', 'a2a4', 'e8g8', 'e1g1', 'b7b5', 'c4b3', 'c8d7', 'a4b5', 'a6b5',
         'a1a8', 'd8a8', 'e2b5', 'f8b8', 'b5d7', 'b8b3', 'd7e6', 'g8f8', 'e6b3', 'e7d6', 'h2h3', 'f6e4', 'b1d2', 'e4d2',
         'c1d2', 'a8a6', 'f1d1', 'a6e2', 'c2c4', 'd6e5', 'd2b4', 'f8f7', 'd1d7', 'f7f6', 'b4d2', 'f6e6', 'd7d5', 'c7c6',
         'd5e5', 'e6e5', 'd2c3', 'e5d6', 'g2g4', 'e2f3', 'c3g7', 'd6c5', 'g7d4', 'c5b4', 'b3c2', 'f3h3', 'c2d1', 'b4c4',
         'd1e2', 'c4b4', 'd4c3', 'b4b3', 'e2d1', 'b3c4', 'd1e2', 'c4b3', 'e2d1', 'b3a2', 'd1e2', 'h3h4', 'g1g2', 'h4e7',
         'e2c4', 'a2b1', 'c4d3', 'b1c1', 'g2f3', 'e7h4', 'd3f5', 'h7h5', 'e3e4', 'h5g4', 'f5g4', 'c1c2', 'e4e5', 'c2d3',
         'g4f5', 'd3c4', 'f5e6', 'c4c5', 'e6a2', 'h4h3', 'f3e4', 'h3h7', 'e4f4', 'h7a7', 'a2b3', 'a7b8', 'b3a2', 'b8a8',
         'a2f7', 'a8a7', 'f7e6', 'a7e7', 'e6b3', 'e7b7', 'b3e6', 'b7e7', 'e6b3', 'c5b5', 'f2f3', 'e7h7', 'e5e6', 'b5c5',
         'c3e5', 'h7b7', 'b3a2', 'b7a7', 'a2b3', 'c5b4', 'b3d1', 'b4b5', 'f4f5', 'a7h7', 'f5g5', 'b5c5', 'f3f4', 'h7e7',
         'g5f5', 'e7h4', 'b2b4', 'c5b6', 'e5d6', 'h4h3', 'f5f6', 'h3h6', 'f6e5', 'h6g7', 'e5f5', 'g7h7', 'f5f6', 'h7h6',
         'f6e5', 'h6g7', 'e5f5', 'g7h7', 'f5f6', 'h7h6']

if __name__ == "__main__":
    args = parse_args()
    if args.moves:
        moves = args.moves

    game = Game(Player('White Player'), Player('Black Player'), Normal())
    variant = game.variant

    if not args.silent:
        board_str = board_rendererer.normal(variant.board)
        print(board_str + '\n')

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
            board_str = board_rendererer.normal(variant.board)
            print(board_str)
            print(stats)
            print(' ( move validation and execution time: {:.5f} )\n'
                  ' (     game statistic collection time: {:.5f} )\n'.format(validation_time, collection_time))

        validation_list.append(validation_time)
        collection_list.append(collection_time)

    g_stop = time()
    print('    all moves execution time: {:.4f} ({:d} moves in total)'.format(g_stop - g_start, len(moves)))
    print('     slowest validation time: {:.4f} fastest: {:.5f}'.format(max(validation_list), min(validation_list)))
    print('slowest data collection time: {:.4f} fastest: {:.5f}'.format(max(collection_list), min(collection_list)))
