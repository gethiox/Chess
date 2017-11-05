#!/usr/bin/env python3
from app.board import StandardBoard
from app.move import StandardMove
from app.player import Player
from app.position import StandardPosition
from app.variants import Normal
from cli import board_rendererer
from interface.game import Game

if __name__ == "__main__":
    player1 = Player("Some white player")
    player2 = Player("Some black player")

    game = Game(player1=player1, player2=player2, variant=Normal(StandardBoard()))
    board_rendererer.tiny(game.variant.board)
    print("FEN: %s\n" % game.variant.board.get_fen())

    moves = [
        StandardMove(source=StandardPosition('f2'), destination=StandardPosition('f3')),
        StandardMove(source=StandardPosition('e7'), destination=StandardPosition('e5')),
        StandardMove(source=StandardPosition('g2'), destination=StandardPosition('g4')),
        StandardMove(source=StandardPosition('d8'), destination=StandardPosition('h4')),
    ]

    for move in moves:
        game.move(move)
        board_rendererer.tiny(game.variant.board)
        print("move: %s\n" % move)

    print('Pieces on the board:')
    for position, piece in game.variant.board.pieces():
        print("%s: %s %s" % (position, piece.side, piece.name))
