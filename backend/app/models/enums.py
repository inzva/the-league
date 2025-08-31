from enum import Enum


class RoomPhase(Enum):
    WAITING = 0
    DRAFT = 1
    PLAYING = 2
    FINISHED = 3


class ActionType(Enum):
    BAN = 1
    PICK = 2
