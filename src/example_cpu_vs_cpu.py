#!/usr/bin/env python3
from argparse import ArgumentParser

from app.engine import EngineHandler
from app.move import StandardMove
from app.player import Player
from app.variants import Normal
from cli import board_rendererer
from interface.game import Game


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(dest='engine_path', type=str, nargs='?', help='path of UCI chess engine')
    parser.add_argument('-s', '--silent', dest='silent', action='store_true', help='path of UCI chess engine')
    return parser.parse_args()


def print_state(game):
    board_str = board_rendererer.normal(game.board)
    fen = str(game.variant)
    data = "On move: {on_move!s:5s}, Available moves: {moves:s}".format(
        on_move=game.variant.on_move,
        moves='disabled',  # len(game.variant.all_available_moves())  # warning: inefficient!
    )
    print(fen)
    print(board_str)
    print(data)
    print()


if __name__ == "__main__":
    args = parse_args()
    if not args.engine_path:
        print('engine path is required to run this script, see --help')
        exit(1)

    mode = Normal()
    print("Playing %s game mode" % mode.name)

    player1 = Player("CPU I")
    player2 = Player("CPU II")

    # engine is created for each side to prevent "self-seeing" moves, it simulate two different players instead of one
    engine1 = EngineHandler(args.engine_path, threads=1, ponder=False)
    engine2 = EngineHandler(args.engine_path, threads=1, ponder=False)

    engine1.start_engine()
    engine2.start_engine()

    game = Game(player1=player1, player2=player2, variant=mode)

    if not args.silent:
        print_state(game)

    try:
        while True:
            str_move = engine1.best_move(str(game.variant), wtime=100, btime=100)
            move = StandardMove.from_str(str_move)
            game.move(move)
            if not args.silent:
                print_state(game)
            if game.variant.game_state[0]:
                break

            str_move = engine2.best_move(str(game.variant), wtime=100, btime=100)
            move = StandardMove.from_str(str_move)
            game.move(move)
            if not args.silent:
                print_state(game)
            if game.variant.game_state[0]:
                break
        if args.silent:
            print_state(game)
        print('State: {state}, Winner(s): {winner}'.format(
            state=game.variant.game_state[1],
            winner=','.join(str(side) for side in game.variant.game_state[0]))
        )
        if not args.silent:
            print('moves:', [str(move) for move in game.variant.moves_history])

        engine1.stop_engine()
        engine2.stop_engine()

    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    exit(0)
