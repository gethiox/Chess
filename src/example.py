#!/usr/bin/env python3
from time import time

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


if __name__ == "__main__":
    game = Game(Player('White Player'), Player('Black Player'), Normal())
    variant = game.variant

    board_str = board_rendererer.normal(variant.board)
    print(board_str + '\n')
    g_start = time()
    validation_list, collection_list = [], []
    for move in generate_moves(
            ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'b1c3', 'g8f6', 'f1c4', 'f8c5', 'a2a3', 'd7d6', 'd2d3', 'c8g4', 'c3d5',
             'f6d5', 'c4d5', 'c6d4', 'c2c3', 'd4f3', 'g2f3', 'g4d7', 'd5b7', 'a8b8', 'b7a6', 'd8f6', 'b2b4', 'd6d5',
             'b4c5', 'f6a6', 'e4d5', 'a6a5', 'c1d2', 'a5c5', 'c3c4', 'c5d4', 'a1c1', 'd4d3', 'h1g1', 'g7g6', 'd1e2',
             'd3e2', 'e1e2', 'd7f5', 'd2b4', 'f7f6', 'f3f4', 'e5f4', 'e2f3', 'e8f7', 'g1e1', 'h8e8', 'f3f4', 'e8e1',
             'c1e1', 'b8e8', 'e1e8', 'f7e8', 'c4c5', 'f5c2', 'c5c6', 'f6f5', 'f4e5', 'e8d8', 'b4d2', 'c2d1', 'd5d6',
             'c7d6', 'e5d6', 'd8c8', 'h2h3', 'd1b3', 'd2e3', 'a7a5', 'h3h4', 'b3c2', 'e3b6', 'a5a4', 'b6e3', 'f5f4',
             'e3f4', 'c2d3', 'd6c5', 'd3e2', 'f4d6', 'e2d3', 'c5b6', 'd3e4', 'b6b5', 'e4f3', 'd6e5', 'f3d1', 'b5c5',
             'd1f3', 'c5b6', 'f3d1', 'b6b5', 'd1f3', 'b5c5', 'f3e2', 'e5g3', 'e2d3', 'g3h2', 'd3e4', 'c5b5', 'e4d5',
             'h2f4', 'd5f3', 'f4d2', 'f3d5', 'b5b6', 'd5f3', 'd2c3', 'f3e4', 'c3e5', 'e4d5', 'e5f4', 'd5f3', 'f4d2',
             'f3e4', 'd2c3', 'e4d5', 'c3e5', 'd5e4', 'e5g3', 'e4d5', 'b6c5', 'd5e4', 'f2f4', 'e4f3', 'c5d6', 'f3e4',
             'g3e1', 'e4f3', 'e1c3', 'f3e4', 'c3d4', 'e4f3', 'd4e5', 'f3e4', 'd6c5', 'e4f3', 'c5b5', 'f3d1', 'e5c3',
             'd1f3', 'b5b6', 'f3d1', 'c3e5', 'd1f3', 'b6c5', 'f3e2', 'e5d4', 'c8c7', 'd4c3', 'c7c8', 'c5d6', 'e2d1',
             'c3a5', 'd1e2', 'a5b6', 'e2f3', 'b6f2', 'c8d8', 'f2e3', 'd8c8', 'e3d4', 'f3e4', 'd4f6', 'e4c2', 'd6c5',
             'c2e4', 'f6c3', 'e4f3', 'c3d2', 'c8c7', 'd2a5', 'c7c8', 'c5b6', 'f3e4', 'a5b4', 'e4d3', 'b4d6', 'd3e4',
             'd6e7', 'e4d3', 'e7b4', 'd3c2', 'b4d2', 'c2e4', 'd2c3', 'e4f3', 'c3d4', 'f3e2', 'd4b2', 'e2d1', 'b2g7',
             'd1f3', 'g7f8', 'f3d1', 'f8d6', 'd1f3', 'd6e7', 'f3e4', 'e7c5', 'e4d3', 'c5e3', 'd3e2', 'e3d2', 'e2f3',
             'd2e1', 'f3e2', 'e1f2', 'e2f3', 'c6c7', 'f3d1', 'f2d4', 'd1f3', 'd4e5', 'f3d1', 'b6c6', 'd1f3', 'c6d6',
             'h7h5', 'e5c3', 'f3e4', 'c3d4', 'e4f3', 'd4c5', 'f3d1', 'c5e3', 'd1c2', 'e3d2', 'c2e4', 'd2c3', 'e4c2',
             'c3f6', 'c2d1', 'd6c6', 'd1f3', 'c6b6', 'f3d1', 'f6e5', 'd1c2', 'b6c6', 'c2e4', 'c6b5', 'e4c2', 'b5b4',
             'c8b7', 'b4a5', 'b7c8', 'a5b6', 'c2e4', 'e5h8', 'e4c2', 'h8d4', 'c2d3', 'd4f2', 'd3e4', 'f2c5', 'e4c2',
             'b6c6', 'c2e4', 'c6d6', 'e4f5', 'c5g1', 'f5e4', 'g1f2', 'e4f5', 'f2e1', 'f5c2', 'e1b4', 'c2d3', 'd6c6',
             'd3e4', 'c6b6', 'e4c2', 'b4e1', 'c2d3', 'e1c3', 'd3e4', 'c3g7', 'e4c2', 'g7f8', 'c2e4', 'f8d6', 'e4f5',
             'b6a5', 'c8d7', 'd6e5', 'f5c2', 'a5b4', 'd7c8', 'f4f5', 'g6f5', 'b4c4', 'c2d1', 'c4d5', 'c8d7', 'd5c5',
             'd1g4', 'e5f4', 'g4d1', 'c5d4', 'd1c2', 'd4c4', 'c2b3', 'c4b5', 'd7c8', 'f4e5', 'b3d1', 'b5a5', 'c8d7',
             'a5b4', 'd1b3', 'e5f4', 'b3c2', 'f4g3', 'c2d1', 'b4b5', 'd7c8', 'g3e5', 'd1c2', 'b5b6', 'c2d1', 'e5f4',
             'd1c2', 'f4d6', 'c2d1', 'b6b5', 'c8d7', 'b5c5', 'd1f3', 'c5d4', 'd7c8', 'd6g3', 'f3d1', 'd4e3', 'c8d7',
             'g3e5', 'd1g4', 'e3d2', 'd7c8', 'd2c3', 'c8d7', 'c3c4', 'g4d1', 'e5d6', 'd1g4', 'd6f4', 'd7c8', 'c4d3',
             'g4d1', 'd3e3', 'c8d7', 'f4d6', 'd7c8', 'e3d3', 'c8d7', 'd6e5', 'd7c8', 'e5f4', 'c8d7', 'f4g3', 'd1g4',
             'g3h2', 'g4d1', 'd3e3', 'd1g4', 'e3d2', 'g4h3', 'h2f4', 'd7c8', 'f4d6', 'c8d7', 'd2c3', 'h3g4', 'c3d4',
             'd7c8', 'd4d3', 'c8d7', 'd3c4', 'g4d1', 'c4b5', 'd7c8', 'd6h2', 'c8d7', 'h2e5', 'd7c8']
    ):

        try:
            t_start = time()
            variant.move(move)
            t_stop = time()
        except NotAValidMove as err:
            print(err)
            print('%s is not a valid move, game state not changed\n' % move)
            continue

        board_str = board_rendererer.normal(variant.board)
        t_p_start = time()
        stats = ("\n"
                 "FEN: {fen}\n"
                 "executed/last move: {move}\n"
                 "move count: {moves}\n"
                 "on move: {on_move}\n"
                 "in check: {check}\n"
                 "available moves: {available_moves}\n"
                 "winner side(s): {game_status}\n"
                 "".format(fen=str(game.variant),
                           move=variant.last_move,
                           moves=variant.moves,
                           on_move=variant.on_move,
                           check=variant.is_check,
                           available_moves='disabled',  # len(variant.all_available_moves()),  # Very inefficient
                           game_status=variant.game_state)
                 )
        t_p_stop = time()
        print(board_str)
        print(stats)

        validation_time = t_stop - t_start
        collection_time = t_p_stop - t_p_start

        print(' ( move validation and execution time: {:.4f} )\n'
              ' (     game statistic collection time: {:.4f} )\n'.format(validation_time,
                                                                         collection_time))
        validation_list.append(validation_time)
        collection_list.append(collection_time)
    g_stop = time()
    print('total move execution time: {:.4f}'.format(g_stop - g_start))
    print('slowest validation time: {:.4f} fastest: {:.4f}'.format(max(validation_list), min(validation_list)))
    print('slowest data collection time: {:.4f} fastest: {:.4f}'.format(max(collection_list), min(collection_list)))
