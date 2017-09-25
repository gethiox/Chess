from typing import Union, Tuple, List, Optional, Iterator

ranks = '12345678'
files = 'abcdefgh'


class Side:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


White = Side("White")
Black = Side("Black")


class Piece:
    """
    I don't know how to force overwrite these parameters when this class is used as Base instance.
    """
    name = 'Piece'
    char = 'p'
    points = 1

    def __init__(self, side: Side):
        self.side = side

    def __repr__(self):
        return '%s %s' % (self.side, self.name)

    def __str__(self):
        return self.char.upper() if self.side == White else self.char.lower()


class Position:
    """
    tuple with two board coordinates is too simple of course
    """
    def __init__(self, pos: Union[str, Tuple[int], List[int]]):
        if isinstance(pos, tuple) or isinstance(pos, list):
            if len(pos) != 2:
                raise ValueError('Position should be given as tuple/list with only two ints')
            self.pos = [pos[0], pos[1]]
        elif isinstance(pos, str):
            if len(pos) != 2:
                raise ValueError('Position should be given as two letter coordinates (file, rank)')
            self.pos = [files.index(pos[0]), ranks.index(pos[1])]

    def __repr__(self):
        return 'Position: %s' % str(self)

    def __str__(self):
        return '%s%s' % (files[self.pos[0]],
                         ranks[self.pos[1]])

    def __iter__(self) -> Iterator[int]:
        for coordinate in self.pos:
            yield coordinate


class Move:
    """
    Two Position aggregator with optional pawn promotion information
    """
    def __init__(self, a: Position, b: Position, promotion: Optional[Piece]):
        self.a = a
        self.b = b
        self.promotion = promotion

    def __repr__(self):
        if self.promotion:
            return 'Move: %s to %s with promotion to %s' % (self.a, self.b, self.promotion.name)
        else:
            return 'Move: %s to %s' % (self.a, self.b)

    def __str__(self):
        if self.promotion:
            return '%s%s%s' % (self.a, self.b, self.promotion.char)
        else:
            return '%s%s' % (self.a, self.b)
