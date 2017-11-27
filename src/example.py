#!/usr/bin/env python3
from argparse import ArgumentParser
from time import time, sleep

from app.move import StandardMove
from app.player import Player
from app.position import StandardPosition
from app.variants import Normal
from cli import board_rendererer
from exceptions.variant import NotAValidMove
from interface.game import Game


def generate_moves(str_moves):
    for str_move in str_moves:
        yield StandardMove(StandardPosition.from_str(str_move[:2]), StandardPosition.from_str(str_move[-2:]))


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--silent', dest='silent', action='store_true', default=False)
    parser.add_argument('-s', '--sleep', dest='sleep', type=float, default=0.0)
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
            "".format(fen=str(variant),
                      move=variant.last_move,
                      moves=variant.moves,
                      on_move=variant.on_move,
                      check=variant.is_check,
                      available_moves='disabled',  # len(variant.all_available_moves()),  # Very inefficient
                      game_status=variant.game_state)
            )


moves = ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'b1c3', 'g8f6', 'f1c4', 'f8c5', 'a2a3', 'd7d6', 'd2d3', 'c8g4', 'c3d5',
         'f6d5', 'c4d5', 'c6d4', 'c2c3', 'd4f3', 'g2f3', 'g4d7', 'd5b7', 'a8b8', 'b7a6', 'd8f6', 'b2b4', 'd6d5',
         'b4c5', 'f6a6', 'e4d5', 'a6a5', 'c1d2', 'a5c5', 'c3c4', 'c5d4', 'a1c1', 'd4d3', 'h1g1', 'g7g6', 'd1e2',
         'd3e2', 'e1e2', 'd7f5', 'd2b4', 'f7f6', 'f3f4', 'e5f4', 'e2f3', 'e8f7', 'g1e1', 'h8e8', 'f3f4', 'e8e1',
         'c1e1', 'b8e8', 'e1e8', 'f7e8', 'c4c5', 'f5c2', 'c5c6', 'f6f5', 'f4e5', 'e8d8', 'b4d2', 'c2d1', 'd5d6',
         'c7d6', 'e5d6', 'd8c8', 'h2h3', 'd1b3', 'd2e3', 'a7a5', 'h3h4', 'b3c2', 'e3b6', 'a5a4', 'b6e3', 'f5f4',
         'e3f4', 'c2d3', 'd6c5', 'd3e2', 'f4d6', 'e2d3', 'c5b6', 'd3e4', 'b6b5', 'e4f3', 'd6e5', 'f3d1', 'b5c5',
         'd1f3', 'c5b6', 'f3d1', 'b6b5', 'd1f3', 'b5c5', 'f3e2', 'e5g3', 'e2d3', 'g3h2', 'd3e4', 'c5b5', 'e4d5',
         'h2f4', 'd5f3', 'f4d2', 'f3d5', 'b5b6', 'd5f3', 'd2c3', 'f3e4', 'c3e5', 'e4d5', 'e5f4', 'd5f3', 'f4d2',
         'f3e4', 'd2c3', 'e4d5', 'c3e5', 'd5e4', 'e5g3', 'e4d5', 'b6c5', 'd5e4', 'f2f4', 'e4f3', 'c5d6']

if __name__ == "__main__":
    args = parse_args()

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
