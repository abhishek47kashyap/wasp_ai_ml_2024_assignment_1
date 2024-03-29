import matplotlib.pyplot as plt
from resources.entity import Entity

import numpy as np 

def visualize_scene(map_size: list[float, float], population: list[Entity]) -> None :
    fig, ax = plt.subplots(figsize=(8, 6))

    x = []
    y = []
    is_root = []
    for entity in population:
        x.append(entity.current_position.x)
        y.append(entity.current_position.y)
        is_root.append(entity.is_root())

    x = np.array(x)
    y = np.array(y)
    is_root = np.array(is_root)

    ax.scatter(x[is_root], y[is_root], color='blue')
    ax.scatter(x[~is_root], y[~is_root], facecolors='none', edgecolors='b')

    ax.set_title('Population of entities')
    ax.set_xlabel('X [meters]')
    ax.set_ylabel('Y [meters]')
    ax.set_xlim(0, map_size[0])
    ax.set_ylim(0, map_size[1])

    # Show the plot
    ax.grid(True)
    plt.show()

def visualize_triplets(map_size: list[float, float], population: list[Entity], triplets: list[list[Entity]], block: bool = True, title: str = None) -> None :
    fig, ax = plt.subplots(figsize=(10, 8))

    x = []
    y = []
    is_root = []
    for entity in population:
        x.append(entity.current_position.x)
        y.append(entity.current_position.y)
        is_root.append(entity.is_root())
    
    x = np.array(x)
    y = np.array(y)
    is_root = np.array(is_root)
    ax.scatter(x[is_root], y[is_root], color='blue')
    ax.scatter(x[~is_root], y[~is_root], facecolors='none', edgecolors='b')
    for entity in population:
        ax.annotate(f"{entity.id}", (entity.current_position.x, entity.current_position.y + 0.2))

    if title is None:
        ax.set_title('Population of entities')
    else:
        ax.set_title(title)
    ax.set_xlabel('X [meters]')
    ax.set_ylabel('Y [meters]')
    ax.set_xlim(0, map_size[0])
    ax.set_ylim(0, map_size[1])

    # Show the plot
    ax.grid(True)
    plt.show(block=block)
