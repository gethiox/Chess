from typing import Union, Tuple

white = 0
black = 1

ranks = '12345678'
files = 'abcdefgh'


class Position:
    def __init__(self, pos: Union[str, Tuple[int]]):
        if isinstance(pos, tuple):
            if len(pos) != 2:
                raise ValueError('Position should be given as tuple/list with only two ints')
            self.pos = [pos[0], pos[1]]
        elif isinstance(pos, str):
            if len(pos) != 2:
                raise ValueError('Position should be given as two letter coordinates (file, rank)')
            self.pos = [files.index(pos[0]), ranks.index(pos[1])]

    def __repr__(self):
        return '<Position: %s>' % str(self)

    def __str__(self):
        return '%s%s' % (files[self.pos[0]], ranks[self.pos[1]])

    def __iter__(self):
        for coordinate in self.pos:
            yield coordinate


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
