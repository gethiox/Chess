#!/usr/bin/env python3
from argparse import ArgumentParser

from app.engine import EngineHandler
from app.move import StandardMove
from app.pieces import King
from app.player import Player
from app.variants import Normal
from cli import board_rendererer
from interface.game import Game


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(dest='engine_path', type=str, nargs='?',
                        help='path of UCI chess engine')
    parser.add_argument('--wtime', dest='wtime', type=int, default=1000,
                        help='time for white in ms (default: 1000)')
    parser.add_argument('--btime', dest='btime', type=int, default=1000,
                        help='time for black in ms (default: 1000)')
    parser.add_argument('--wthreads', dest='wthreads', type=int, default=1,
                        help='threads for white side engine (default: 1)')
    parser.add_argument('--bthreads', dest='bthreads', type=int, default=1,
                        help='threads for black side engine (default: 1)')
    parser.add_argument('--wponder', dest='wponder', action='store_true',
                        help='allow white\'s engine to ponder when black on move')
    parser.add_argument('--bponder', dest='bponder', action='store_true',
                        help='allow black\'s engine to ponder when white on move')
    parser.add_argument('--silent', dest='silent', action='store_true',
                        help='Display only ending game state')
    parser.add_argument('--count', dest='count', action='store_true',
                        help='Enable counting of available moves')
    return parser.parse_args()


def print_state(game):
    board_str = board_rendererer.normal(
        game.variant.board,
        info_fields=[game.variant.last_move.source, game.variant.last_move.destination] if game.variant.last_move else [],
        warn_fields=[x[0] for x in
                     game.variant.board.find_pieces(King(game.variant.on_move))] if game.variant.is_check else []
    )
    fen = "FEN: %s" % str(game.variant)
    data = "On move: {on_move!s:5s}, last move: {last_move!s:5s} Available moves: {moves!s:s}".format(
        on_move=game.variant.on_move,
        last_move=game.variant.last_move,
        moves=len(game.variant.all_available_moves()) if args.count else 'Disabled',
    )
    print(board_str)
    print(fen)
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
    engine1 = EngineHandler(args.engine_path, threads=args.wthreads, ponder=args.wponder, hash=64)
    engine2 = EngineHandler(args.engine_path, threads=args.bthreads, ponder=args.bponder, hash=64)

    engine1.start_engine()
    engine2.start_engine()

    game = Game(player1=player1, player2=player2, variant=mode)

    if not args.silent:
        print_state(game)

    try:
        while True:
            str_move = engine1.best_move(
                moves_seq=' '.join([str(move) for move in game.variant.moves_history]),
                wtime=args.wtime,
                btime=args.btime
            )
            move = StandardMove.from_str(str_move)
            game.move(move)
            if not args.silent:
                print_state(game)
            if game.variant.game_state[0]:
                break

            str_move = engine2.best_move(
                moves_seq=' '.join([str(move) for move in game.variant.moves_history]),
                wtime=args.wtime,
                btime=args.btime
            )
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

        print('Winner(s): {!s:6s} Moves: {!s:3s} Description: {:s}'.format(winners, moves, desc))
        if not args.silent:
            print('moves:', [str(move) for move in game.variant.moves_history])

        engine1.stop_engine()
        engine2.stop_engine()

    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as err:
        print('Catched exception:', err)
        print("Game interrupted by unexpected error")
        print('already executed moves:')
        print([str(move) for move in game.variant.moves_history])
        print('move intended to execute by engine:', str_move)
        print_state(game)
        print("This chess implementation thinks next moves are available:",
              ", ".join(str(x) for x in game.variant.all_available_moves()))

        raise
    exit(0)
