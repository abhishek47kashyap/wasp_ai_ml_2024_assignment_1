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

    ax.set_title('Scatter Plot of 2D Points')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_xlim(0, map_size[0])
    ax.set_ylim(0, map_size[1])

    # # Add a legend
    # ax.legend()

    # Show the plot
    ax.grid(True)
    plt.show()