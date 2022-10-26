# PYTRIS™ Copyright (c) 2017 Jason Kim All Rights Reserved.

from engine import *
from environment import *


def main():
    environment = Environment()
    engine = TetrisEngine(environment)

    if isinstance(engine, TetrisEngine):
        # get the score history
        engine.score_history()

    while not environment.done:
        # Pause screen
        if environment.pause:
            engine.on_pause()

        # Game screen
        elif environment.start:
            engine.on_game()

        # Game over screen
        elif environment.game_over:
            engine.on_game_over()

        # Start screen
        else:
            engine.on_start()

    engine.quit()


###########################################################
# Loop Start
###########################################################
main()
