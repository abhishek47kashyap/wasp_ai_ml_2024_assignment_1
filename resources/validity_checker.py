from resources.entity import Entity
from resources.math_utils import euclidean_distance

class CollisionChecker:
    def __init__(self, min_separation: float = 0.0):
        self._min_separation = max(0.0, min_separation)   # should be positive

    def in_collision(self, a: Entity, b: Entity) -> bool:
        return (self.get_separation(a, b) < self._min_separation)
    
    def get_collision_depth(self, a: Entity, b: Entity) -> float:
        return -self.get_separation(a, b)

    def get_separation(self, a: Entity, b: Entity) -> float:
        return (euclidean_distance(a, b) - a.radius - b.radius)
