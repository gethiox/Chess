#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from copy import deepcopy as copy
from string import ascii_letters, digits, ascii_lowercase

from src.exceptions import *
from src.helpers import color
from src.helpers.args import parse_args
from src.network import Network
from src.game_modes import human_vs_human, human_vs_cpu, cpu_vs_cpu


class Chess:
    def __init__(self, auto_show_board=False, colors=True, symbols=False):
        self.history = {}
        self.history_seq = 0
        self.board = [[None for x in range(8)] for i in range(8)]
        self.on_move = 'w'
        self.castle = 'KQkq'
        self.en_passant = None
        self.half_moves = 0
        self.moves = 1
        self.moves_seq = []

        self.auto_show_board = auto_show_board
        self.colors = colors
        self.symbols = symbols

    def _exec_move(self, pos_a, pos_b, promotion='q', debug=False):
        x1, y1 = self.convert_to_matrix(pos_a)
        x2, y2 = self.convert_to_matrix(pos_b)
        piece = self.board[y1][x1]
        promoted = False

        if not debug:
            valid_moves = self.legal_moves(pos_a)

            if piece is None:
                raise NoPiece('%s is an empty field.' % pos_a)
            elif piece.isupper() and self.on_move != 'w':
                raise WrongMoveOrder('Black on move, not white!')
            elif piece.islower() and self.on_move != 'b':
                raise WrongMoveOrder('White on move, not black!')
            elif pos_b not in valid_moves:
                raise IllegalMove('%s%s: It is not a valid move!\n' % (pos_a, pos_b))
            elif self.am_i_mated() or self.am_i_stalemated():
                if self.on_move == 'w':
                    raise GameOver('Game ended, black won!')
                elif self.on_move == 'w':
                    raise GameOver('Game ended, white won!')

            self.history[self.history_seq] = self._get_backup()

        self.board[y1][x1] = None
        self.board[y2][x2] = piece

        if piece == 'P' and y2 == 7:
            self.board[y2][x2] = promotion.capitalize()
            promoted = True
        elif piece == 'p' and y2 == 0:
            self.board[y2][x2] = promotion.casefold()
            promoted = True

        if piece in 'pP' and pos_b == self.en_passant:
            self.board[y1][x2] = None

        if piece in 'kK':
            if piece == 'K':
                if pos_a == 'e1' and pos_b == 'g1':
                    self.board[0][7] = None
                    self.board[0][5] = 'R'
                elif pos_a == 'e1' and pos_b == 'c1':
                    self.board[0][0] = None
                    self.board[0][3] = 'R'
            elif piece == 'k':
                if pos_a == 'e8' and pos_b == 'g8':
                    self.board[7][7] = None
                    self.board[7][5] = 'r'
                elif pos_a == 'e8' and pos_b == 'c8':
                    self.board[7][0] = None
                    self.board[7][3] = 'r'

        if not debug:
            # postmove operations

            if piece in 'kK' and self.castle is not None:
                if piece.isupper():
                    self.castle = self.castle.replace('K', '')
                    self.castle = self.castle.replace('Q', '')
                elif piece.islower():
                    self.castle = self.castle.replace('k', '')
                    self.castle = self.castle.replace('q', '')
                if not self.castle:
                    self.castle = None

            elif piece in 'rR' and self.castle is not None:
                if piece.isupper():
                    if x1 == 7:
                        self.castle = self.castle.replace('K', '')
                    elif x1 == 0:
                        self.castle = self.castle.replace('Q', '')
                elif piece.islower():
                    if x1 == 7:
                        self.castle = self.castle.replace('k', '')
                    elif x1 == 0:
                        self.castle = self.castle.replace('q', '')
                if not self.castle:
                    self.castle = None

            if piece in 'pP' and abs(y1 - y2) == 2:
                self.en_passant = self.convert_to_algebra(x1, int((y1 + y2) / 2))
            else:
                self.en_passant = None

            if self.on_move == 'w':
                self.on_move = 'b'
            else:
                self.on_move = 'w'
                self.moves += 1

            self.history_seq += 1
            self.history[self.history_seq] = self._get_backup()

            if not promoted:
                self.moves_seq.append(pos_a + pos_b)
            else:
                self.moves_seq.append(pos_a + pos_b + promotion)

            state = self._board_state()

            if self.auto_show_board:
                position = self.get_position()
                self.show_board()
                print(position)

            return state

    def _get_backup(self):
        data = (copy(self.board),
                copy(self.on_move),
                copy(self.castle),
                copy(self.en_passant),
                copy(self.half_moves),
                copy(self.moves),
                copy(self.moves_seq),
                hash(str(self.board)))
        return data

    def _restore_backup(self, backup):
        (self.board,
         self.on_move,
         self.castle,
         self.en_passant,
         self.half_moves,
         self.moves,
         self.moves_seq,
         _) = copy(backup)

    def _clear_board(self):
        self.board = [[None for x in range(8)] for i in range(8)]

    def _avabile_moves(self, pos):
        pos_x, pox_y = self.convert_to_matrix(pos)

        piece = self.board[pox_y][pos_x]
        if piece is None:
            raise NoPiece('No piece at %s' % pos)
        else:
            color = self.read_color(piece)
            piece = piece.casefold()

        moves = []

        # Pawns ###
        if piece == 'p' and color == 'w':
            # test for move one square ahead
            tmp_x, tmp_y = pos_x, pox_y + 1
            if tmp_x in range(8) and tmp_y in range(8):
                if self.board[tmp_y][tmp_x] is None:
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
            # test for move two squares ahead
            tmp_x, tmp_y = pos_x, pox_y + 2
            if tmp_x in range(8) and tmp_y in range(8):
                if pox_y == 1 and self.board[tmp_y][tmp_x] is None:
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
            # tests for capturing enemy pieces
            tmp_x, tmp_y = pos_x + 1, pox_y + 1
            if tmp_x in range(8) and tmp_y in range(8):
                if self.board[tmp_y][tmp_x] is not None and self.read_color(self.board[tmp_y][tmp_x]) != color:
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
            tmp_x, tmp_y = pos_x - 1, pox_y + 1
            if tmp_x in range(8) and tmp_y in range(8):
                if self.board[tmp_y][tmp_x] is not None and self.read_color(self.board[tmp_y][tmp_x]) != color:
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
            # test for en passant possibility
            if self.en_passant and pox_y == 4:
                tmp_x, tmp_y = self.convert_to_matrix(self.en_passant)
                if (pos_x + 1 == tmp_x or pos_x - 1 == tmp_x) and pox_y + 1 == tmp_y:
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))

        elif piece == 'p' and color == 'b':
            tmp_x, tmp_y = pos_x, pox_y - 1
            if tmp_x in range(8) and tmp_y in range(8):
                if self.board[tmp_y][tmp_x] is None:
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
            tmp_x, tmp_y = pos_x, pox_y - 2
            if tmp_x in range(8) and tmp_y in range(8):
                if pox_y == 6 and self.board[tmp_y][tmp_x] is None:
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
            tmp_x, tmp_y = pos_x + 1, pox_y - 1
            if tmp_x in range(8) and tmp_y in range(8):
                if self.board[tmp_y][tmp_x] is not None and self.read_color(self.board[tmp_y][tmp_x]) != color:
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
            tmp_x, tmp_y = pos_x - 1, pox_y - 1
            if tmp_x in range(8) and tmp_y in range(8):
                if self.board[tmp_y][tmp_x] is not None and self.read_color(self.board[tmp_y][tmp_x]) != color:
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
            if self.en_passant and pox_y == 3:
                tmp_x, tmp_y = self.convert_to_matrix(self.en_passant)
                if (pos_x + 1 == tmp_x or pos_x - 1 == tmp_x) and pox_y - 1 == tmp_y:
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))

        # Rook ###
        elif piece == 'r':
            # tests for moving rook in all four directions
            for i in range(1, 8):
                tmp_x, tmp_y = pos_x + i, pox_y
                if tmp_x in range(8) and tmp_y in range(8):
                    if self.board[tmp_y][tmp_x] is None:
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                    elif color != self.read_color(self.board[tmp_y][tmp_x]):
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp_x, tmp_y = pos_x - i, pox_y
                if tmp_x in range(8) and tmp_y in range(8):
                    if self.board[tmp_y][tmp_x] is None:
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                    elif color != self.read_color(self.board[tmp_y][tmp_x]):
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp_x, tmp_y = pos_x, pox_y + i
                if tmp_x in range(8) and tmp_y in range(8):
                    if self.board[tmp_y][tmp_x] is None:
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                    elif color != self.read_color(self.board[tmp_y][tmp_x]):
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp_x, tmp_y = pos_x, pox_y - i
                if tmp_x in range(8) and tmp_y in range(8):
                    if self.board[tmp_y][tmp_x] is None:
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                    elif color != self.read_color(self.board[tmp_y][tmp_x]):
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                        break
                    else:
                        break
                else:
                    break

        # Knight ###
        elif piece == 'n':
            # tests for knight jumps
            tmp_x, tmp_y = pos_x + 2, pox_y - 1
            if tmp_x in range(8) and tmp_y in range(8):
                if self.board[tmp_y][tmp_x] is None:
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                elif color != self.read_color(self.board[tmp_y][tmp_x]):
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
            tmp_x, tmp_y = pos_x + 2, pox_y + 1
            if tmp_x in range(8) and tmp_y in range(8):
                if self.board[tmp_y][tmp_x] is None:
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                elif color != self.read_color(self.board[tmp_y][tmp_x]):
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
            tmp_x, tmp_y = pos_x + 1, pox_y + 2
            if tmp_x in range(8) and tmp_y in range(8):
                if self.board[tmp_y][tmp_x] is None:
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                elif color != self.read_color(self.board[tmp_y][tmp_x]):
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
            tmp_x, tmp_y = pos_x - 1, pox_y + 2
            if tmp_x in range(8) and tmp_y in range(8):
                if self.board[tmp_y][tmp_x] is None:
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                elif color != self.read_color(self.board[tmp_y][tmp_x]):
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
            tmp_x, tmp_y = pos_x - 2, pox_y + 1
            if tmp_x in range(8) and tmp_y in range(8):
                if self.board[tmp_y][tmp_x] is None:
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                elif color != self.read_color(self.board[tmp_y][tmp_x]):
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
            tmp_x, tmp_y = pos_x - 2, pox_y - 1
            if tmp_x in range(8) and tmp_y in range(8):
                if self.board[tmp_y][tmp_x] is None:
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                elif color != self.read_color(self.board[tmp_y][tmp_x]):
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
            tmp_x, tmp_y = pos_x - 1, pox_y - 2
            if tmp_x in range(8) and tmp_y in range(8):
                if self.board[tmp_y][tmp_x] is None:
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                elif color != self.read_color(self.board[tmp_y][tmp_x]):
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
            tmp_x, tmp_y = pos_x + 1, pox_y - 2
            if tmp_x in range(8) and tmp_y in range(8):
                if self.board[tmp_y][tmp_x] is None:
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                elif color != self.read_color(self.board[tmp_y][tmp_x]):
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))

        # Bishop ###
        elif piece == 'b':
            # like a roock, tests for all four directions
            for i in range(1, 8):
                tmp_x, tmp_y = pos_x + i, pox_y + i
                if tmp_x in range(8) and tmp_y in range(8):
                    if self.board[tmp_y][tmp_x] is None:
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                    elif color != self.read_color(self.board[tmp_y][tmp_x]):
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp_x, tmp_y = pos_x + i, pox_y - i
                if tmp_x in range(8) and tmp_y in range(8):
                    if self.board[tmp_y][tmp_x] is None:
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                    elif color != self.read_color(self.board[tmp_y][tmp_x]):
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp_x, tmp_y = pos_x - i, pox_y + i
                if tmp_x in range(8) and tmp_y in range(8):
                    if self.board[tmp_y][tmp_x] is None:
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                    elif color != self.read_color(self.board[tmp_y][tmp_x]):
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp_x, tmp_y = pos_x - i, pox_y - i
                if tmp_x in range(8) and tmp_y in range(8):
                    if self.board[tmp_y][tmp_x] is None:
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                    elif color != self.read_color(self.board[tmp_y][tmp_x]):
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                        break
                    else:
                        break
                else:
                    break

        # Queen ###
        elif piece == 'q':
            # tests in all eight directions
            for i in range(1, 8):
                tmp_x, tmp_y = pos_x + i, pox_y + i
                if tmp_x in range(8) and tmp_y in range(8):
                    if self.board[tmp_y][tmp_x] is None:
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                    elif color != self.read_color(self.board[tmp_y][tmp_x]):
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp_x, tmp_y = pos_x + i, pox_y - i
                if tmp_x in range(8) and tmp_y in range(8):
                    if self.board[tmp_y][tmp_x] is None:
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                    elif color != self.read_color(self.board[tmp_y][tmp_x]):
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp_x, tmp_y = pos_x - i, pox_y + i
                if tmp_x in range(8) and tmp_y in range(8):
                    if self.board[tmp_y][tmp_x] is None:
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                    elif color != self.read_color(self.board[tmp_y][tmp_x]):
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp_x, tmp_y = pos_x - i, pox_y - i
                if tmp_x in range(8) and tmp_y in range(8):
                    if self.board[tmp_y][tmp_x] is None:
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                    elif color != self.read_color(self.board[tmp_y][tmp_x]):
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                        break
                    else:
                        break
                else:
                    break

            for i in range(1, 8):
                tmp_x, tmp_y = pos_x + i, pox_y
                if tmp_x in range(8) and tmp_y in range(8):
                    if self.board[tmp_y][tmp_x] is None:
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                    elif color != self.read_color(self.board[tmp_y][tmp_x]):
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp_x, tmp_y = pos_x - i, pox_y
                if tmp_x in range(8) and tmp_y in range(8):
                    if self.board[tmp_y][tmp_x] is None:
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                    elif color != self.read_color(self.board[tmp_y][tmp_x]):
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp_x, tmp_y = pos_x, pox_y + i
                if tmp_x in range(8) and tmp_y in range(8):
                    if self.board[tmp_y][tmp_x] is None:
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                    elif color != self.read_color(self.board[tmp_y][tmp_x]):
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp_x, tmp_y = pos_x, pox_y - i
                if tmp_x in range(8) and tmp_y in range(8):
                    if self.board[tmp_y][tmp_x] is None:
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                    elif color != self.read_color(self.board[tmp_y][tmp_x]):
                        moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                        break
                    else:
                        break
                else:
                    break

        # King ###
        elif piece == 'k':
            # tests for moving king
            tmp_x, tmp_y = pos_x + 1, pox_y + 1
            if tmp_x in range(8) and tmp_y in range(8):
                if self.board[tmp_y][tmp_x] is None:
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                elif color != self.read_color(self.board[tmp_y][tmp_x]):
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))

            tmp_x, tmp_y = pos_x + 1, pox_y - 1
            if tmp_x in range(8) and tmp_y in range(8):
                if self.board[tmp_y][tmp_x] is None:
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                elif color != self.read_color(self.board[tmp_y][tmp_x]):
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))

            tmp_x, tmp_y = pos_x - 1, pox_y + 1
            if tmp_x in range(8) and tmp_y in range(8):
                if self.board[tmp_y][tmp_x] is None:
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                elif color != self.read_color(self.board[tmp_y][tmp_x]):
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))

            tmp_x, tmp_y = pos_x - 1, pox_y - 1
            if tmp_x in range(8) and tmp_y in range(8):
                if self.board[tmp_y][tmp_x] is None:
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                elif color != self.read_color(self.board[tmp_y][tmp_x]):
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))

            tmp_x, tmp_y = pos_x + 1, pox_y
            if tmp_x in range(8) and tmp_y in range(8):
                if self.board[tmp_y][tmp_x] is None:
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                elif color != self.read_color(self.board[tmp_y][tmp_x]):
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))

            tmp_x, tmp_y = pos_x - 1, pox_y
            if tmp_x in range(8) and tmp_y in range(8):
                if self.board[tmp_y][tmp_x] is None:
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                elif color != self.read_color(self.board[tmp_y][tmp_x]):
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))

            tmp_x, tmp_y = pos_x, pox_y + 1
            if tmp_x in range(8) and tmp_y in range(8):
                if self.board[tmp_y][tmp_x] is None:
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                elif color != self.read_color(self.board[tmp_y][tmp_x]):
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))

            tmp_x, tmp_y = pos_x, pox_y - 1
            if tmp_x in range(8) and tmp_y in range(8):
                if self.board[tmp_y][tmp_x] is None:
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))
                elif color != self.read_color(self.board[tmp_y][tmp_x]):
                    moves.append(self.convert_to_algebra(tmp_x, tmp_y))

            # tests of castling availability
            if self.castle is not None and color == 'w':
                if 'K' in self.castle:
                    if self.board[0][5] is None and self.board[0][6] is None and self.board[0][7] == 'R':
                        moves.append('g1')
                if 'Q' in self.castle:
                    if self.board[0][1] is None and self.board[0][2] is None and self.board[0][3] is None and self.board[0][0] == 'R':
                        moves.append('c1')
            elif self.castle is not None and color == 'b':
                if 'k' in self.castle:
                    if self.board[7][5] is None and self.board[7][6] is None and self.board[7][7] == 'r':
                        moves.append('g8')
                if 'q' in self.castle:
                    if self.board[7][1] is None and self.board[7][2] is None and self.board[7][3] is None and self.board[7][0] == 'r':
                        moves.append('c8')

        return moves

    def _attacked_fields(self):
        validation = []

        y = 0
        for row in self.board:
            x = 0
            for piece in row:
                if piece is not None and (piece.islower() if self.on_move == 'w' else piece.isupper()):
                    validation.extend(self._avabile_moves(self.convert_to_algebra(x, y)))
                x += 1
            y += 1

        validation = list(set(validation))
        return validation

    def _board_state(self):
        checked, mated, stalemated, pated = (self.am_i_checked(),
                                             self.am_i_mated(),
                                             self.am_i_stalemated(),
                                             self.am_i_pated())

        game_over = (mated or stalemated or pated)

        return game_over, checked, mated, stalemated, pated

    def legal_moves(self, pos):
        moves = self._avabile_moves(pos)
        real_moves = []
        checked = self.am_i_checked()

        backup = self._get_backup()
        for move in moves:
            self._exec_move(pos, move, debug=True)
            if not self.am_i_checked():
                real_moves.append(move)
            self._restore_backup(backup)

        x, y = self.convert_to_matrix(pos)

        if self.board[y][x] == 'K' and self.castle is not None and x == 4 and y == 0:
            if ('f1' not in real_moves and 'K' in self.castle) or checked:
                if 'g1' in real_moves:
                    real_moves.remove('g1')
            if ('d1' not in real_moves and 'Q' in self.castle) or checked:
                if 'c1' in real_moves:
                    real_moves.remove('c1')
        elif self.board[y][x] == 'k' and self.castle is not None and x == 4 and y == 7:
            if ('f8' not in real_moves and 'k' in self.castle) or checked:
                if 'g8' in real_moves:
                    real_moves.remove('g8')
            if ('d8' not in real_moves and 'q' in self.castle) or checked:
                if 'c8' in real_moves:
                    real_moves.remove('c8')

        return real_moves

    def new_game(self, type='standard'):
        if type == 'standard':
            self._clear_board()

            self.board[0][0], self.board[0][7] = 'R', 'R'
            self.board[0][1], self.board[0][6] = 'N', 'N'
            self.board[0][2], self.board[0][5] = 'B', 'B'
            self.board[0][3], self.board[0][4] = 'Q', 'K'

            for i in range(8):
                self.board[1][i] = 'P'

            for i in range(8):
                self.board[6][i] = 'p'

            self.board[7][0], self.board[7][7] = 'r', 'r'
            self.board[7][1], self.board[7][6] = 'n', 'n'
            self.board[7][2], self.board[7][5] = 'b', 'b'
            self.board[7][3], self.board[7][4] = 'q', 'k'

            self.on_move = 'w'
            self.castle = 'KQkq'
            self.en_passant = None
            self.half_moves = 0
            self.moves = 1

            self.history = {}
            self.history_seq = 0
            self.moves_seq = []

        if self.auto_show_board:
            position = self.get_position()
            self.show_board()
            print(position)

    def move(self, move, move2=None, promotion='q', debug=False):
        if isinstance(move, str) and isinstance(move2, str) and len(move) == len(move2) == 2:
            return self._exec_move(move, move2, promotion=promotion, debug=debug)
        elif isinstance(move, str) and len(move) == 4:
            return self._exec_move(move[0:2], move[2:4], promotion=promotion, debug=debug)
        elif isinstance(move, str) and len(move) == 5:
            return self._exec_move(move[0:2], move[2:4], promotion=move[4], debug=debug)
        else:
            raise TypeError('Wrong move syntax')

    def undo(self, moves=1):
        try:
            self.board = copy(self.history[self.history_seq - moves][0])
            self.on_move = copy(self.history[self.history_seq - moves][1])
            self.castle = copy(self.history[self.history_seq - moves][2])
            self.en_passant = copy(self.history[self.history_seq - moves][3])
            self.half_moves = copy(self.history[self.history_seq - moves][4])
            self.moves = copy(self.history[self.history_seq - moves][5])
            self.moves_seq = copy(self.history[self.history_seq - moves][6])

            print('undo %s moves!' % moves)
            if self.auto_show_board:
                self.show_board()
            self.history_seq -= moves
        except KeyError:
            print('operation not in range, max available moves: %d' % len(self.history))
        return self._board_state()

    def redo(self, moves=1):
        try:
            self.board = copy(self.history[self.history_seq + moves][0])
            self.on_move = copy(self.history[self.history_seq + moves][1])
            self.castle = copy(self.history[self.history_seq + moves][2])
            self.en_passant = copy(self.history[self.history_seq + moves][3])
            self.half_moves = copy(self.history[self.history_seq + moves][4])
            self.moves = copy(self.history[self.history_seq + moves][5])
            self.moves_seq = copy(self.history[self.history_seq + moves][6])

            print('redo %s moves!' % moves)
            if self.auto_show_board:
                self.show_board()
            self.history_seq += moves
        except KeyError:
            print('operation not in range, max available moves: %d' % len(self.history))
        else:
            return self._board_state()

    def show_board(self, compact=False, flipped=False, description=True):
        if flipped:
            board = []
            for row in self.board:
                board.append(reversed(row))
        else:
            board = reversed(self.board)

        board_string = ''

        row_count = 1
        for row in board:
            if not compact:
                board_string += ' +---+---+---+---+---+---+---+---+ \n'
            string = ' ' if compact else ' | '
            for piece in row:
                if piece is None:
                    string += '.' if compact else ' '
                elif piece == '+':
                    string += color.bold(color.yellow(piece)) if self.colors else piece
                elif self.symbols:
                    string += self.chess_symbol(piece)
                elif self.colors:
                    string += color.bold(color.green(piece)) if piece.isupper() else color.bold(color.red(piece))
                else:
                    string += piece
                string += ' ' if compact else ' | '

            if description and not flipped:
                string += str(9 - row_count)
            elif description and flipped:
                string += str(row_count)

            board_string += string + '\n'
            row_count += 1
        if not compact:
            board_string += ' +---+---+---+---+---+---+---+---+ \n'
            if description and not flipped:
                board_string += '   a   b   c   d   e   f   g   h   \n'
            elif description and flipped:
                board_string += '   h   g   f   e   d   c   b   a   \n'
        elif compact and description:
            if not flipped:
                board_string += ' a b c d e f g h \n'
            else:
                board_string += ' h g f e d c b a \n'

        print(board_string)

    def show_legal_moves(self, pos, compact=False):
        v1, v2 = self.convert_to_matrix(pos)
        if self.read_color(self.board[v2][v1]) != self.on_move:
            if self.on_move == 'w':
                print('Whine on move! You can verify only white pieces now.')
            elif self.on_move == 'b':
                print('Black on move! You can verify only black pieces now.')
        else:
            moves = self.legal_moves(pos)

            if moves is None:
                print('Any piece on %s field!' % pos)
            else:
                backup = copy(self.board)
                for move in moves:
                    x, y = self.convert_to_matrix(move)
                    self.board[y][x] = '+'

                self.show_board(compact=compact)
                self.board = backup

    def get_moves_seq(self):
        return ' '.join(self.moves_seq)

    def get_position(self):
        fenstring = ''
        empty_field = 0
        row_count = 0
        for row in reversed(self.board):
            for piece in row:
                if piece is not None:
                    if empty_field > 0:
                        fenstring += str(empty_field)
                        empty_field = 0
                    fenstring += piece
                else:
                    empty_field += 1
            if empty_field > 0:
                fenstring += str(empty_field)
                empty_field = 0
            if row_count < 7:
                fenstring += '/'
            row_count += 1

        fenstring += ' %s' % self.on_move

        if self.castle is not None:
            fenstring += ' %s' % self.castle
        else:
            fenstring += ' -'

        if self.en_passant is not None:
            fenstring += ' %s' % self.en_passant
        else:
            fenstring += ' -'

        fenstring += ' %s' % str(self.moves)
        fenstring += ' %s' % str(self.half_moves)

        return fenstring

    def set_position(self, fenstring, display=False):
        """
        Fen documentation:
        http://www.thechessdrum.net/PGN_Reference.txt
        """

        if not isinstance(fenstring, str):
            raise TypeError('fenstring must be a string!')

        fenstring = fenstring.replace(u'\u200b', '')
        fendata = fenstring.split(' ')
        fenboard = fendata[0].split('/')

        if len(fenboard) != 8:
            raise WrongBoardSize('Missing/too_much rows of pieces in fenstring!')

        dumped = [[None for x in range(8)] for i in range(8)]
        b_kings, w_kings = 0, 0
        x, y = 0, 0
        for row in reversed(fenboard):
            row_pieces = 0
            if len(row) > 8:
                raise WrongBoardSize('too_much pieces in one row of fenstring!')
            for piece in row:
                if piece not in digits:
                    dumped[x][y] = piece
                    row_pieces += 1
                    if piece == 'K':
                        w_kings += 1
                    elif piece == 'k':
                        b_kings += 1
                    y += 1
                else:
                    for i in range(int(piece)):
                        dumped[x][y] = None
                        row_pieces += 1
                        y += 1
            if row_pieces != 8:
                print(row_pieces)
                raise WrongBoardSize('Missing/Too many pieces in one row of fenstring!')
            y = 0
            x += 1

        if w_kings != 1 or b_kings != 1:
            raise KingsCount('Missing/Too many Kings on the board!')

        self.board = dumped
        if len(fendata) == 6:
            self.on_move = fendata[1]
            if fendata[2] != '-':
                self.castle = fendata[2]
            else:
                self.castle = None
            if fendata[3] != '-':
                self.en_passant = fendata[3]
            else:
                self.castle = None
            self.half_moves = int(fendata[5])
            self.moves = int(fendata[4])

        if display:
            self.show_board()

        return True

    def am_i_checked(self):
        king_pos = None

        y = 0
        for row in self.board:
            x = 0
            for piece in row:
                if piece == ('K' if self.on_move == 'w' else 'k'):
                    king_pos = self.convert_to_algebra(x, y)
                x += 1
            y += 1

        if king_pos is None:
            raise IOError('What the fuck, where is my king?!?!')
        if king_pos in self._attacked_fields():
            return True
        else:
            return False

    def am_i_stalemated(self):
        all_avabile_moves = []
        board = copy(self.board)

        y = 0
        for row in board:
            x = 0
            for piece in row:
                if piece is not None and (piece.isupper() if self.on_move == 'w' else piece.islower()):
                    all_avabile_moves.extend(self.legal_moves(self.convert_to_algebra(x, y)))
                x += 1
            y += 1

        all_avabile_moves = list(set(all_avabile_moves))

        if not all_avabile_moves and not self.am_i_checked():
            return True
        else:
            return False

    def am_i_mated(self):
        all_avabile_moves = []
        board = copy(self.board)

        y = 0
        for row in board:
            x = 0
            for piece in row:
                if piece is not None and (piece.isupper() if self.on_move == 'w' else piece.islower()):
                    all_avabile_moves.extend(self.legal_moves(self.convert_to_algebra(x, y)))
                x += 1
            y += 1

        all_avabile_moves = list(set(all_avabile_moves))

        if not all_avabile_moves and self.am_i_checked():
            return True
        else:
            return False

    def am_i_pated(self):
        hash_list = []
        for i in range(self.history_seq):
            hash_list.append(self.history[i][7])

        for i in hash_list:
            if hash_list.count(i) >= 3:
                return True
        return False

    @staticmethod
    def chess_symbol(piece):
        if piece == 'K':
            return '\u2654'
        elif piece == 'Q':
            return '\u2655'
        elif piece == 'R':
            return '\u2656'
        elif piece == 'B':
            return '\u2657'
        elif piece == 'N':
            return '\u2658'
        elif piece == 'P':
            return '\u2659'

        elif piece == 'k':
            return '\u265A'
        elif piece == 'q':
            return '\u265B'
        elif piece == 'r':
            return '\u265C'
        elif piece == 'b':
            return '\u265D'
        elif piece == 'n':
            return '\u265E'
        elif piece == 'p':
            return '\u265F'

    @staticmethod
    def read_color(piece_code):
        if piece_code is None:
            return None
        elif isinstance(piece_code, str):
            if piece_code.isupper():
                return 'w'
            else:
                return 'b'

    @staticmethod
    def convert_to_matrix(string):
        if not isinstance(string, str):
            raise TypeError('you need to select position as text only!')
        if len(string) != 2:
            raise ValueError('wrong value! insert two chars for describe position on board. (eg. "a2")')
        if string[0] not in ascii_letters:
            raise ValueError('first letter need to be a char!')
        if string[1] not in digits:
            raise ValueError('second letter need to be a digit')

        a_in, b_in = string[0], string[1]

        a_out = ascii_lowercase.index(a_in.casefold())
        if not 0 <= a_out <= 7:
            raise ValueError('rank out of range!')

        b_out = int(b_in) - 1
        if not 0 <= b_out <= 7:
            raise ValueError('file out of range!')

        return a_out, b_out

    @staticmethod
    def convert_to_algebra(v1, v2):
        if not isinstance(v1, int) or not isinstance(v2, int):
            raise TypeError('values need to be an int!')
        if not 0 <= v1 <= 7:
            raise ValueError('file out of range!')
        if not 0 <= v2 <= 7:
            raise ValueError('rank out of range!')

        return ascii_lowercase[v1] + str(v2 + 1)


if __name__ == '__main__':
    with open('src/helpers/banner') as banner:
        print(banner.read())

    args = parse_args()
    if args.auto:
        cpu_vs_cpu(Chess, engine_binary_path=args.stock)
    elif args.join:
        client = Network(Chess)
        client.join(args.join, args.port)
    elif args.host:
        server = Network(Chess)
        server.host(args.host, args.port)
    elif args.human:
        human_vs_cpu(Chess, engine_binary_path=args.stock)
    else:
        human_vs_human(Chess, engine_binary_path=args.stock)




