from resources.containers import EntityPosition
from resources.entity import Entity

from resources.validity_checker import CollisionChecker
from resources.visualization import visualize_scene, visualize_triplets
from resources.math_utils import euclidean_distance, distance_from_point_to_line_between_two_points

import random
random.seed(20) # 20 and 50 produce good numbers for debugging

def generate_random_position(map_size: list[float, float]) -> EntityPosition:
    return EntityPosition(x=random.uniform(0, map_size[0]), y=random.uniform(0, map_size[1]))

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
        print("Visualizing triplets ..")
        visualize_triplets(map_size, self._population, self._triplets_to_entities(self._triplets), block=False, title="START")

        print(f"Game initialized!")

    def run(self):
        if len(self._triplets) == 0:
            print("No triplets found, game cannot be played")
            return

        print("============= POPULATION STATE IN THE BEGINNING ===============")
        print(self._population)
        print()
        
        print(f"Running {self._max_iter} iterations of the game..")
        game_states = []
        for iter in range(self._max_iter):
            print(f"\tIteration {iter+1} / {self._max_iter}")
            self._step()
            game_states.append(GameState(iter, self._max_iter, self._triplets_to_entities(self._triplets)))
        print("Game has ended!")

        print("============= POPULATION STATE IN THE END ===============")
        print(self._population)
        print()

        for state in game_states:
            print(state)

        visualize_triplets(self._map_size, self._population, self._triplets_to_entities(self._triplets), block=True, title="END")

    def _create_population(self) -> list[Entity]:
        print(f"Creating a population of {self._num_entities} in a map of size {self._map_size} ..")
        population = [
            Entity(
                initial_position=generate_random_position(self._map_size),
                perception_radius=self._max_perception_radius,
                id=0
            )
        ]
        for i in range(1, self._num_entities):
            in_collision = True
            num_in_collision = 0
            while in_collision:
                new_entity = Entity(
                    initial_position=generate_random_position(self._map_size),
                    perception_radius=self._max_perception_radius,
                    id=i
                )
                in_collision = self._entity_in_collision(new_entity, population)
                num_in_collision += 1
            population.append(new_entity)
            # print(f"\tSpawned entity {i+1} / {self._num_entities}: {new_entity} (required {num_in_collision} collision checks)")
        print(f"Population created")
        return population

    def _create_triplets(self) -> list[list[int]]:
        print(f"Creating triplets ..")
        triplets = []
        for i, entity in enumerate(self._population):
            # get all entities within view of the current entity
            other_entities = self._population[:i] + self._population[i+1:]
            visible_entities = [i for i in other_entities if euclidean_distance(entity.current_position, i.current_position) <= self._max_perception_radius]

            # out of the visible entities, randomly select two to form a triplet
            if len(visible_entities) >= 2:
                random_selections = random.sample(visible_entities, 2)
                triplet = [entity.id, random_selections[0].id, random_selections[1].id]

                triplets.append(triplet)
            else:
                print(f"\t{len(visible_entities)} visible neighbors for entity {entity}")

        print(f"Triplets created: {len(triplets)}")
        for i, triplet in enumerate(triplets):
            root, a, b = triplet
            print(f"\t{i+1}) id {root} is linked to ids {a} and {b}")
        return triplets

    def _entity_in_collision(self, entity: Entity, population: list[Entity]):
        for i in population:
            if self._collision_checker.in_collision(entity, i):
                return True
        return False

    def _get_entity_from_id(self, id: int) -> Entity:
        for entity in self._population:
            if id == entity.id:
                return entity

        print(f"[ERROR] Population does not have an entity with ID {id}")
        return None

    def _step(self):
        entities = self._triplets_to_entities(self._triplets)
        for (root, a, b) in entities:
            root.move_towards_halfway_between(a.current_position, b.current_position, self._step_size)

    def _triplets_to_entities(self, ids: list[int]) -> list[Entity]:
        if len(self._population) == 0:
            return []

        return [[self._get_entity_from_id(i) for i in sublist] for sublist in ids]

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
