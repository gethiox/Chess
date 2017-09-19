from src.domain.pieces import Piece

ranks = '12345678'
files = 'abcdefgh'


class Position:
    def __init__(self, x, y):
        self.pos = [x, y]

    def __repr__(self):
        return '<Position: %s>' % str(self)

    def __str__(self):
        return '%s%s' % (files[self.pos[0]], ranks[self.pos[1]])

    def __iter__(self):
        for coordinate in self.pos:
            yield coordinate


class King(Piece):
    name = 'King'
    char = 'k'


class Queen(Piece):
    name = 'Queen'
    char = 'q'


class Rook(Piece):
    name = 'Rook'
    char = 'r'


class Bishop(Piece):
    name = 'Bishop'
    char = 'b'


class Knight(Piece):
    name = 'Knight'
    char = 'N'


class Pawn(Piece):
    name = 'Pawn'
    char = 'p'
