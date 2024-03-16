from resources.containers import EntityPose
from resources.entity import Entity

from resources.validity_checker import CollisionChecker
from resources.visualization import visualize_scene, visualize_triplets
from resources.math_utils import euclidean_distance

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
        # print("Visualizing entities..")
        # visualize_scene(map_size, self._population)

        self._triplets = self._create_triplets()
        # print("Visualizing triplets ..")
        # visualize_triplets(map_size, self._population, self._triplets)

        print(f"Game initialized!")

    def run(self):
        if len(self._triplets) == 0:
            print("No triplets found, game cannot be played")
            return

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

    def _create_triplets(self) -> list[list[Entity]]:
        print(f"Creating triplets ..")
        triplets = []
        for i, entity in enumerate(self._population):
            other_entities = self._population[:i] + self._population[i+1:]

            # get all entities within view i.e perception_distance
            visible_entities = []
            for other_entity in other_entities:
                if euclidean_distance(entity, other_entity) <= self._max_perception_distance:
                    visible_entities.append(other_entity)

            # out of the visible entities, randomly select two to form a triplet
            if len(visible_entities) >= 2:
                random_selections = random.sample(visible_entities, 2)
                triplet = [entity, random_selections[0], random_selections[1]]

                triplets.append(triplet)
            else:
                print(f"\t{len(visible_entities)} visible neighbors for entity {entity}")
        
        print(f"Triplets created: {len(triplets)}")
        for i, triplet in enumerate(triplets):
            root, a, b = triplet
            print(f"\t{i+1}) id {root.id} is linked to ids {a.id} and {b.id}")
        return triplets
            

    def _entity_in_collision(self, entity: Entity, population: list[Entity]):
        for i in population:
            if self._collision_checker.in_collision(entity, i):
                return True
        return False

    def _step(self):
        raise NotImplementedError
