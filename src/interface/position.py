from abc import ABCMeta, abstractmethod


class Position(metaclass=ABCMeta):
    def __repr__(self):
        return "<Position>"

    @abstractmethod
    def __str__(self):
        """Should be implemented for converting position to string purpose if possible, eg. 'e4'"""
        pass

    @abstractmethod
    def __iter__(self):
        """Should be implemented for converting to sequence where first value is a X coordinate, second Y etc."""
        pass

    @abstractmethod
    def __getitem__(self, item):
        """Should be implemented for index access purpose (Position[index]). 0 for X, 1 for Y, 2 for Z etc."""
        pass

    @abstractmethod
    def __eq__(self, other):
        """Implement for finding same position in sequence"""
        pass
