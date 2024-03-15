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

        self._max_perception_distance = 5 # [m] max needed: ((map_size[0] ** 2) + (map_size[1] ** 2)) ** 0.5
        self._collision_checker = CollisionChecker()

        self._population = self._create_population()
        print("Visualizing ..")
        visualize_scene(map_size, self._population)

        print(f"Game initialized!")

    def run(self):
        print(f"Running {self._max_iter} iterations of the game..")
        for iter in range(self._max_iter):
            print(f"\tIteration {iter+1} / {self._max_iter}")
    

    def _create_population(self) -> list[Entity]:
        print(f"Creating a population of {self._num_entities} in a map of size {self._map_size} ..")
        population = [
            Entity(
                initial_position=generate_random_pose(self._map_size),
                perception_radius=self._max_perception_distance,
                id=0
            )
        ]
        print(f"\tFirst entity: {population[0]}")
        for i in range(1, self._num_entities):
            in_collision = True
            num_in_collision = 0
            while in_collision:
                new_entity = Entity(
                    initial_position=generate_random_pose(self._map_size),
                    perception_radius=self._max_perception_distance,
                    id=i
                )
                in_collision = self._entity_in_collision(new_entity, population)
                num_in_collision += 1
            population.append(new_entity)
            # print(f"\tSpawned entity {i+1} / {self._num_entities}: {new_entity} (required {num_in_collision} collision checks)")
        print(f"Population created")
        return population

    def _entity_in_collision(self, entity: Entity, population: list[Entity]):
        for i in population:
            if self._collision_checker.in_collision(entity, i):
                return True
        return False

    def _step(self):
        raise NotImplementedError
