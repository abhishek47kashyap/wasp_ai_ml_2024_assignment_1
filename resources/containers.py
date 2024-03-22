from dataclasses import dataclass
from enum import Enum

@dataclass
class EntityPosition:
    x: float
    y: float

    def __repr__(self) -> str:
        return f"EntityPosition(x = {self.x:.6f}, y = {self.y:.6f})"

class GamePolicy(Enum):
    Invalid = 0
    PolicyA = 1
    PolicyB = 2
