import uuid
from enum import Enum
from attr import dataclass

class Player:
    def __init__(self, display_name: str) -> None:
        self.id = uuid.uuid4()
        self.display_name = display_name

@dataclass
class BingoCell:
    number: int
    checked: bool

class CellCheckResult(Enum):
    OK = 0
    NotFound = 1
    AlreadyChecked = 2

class RoomJoinResult(Enum):
    OK = 0
    NotFound = 1
    RoomFull = 2
    Locking = 3
