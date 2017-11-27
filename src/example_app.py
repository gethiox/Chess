#!/usr/bin/env python3
from argparse import ArgumentParser

from app.move import StandardMove
from app.pieces import from_str
from app.player import Player
from app.position import StandardPosition
from app.variants import Normal, KingOfTheHill, ThreeCheck
from cli import board_rendererer
from interface.game import Game


def parse_args():
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--normal', dest='normal', action='store_true', help='Classic Chess (default)')
    group.add_argument('--hill', dest='hill', action='store_true', help='King of The Hill')
    group.add_argument('--check', dest='check', action='store_true', help='Three Check')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.normal:
        mode = Normal()
    elif args.hill:
        mode = KingOfTheHill()
    elif args.check:
        mode = ThreeCheck()
    else:
        mode = Normal()

    print("Playing %s game mode" % mode.name)

    player = Player("player")

    game = Game(player1=player, player2=player, variant=mode)
    print(board_rendererer.normal(game.board))
    print("On move: {on_move!s:5s}, Avabile moves: {moves:d}".format(
        on_move=game.variant.on_move,
        moves=len(game.variant.all_available_moves())))
    print("Insert move, eg. \"e2e4\" (tyoe \'board\' to show board, \'back\' to rollback last moves)")
    try:
        while True:
            move_str = input("Move: ")
            if move_str == "board":
                print(board_rendererer.normal(game.board))
                continue
            elif move_str == "back":
                i = int(input("How many moves do you want to rollback? "))
                try:
                    game.variant.load_history(i)
                except IndexError:
                    print("Given value are above of the length of moves history")
                    continue
                print(board_rendererer.normal(game.board))
                continue
            try:
                source = StandardPosition.from_str(move_str[0:2])
                destination = StandardPosition.from_str(move_str[2:4])
                promotion_char = move_str[4:]
            except ValueError as err:
                print("bad syntax (%s)" % err)
                continue
            if not game.board.validate_position(source) or not game.board.validate_position(destination):
                print("You give position above actual board range (%dx%d)" % game.board.size)
                continue

            if promotion_char:
                move = StandardMove(source=source, destination=destination,
                                    promotion=from_str(promotion_char, initialized=False))
            else:
                move = StandardMove(source=source, destination=destination)
            try:
                game.move(move)
            except Exception as err:
                print(err)
                continue
            print(board_rendererer.normal(game.board))
            print("Avabile moves: %d" % len(game.variant.all_available_moves()))
            if game.variant.game_state:
                print('game is over! Winner: %s' % game.variant.game_state)
                break

    except KeyboardInterrupt:
        print('\nThanks for moving pieces!')
        exit(0)
