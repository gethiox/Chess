from abc import ABCMeta, abstractmethod


class Side(metaclass=ABCMeta):
    @property
    @abstractmethod
    def name(self) -> str:
        """return defined side name"""
        pass

    @property
    @abstractmethod
    def char(self) -> str:
        """return defined one-char side name"""
        pass

    @property
    @abstractmethod
    def capitalize(self) -> bool:
        """
        Return True if Piece char representation should be capitalized
        Should be implemented only for FEN boards representation purpose
        """
        pass

    def __repr__(self):
        return "<%s Side>" % self.name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, type(self))
