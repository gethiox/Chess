#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import socket
import subprocess
from copy import deepcopy as copy
from string import ascii_letters, digits, ascii_lowercase
from time import sleep

from src.helpers import color
from src.exceptions import *


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
                raise WrongMoveOrder('Black on move you retarted motherfucker!, not white!')
            elif piece.islower() and self.on_move != 'b':
                raise WrongMoveOrder('White on move you retarted idiot!, not black!')
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

            if self.auto_show_board:
                self.show_board()
                print(self.get_position())

            return self._board_state()

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
        a1, a2 = self.convert_to_matrix(pos)

        piece = self.board[a2][a1]
        if piece is None:
            raise NoPiece('No piece at %s' % pos)
        color = self.read_color(piece)

        moves = []

        # Pawns ###
        if piece.casefold() == 'p' and color == 'w':
            tmp1, tmp2 = a1, a2 + 1
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
            tmp1, tmp2 = a1, a2 + 2
            if tmp1 in range(8) and tmp2 in range(8):
                if a2 == 1 and self.board[tmp2][tmp1] is None:
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
            tmp1, tmp2 = a1 + 1, a2 + 1
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is not None and self.read_color(self.board[tmp2][tmp1]) != color:
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
            tmp1, tmp2 = a1 - 1, a2 + 1
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is not None and self.read_color(self.board[tmp2][tmp1]) != color:
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
            if self.en_passant and a2 == 4:
                tmp1, tmp2 = self.convert_to_matrix(self.en_passant)
                if (a1 + 1 == tmp1 or a1 - 1 == tmp1) and a2 + 1 == tmp2:
                    moves.append(self.convert_to_algebra(tmp1, tmp2))

        elif piece.casefold() == 'p' and color == 'b':
            tmp1, tmp2 = a1, a2 - 1
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
            tmp1, tmp2 = a1, a2 - 2
            if tmp1 in range(8) and tmp2 in range(8):
                if a2 == 6 and self.board[tmp2][tmp1] is None:
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
            tmp1, tmp2 = a1 + 1, a2 - 1
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is not None and self.read_color(self.board[tmp2][tmp1]) != color:
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
            tmp1, tmp2 = a1 - 1, a2 - 1
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is not None and self.read_color(self.board[tmp2][tmp1]) != color:
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
            if self.en_passant and a2 == 3:
                tmp1, tmp2 = self.convert_to_matrix(self.en_passant)
                if (a1 + 1 == tmp1 or a1 - 1 == tmp1) and a2 - 1 == tmp2:
                    moves.append(self.convert_to_algebra(tmp1, tmp2))

        # Rook ###
        elif piece.casefold() == 'r':
            for i in range(1, 8):
                tmp1, tmp2 = a1 + i, a2
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp1, tmp2 = a1 - i, a2
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp1, tmp2 = a1, a2 + i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp1, tmp2 = a1, a2 - i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break

        # Knight ###
        elif piece.casefold() == 'n':
            tmp1, tmp2 = a1 + 2, a2 - 1
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
                elif color != self.read_color(self.board[tmp2][tmp1]):
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
            tmp1, tmp2 = a1 + 2, a2 + 1
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
                elif color != self.read_color(self.board[tmp2][tmp1]):
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
            tmp1, tmp2 = a1 + 1, a2 + 2
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
                elif color != self.read_color(self.board[tmp2][tmp1]):
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
            tmp1, tmp2 = a1 - 1, a2 + 2
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
                elif color != self.read_color(self.board[tmp2][tmp1]):
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
            tmp1, tmp2 = a1 - 2, a2 + 1
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
                elif color != self.read_color(self.board[tmp2][tmp1]):
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
            tmp1, tmp2 = a1 - 2, a2 - 1
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
                elif color != self.read_color(self.board[tmp2][tmp1]):
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
            tmp1, tmp2 = a1 - 1, a2 - 2
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
                elif color != self.read_color(self.board[tmp2][tmp1]):
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
            tmp1, tmp2 = a1 + 1, a2 - 2
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
                elif color != self.read_color(self.board[tmp2][tmp1]):
                    moves.append(self.convert_to_algebra(tmp1, tmp2))

        # Bishop ###
        elif piece.casefold() == 'b':
            for i in range(1, 8):
                tmp1, tmp2 = a1 + i, a2 + i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp1, tmp2 = a1 + i, a2 - i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp1, tmp2 = a1 - i, a2 + i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp1, tmp2 = a1 - i, a2 - i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break

        # Queen ###
        elif piece.casefold() == 'q':
            for i in range(1, 8):
                tmp1, tmp2 = a1 + i, a2 + i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp1, tmp2 = a1 + i, a2 - i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp1, tmp2 = a1 - i, a2 + i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp1, tmp2 = a1 - i, a2 - i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break

            for i in range(1, 8):
                tmp1, tmp2 = a1 + i, a2
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp1, tmp2 = a1 - i, a2
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp1, tmp2 = a1, a2 + i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                tmp1, tmp2 = a1, a2 - i
                if tmp1 in range(8) and tmp2 in range(8):
                    if self.board[tmp2][tmp1] is None:
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                    elif color != self.read_color(self.board[tmp2][tmp1]):
                        moves.append(self.convert_to_algebra(tmp1, tmp2))
                        break
                    else:
                        break
                else:
                    break

        # King ###
        elif piece.casefold() == 'k':
            tmp1, tmp2 = a1 + 1, a2 + 1
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
                elif color != self.read_color(self.board[tmp2][tmp1]):
                    moves.append(self.convert_to_algebra(tmp1, tmp2))

            tmp1, tmp2 = a1 + 1, a2 - 1
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
                elif color != self.read_color(self.board[tmp2][tmp1]):
                    moves.append(self.convert_to_algebra(tmp1, tmp2))

            tmp1, tmp2 = a1 - 1, a2 + 1
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
                elif color != self.read_color(self.board[tmp2][tmp1]):
                    moves.append(self.convert_to_algebra(tmp1, tmp2))

            tmp1, tmp2 = a1 - 1, a2 - 1
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
                elif color != self.read_color(self.board[tmp2][tmp1]):
                    moves.append(self.convert_to_algebra(tmp1, tmp2))

            tmp1, tmp2 = a1 + 1, a2
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
                elif color != self.read_color(self.board[tmp2][tmp1]):
                    moves.append(self.convert_to_algebra(tmp1, tmp2))

            tmp1, tmp2 = a1 - 1, a2
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
                elif color != self.read_color(self.board[tmp2][tmp1]):
                    moves.append(self.convert_to_algebra(tmp1, tmp2))

            tmp1, tmp2 = a1, a2 + 1
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
                elif color != self.read_color(self.board[tmp2][tmp1]):
                    moves.append(self.convert_to_algebra(tmp1, tmp2))

            tmp1, tmp2 = a1, a2 - 1
            if tmp1 in range(8) and tmp2 in range(8):
                if self.board[tmp2][tmp1] is None:
                    moves.append(self.convert_to_algebra(tmp1, tmp2))
                elif color != self.read_color(self.board[tmp2][tmp1]):
                    moves.append(self.convert_to_algebra(tmp1, tmp2))

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

        backup = self._get_backup()
        for move in moves:
            self._exec_move(pos, move, debug=True)
            if not self.am_i_checked():
                real_moves.append(move)
            self._restore_backup(backup)

        x, y = self.convert_to_matrix(pos)
        if self.board[y][x] == 'K' and self.castle is not None and x == 4 and y == 0:
            if 'f1' not in real_moves and 'K' in self.castle:
                if 'g1' in real_moves:
                    real_moves.remove('g1')
            if 'd1' not in real_moves and 'Q' in self.castle:
                if 'c1' in real_moves:
                    real_moves.remove('c1')
        elif self.board[y][x] == 'k' and self.castle is not None and x == 4 and y == 7:
            if 'f8' not in real_moves and 'k' in self.castle:
                if 'g8' in real_moves:
                    real_moves.remove('g8')
            if 'd8' not in real_moves and 'q' in self.castle:
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
            self.show_board()

    def move(self, move, promotion='q', debug=False):
        if isinstance(move, str) and len(move) == 4:
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

    def show_board(self, compact=False, flipped=False):
        if flipped:
            board = self.board
        else:
            board = reversed(self.board)

        if not compact:
            for row in board:
                print(' +---+---+---+---+---+---+---+---+ ')
                string = ' | '
                for piece in row:
                    if piece is None:
                        string += ' '
                    elif piece == '+':
                        string += color.yellow(piece) if self.colors else piece
                    elif self.symbols:
                        string += self.chess_symbol(piece)
                    elif self.colors:
                        string += color.green(piece) if piece.isupper() else color.red(piece)
                    else:
                        string += piece
                    string += ' | '
                print(string)
            print(' +---+---+---+---+---+---+---+---+ ')
            print()

        else:
            for row in board:
                string = ' '
                for piece in row:
                    if piece is None:
                        string += '.'
                    elif piece == '+':
                        string += color.yellow(piece) if self.colors else piece
                    elif self.symbols:
                        string += self.chess_symbol(piece)
                    elif self.colors:
                        string += color.green(piece) if piece.isupper() else color.red(piece)
                    else:
                        string += piece
                    string += ' '
                print(string)
            print()

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
        # Fen documentation http://www.thechessdrum.net/PGN_Reference.txt
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
    def read_piece(piece_code):
        if piece_code in 'pP':
            return 'pawn'
        elif piece_code in 'rR':
            return 'rook'
        elif piece_code in 'nN':
            return 'knight'
        elif piece_code in 'bB':
            return 'bishop'
        elif piece_code in 'qQ':
            return 'queen'
        elif piece_code in 'kK':
            return 'king'

    @staticmethod
    def read_color(piece_code):
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


