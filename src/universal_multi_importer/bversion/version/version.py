from __future__ import annotations
from typing import Union
import math
from decimal import Decimal, getcontext, ROUND_HALF_UP


class Version:
    """
    This class allow basic representation of blender version as tuple of 3 ints.
    you can easily compare versions together
    """

    def __init__(self, version: Union[tuple[int, int, int], str, float]):
        self._version: tuple[int, int, int]
        if isinstance(version, float):
            main, _ = str(version).split(".")
            sec = Decimal(str(version)) - Decimal(main)
            sec = sec * Decimal("10")
            sec, third = str(sec.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)).split(".")
            third = int(third)
            main = int(main)
            sec = int(sec)
            third = int(third)

            self._version = (main, sec, third)

        elif isinstance(version, tuple) and len(version) == 3:
            self._version = version

        elif isinstance(version, str) and len(version) == 0:
            self._version = (0, 0, 0)

        elif isinstance(version, str):
            version_split = version.split(".")
            if not len(version_split):
                raise ValueError

            main, sec, third = [0, 0, 0]
            if len(version_split) == 3:
                main, sec, third = version_split
            elif len(version_split) == 2:
                main, sec = version_split
            elif len(version_split) == 1:
                main = version_split[0]

            self._version = (int(main), int(sec), int(third))

        else:
            self._version = (0, 0, 0)

    @property
    def version(self) -> tuple[int, int, int]:
        """
        :returns: the version formatted as a tuple of 3 int elements
        """
        return self._version

    @property
    def as_float(self) -> float:
        """
        :returns: the version as float
        """
        main = Decimal(self._version[0])
        sec = Decimal(self._version[1]) * Decimal("0.1")
        third = Decimal(self._version[2]) * Decimal("0.001")
        return float(main + sec + third)

    def __str__(self):
        return f"{self.version[0]}.{self.version[1]}.{self.version[2]}"

    def __repr__(self):
        return str(self._version)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, (tuple, float, Version)):
            return NotImplemented

        if not isinstance(other, Version):
            other = Version(other)

        if (
            self.version[0] == other.version[0]
            and self.version[1] == other.version[1]
            and self.version[2] == other.version[2]
        ):
            return True

        return False

    def __gt__(self, other: Union[tuple[int, int, int], float, Version]) -> bool:
        if not isinstance(other, Version):
            other = Version(other)

        if self.version[0] < other.version[0]:
            return False
        elif self.version[0] > other.version[0]:
            return True
        else:
            if self.version[1] < other.version[1]:
                return False
            elif self.version[1] > other.version[1]:
                return True
            else:
                if self.version[2] > other.version[2]:
                    return True
                else:
                    return False

    def __lt__(self, other: Union[tuple[int, int, int], float, Version]) -> bool:
        if not isinstance(other, Version):
            other = Version(other)

        if self.version[0] < other.version[0]:
            return True
        elif self.version[0] > other.version[0]:
            return False
        else:
            if self.version[1] < other.version[1]:
                return True
            elif self.version[1] > other.version[1]:
                return False
            else:
                if self.version[2] < other.version[2]:
                    return True
                else:
                    return False

    def __ge__(self, other: Union[tuple[int, int, int], float, Version]) -> bool:
        if not isinstance(other, Version):
            other = Version(other)

        if self.version[0] < other.version[0]:
            return False
        elif self.version[0] > other.version[0]:
            return True
        else:
            if self.version[1] < other.version[1]:
                return False
            elif self.version[1] > other.version[1]:
                return True
            else:
                if self.version[2] >= other.version[2]:
                    return True
                else:
                    return False

    def __le__(self, other: Union[tuple[int, int, int], float, Version]) -> bool:
        if not isinstance(other, Version):
            other = Version(other)

        if self.version[0] < other.version[0]:
            return True
        elif self.version[0] > other.version[0]:
            return False
        else:
            if self.version[1] < other.version[1]:
                return True
            elif self.version[1] > other.version[1]:
                return False
            else:
                if self.version[2] <= other.version[2]:
                    return True
                else:
                    return False
