See [example.py](docs/CONTRIBUTING.md)

```python3
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
print(game.variant.board.pieces(), '\n')

board_rendererer.normal(game.variant.board)
```

Output:
```
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
P P P P P P P P
R N B Q K B N R
FEN: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR

r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . P . .
P P P P P . P P
R N B Q K B N R
move: f2f3

r n b q k b n r
p p p p . p p p
. . . . . . . .
. . . . p . . .
. . . . . . . .
. . . . . P . .
P P P P P . P P
R N B Q K B N R
move: e7e5

r n b q k b n r
p p p p . p p p
. . . . . . . .
. . . . p . . .
. . . . . . P .
. . . . . P . .
P P P P P . . P
R N B Q K B N R
move: g2g4

r n b . k b n r
p p p p . p p p
. . . . . . . .
. . . . p . . .
. . . . . . P q
. . . . . P . .
P P P P P . . P
R N B Q K B N R
move: d8h4

Pieces on the board:
{<Position a1>: <White Rook>, <Position b1>: <White Knight>, <Position c1>: <White Bishop>, <Position d1>: <White Queen>, <Position e1>: <White King>, <Position f1>: <White Bishop>, <Position g1>: <White Knight>, <Position h1>: <White Rook>, <Position a2>: <White Pawn>, <Position b2>: <White Pawn>, <Position c2>: <White Pawn>, <Position d2>: <White Pawn>, <Position e2>: <White Pawn>, <Position h2>: <White Pawn>, <Position f3>: <White Pawn>, <Position g4>: <White Pawn>, <Position h4>: <Black Queen>, <Position e5>: <Black Pawn>, <Position a7>: <Black Pawn>, <Position b7>: <Black Pawn>, <Position c7>: <Black Pawn>, <Position d7>: <Black Pawn>, <Position f7>: <Black Pawn>, <Position g7>: <Black Pawn>, <Position h7>: <Black Pawn>, <Position a8>: <Black Rook>, <Position b8>: <Black Knight>, <Position c8>: <Black Bishop>, <Position e8>: <Black King>, <Position f8>: <Black Bishop>, <Position g8>: <Black Knight>, <Position h8>: <Black Rook>}

+---+---+---+---+---+---+---+---+
| r | n | b |   | k | b | n | r |
+---+---+---+---+---+---+---+---+
| p | p | p | p |   | p | p | p |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   | p |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   | P | q |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   | P |   |   |
+---+---+---+---+---+---+---+---+
| P | P | P | P | P |   |   | P |
+---+---+---+---+---+---+---+---+
| R | N | B | Q | K | B | N | R |
+---+---+---+---+---+---+---+---+```