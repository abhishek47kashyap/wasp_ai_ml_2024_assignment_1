import matplotlib.pyplot as plt
from resources.entity import Entity

def visualize_scene(map_size: list[float, float], population: list[Entity]):
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