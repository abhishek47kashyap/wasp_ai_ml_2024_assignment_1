from resources.containers import EntityPosition, GamePolicy, PolicyBParams
from resources.entity import Entity
from resources.validity_checker import CollisionChecker
from resources.visualization import visualize_scene, visualize_triplets
from resources.math_utils import euclidean_distance, distance_from_point_to_line_between_two_points

import yaml
from copy import deepcopy

import random
random.seed(20) # 20 and 50 produce good numbers for debugging

def generate_random_position(map_size: list[float, float]) -> EntityPosition:
    return EntityPosition(x=random.uniform(0, map_size[0]), y=random.uniform(0, map_size[1]))

class Game:
    def __init__(self, config_filepath: str):
        self._num_entities = None
        self._iterations = None
        self._map_size = None
        self._step_size = None
        self._policy = None
        self._policy_B_params = None
        if not self._init_config(config_filepath):
            print(f"[ERROR] Cannot continue with game initialization, configs could not be loaded from {config_filepath}")
            return

        self._max_perception_radius = 5 # [m] max needed: ((map_size[0] ** 2) + (map_size[1] ** 2)) ** 0.5
        self._collision_checker = CollisionChecker()

        self._population = self._create_population()
        # visualize_scene(self._map_size, self._population)

        self._triplets, self._not_roots = self._create_triplets()
        visualize_triplets(self._map_size, self._population, self._triplets_to_entities(self._triplets), block=False, title="INITIAL STATE")

        print(f"Game initialized!")

    def run(self):
        if len(self._triplets) == 0:
            print("No triplets found, game cannot be played")
            return

        start_state = deepcopy(self._population)
        
        print(f"Running {self._iterations} iterations of the game..")
        game_states = []
        for iter in range(self._iterations):
            print(f"\tIteration {iter+1} / {self._iterations}")
            self._step()
            game_states.append(GameState(iter, self._iterations, self._triplets_to_entities(self._triplets)))
        print("Game has ended!")

        end_state = deepcopy(self._population)
        self._log_game_summary(start_state, end_state)

        visualize_triplets(self._map_size, self._population, self._triplets_to_entities(self._triplets), block=True, title="FINAL STATE")

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
        not_roots = []
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
                not_roots.append(entity.id)

        print(f"Triplets created: {len(triplets)}")
        for i, triplet in enumerate(triplets):
            root, a, b = triplet
            print(f"\t{i+1}) id {root} is linked to ids {a} and {b}")
        print(f"\tNon root entities: {not_roots}")
        return triplets, not_roots

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

    def _init_config(self, config_filepath: str) -> bool:
        """
            Loads parameters from config file. Returns True/False for success/failure.
            Mutates config class variables.
        """
        with open(config_filepath) as stream:
            try:
                params = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(f"[ERROR] Could not read parameters from {config_filepath}: {exc}")
                return False
            else:
                print(f"Loaded parameters from {config_filepath}:")
                for key in params.keys():
                    print(f"\t{key} : {params[key]}")
        self._num_entities = max(3, params["num_entities"])
        self._iterations = params["iterations"]
        self._map_size = params["map_size"]
        self._step_size = params["step_size"]

        policy = params["policy"]
        if policy not in ['A', 'B']:
            print(f"[ERROR] Game policy must be either A or B. Cannot continue with game initialization!")
            return False

        self._policy = GamePolicy.PolicyA if (policy == 'A') else GamePolicy.PolicyB
        self._policy_B_params = PolicyBParams(dist_behind=params["policy_B"]["dist_behind"])

        return True

    def _log_game_summary(self, start_state: list[Entity], end_state: list[Entity]) -> None:
        print("Entities start --> end coordinates:")
        for (a, b) in zip(start_state, end_state):
            if (a.id == b.id):
                distance_moved = euclidean_distance(a.current_position, b.current_position)
                if a.id in self._not_roots:
                    if distance_moved > 0:
                        print(f"\t[WARN: should not have moved] ID {a.id}: ({a.current_position.x:.3f}, {a.current_position.y:.3f}) --> ({b.current_position.x:.3f}, {b.current_position.y:.3f}), distance moved = {distance_moved:.3f}m")
                    else:
                        print(f"\tID {a.id}: ({a.current_position.x:.3f}, {a.current_position.y:.3f}) [DID NOT MOVE]")
                else:
                    print(f"\tID {a.id}: ({a.current_position.x:.3f}, {a.current_position.y:.3f}) --> ({b.current_position.x:.3f}, {b.current_position.y:.3f}), distance moved = {distance_moved:.3f}m, convergence reached: {b.has_converged()}, history: {b.get_tracking_history()}")
            else:
                print(f"[WARN] IDs should be in the same order for start and end states, but found start state ID {a.id} and end state ID {b.id}")

    def _step(self):
        entities = self._triplets_to_entities(self._triplets)
        for (root, a, b) in entities:
            if self._policy == GamePolicy.PolicyA:
                root.move_towards_halfway_between(a.current_position, b.current_position, self._step_size)
            else:
                print(f"Moving entity {root.id} to a position behind {b.id} to shielf from {a.id}")
                root.move_behind_entity(a.current_position, b.current_position, self._step_size)

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
