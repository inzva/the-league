from enum import IntEnum

# IntEnum instead of Enum fixes JSON serialization issues


class RoomPhase(IntEnum):
    WAITING = 0
    DRAFT = 1
    PLAYING = 2
    FINISHED = 3


class ActionType(IntEnum):
    BAN = 1
    PICK = 2
