from src.interface.side import Side


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
