# PYTRIS™ Copyright (c) 2017 Jason Kim All Rights Reserved.
import os

import pygame.time

from Game import Game
from agent import Agent
from graphic_engine import *
from environment import *
import argparse

def main():
    environment = Environment(True)
    agent = Agent()

    parser = argparse.ArgumentParser()
    parser.add_argument("--headless", help="Run IA in headless", type=bool, default=False, required=False)
    args = parser.parse_args()

    game = Game(environment)

    engine = TetrisEngine(environment, agent, game)

    if args.headless is False:
        while True:
            if environment.game_over is True:
                environment.reset(True)
                print("Reset")

            else:
                if game.update_state_mino() == "create":
                    hard_drop = game.hard_drop()

                    if hard_drop is True:
                        game.is_stackable()

                    agent.change_state(environment.matrix)
                    lines_count = environment.erase_count * LINE_CLEAR_REWARD
                    holes_count = environment.holes_created_count() * HOLE_REWARD
                    reward = lines_count + holes_count
                    agent.insert_reward_in_state_qtable(environment.mino, environment.dx,
                                                               reward,
                                                               environment.get_boundaries())
                    environment.goal -= environment.erase_count
                    if environment.goal < 1 and environment.level < 15:
                        environment.level += 1
                        environment.goal += environment.level * 5

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
