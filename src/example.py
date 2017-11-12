#!/usr/bin/env python3
from time import time

from app.move import StandardMove
from app.player import Player
from app.position import StandardPosition
from app.variants import Normal
from cli import board_rendererer
from interface.game import Game


def generate_moves(str_moves):
    for str_move in str_moves:
        yield StandardMove(StandardPosition(str_move[:2]), StandardPosition(str_move[-2:]))


if __name__ == "__main__":
    game = Game(Player('White Player'), Player('Black Player'), Normal())
    variant = game.variant

    board_rendererer.tiny(variant.board)
    print()
    for move in generate_moves(['f2f3', 'e7e6', 'g2g3', 'd8e7', 'g3g4', 'e7h4']):
        t_start = time()
        status = variant.move(move)
        t_stop = time()
        if status:
            print('%s is a valid move' % move)
        else:
            print('%s is not a valid move, game state not changed' % move)

        board_rendererer.tiny(variant.board)
        t_p_start = time()
        print(
            "\n"
            "half move: {half}\n"
            "move: {moves}\n"
            "on move: {on_move}\n"
            "last move: {last_move}\n"
            "available moves: {available_moves}\n"
            "winner side(s): {game_status}\n"
            "".format(half=variant.half_moves,
                      moves=variant.moves,
                      on_move=variant.on_move,
                      last_move=variant.last_move,
                      available_moves=len(variant.all_available_moves),
                      game_status=variant.game_state)
        )
        t_p_stop = time()
        # print('          ( move validation and execution time: {:.4f} )\n'
        #       ' ( data collection time for above informations: {:.4f} )'.format(
        #     t_stop - t_start,
        #     t_p_stop - t_p_start,
        # ))
