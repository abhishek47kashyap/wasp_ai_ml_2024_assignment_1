# WASP AI & ML 2024 (assignment 1)

This repository contains the implementation for Homework Assignment 1 of the course _WASP Artificial Intelligence and Machine Learning 2024_.

## Environment setup

This repository has been tested on Ubuntu 22.04.

1. Download and install [Anaconda](https://www.anaconda.com/download).
2. Clone this repository.
3. Create a `conda` environment following the instructions below.

```
cd /path/to/wasp_ai_ml_2024_assignment_1

conda create -y -n wasp_ai_ml python=3.10
conda activate wasp_ai_ml
conda env update --file environment.yml --prune
```

## Configuring parameters
The configuration parameters are in the file `config/params.yaml`.

- `random_seed`: seed value for `random.seed()`
- `num_entities`: population size
- `timesteps`: maximum number of timesteps to run the game for
- `map_size`: size of the map/room, should be a list of two positive numbers
- `step_size`: distance covered by an entity at every timestep
- `perception_radius`: distance up to which an agent can see another agent
- `gui`: set `enable` to `True` to visualize game progress and save a snapshot of the game every timestep
- `save_directory`: directory where all snapshots will be saved
- `positioning_scenario`: should be either `A` or `B`
- `positioning_scenario_B`: parameters related to `positioning_scenario` `B`

## Running the game
After configuring all parameters, execute from the root of the repository: `python main.py`

The game will end prior to reaching `timesteps` defined in `config/params.yaml` if all agents (that can converge) converges by an earlier timestep.

## Running tests
The game uses some math functions defined in `resources.math_utils.py`. To run unit tests for the math function, execute from the root of the repository: `python -m tests.math_utils`
