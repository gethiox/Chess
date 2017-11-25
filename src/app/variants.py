# see more: https://en.wikipedia.org/wiki/List_of_chess_variants
import itertools
from copy import deepcopy
from math import inf as infinity
from typing import Type, TYPE_CHECKING, Tuple, Set, List, Optional, Dict

from app.board import StandardBoard
from app.move import StandardMove
from app.pieces import King, Pawn, Knight, Bishop, Rook, Queen
from app.position import StandardPosition
from app.sides import White, Black
from exceptions.variant import WrongMoveOrder, NotAValidMove, CausesCheck, NoPiece
from interface.variant import Variant

if TYPE_CHECKING:
    from interface.piece import Piece
    from interface.side import Side


class Normal(Variant):
    """
    This is a base classic chess implementation, it could be inherited to implement similar chess variants
    """

    def __init__(self, init_board_state: bool = True):
        self.__board = StandardBoard()
        if init_board_state:
            self.init_board_state()

        self.__half_moves = 1
        self.__moves_history = []
        self.__board_history = []

        self.__en_passant = None  # None or StandardPosition when pawn move trough two fields, any other set None value
        self.__half_moves_since_pawn_moved = 0
        # self.__castling

    @property
    def name(self):
        return "Classic Chess"

    @property
    def en_passant(self):
        return self.__en_passant

    @property
    def half_moves(self):
        return self.__half_moves

    @property
    def moves(self):
        return (self.__half_moves + 1) // len(self.sides)

    @property
    def moves_history(self) -> List['StandardMove']:
        return self.__moves_history

    @property
    def last_move(self) -> Optional['StandardMove']:
        try:
            return self.moves_history[-1]
        except IndexError:
            return None

    @property
    def on_move(self) -> Type['Side']:
        return self.sides[(self.__half_moves - 1) % len(self.sides)]

    @property
    def game_state(self) -> Optional[Set[Type['Side']]]:
        king_pos, _ = list(self.board.find_pieces(King(self.on_move)).items())[0]
        if not self.can_i_make_a_move():
            if king_pos in self.attacked_fields_by_sides(set(self.sides) - {self.on_move}):
                return set(self.sides) - {self.on_move}
            else:
                return set(self.sides)
        return None

    @property
    def board(self) -> StandardBoard:
        return self.__board

    @property
    def sides(self) -> List[Type['Side']]:
        return [White, Black]

    @property
    def pieces(self) -> Set[Type['Piece']]:
        # TODO: not used, to remove or something
        return {King, Queen, Rook, Bishop, Knight, Pawn}

    def init_board_state(self):
        self.board.put_piece(piece=Rook(White), position=StandardPosition((0, 0)))
        self.board.put_piece(piece=Rook(White), position=StandardPosition((7, 0)))
        self.board.put_piece(piece=Knight(White), position=StandardPosition((1, 0)))
        self.board.put_piece(piece=Knight(White), position=StandardPosition((6, 0)))
        self.board.put_piece(piece=Bishop(White), position=StandardPosition((2, 0)))
        self.board.put_piece(piece=Bishop(White), position=StandardPosition((5, 0)))
        self.board.put_piece(piece=Queen(White), position=StandardPosition((3, 0)))
        self.board.put_piece(piece=King(White), position=StandardPosition((4, 0)))

        for i in range(8):
            self.board.put_piece(piece=Pawn(White), position=StandardPosition((i, 1)))

        for i in range(8):
            self.board.put_piece(piece=Pawn(Black), position=StandardPosition((i, 6)))

        self.board.put_piece(piece=Rook(Black), position=StandardPosition((0, 7)))
        self.board.put_piece(piece=Rook(Black), position=StandardPosition((7, 7)))
        self.board.put_piece(piece=Knight(Black), position=StandardPosition((1, 7)))
        self.board.put_piece(piece=Knight(Black), position=StandardPosition((6, 7)))
        self.board.put_piece(piece=Bishop(Black), position=StandardPosition((2, 7)))
        self.board.put_piece(piece=Bishop(Black), position=StandardPosition((5, 7)))
        self.board.put_piece(piece=Queen(Black), position=StandardPosition((3, 7)))
        self.board.put_piece(piece=King(Black), position=StandardPosition((4, 7)))

        return self.board.get_fen()

    def assert_move(self, move: 'StandardMove'):
        source, destination = move.source, move.destination
        piece = self.board.get_piece(source)
        if not piece:
            raise NoPiece("Any piece on %s, you need to move pieces, not air." % source)
        if destination not in self.standard_moves(source) | self.standard_captures(source) | self.special_moves(source):
            raise NotAValidMove("%s is not a proper move for a %s %s" % (move, piece.side, piece.name))
        test_board = deepcopy(self.board)
        test_piece = test_board.remove_piece(source)
        test_board.put_piece(test_piece, destination)
        king_pos, king = list(test_board.find_pieces(King(self.on_move)).items())[0]
        if king_pos in self.attacked_fields_by_sides(set(self.sides) - {piece.side}, test_board):
            raise CausesCheck("{move} move causes {side} {name} ({pos}) check delivered by: [{atck}]".format(
                move=move, side=king.side, name=king.name, pos=king_pos,
                atck=', '.join(
                    ["%s: %s" % (position, '%s %s' % (piece.side, piece.name))
                     for position, piece
                     in self.who_can_step_here(king_pos, test_board).items()]
                )
            ))

    def move(self, move: 'StandardMove') -> bool:
        # TODO: Refactor or something, or maybe not
        self.assert_move(move)
        moved_piece = self.board.get_piece(position=move.source)
        if moved_piece.side != self.on_move:
            raise WrongMoveOrder("You are trying to move %s when %s are on move" % (moved_piece.side, self.on_move))
        moved_piece = self.board.remove_piece(position=move.source)
        self.board.put_piece(piece=moved_piece, position=move.destination)
        self.moves_history.append(move)
        self.__half_moves += 1
        if isinstance(moved_piece, Pawn):
            if abs(move.source.rank - move.destination.rank) == 2:
                self.__en_passant = StandardPosition(
                    (move.source.file,
                     int((move.source.rank + move.destination.rank) / 2))
                )
            else:
                self.__en_passant = None
            self.__half_moves_since_pawn_moved = 0
        else:
            if self.__en_passant:
                self.__en_passant = None
            self.__half_moves_since_pawn_moved += 1
        return True

    def standard_moves(self, position: 'StandardPosition', board: StandardBoard = None) -> Set['StandardPosition']:
        if not board:
            board = self.board
        piece = board.get_piece(position)
        if not piece:
            raise NoPiece('Any piece on %s' % position)

        new_positions = set()
        for m_desc in piece.movement.move:
            for vector in self.__transform_vector(m_desc.vector, m_desc.any_direction, piece.side):
                if m_desc.distance is infinity:
                    loop = itertools.count(1)
                else:
                    loop = range(1, m_desc.distance + 1)

                for distance in loop:
                    new_position = StandardPosition(
                        (position[0] + int(vector[0] * distance),
                         position[1] + int(vector[1] * distance))
                    )
                    if not board.validate_position(new_position):
                        break

                    new_piece = board.get_piece(new_position)
                    if new_piece is not None:
                        break
                    new_positions.add(new_position)

        return new_positions

    def special_moves(self, position: 'StandardPosition', board: StandardBoard = None) -> Set['StandardPosition']:
        # TODO: replace for some more convenient solution
        if not board:
            board = self.board
        piece = board.get_piece(position)
        if not piece:
            raise NoPiece('Any piece on %s' % position)

        new_positions = set()
        if isinstance(piece, Pawn):
            new_position = None
            if piece == Pawn(Black) and position.rank == 6:
                new_position = StandardPosition(
                    (position[0],
                     position[1] - 2)
                )
            elif piece == Pawn(White) and position.rank == 1:
                new_position = StandardPosition(
                    (position[0],
                     position[1] + 2)
                )
            if new_position and board.validate_position(new_position):
                new_piece = board.get_piece(new_position)
                if new_piece is None:
                    new_positions.add(new_position)
        return new_positions

    def standard_captures(self, position: 'StandardPosition', board: StandardBoard = None) -> Set['StandardPosition']:
        if not board:
            board = self.board
        piece = board.get_piece(position)
        if not piece:
            raise NoPiece('Any piece on %s' % position)

        new_positions = set()
        for c_desc in piece.movement.capture:
            for vector in self.__transform_vector(c_desc.vector, c_desc.any_direction, piece.side):
                if c_desc.distance is infinity:
                    loop = itertools.count(1)
                else:
                    loop = range(1, c_desc.distance + 1)

                for distance in loop:
                    new_position = StandardPosition(
                        (position[0] + int(vector[0] * distance),
                         position[1] + int(vector[1] * distance))
                    )
                    if not board.validate_position(new_position):
                        break

                    new_piece = board.get_piece(new_position)
                    if not new_piece:
                        continue
                    if new_piece and new_piece.side != piece.side:
                        new_positions.add(new_position)
                        if c_desc.capture_break:
                            break
                    elif new_piece and new_piece.side == piece.side:
                        break

        return new_positions

    def attacked_fields(self, position: 'StandardPosition', board: StandardBoard = None) -> Set['StandardPosition']:
        if not board:
            board = self.board
        piece = board.get_piece(position)
        if not piece:
            raise NoPiece('Any piece on %s' % position)

        new_positions = set()
        for c_desc in piece.movement.capture:
            for vector in self.__transform_vector(c_desc.vector, c_desc.any_direction, piece.side):
                if c_desc.distance is infinity:
                    loop = itertools.count(1)
                else:
                    loop = range(1, c_desc.distance + 1)

                for distance in loop:
                    new_position = StandardPosition(
                        (position[0] + int(vector[0] * distance),
                         position[1] + int(vector[1] * distance))
                    )
                    if not board.validate_position(new_position):
                        break

                    new_piece = board.get_piece(new_position)
                    if not new_piece:
                        new_positions.add(new_position)
                    elif new_piece and new_piece.side != piece.side:
                        new_positions.add(new_position)
                        break
                    elif new_piece and new_piece.side == piece.side:
                        break

        return new_positions

    def attacked_fields_by_sides(self, sides: Set[Type['Side']], board: 'StandardBoard' = None) \
            -> Set['StandardPosition']:
        if not board:
            board = self.board

        return {pos for position, piece in board.pieces.items()
                for pos in self.attacked_fields(position, board)
                for side in sides if piece.side == side}

    def who_can_step_here(self, position: 'StandardPosition', board: 'StandardBoard' = None) \
            -> Dict['StandardPosition', 'Piece']:
        if not board:
            board = self.board

        return {pos: piece for pos, piece in board.pieces.items() if position in self.attacked_fields(pos, board)}

    def all_available_moves(self, side: Type['Side'] = None):
        # Warning! Very inefficient! TODO: Refactor or remove
        if not side:
            side = self.on_move

        moves = set()
        for pos, piece in self.board.pieces.items():
            if piece.side != side:
                continue
            for destination in self.standard_moves(pos) | self.standard_captures(pos) | self.special_moves(pos):
                move = StandardMove(pos, destination)
                try:
                    self.assert_move(move)
                except NotAValidMove:
                    continue
                else:
                    moves.add(move)
        return moves

    @staticmethod
    def __transform_vector(vector: Tuple[int, int], all_directions: bool, side) -> Set[Tuple[int, int]]:
        # TODO: standard interface for resolving all vector combinations and for transforming not-all-directions vector
        # TODO: eg. a pawn, for Whites move forward means incrementing rank value, for Black - decrementing
        if all_directions:
            return {
                (vector[0], vector[1]),
                (vector[1], vector[0]),
                (vector[1], vector[0] * -1),
                (vector[0], vector[1] * -1),
                (vector[0] * -1, vector[1] * -1),
                (vector[1] * -1, vector[0] * -1),
                (vector[1] * -1, vector[0]),
                (vector[0] * -1, vector[1]),
            }

        if side == Black:
            return {(vector[0] * -1, vector[1] * -1)}
        else:
            return {vector}

    def can_i_make_a_move(self) -> bool:
        for pos, piece in self.board.pieces.items():
            if piece and piece.side == self.on_move:
                for moves in [self.standard_moves(pos), self.standard_captures(pos), self.special_moves(pos)]:
                    for dest in moves:
                        try:
                            self.assert_move(StandardMove(pos, dest))
                        except:
                            continue
                        return True
        return False

    def fen(self):
        return str(self)

    def __hash__(self):
        return hash(tuple(self.__moves_history))

    def __str__(self):
        return "{board} {on_move} {castling} {en_passant} {half_since_pawn} {moves}".format(
            board=self.__board.get_fen(),
            on_move=self.on_move.char,
            castling=None,  # TODO: TODO
            en_passant=str(self.__en_passant) if self.__en_passant else "-",  # TODO: implement en_passant
            half_since_pawn=self.__half_moves_since_pawn_moved,
            moves=self.moves,
        )


