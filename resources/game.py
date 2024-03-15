from resources.containers import EntityPose
from resources.entity import Entity

from resources.validity_checker import CollisionChecker
from resources.visualization import visualize_scene

import random

def generate_random_pose(map_size: list[float, float]) -> EntityPose:
    return EntityPose(x=random.uniform(0, map_size[0]), y=random.uniform(0, map_size[1]))

class Game:
    def __init__(self, num_entities: int, max_iter: int, map_size: list[float, float]):
        self._num_entities = max(3, num_entities)
        self._max_iter = max_iter
        self._map_size = map_size

        self._max_perception_distance = ((map_size[0] ** 2) + (map_size[1] ** 2)) ** 0.5
        self._collision_checker = CollisionChecker()

        # Create a population of collision-free entities
        print(f"Creating a population of {num_entities} in a map of size {map_size} ..")
        self._population = [
            Entity(
                initial_position=generate_random_pose(self._map_size),
                perception_radius=self._max_perception_distance,
                id=0
            )
        ]
        print(f"\tFirst entity: {self._population[0]}")
        for i in range(1, num_entities):
            in_collision = True
            num_in_collision = 0
            while in_collision:
                new_entity = Entity(
                    initial_position=generate_random_pose(self._map_size),
                    perception_radius=self._max_perception_distance,
                    id=i
                )
                in_collision = self._entity_in_collision(new_entity)
                num_in_collision += 1
            self._population.append(new_entity)
            print(f"\tSpawned entity {i+1} / {num_entities}: {new_entity} (required {num_in_collision} collision checks)")
        print(f"Population created")

        print("Visualizing ..")
        visualize_scene(map_size, self._population)

    
    def step(self):
        raise NotImplementedError

    def _entity_in_collision(self, entity: Entity):
        for i in self._population:
            if self._collision_checker.in_collision(entity, i):
                return True
        return False