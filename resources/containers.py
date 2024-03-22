from dataclasses import dataclass

@dataclass
class EntityPosition:
    x: float
    y: float

    def __repr__(self) -> str:
        return f"EntityPosition(x = {self.x:.6f}, y = {self.y:.6f})"
