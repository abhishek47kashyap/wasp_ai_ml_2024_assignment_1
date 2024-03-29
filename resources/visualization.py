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

def visualize_triplets(
        map_size: list[float, float],
        population: list[Entity],
        block: bool = True,
        title: str = None,
        save_filepath: str = None,
        timeout: float = None,   # in seconds
        on_keypress: bool = None
    ) -> None :
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
    ax.set_xlim(-3, map_size[0]+3)
    ax.set_ylim(-3, map_size[1]+3)
    ax.grid(True)

    if save_filepath:
        fig.savefig(save_filepath)

    """
        matplotlib's show() does not support timeout so here's a workround
        to make the plot time out and close:
        https://stackoverflow.com/a/30365738/6010333
    """
    def close_event():
        plt.close()
    if block and (timeout is not None) and (not on_keypress):
        timer = fig.canvas.new_timer(interval = timeout * 1000)
        timer.add_callback(close_event)
        timer.start()

    plt.show(block=block)
