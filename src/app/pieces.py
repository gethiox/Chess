from domain.pieces import Piece, Position, white, black


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
    char = 'n'


class Pawn(Piece):
    name = 'Pawn'
    char = 'p'


def from_str(piece: str, position: Position) -> Piece:
    for real_piece in [King, Queen, Rook, Bishop, Knight, Pawn]:
        if real_piece.char == piece.lower():
            return real_piece(black if piece.islower() else white, position)
