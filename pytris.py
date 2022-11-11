# PYTRIS™ Copyright (c) 2017 Jason Kim All Rights Reserved.
import argparse
import time

from Game import Game
from agent import Agent
from environment import *
from graphic_engine import *

save_time = time.time()


def headless(environment, agent, game):
    global save_time
    if time.time() - agent.timer > 1:
        print("Actions per sec : ", agent.actions)
        agent.actions = 0
        agent.timer = time.time()

    if time.time() - save_time > 60:
        print("Saving total game = ", environment.game_process_counter)
        agent.save("agent.dat")
        save_time = time.time()

    if environment.game_over is True:
        environment.next()
        environment.reset(True)
    else:

        if game.update_state_mino() == "create":
            hard_drop = game.hard_drop()

            if hard_drop is True:
                agent.change_state(environment.matrix)
                lines_count = environment.erase_count * LINE_CLEAR_REWARD
                holes_count = environment.holes_created_count() * HOLE_REWARD
                bp = environment.is_bumpiness_increased_by(agent.previous_bp,
                                                           environment.get_boundaries()) * BUMPINESS_REWARD
                is_blockade_created = environment.is_blockade_created() * BLOCKADE_REWARD

                reward = lines_count + holes_count + bp + is_blockade_created
                agent.insert_reward_in_state_qtable(environment.mino, environment.dx,
                                                    reward,
                                                    environment.get_state_boundaries(), environment.rotation)
                game.is_stackable()

            environment.goal -= environment.erase_count
            if environment.goal < 1 and environment.level < 15:
                environment.level += 1
                environment.goal += environment.level * 5
        else:
            action = agent.step(environment.mino, environment.dx, environment.rotation)
            game.on_step(action)


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
                headless(environment, agent, game)
        except KeyboardInterrupt:
            agent.save("agent.dat")
    else:
        engine = TetrisEngine(environment, agent, game)

        while not environment.done:
            # # Pause screen
            # if environment.pause:
            #     engine.on_pause()

            # Game screen
            if environment.start:
                engine.on_game()
                # print(environment.dx)

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
