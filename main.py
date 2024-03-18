from resources.game import Game

if __name__ == "__main__":
    config_filepath = "config/params.yaml"
    game = Game(
        config_filepath = config_filepath
    )
    game.run()