class Engine:
    def __init__(self, engine_binary_path='./src/helpers/stockfish', ponder=False):
        self.path = engine_binary_path
        self.process = None
        self.playing_color = None
        self.logic_thread = None
        self.sigterm = False
        self.pondering = False
        self.ponder = ponder

    def _read(self):
        line = self.process.stdout.readline().decode()
        if '\n' in line:
            line = line.replace('\n', '')
        return line

    def _write(self, string):
        if '\n' not in string:
            string += '\n'
        self.process.stdin.write(string.encode())
        self.process.stdin.flush()

    def run_engine(self):
        args = [self.path]
        self.process = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        self._write('setoption name Threads value 4')
        self._write('setoption name Hash value 256')
        self._write('setoption name Ponder value true')
        self._write('setoption name MultiPV value 2')
        self._write('ucinewgame')

    def start_ponder(self):
        if not self.pondering:
            self._write('go ponder')
            self.pondering = True

    def stop_ponder(self):
        if self.pondering:
            self._write('stop')
            output = self._read()
            while 'bestmove' not in output:
                output = self._read()
            self.pondering = False

    def bestmove(self, fenstring=None, moves_seq=None):
        if fenstring is not None:
            if self.ponder:
                self.stop_ponder()
            self._write('position fen %s' % fenstring)
            self._write('go wtime 5000 btime 5000')
            output = self._read()
            while 'bestmove' not in output:
                output = self._read()
            bestmove = output.split()[1]
            if self.ponder:
                self.start_ponder()
        elif moves_seq is not None:
            if self.ponder:
                self.stop_ponder()
            if len(moves_seq) > 0:
                self._write('position startpos moves %s' % moves_seq)
            else:
                self._write('position startpos')
            self._write('go wtime 50000 btime 5000')
            output = self._read()
            while 'bestmove' not in output:
                output = self._read()
            bestmove = output.split()[1]
            if self.ponder:
                self.start_ponder()
        else:
            raise ValueError

        return bestmove


