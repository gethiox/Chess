from abc import ABCMeta, abstractmethod
from typing import Type, TYPE_CHECKING, Tuple, Sequence

if TYPE_CHECKING:
    from interface.side import Side

Vector = Tuple[int, int]  # Determine movement vector
AnyDirection = bool  # Determine if movement Vector cover all combinations in any direction
Distance = int  # Determine maximum move/capture distance (iterations of Vector)
SelfCapture = bool  # Determine if self-capture is allowed (any variant even supports it?)
CaptureBreak = bool  # Determine if a capture breaks availability to move behind enemy piece


class MoveDescription:
    def __init__(self, vector: Tuple[int, int], any_direction: bool, distance: int, capture_break: bool = True):
        self.vector = vector
        self.any_direction = any_direction
        self.distance = distance
        self.capture_break = capture_break


class CaptureDescription:
    def __init__(self, vector: Tuple[int, int], any_direction: bool, distance: int, self_capture: bool = False):
        self.vector = vector
        self.any_direction = any_direction
        self.distance = distance
        self.self_capture = self_capture


class Movement:
    """
    This object explains for game engine basics of available piece movements, eg. where can go and where can capture.
    Explanation doesn't relate to GameMode specific movements which depends on game state, eg en passant (last pawn 
    move), or castling (King or Rook was ever moved, is field between King's source and destination attacked)
    Movement is separated to two section - capture and move. It may determine different Piece mechanics, eg. for 
    a pawn - can move forward but capture only diagonal in the front. This interface should be flexible to determine
    any type of movement, even as the stupidest as human being can imagine (as long as not depend on the game state).
    If not, Use this interface to implement your stupid movement ability.
    """

    def __init__(self, move_descriptions: Sequence[MoveDescription],
                 capture_descriptions: Sequence[CaptureDescription] = None):
        self.__move_descriptions = move_descriptions
        if capture_descriptions is not None:
            self.__capture_descriptions = capture_descriptions
        else:
            new_capture_descriptions = []
            for move_description in move_descriptions:
                new_capture_descriptions.append(
                    CaptureDescription(
                        vector=move_description.vector,
                        any_direction=move_description.any_direction,
                        distance=move_description.distance,
                        self_capture=False
                    )
                )
            self.__capture_descriptions = new_capture_descriptions

    @property
    @abstractmethod
    def move(self) -> Sequence[MoveDescription]:
        return self.__move_descriptions

    @property
    def capture(self) -> Sequence[CaptureDescription]:
        return self.__capture_descriptions


class Piece(metaclass=ABCMeta):
    def __init__(self, side: Type['Side']):
        self.__side = side

    @property
    @abstractmethod
    def name(self) -> str:
        """return piece name starts with uppercase, eg. Pawn"""
        pass

    @property
    @abstractmethod
    def char(self) -> str:
        """return one lowercase letter representation of piece, eg. p"""
        pass

    @property
    @abstractmethod
    def points(self) -> int:
        """return int piece value representation, eg. 1"""
        pass

    @property
    @abstractmethod
    def movement(self) -> 'Movement':
        """return something that describe piece movement and is easy to use by game engine, any ideas?"""
        pass

    @property
    def side(self) -> Type['Side']:
        return self.__side

    def __repr__(self):
        return '<%s %s>' % (self.side, self.name)

    def __str__(self):
        return self.char.upper() if self.side.capitalize else self.char.lower()

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return isinstance(other, type(self)) and other.side == self.side

    def __ne__(self, other):
        if isinstance(other, type(self)):
            return not (isinstance(other, type(self)) and other.side == self.side)
        return True
