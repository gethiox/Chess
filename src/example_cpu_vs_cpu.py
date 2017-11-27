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
    return parser.parse_args()


def print_state(game):
    board_str = board_rendererer.normal(game.board)
    data = "On move: {on_move!s:5s}, Available moves: {moves:s}".format(
        on_move=game.variant.on_move,
        moves='disabled',  # len(game.variant.all_available_moves())  # warning: inefficient!
    )
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
    engine2 = EngineHandler(args.engine_path, threads=1, ponder=True)

    game = Game(player1=player1, player2=player2, variant=mode)

    print_state(game)

    try:
        while True:
            str_move = engine1.best_move(str(game.variant), wtime=5000, btime=5000)
            move = StandardMove.from_str(str_move)
            game.move(move)
            print_state(game)
            if game.variant.game_state:
                break

            str_move = engine2.best_move(str(game.variant), wtime=1000, btime=1000)
            move = StandardMove.from_str(str_move)
            game.move(move)
            print_state(game)
            if game.variant.game_state:
                break
        print('Winner(s):', ','.join(str(side) for side in game.variant.game_state))
        print('moves:', [str(move) for move in game.variant.moves_history])
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    exit(0)
