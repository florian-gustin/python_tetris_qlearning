# PYTRIS™ Copyright (c) 2017 Jason Kim All Rights Reserved.

from Game import Game
from agent import Agent
from engines.headless_engine import HeadlessEngine
from engines.graphic_engine import *
from environment import *
import argparse



def main():
    environment = Environment(True)
    agent = Agent()

    parser = argparse.ArgumentParser()
    parser.add_argument("--headless", help="Run IA in headless", type=bool, default=False, required=False)
    args = parser.parse_args()

    game = Game(environment)

    if args.headless is True:
        try:
            while True:
                HeadlessEngine(environment, agent, game).run()
        except KeyboardInterrupt:
            agent.save("agent.dat")
    else:
        engine = GraphicEngine(environment, agent, game)

        while not environment.done:
            # # Pause screen
            # if environment.pause:
            #     engine.on_pause()

            # Game screen
            if environment.start:
                engine.on_game()
                #print(environment.dx)

            # Game over screen
            elif environment.game_over:
                engine.on_reset()
                # engine.on_game_over()

            # Start screen
            else:
                engine.on_start()

        engine.quit()


###########################################################
# Loop Start
###########################################################

if __name__ == '__main__':
    main()
