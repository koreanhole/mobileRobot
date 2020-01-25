import enum


@enum.unique
class Direction(enum.Enum):
    __slots__ = ["up", "right", "down", "left", "closed"]
    up = 0
    right = 1
    down = 2
    left = 3
    closed = -1


@enum.unique
class State(enum.Enum):
    __slots__ = ["hazard", "unseen_hazrd", "seen_hazrd", "target", "checked_target", "unchecked_target", "blob",
                 "checked_blob", "unchecked_blob", "robot", "checked_blob"]

    hazard = 0
    unseen_hazard = 1
    seen_hazard = 2

    blob = 3
    checked_blob = 4
    unchecked_blob = 5

    target = 6
    checked_target = 7
    unchecked_target = 8

    robot = 9
