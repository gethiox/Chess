import re
from string import ascii_lowercase
from typing import Union, Tuple, List, Optional, Iterator

location_regex = re.compile(r'^(?P<file>[a-zA-Z]+)(?P<rank>[0-9]+)$')


class Side:
    def __init__(self, name: str):
        self.__name = name

    @property
    def name(self):
        return self.__name

    def __repr__(self):
        return self.__name

    def __str__(self):
        return self.__name


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
        self.__side = side

    @property
    def side(self) -> Side:
        return self.__side

    def __repr__(self):
        return '%s %s' % (self.__side, self.name)

    def __str__(self):
        return self.char.upper() if self.__side == White else self.char.lower()


class Position:
    """
    tuple with two board coordinates is too simple of course
    """

    def __init__(self, pos: Union[str, Tuple[int, int], List[int]]):
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

    def __repr__(self):
        return 'Position: %s' % self

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

    def __repr__(self):
        if self.__promotion:
            return 'Move: %s to %s with promotion to %s' % (self.__a, self.__b, self.__promotion.name)
        else:
            return 'Move: %s to %s' % (self.__a, self.__b)

    def __str__(self):
        if self.__promotion:
            return '%s%s%s' % (self.__a, self.__b, self.__promotion.char)
        else:
            return '%s%s' % (self.__a, self.__b)
