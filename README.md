Branch is highly experimental and should be not considered as useful

You can play with pieces here - complete game logic not yet implemented

See [example_app.py](src/example_app.py)

```python
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
```

Output:
```
+---+---+---+---+---+---+---+---+
| r | n | b | q | k | b | n | r |
+---+---+---+---+---+---+---+---+
| p | p | p | p | p | p | p | p |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
| P | P | P | P | P | P | P | P |
+---+---+---+---+---+---+---+---+
| R | N | B | Q | K | B | N | R |
+---+---+---+---+---+---+---+---+
Insert move, eg. "e2e4"
Move: a1z9
You give position above actual board range (8x8)
Move: a2a3
+---+---+---+---+---+---+---+---+
| r | n | b | q | k | b | n | r |
+---+---+---+---+---+---+---+---+
| p | p | p | p | p | p | p | p |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
| P |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   | P | P | P | P | P | P | P |
+---+---+---+---+---+---+---+---+
| R | N | B | Q | K | B | N | R |
+---+---+---+---+---+---+---+---+
Move: e7e6
+---+---+---+---+---+---+---+---+
| r | n | b | q | k | b | n | r |
+---+---+---+---+---+---+---+---+
| p | p | p | p |   | p | p | p |
+---+---+---+---+---+---+---+---+
|   |   |   |   | p |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
| P |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   | P | P | P | P | P | P | P |
+---+---+---+---+---+---+---+---+
| R | N | B | Q | K | B | N | R |
+---+---+---+---+---+---+---+---+
```

Another impractical example
See [example.py](src/example.py)

```python
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
print(game.board.pieces(), '\n')

board_rendererer.normal(game.board)

pos = StandardPosition("a2")
piece = game.board.get_piece(pos)
print("Piece: %s %s (%s)\nMoves: %s\nCaptures: %s" % (
    piece.side,
    piece.name,
    str(pos),
    [str(pos) for pos in game.variant.available_moves(pos)],
    [str(pos) for pos in game.variant.available_captures(pos)],
))

pos = StandardPosition("h4")
piece = game.board.get_piece(pos)
print("Piece: %s %s (%s)\nMoves: %s\nCaptures: %s" % (
    piece.side,
    piece.name,
    str(pos),
    [str(pos) for pos in game.variant.available_moves(pos)],
    [str(pos) for pos in game.variant.available_captures(pos)],
))
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
{<Position a1>: <White Rook>, <Position b1>: <White Knight>, <Position c1>: <White Bishop>,
 <Position d1>: <White Queen>, <Position e1>: <White King>, <Position f1>: <White Bishop>,
 <Position g1>: <White Knight>, <Position h1>: <White Rook>, <Position a2>: <White Pawn>,
 <Position b2>: <White Pawn>, <Position c2>: <White Pawn>, <Position d2>: <White Pawn>,
 <Position e2>: <White Pawn>, <Position h2>: <White Pawn>, <Position f3>: <White Pawn>,
 <Position g4>: <White Pawn>, <Position h4>: <Black Queen>, <Position e5>: <Black Pawn>,
 <Position a7>: <Black Pawn>, <Position b7>: <Black Pawn>, <Position c7>: <Black Pawn>,
 <Position d7>: <Black Pawn>, <Position f7>: <Black Pawn>, <Position g7>: <Black Pawn>,
 <Position h7>: <Black Pawn>, <Position a8>: <Black Rook>, <Position b8>: <Black Knight>,
 <Position c8>: <Black Bishop>, <Position e8>: <Black King>, <Position f8>: <Black Bishop>,
 <Position g8>: <Black Knight>, <Position h8>: <Black Rook>}

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
+---+---+---+---+---+---+---+---+
Piece: White Pawn (a2)
Moves: ['a3']
Captures: []
Piece: Black Queen (h4)
Moves: ['h5', 'h6', 'h3', 'g5', 'f6', 'e7', 'd8', 'g3', 'f2']
Captures: ['h2', 'g4', 'e1']
```