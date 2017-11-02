from interface.move import Move


class StandardMove(Move):
    """
    Two Position aggregator with optional pawn promotion information
    """

    @property
    def a(self):
        return self.__a

    @property
    def b(self):
        return self.__b

    @property
    def promotion(self):
        return self.__promotion
