# PYTRIS™ Copyright (c) 2017 Jason Kim All Rights Reserved.
from agent import Agent
from engine import *
from environment import *


def main():
    environment = Environment()
    agent = Agent()
    engine = TetrisEngine(environment, agent)

    while not environment.done:
        # # Pause screen
        # if environment.pause:
        #     engine.on_pause()

        # Game screen
        if environment.start:
            engine.on_game()
            print(environment.dx)

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

if __name__ == '__main__':
    main()