class Network:
    def __init__(self, game):
        self.cnx = socket.socket()
        self.game = game
        self.socket = None

    @staticmethod
    def handle_client(client_socket):
        request = client_socket.recv(1024)

        print(request.decode())

        client_socket.close()

    def host(self, host='127.0.0.1', port=5678):
        self.cnx.bind((host, port))
        self.cnx.listen(1)
        while True:
            connection, addr = self.cnx.accept()
            print('nawiązano połączenie z %s!' % addr[0])
            while True:
                data = connection.recv(4096)
                if not data:
                    print('nodata')
                    break
                if 'kurwa' in data.decode():
                    connection.send('404 ERROR: TY WULGARNY KUTASIE!'.encode())
                else:
                    connection.send('200 OK: dane ok ziomek.'.encode())
                    print(data.decode())
                if data.decode() == 'exit':
                    break
            connection.close()
            print('zakończono połączenie z %s!' % addr[0])
        self.cnx.close()

    def join(self, host='127.0.0.1', port=5678):
        self.cnx.connect((host, port))
        while True:
            data = input()
            self.cnx.send(data.encode())
            response = self.cnx.recv(4096)
            print(response.decode())
            if data == 'exit':
                break
        self.cnx.close()

    def move(self, move):
        if self.socket is not None:
            self.game.move(move)
            self.cnx.send(move.encode())

        else:
            raise Exception('No active connection')


def parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--help', action='help', help='Show Help')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-n', '--normal', dest='human', action='store_true',
                       help='Hunam vs Computer (chess engine required)')
    group.add_argument('-a', '--auto', dest='auto', action='store_true',
                       help='Computer vs Computer (chess engine required)')

    group.add_argument('-h', '--host', dest='host', metavar='<ip>', default=None,
                       help='Host a network game')
    group.add_argument('-j', '--join', dest='join', metavar='<ip>', default=None,
                       help='Join a network game')

    parser.add_argument('-p', '--port', dest='port', metavar='<port>', type=int, default=5678,
                        help='Destination Port')
    parser.add_argument('-s', '--stock', dest='stock', metavar='./stockfish', type=str, default='./src/helpers/stockfish',
                        help='Path to the Stockfish binary')

    args = parser.parse_args()
    return args


