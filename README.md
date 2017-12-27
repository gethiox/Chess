I don't know how you found this repository but I can guess that you
probably looking for more supported solution: [python-chess](https://pypi.python.org/pypi/python-chess)

It's my private and not very well supported chess implementation at the
moment.
My aim of that project is to improve my skills and experimenting with
random things. Moreover the main goal of this implementation is to be
as easy as possible to extend, eg. for adding new chess variants
and mechanics. Code quality and readability is more important than
performance, optimizations is a secondary matter and should never be
at the first place (if so it could be better and easier to use other
language than Python).

`setup.py` are not yet provided, as long as it doesn't need any of
external libraries it is convenient to run provided scripts or create
your own. Of course `setup.py` will be prepared in the near future.

Note:
If you read the code you could feel something weird about everything
that touches the Players and some other things. My approach is to
project flexible implementation, even for chess for more than two
players and chessboards that has more than two dimensions.

Arbitrary development status:
- [x] Classic Chess implementation
      - [x] Piece movement
      - [x] en-passant
      - [x] castling
- [ ] Some useful features
      - [x] Game end-state explanation (why game was interrupted, eg. insufficient material)
      - [x] FEN I/O support
      - [x] Chess engine handler (eg. for [stockfish](https://stockfishchess.org/))
      - [x] Full game move validation (check if move is possible according to the variation rules)
      - [x] Threefold repetition validation
      - [x] 50-move-rule validation
      - [x] simple insufficient material validation
      - [x] available moves generator (Note: inefficient)
      - [ ] chess-engine mode (Note: xD)
      - [ ] PGN move notation support
      - [ ] PGN game file reading/writing support
- [ ] Tests which given a proof that everything is working fine
      - [x] Base26 encoding and decoding
      - [ ] Game-logic tests
- [ ] Other variants
      - [x] King of the Hill
      - [x] Three Check
      - [ ] Chess960
      - [ ] CrazyHouse
      - [ ] Horde
      - [ ] PreChess
      - [ ] UpsideDown
      - [ ] Double Chess
      - [ ] Anti Chess
      - [ ] Racing Kings
      - [ ] Four player Chess
      - [ ] 3D Chess

Examples:
Simple chess app to play with yourself ([example_app.py](src/example_app.py))
```
sh-4.4$ ./src/example_app.py --hill
Playing King of The Hill game mode
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
On move: White, Available moves: 20
Insert move, eg. "e2e4" (tyoe 'board' to show board, 'back' to rollback last moves)
Move: e2e4
+---+---+---+---+---+---+---+---+
| r | n | b | q | k | b | n | r |
+---+---+---+---+---+---+---+---+
| p | p | p | p | p | p | p | p |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   | P |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
| P | P | P | P |   | P | P | P |
+---+---+---+---+---+---+---+---+
| R | N | B | Q | K | B | N | R |
+---+---+---+---+---+---+---+---+
On move: Black, Available moves: 20
Move: d7d5
+---+---+---+---+---+---+---+---+
| r | n | b | q | k | b | n | r |
+---+---+---+---+---+---+---+---+
| p | p | p |   | p | p | p | p |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   | p |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   | P |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
| P | P | P | P |   | P | P | P |
+---+---+---+---+---+---+---+---+
| R | N | B | Q | K | B | N | R |
+---+---+---+---+---+---+---+---+
On move: White, Available moves: 31
Move: back
How many moves do you want to rollback? 1
+---+---+---+---+---+---+---+---+
| r | n | b | q | k | b | n | r |
+---+---+---+---+---+---+---+---+
| p | p | p | p | p | p | p | p |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   | P |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
| P | P | P | P |   | P | P | P |
+---+---+---+---+---+---+---+---+
| R | N | B | Q | K | B | N | R |
+---+---+---+---+---+---+---+---+
Move:
```

part of [example.py](src/example.py) for profiling purpose.

```
sh-4.4$ ./src/example.py
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


FEN: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
executed/last move: None
move count: 1
on move: White
in check: False
available moves: 20
winner side(s): None
game state description: None


 (     game statistic collection time: 0.15166 )

+---+---+---+---+---+---+---+---+
| r | n | b | q | k | b | n | r |
+---+---+---+---+---+---+---+---+
| p | p | p | p | p | p | p | p |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   | P |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
| P | P | P |   | P | P | P | P |
+---+---+---+---+---+---+---+---+
| R | N | B | Q | K | B | N | R |
+---+---+---+---+---+---+---+---+

FEN: rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1
executed/last move: d2d4
move count: 1
on move: Black
in check: False
available moves: 20
winner side(s): None
game state description: None

 ( move validation and execution time: 0.00584 )
 (     game statistic collection time: 0.22791 )

+---+---+---+---+---+---+---+---+
| r | n | b | q | k | b | n | r |
+---+---+---+---+---+---+---+---+
| p | p | p |   | p | p | p | p |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   | p |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   | P |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
| P | P | P |   | P | P | P | P |
+---+---+---+---+---+---+---+---+
| R | N | B | Q | K | B | N | R |
+---+---+---+---+---+---+---+---+

FEN: rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w KQkq d6 0 2
executed/last move: d7d5
move count: 2
on move: White
in check: False
available moves: 27
winner side(s): None
game state description: None

 ( move validation and execution time: 0.01156 )
 (     game statistic collection time: 0.20120 )

(...)

+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   | k | p | B | P | K |   | q |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   | P |   |   |   | P |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   | B |   |   |   |   |
+---+---+---+---+---+---+---+---+

FEN: 8/8/1kpBPK1q/8/1P3P2/8/8/3B4 w - - 17 81
executed/last move: h7h6
move count: 81
on move: White
in check: True
available moves: 4
winner side(s): {<Black Side>, <White Side>}
game state description: threefold repetition

 ( move validation and execution time: 0.00281 )
 (     game statistic collection time: 0.05707 )

    all moves execution time: 15.8679 (160 moves in total)
     slowest validation time: 0.0069 fastest: 0.00237
slowest data collection time: 0.6069 fastest: 0.04338
```