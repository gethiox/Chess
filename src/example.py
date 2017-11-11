#!/usr/bin/env python3
from app.move import StandardMove
from app.player import Player
from app.position import StandardPosition
from app.sides import White, Black
from app.variants import Normal
from cli import board_rendererer
from interface.game import Game

if __name__ == "__main__":
    player1 = Player("Some white player")
    player2 = Player("Some black player")

    game = Game(player1=player1, player2=player2, variant=Normal())
    board_rendererer.tiny(game.board)
    print("FEN: %s\n" % game.board.get_fen())

    moves = [
        StandardMove(source=StandardPosition('f2'), destination=StandardPosition('f3')),
        StandardMove(source=StandardPosition('e7'), destination=StandardPosition('e5')),
        StandardMove(source=StandardPosition('g2'), destination=StandardPosition('g4')),
        StandardMove(source=StandardPosition('d8'), destination=StandardPosition('h4')),
    ]

    for move in moves:
        game.move(move)
        board_rendererer.tiny(game.board)
        print("move: %s\n" % move)

    print('Pieces on the board:')
    print(game.board.pieces, '\n')

    board_rendererer.normal(game.board)

    pos = StandardPosition("a2")
    piece = game.board.get_piece(pos)
    print("Piece: %s %s (%s)\nMoves: %s\nCaptures: %s\nAttacked Fields: %s\n" % (
        piece.side,
        piece.name,
        str(pos),
        [str(pos) for pos in game.variant.available_moves(pos)],
        [str(pos) for pos in game.variant.available_captures(pos)],
        [str(pos) for pos in game.variant.attacked_fields(pos)],
    ))

    pos = StandardPosition("h4")
    piece = game.board.get_piece(pos)
    print("Piece: %s %s (%s)\nMoves: %s\nCaptures: %s\nAttacked Fields: %s\n" % (
        piece.side,
        piece.name,
        str(pos),
        [str(pos) for pos in game.variant.available_moves(pos)],
        [str(pos) for pos in game.variant.available_captures(pos)],
        [str(pos) for pos in game.variant.attacked_fields(pos)],
    ))

    print("attacked fields by White:")
    print("%s" % [str(pos) for pos in game.variant.attacked_fields_by_side(White)])
    print("attacked fields by Black:")
    print("%s" % [str(pos) for pos in game.variant.attacked_fields_by_side(Black)])
