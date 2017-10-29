import re
from math import inf as infinity
from string import ascii_lowercase
from typing import Union, Tuple, List, Iterator, Optional

from domain.pieces import Piece, Side, Position

location_regex = re.compile(r'^(?P<file>[a-zA-Z]+)(?P<rank>[0-9]+)$')


class King(Piece):
    @property
    def char(self):
        return "k"

    @property
    def points(self):
        return infinity

    @property
    def name(self):
        return "King"


class Queen(Piece):
    @property
    def points(self) -> int:
        return 9

    @property
    def char(self) -> str:
        return "q"

    @property
    def name(self) -> str:
        return "Queen"


class Rook(Piece):
    @property
    def points(self) -> int:
        return 5

    @property
    def char(self) -> str:
        return 'r'

    @property
    def name(self) -> str:
        return "Rook"


class Bishop(Piece):
    @property
    def points(self) -> int:
        return 3

    @property
    def char(self) -> str:
        return 'b'

    @property
    def name(self) -> str:
        return 'Bishop'


class Knight(Piece):
    @property
    def points(self) -> int:
        return 3

    @property
    def char(self) -> str:
        return "n"

    @property
    def name(self) -> str:
        return "Knight"


class Pawn(Piece):
    @property
    def points(self) -> int:
        return 1

    @property
    def char(self) -> str:
        return "p"

    @property
    def name(self) -> str:
        return "Pawn"


class WhiteSide(Side):
    @property
    def char(self):
        return "w"

    @property
    def name(self) -> str:
        return "White"

    @property
    def capitalize(self) -> bool:
        return True


class BlackSide(Side):
    @property
    def char(self):
        return "b"

    @property
    def name(self) -> str:
        return "Black"

    @property
    def capitalize(self) -> bool:
        return False


White = WhiteSide()
Black = BlackSide()

str_map = {
    'k': King,
    'q': Queen,
    'r': Rook,
    'b': Bishop,
    'n': Knight,
    'p': Pawn,
}


def from_str(piece: str) -> Piece:
    """
    Method designed to return Piece object from given one-letter string.
    Needed only for processing FEN board-state format.
    """
    if piece.lower() not in ('k', 'q', 'r', 'b', 'n', 'p'):
        raise ValueError('"%s" not defined as Chess piece.', piece)
    return str_map[piece.lower()](White) if piece.isupper() else str_map[piece.lower()](Black)


class StandardPosition(Position):
    """
    tuple with two board coordinates is too simple of course, here is a standard 2D Position object implementation.
    """

    def __init__(self, pos: Union[str, Tuple[int, int], List[int]]):  # TODO: decide to support stable and one interface
        if isinstance(pos, tuple) or isinstance(pos, list):
            if len(pos) != 2:
                raise ValueError('Position should be given as tuple/list with only two ints')
            self.__file = pos[0]
            self.__rank = pos[1]
        elif isinstance(pos, str):
            output = location_regex.search(pos)
            if not output:
                raise ValueError('Position should be given as two letter coordinates (file, rank)')
            self.__rank = self.__rank_from_str_to_int(output.group('rank'))
            self.__file = self.__file_from_str_to_int(output.group('file'))

    @property
    def file(self) -> int:
        return self.__file

    @property
    def rank(self) -> int:
        return self.__rank

    @staticmethod
    def __rank_from_str_to_int(rank: str) -> int:
        """
        Converting rank from standard string format to internal int value (starts from 0 instead of 1),
        eg. 1 in standard string means 0 in internal int format (value is a second part of position, eg "a1")
        """
        return int(rank) - 1

    @staticmethod
    def __rank_from_int_to_str(rank: int) -> str:
        """
        Converting rank from internal value to standard string format (starts from 1 instead of 0),
        eg. 0 in internal int means 1 in standard string format (value is a second part of position, eg "a1")
        """
        return str(rank + 1)

    @staticmethod
    def __file_from_str_to_int(rank: str) -> int:
        """
        Converting file from standard string format to internal int value,
        eg. "A" means 0, "B": 1, "Z": 25, "BA": 26 (Note: 26 == "BA", not "AA" because "A" and "AA" is an equal value,
        just like 01 == 1 in decimal system)
        """
        # Warning, my own, not very well tested implementation of base26 converter
        values = []
        for letter in rank:
            values.append(ascii_lowercase.index(letter.lower()))
        index_value = 0
        counter = 0
        for value in reversed(values):
            if counter < 1:
                index_value += value
            else:
                index_value += (value * 26) ** counter
            counter += 1
        return index_value

    @staticmethod
    def __file_from_int_to_str(file: int) -> str:
        """
        Converting file from internal int value to standard string format,
        eg. 0 means "A", 1: "B", 25: "Z", 26: "BA" (Note: 26 == "BA", not "AA" because "A" and "AA" is an equal value,
        just like 01 == 1 in decimal system)
        """
        # Warning, my own, not very well tested implementation of base26 converter
        output_chars = 1
        while (len(ascii_lowercase)) ** output_chars <= file:
            output_chars += 1
        values = []
        for i in range(output_chars):
            val = (file // len(ascii_lowercase) ** i) % (len(ascii_lowercase))
            values.append(val)

        return "".join(ascii_lowercase[x] for x in reversed(values))

    def __str__(self):
        return '%s%s' % (self.__file_from_int_to_str(self.file),
                         self.__rank_from_int_to_str(self.rank))

    def __iter__(self) -> Iterator[int]:
        for coordinate in (self.file, self.rank):
            yield coordinate

    def __getitem__(self, item) -> int:
        if item == 0:
            return self.file
        elif item == 1:
            return self.rank
        else:
            raise IndexError("tuple index out of range")


class Move:
    """
    Two Position aggregator with optional pawn promotion information
    """

    def __init__(self, a: Position, b: Position, promotion: Optional[Piece] = None):
        self.__a = a
        self.__b = b
        self.__promotion = promotion

    @property
    def a(self):
        return self.__a

    @property
    def b(self):
        return self.__b

    @property
    def promotion(self):
        return self.__promotion

    def __repr__(self):  # TODO: update for positions objects without support of converting to string
        if self.__promotion:
            return 'Move: %s to %s with promotion to %s' % (self.__a, self.__b, self.__promotion.name)
        else:
            return 'Move: %s to %s' % (self.__a, self.__b)

    def __str__(self):
        if self.__promotion:
            return '%s%s%s' % (self.__a, self.__b, self.__promotion.char)
        else:
            return '%s%s' % (self.__a, self.__b)
