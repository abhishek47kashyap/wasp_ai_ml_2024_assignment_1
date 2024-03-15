
from resources.containers import EntityPose

class Entity:
    def __init__(self, initial_position: EntityPose, perception_radius: float, id: int, radius: float = 0.3):
        self.id = id
        self.radius = radius
        self.perception_radius = perception_radius
        self.current_position = initial_position

        self._initial_position = initial_position

    def update_current_pose(self, pose: EntityPose):
        self.current_position = pose

    def __repr__(self) -> str:
        return f"Id {self.id}: position ({self.current_position.x:.3f}, {self.current_position.y:.3f})"
        
