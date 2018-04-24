from typing import Tuple, Optional, Set, Type, TYPE_CHECKING

from chess.app.pieces import King
from chess.app.variants.classic import Normal

if TYPE_CHECKING:
    from chess.interface.side import Side


class KingOfTheHill(Normal):
    @property
    def name(self):
        return "King of The Hill"

    @property
    def game_state(self) -> Tuple[Optional[Set[Type['Side']]], Optional[str]]:
        # find kings position and return winner if king is standing on the hill (d4, e4, d5, e5)
        kings = []
        for side in self.sides:
            king_pos, piece = self.board.find_pieces(King(side))[0]
            kings.append((king_pos, piece))

        for king_pos, piece in kings:
            if king_pos.file in (3, 4) and king_pos.rank in (3, 4):
                return {piece.side}, 'king on the hill'

        # else return winner by standard chess rule
        return super(KingOfTheHill, self).game_state
