Branch is highly experimental and should be not considered as useful  
Warning: en passant, castling, pawn promotion and pawn first two-field move is not yet implemented.

Simple chess app to play with pieces [example_app.py](src/example_app.py)  
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
Insert move, eg. "e2e4" (tyoe 'board' to show board)
Move: e2e4
give me a valid chess move
Move: e2e3
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
|   |   |   |   | P |   |   |   |
+---+---+---+---+---+---+---+---+
| P | P | P | P |   | P | P | P |
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
|   |   |   |   | P |   |   |   |
+---+---+---+---+---+---+---+---+
| P | P | P | P |   | P | P | P |
+---+---+---+---+---+---+---+---+
| R | N | B | Q | K | B | N | R |
+---+---+---+---+---+---+---+---+
```

The shortest possible game with some random statistics [example.py](src/example.py)

```
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
P P P P P P P P
R N B Q K B N R

f2f3 is a valid move
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . P . .
P P P P P . P P
R N B Q K B N R

half move: 2
move: 1
on move: Black
last move: f2f3
available moves: 12
winner side(s): None

e7e6 is a valid move
r n b q k b n r
p p p p . p p p
. . . . p . . .
. . . . . . . .
. . . . . . . .
. . . . . P . .
P P P P P . P P
R N B Q K B N R

half move: 3
move: 2
on move: White
last move: e7e6
available moves: 12
winner side(s): None

g2g3 is a valid move
r n b q k b n r
p p p p . p p p
. . . . p . . .
. . . . . . . .
. . . . . . . .
. . . . . P P .
P P P P P . . P
R N B Q K B N R

half move: 4
move: 2
on move: Black
last move: g2g3
available moves: 23
winner side(s): None

d8e7 is a valid move
r n b . k b n r
p p p p q p p p
. . . . p . . .
. . . . . . . .
. . . . . . . .
. . . . . P P .
P P P P P . . P
R N B Q K B N R

half move: 5
move: 3
on move: White
last move: d8e7
available moves: 14
winner side(s): None

g3g4 is a valid move
r n b . k b n r
p p p p q p p p
. . . . p . . .
. . . . . . . .
. . . . . . P .
. . . . . P . .
P P P P P . . P
R N B Q K B N R

half move: 6
move: 3
on move: Black
last move: g3g4
available moves: 21
winner side(s): None

e7h4 is a valid move
r n b . k b n r
p p p p . p p p
. . . . p . . .
. . . . . . . .
. . . . . . P q
. . . . . P . .
P P P P P . . P
R N B Q K B N R

half move: 7
move: 4
on move: White
last move: e7h4
available moves: 0
winner side(s): {<Black Side>}
```