import argparse

from agent import Agent
from engines.dummy_engine import DummyEngine
from engines.headless_engine import HeadlessEngine
from game.environment import *
from game import Game
from graph.statistic import Statistic


def main():
    statistic = Statistic()
    environment = Environment(True)
    agent = Agent()

    parser = argparse.ArgumentParser()
    parser.add_argument("--headless", help="Run IA in headless", type=bool, default=False, required=False)
    args = parser.parse_args()

    game = Game(environment)

    if args.headless is True:
        engine = HeadlessEngine(environment, agent, game)

        try:
            while True:
                engine.execute()
        except KeyboardInterrupt:
            agent.save("agent.dat")
            statistic.apply(agent.reward_count_history)
    else:
        engine = DummyEngine(environment, agent, game)

        while not environment.done:
            # # Pause screen
            # if environment.pause:
            #     engine.on_pause()

            # Game screen
            if environment.start:
                engine.execute()
                #print(environment.dx)

            # Game over screen
            elif environment.game_over:
                engine.on_reset()
                # engine.on_game_over()


        engine.quit()


###########################################################
# Loop Start
###########################################################

if __name__ == '__main__':
    main()
