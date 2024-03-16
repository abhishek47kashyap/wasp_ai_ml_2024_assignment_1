from resources.containers import EntityPose
from resources.entity import Entity

from resources.validity_checker import CollisionChecker
from resources.visualization import visualize_scene, visualize_triplets
from resources.math_utils import euclidean_distance, distance_from_point_to_line_between_two_points

import random

def generate_random_pose(map_size: list[float, float]) -> EntityPose:
    return EntityPose(x=random.uniform(0, map_size[0]), y=random.uniform(0, map_size[1]))

class Game:
    def __init__(self, num_entities: int, max_iter: int, map_size: list[float, float], step_size: float):
        self._num_entities = max(3, num_entities)
        self._max_iter = max_iter
        self._map_size = map_size
        self._step_size = step_size

        self._max_perception_radius = 5 # [m] max needed: ((map_size[0] ** 2) + (map_size[1] ** 2)) ** 0.5
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
        game_states = []
        for iter in range(self._max_iter):
            print(f"\tIteration {iter+1} / {self._max_iter}")
            self._step()
            game_states.append(GameState(iter, self._max_iter, self._triplets))
        print("Game has ended!")

        for state in game_states:
            print(state)

    def _create_population(self) -> list[Entity]:
        print(f"Creating a population of {self._num_entities} in a map of size {self._map_size} ..")
        population = [
            Entity(
                initial_position=generate_random_pose(self._map_size),
                perception_radius=self._max_perception_radius,
                id=0
            )
        ]
        for i in range(1, self._num_entities):
            in_collision = True
            num_in_collision = 0
            while in_collision:
                new_entity = Entity(
                    initial_position=generate_random_pose(self._map_size),
                    perception_radius=self._max_perception_radius,
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
                if euclidean_distance(entity, other_entity) <= self._max_perception_radius:
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
        for (root, a, b) in self._triplets:
            root.move_towards_somewhere_between(a.current_position, b.current_position, self._step_size)
        
        """
            TODO:
                - Iterate over self._triplets in random order
                - For every triplet, after a move command, positions in self._population and self._triplets should get updated
                    - This is bad design, there should be only one source of positions, and that should be self._population.
                    - Only IDs can stay in self._triplets and some helper method can convert a list[id, id, id] into list[entity, entity, entity]
        """

class GameState:
    def __init__(self, iter: int, max_iter: int, triplets: list[list[Entity]]):
        self.iter = iter
        self.max_iter = max_iter
        self.triplets = triplets

    def __repr__(self) -> str:
        lines = [
            f"Iteration: {self.iter+1} / {self.max_iter}: triplet count {len(self.triplets)}"
        ]
        for i, (root, a, b) in enumerate(self.triplets):
            shortest_distance, _ = distance_from_point_to_line_between_two_points(a.current_position, b.current_position, root.current_position)
            lines.append(f"\ttriplet {i+1}: {root.id} linked to {a.id} and {b.id}, distance = {shortest_distance:.3f}m")
        
        return '\n'.join(lines)

def show_game_progress(map_size: list[float, float], game_states: list[GameState]):
    """
        Some helpful links on how to animate game progress
        - https://medium.com/@qiaofengmarco/animate-your-data-visualization-with-matplotlib-animation-3e3c69679c90
        - https://stackoverflow.com/questions/42722691/python-matplotlib-update-scatter-plot-from-a-function
    """
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_title(f'Game progress over {len(game_states)} states')
    ax.set_xlabel('X [meters]')
    ax.set_ylabel('Y [meters]')
    ax.set_xlim(0, map_size[0])
    ax.set_ylim(0, map_size[1])

    for game_state in game_states:
        ...
