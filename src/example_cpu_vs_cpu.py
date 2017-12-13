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
    parser.add_argument('--silent', dest='silent', action='store_true', help='Display only ending game state')
    return parser.parse_args()


def print_state(game):
    board_str = board_rendererer.normal(game.board)
    fen = "FEN: %s" % str(game.variant)
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
    if not args.silent:
        print("Playing %s game mode" % mode.name)

    player1 = Player("CPU I")
    player2 = Player("CPU II")

    # engine is created for each side to prevent "self-seeing" moves, it simulate two different players instead of one
    engine1 = EngineHandler(args.engine_path, threads=1, ponder=False, hash=64)
    engine2 = EngineHandler(args.engine_path, threads=1, ponder=False, hash=64)

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

        winners, desc = game.variant.game_state
        if len(winners) > 1:
            winners = 'Draw'
        else:
            winners = winners.pop()
        moves = len(game.variant.moves_history)

        if not args.silent:
            print_state(game)
        print('Winner(s): {!s:6s} Moves: {!s:3s} Description: {:s}'.format(winners, moves, desc))
        if not args.silent:
            print('moves:', [str(move) for move in game.variant.moves_history])

        engine1.stop_engine()
        engine2.stop_engine()

    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception:
        print("Game interrupted by unexpected error")
        print('already executed moves:')
        print([str(move) for move in game.variant.moves_history])
        print('move intended to execute by engine:', str_move)
        print_state(game)
        print("This chess implementation thinks next moves are available:",
              ", ".join(str(x) for x in game.variant.all_available_moves()))

        raise
    exit(0)