def human_vs_human(engine_binary_path):
    game = Chess(auto_show_board=True)
    game.new_game()

    while True:
        while True:
            try:
                status = game.move(input('[Białe] Podaj ruch: '))
            except KeyboardInterrupt:
                print()
                exit(0)
            except:
                print('nieprawidłowe posunięcie')
                continue
            else:
                break

        if status[0]:
            if game.on_move == 'w':
                if status[2]:
                    print('game over, black won')
                if status[3]:
                    print('stalemate! no legal moves for white!')
                if status[4]:
                    print('stalemate! three position repetition by white!')
            elif game.on_move == 'b':
                if status[2]:
                    print('game over, white won')
                if status[3]:
                    print('stalemate! no legal moves for black!')
                if status[4]:
                    print('stalemate! three position repetition by black!')
            sleep(2)
            break

        while True:
            try:
                status = game.move(input('[czarne] Podaj ruch: '))
            except KeyboardInterrupt:
                print()
                exit(0)
            except:
                print('nieprawidłowe posunięcie')
                continue
            else:
                break

        if status[0]:
            if game.on_move == 'w':
                if status[2]:
                    print('game over, black won')
                if status[3]:
                    print('stalemate! no legal moves for white!')
                if status[4]:
                    print('stalemate! three position repetition by white!')
            elif game.on_move == 'b':
                if status[2]:
                    print('game over, white won')
                if status[3]:
                    print('stalemate! no legal moves for black!')
                if status[4]:
                    print('stalemate! three position repetition by black!')
            sleep(2)
            break


def human_vs_cpu(engine_binary_path):
    game = Chess(auto_show_board=True)
    e1 = Engine(ponder=True, engine_binary_path=engine_binary_path)
    e1.run_engine()
    game.new_game()

    while True:
        while True:
            try:
                status = game.move(input('Podaj ruch: '))
            except KeyboardInterrupt:
                print()
                exit(0)
            except:
                print('nieprawidłowe posunięcie')
                continue
            else:
                break

        if status[0]:
            if game.on_move == 'w':
                if status[2]:
                    print('game over, black won')
                if status[3]:
                    print('stalemate! no legal moves for white!')
                if status[4]:
                    print('stalemate! three position repetition by white!')
            elif game.on_move == 'b':
                if status[2]:
                    print('game over, white won')
                if status[3]:
                    print('stalemate! no legal moves for black!')
                if status[4]:
                    print('stalemate! three position repetition by black!')
            sleep(2)
            break
        status = game.move(e1.bestmove(moves_seq=game.get_moves_seq()))
        if status[0]:
            if game.on_move == 'w':
                if status[2]:
                    print('game over, black won')
                if status[3]:
                    print('stalemate! no legal moves for white!')
                if status[4]:
                    print('stalemate! three position repetition by white!')
            elif game.on_move == 'b':
                if status[2]:
                    print('game over, white won')
                if status[3]:
                    print('stalemate! no legal moves for black!')
                if status[4]:
                    print('stalemate! three position repetition by black!')
            sleep(2)
            break


def cpu_vs_cpu(engine_binary_path):
    game = Chess(auto_show_board=True)
    e1 = Engine(ponder=True, engine_binary_path=engine_binary_path)
    e1.run_engine()
    e2 = Engine(ponder=False, engine_binary_path=engine_binary_path)
    e2.run_engine()
    game.new_game()

    while True:
        for i in range(300):
            status = game.move(e1.bestmove(moves_seq=game.get_moves_seq()))
            if status[0]:
                if game.on_move == 'w':
                    if status[2]:
                        print('game over, black won')
                    if status[3]:
                        print('stalemate! no legal moves for white!')
                    if status[4]:
                        print('stalemate! three position repetition by white!')
                elif game.on_move == 'b':
                    if status[2]:
                        print('game over, white won')
                    if status[3]:
                        print('stalemate! no legal moves for black!')
                    if status[4]:
                        print('stalemate! three position repetition by black!')
                sleep(2)
                break
            status = game.move(e2.bestmove(moves_seq=game.get_moves_seq()))
            if status[0]:
                if game.on_move == 'w':
                    if status[2]:
                        print('game over, black won')
                    if status[3]:
                        print('stalemate! no legal moves for white!')
                    if status[4]:
                        print('stalemate! three position repetition by white!')
                elif game.on_move == 'b':
                    if status[2]:
                        print('game over, white won')
                    if status[3]:
                        print('stalemate! no legal moves for black!')
                    if status[4]:
                        print('stalemate! three position repetition by black!')
                sleep(2)
                break
        game.new_game()


if __name__ == '__main__':
    args = parse_args()
    if args.auto:
        cpu_vs_cpu(engine_binary_path=args.stock)
    elif args.join:
        client = Network()
        client.join(args.join, args.port)
    elif args.host:
        server = Network()
        server.host(args.host, args.port)
    elif args.human:
        human_vs_cpu(engine_binary_path=args.stock)
    else:
        human_vs_human(engine_binary_path=args.stock)




