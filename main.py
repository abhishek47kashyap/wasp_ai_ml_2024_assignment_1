from resources.game import Game

if __name__ == "__main__":
    game = Game(
        num_entities=10,
        max_iter=3,
        map_size=[20, 20],  # [meters]
        step_size=0.5       # [meters]
    )
    game.run()
