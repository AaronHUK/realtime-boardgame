from enum import Enum, unique


@unique
class Phase(Enum):
    INIT = 1
    START_TURN = 2
    DECLARE = 3
    ACTION = 4
    RESOLVE = 5
