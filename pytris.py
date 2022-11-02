# PYTRIS™ Copyright (c) 2017 Jason Kim All Rights Reserved.
import os

import pygame.time

from Game import Game
from agent import Agent
from graphic_engine import *
from environment import *
import argparse

def main():
    environment = Environment()
    agent = Agent()

    parser = argparse.ArgumentParser()
    parser.add_argument("--headless", help="Run IA in headless", type=bool, default=False, required=False)
    args = parser.parse_args()

    game = Game(environment)

    engine = TetrisEngine(environment, agent, game)

    if args.headless is False:
        while True:
            action = agent.best_action(environment.mino, environment.dx)
            game.on_step(action)
        return

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
