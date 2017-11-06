#!/usr/bin/env python3
from app.move import StandardMove
from app.player import Player
from app.position import StandardPosition
from app.sides import White, Black
from app.variants import Normal
from cli import board_rendererer
from interface.game import Game

if __name__ == "__main__":
    player = Player("player")

    game = Game(player1=player, player2=player, variant=Normal())
    board_rendererer.normal(game.board)
    print("Insert move, eg. \"e2e4\"")
    try:
        while True:
            move_str = input("Move: ")
            try:
                source = StandardPosition(move_str[:2])
                destination = StandardPosition(move_str[2:])
            except ValueError as err:
                print("bad syntax (%s)" % err)
                continue
            if not game.board.validate_position(source) or not game.board.validate_position(destination):
                print("You give position above actual board range (%dx%d)" % game.board.size)
                continue
            move = StandardMove(source=source, destination=destination)
            if not game.variant.assert_move(move):
                print("%s is not a valid move" % move)
                continue

            game.move(move)
            board_rendererer.normal(game.board)

    except KeyboardInterrupt:
        print('\nThanks for moving pieces!')
        exit(0)