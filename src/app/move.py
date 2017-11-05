from interface.move import Move


class StandardMove(Move):
    """
    Two Position aggregator with optional pawn promotion information
    """

    @property
    def source(self):
        return self._source

    @property
    def destination(self):
        return self._destination

    @property
    def promotion(self):
        return self._promotion
