#!/usr/bin/env python3
from app.move import StandardMove
from app.player import Player
from app.position import StandardPosition
from app.variants import Normal, KingOfTheHill, ThreeCheck
from cli import board_rendererer
from interface.game import Game

if __name__ == "__main__":
    print('Which variant do you want to play?\n'
          '1 - Normal\n'
          '2 - King of The Hill\n'
          '3 - Three Check')
    answer = int(input("Selected mode: "))
    if answer == 1:
        mode = Normal()
    elif answer == 2:
        mode = KingOfTheHill()
    elif answer == 3:
        mode = ThreeCheck()
    else:
        raise NotImplementedError("you need to specify correct int value, try harder next time!")
    print("Playing %s game mode" % mode.name)

    player = Player("player")

    game = Game(player1=player, player2=player, variant=mode)
    board_rendererer.normal(game.board)
    print("Insert move, eg. \"e2e4\" (tyoe \'board\' to show board)")
    try:
        while True:
            move_str = input("Move: ")
            if move_str == "board":
                board_rendererer.normal(game.board)
                continue
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
            try:
                game.move(move)
            except Exception as err:
                print(err)
                continue
            board_rendererer.normal(game.board)
            if game.variant.game_state:
                print('game is over! Winner: %s' % game.variant.game_state)
                break

    except KeyboardInterrupt:
        print('\nThanks for moving pieces!')
        exit(0)
