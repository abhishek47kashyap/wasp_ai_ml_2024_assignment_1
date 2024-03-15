from resources.entity import Entity

class CollisionChecker:
    def __init__(self, min_separation: float = 0.0):
        self._min_separation = max(0.0, min_separation)   # should be positive

    def in_collision(self, a: Entity, b: Entity) -> bool:
        return (self.get_separation(a, b) > self._min_separation)
    
    def get_collision_depth(self, a: Entity, b: Entity) -> float:
        return -self.get_separation(a, b)

    def get_separation(self, a: Entity, b: Entity) -> float:
        dist_between_centers = ((a.current_position.x - b.current_position.x)**2 + (a.current_position.y - b.current_position.y)**2) ** 0.5
        return (dist_between_centers - a.size - b.size)