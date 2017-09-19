from src.app.pieces import Position

white = 0
black = 1


class Piece:
    name = 'Piece'
    char = 'p'

    def __init__(self, side: int, position: Position):
        self.side = side
        self.position = position

    def __repr__(self):
        if self.side == white:
            return '<White %s>' % self.name
        elif self.side == black:
            return '<Black %s>' % self.name
        raise Exception('oops')

    def __str__(self):
        if self.side == white:
            return self.char.upper()
        elif self.side == black:
            return self.char.lower()
        raise Exception('oops')
