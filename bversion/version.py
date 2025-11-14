from typing import Union

class Version:
    '''
    This class allow basic representation of blender version as tuple of 3 ints.
    you can easily compare versions together
    '''

    def __init__(self, version: Union[tuple[int], str]):
        if len(version) == 0:
            self._version = (0, 0, 0)
        elif isinstance(version, str):
            self._version = tuple(int(float(i)) for i in version.split('.') if len(i)>0)
        elif isinstance(version, tuple):
            self._version = version
        elif isinstance(version, float):
            self._version = tuple(int(float(i)) for i in str(version).split('.') if len(i)>0) + (0,)

        if len(self._version) < 3:
            for _ in range(3-len(self._version)):
                self._version += (0,)

    @property
    def version(self) -> tuple[int]:
        '''
        :returns: the version formatted as a tuple of 3 int elements
        '''
        return self._version

    @property
    def as_float(self) -> float:
        '''
        :returns: the version as float
        '''
        return float(self._version[0] + self._version[1] * 0.1 + self._version[2] * 0.001)

    def __str__(self):
        return f'{self.version[0]}.{self.version[1]}.{self.version[2]}'

    def __repr__(self):
        return self._version

    def __eq__(self, other:Union[tuple[int], float]):
        if isinstance(other, float):
            other = Version(tuple(int(i) for i in str(other).split('.')) + (0,))

        if (self.version[0] == other.version[0] and
            self.version[1] == other.version[1] and
            self.version[2] == other.version[2]):
            return True

        return False

    def __gt__(self, other:Union[tuple[int], float]):
        if isinstance(other, float):
            other = Version(tuple(int(i) for i in str(other).split('.')) + (0,))

        if self.version[0] <= other.version[0]: return False
        elif self.version[1] <= other.version[1]: return False
        elif self.version[2] > other.version[2]: return True

        return False

    def __lt__(self, other:Union[tuple[int], float]):
        if isinstance(other, float):
            other = Version(tuple(int(i) for i in str(other).split('.')) + (0,))

        if self.version[0] >= other.version[0]: return False
        elif self.version[1] >= other.version[1]: return False
        elif self.version[2] < other.version[2]: return True

        return False

    def __ge__(self, other:Union[tuple[int], float]):
        if isinstance(other, float):
            other = Version(tuple(int(i) for i in str(other).split('.')) + (0,))

        if self.version[0] < other.version[0]: return False
        elif self.version[0] > other.version[0]: return True
        else:
            if self.version[1] < other.version[1]: return False
            elif self.version[1] > other.version[1]: return True
            else:
                if self.version[2] >= other.version[2]: return True
                else: return False

    def __le__(self, other:Union[tuple[int], float]):
        if isinstance(other, float):
            other = Version(tuple(int(i) for i in str(other).split('.')) + (0,))

        if self.version[0] < other.version[0]: return True
        elif self.version[0] > other.version[0]: return False
        else:
            if self.version[1] < other.version[1]: return True
            elif self.version[1] > other.version[1]: return False
            else:
                if self.version[2] <= other.version[2]: return True
                else: return False

        return True