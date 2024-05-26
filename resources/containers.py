from dataclasses import dataclass
from enum import Enum

@dataclass
class EntityPosition:
    x: float
    y: float

    def __repr__(self) -> str:
        return f"EntityPosition(x = {self.x:.6f}, y = {self.y:.6f})"

@dataclass
class PositionScenerioBParams:
    dist_behind: float

@dataclass
class GuiParams:
    enabled: bool
    on_keypress: bool
    delay: float

class PositioningScenario(Enum):
    Invalid = 0
    ScenarioA = 1
    ScenarioB = 2
