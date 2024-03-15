
from resources.containers import EntityPose

def euclidean_distance(a: EntityPose, b: EntityPose) -> float:
    return ((a.current_position.x - b.current_position.x)**2 + (a.current_position.y - b.current_position.y)**2) ** 0.5