class KingOfTheHill(Normal):
    @property
    def name(self):
        return "King of The Hill"

    @property
    def game_state(self) -> Optional[Set[Type['Side']]]:
        # find kings position and return winner if king is standing on the hill (d4, e4, d5, e5)
        kings = []
        for side in self.sides:
            king_pos, piece = list(self.board.find_pieces(King(side)).items())[0]
            kings.append((king_pos, piece))

        for king_pos, piece in kings:
            if king_pos.file in (3, 4) and king_pos.rank in (3, 4):
                return {piece.side}

        # else return winner by standard chess rule
        return super(KingOfTheHill, self).game_state


class ThreeCheck(Normal):
    @property
    def name(self):
        return "King of The Hill"

    def __init__(self):
        super().__init__()
        self.checks = {side: 0 for side in self.sides}

    def move(self, move: 'StandardMove'):
        piece = self.board.get_piece(move.source)
        super(ThreeCheck, self).move(move)

        our_side = piece.side
        enemy_side_set = set(self.sides) - {our_side}
        if len(enemy_side_set) != 1:
            raise Exception("Something went wrong")  # TODO
        enemy_side = enemy_side_set.pop()

        enemy_kings_dict = self.board.find_pieces(King(enemy_side))
        if len(enemy_kings_dict) != 1:
            raise Exception("Something went even worse")  # TODO
        enemy_king_position, enemy_king = list(enemy_kings_dict.items())[0]
        if enemy_king_position in self.attacked_fields_by_sides({our_side}):
            self.checks[our_side] += 1

    @property
    def game_state(self):
        # determine winner by who get enough check attacks
        for side, value in self.checks.items():
            if value >= 3:
                return {side}

        # else determine by standard rules
        return super(ThreeCheck, self).game_state

#
# class Chess960(Variant):
#     pass
#
#
# class Crazyhouse(Variant):
#     pass
#
#
# class Horde(Variant):
#     pass
#
#
# class PreChess(Variant):
#     """Could be interesting to implement"""
#     pass
#
#
# class UpsideDown(Variant):
#     pass
#
#
# class Double(Variant):
#     """Could be interesting to implement as well"""
#     pass
#
#
# class Antichess(Variant):
#     """Just because LiChess supports it"""
#     pass
#
#
# class RacingKings(Variant):
#     """Like above"""
#     pass
