import matplotlib.pyplot as plt
from resources.entity import Entity

def visualize_scene(map_size: list[float, float], population: list[Entity]) -> None :
    fig, ax = plt.subplots(figsize=(8, 6))

    x = []
    y = []
    for entity in population:
        x.append(entity.current_position.x)
        y.append(entity.current_position.y)
    
    ax.scatter(x, y, color='blue')

    ax.set_title('Population of entities')
    ax.set_xlabel('X [meters]')
    ax.set_ylabel('Y [meters]')
    ax.set_xlim(0, map_size[0])
    ax.set_ylim(0, map_size[1])

    # Show the plot
    ax.grid(True)
    plt.show()

def visualize_triplets(map_size: list[float, float], population: list[Entity], triplets: list[list[Entity]]) -> None :
    fig, ax = plt.subplots(figsize=(10, 8))

    x = []
    y = []
    for entity in population:
        x.append(entity.current_position.x)
        y.append(entity.current_position.y)
    
    ax.scatter(x, y, color='blue')
    for entity in population:
        ax.annotate(f"{entity.id}", (entity.current_position.x, entity.current_position.y + 0.2))

    for (root, a, b) in triplets:
        x = root.current_position.x
        y = root.current_position.y
        dx_a = a.current_position.x - x
        dy_a = a.current_position.y - y
        dx_b = b.current_position.x - x
        dy_b = b.current_position.y - y
        ax.arrow(x, y, dx_a, dy_a, color='red')
        ax.arrow(x, y, dx_b, dy_b, color='green')

    ax.set_title('Population of entities')
    ax.set_xlabel('X [meters]')
    ax.set_ylabel('Y [meters]')
    ax.set_xlim(0, map_size[0])
    ax.set_ylim(0, map_size[1])

    # Show the plot
    ax.grid(True)
    plt.show()