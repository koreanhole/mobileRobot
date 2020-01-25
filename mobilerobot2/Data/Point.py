from Data.Enums import Direction
from Data.Enums import State


class Point():
    # 변수와 자료형을 지정.
    # 점은 , xy 좌표, state, path, direction 으로 이루어 진다. path와 direction은 미리 enum으로 지정된 값을 사용한다.
    # State,Direction enum 값들은 Enums 에 저장되 있다.
    __slots__ = ["__x", "__y", "__state", "__path", "__direction"]
    __x: int
    __y: int
    __direction: Direction
    __path: Direction
    __state: State

    def __init__(self, x, y, state):
        self.__x = x
        self.__y = y
        self.__state = state
        self.__direction = Direction.closed
        self.__path = Direction.closed

    # 점의 좌표이동.
    def move(self, x, y):
        self.__x += x
        self.__y += y

    def setLocation(self, x, y):
        self.__x = x
        self.__y = y

    def setState(self, state):
        if isinstance(state, State):
            self.__state = state
        else:
            raise TypeError("state must be Enums.State")

    def setPath(self, path):
        if isinstance(path, Direction):
            self.__path = path
        else:
            raise TypeError("Path must be Enums.Direction")

    def setDirection(self, direction):
        if isinstance(direction, Direction):
            self.__direction = direction
        else:
            raise TypeError("__direction must be Enums.Direction")

    def getLocation(self):
        return (self.__x, self.__y)

    def getPath(self):
        return self.__path

    def getDirection(self):
        return self.__direction

    def getState(self):
        return self.__state




