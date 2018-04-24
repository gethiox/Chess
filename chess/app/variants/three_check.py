from typing import Tuple, Optional, Set, Type, TYPE_CHECKING

from chess.app.pieces import King
from chess.app.variants.classic import Normal

if TYPE_CHECKING:
    from chess.app.move import StandardMove
    from chess.interface.side import Side


class ThreeCheck(Normal):
    @property
    def name(self):
        return "Three Check"

    def __init__(self):
        super().__init__()
        self.checks = {side: 0 for side in self.sides}

    def move(self, move: 'StandardMove'):
        piece = self.board.get_piece(move.source)
        super(ThreeCheck, self).move(move)

        our_side = piece.side
        enemy_side = (set(self.sides) - {our_side}).pop()

        enemy_king_position, _ = self.board.find_pieces(King(enemy_side))[0]
        if enemy_king_position in self.attacked_fields_by_sides({our_side}):
            self.checks[our_side] += 1

    @property
    def game_state(self) -> Tuple[Optional[Set[Type['Side']]], Optional[str]]:
        # determine winner by who get enough check attacks
        for side, value in self.checks.items():
            if value >= 3:
                return {side}, 'three check'

        # else determine by standard rules
        return super(ThreeCheck, self).game_state
