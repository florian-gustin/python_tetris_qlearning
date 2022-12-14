import argparse

from agent.agent import Agent
from constants.config import ALPHA, GAMMA, EXPLORATION
from engines.game_mode.gui_agent_engine import GUIAgentEngine
from engines.game_mode.gui_player_engine import GUIPlayerEngine
from engines.game_mode.headless_agent_engine import HeadlessAgentEngine
from game.environment import *
from game.game import Game
from graph.statistic import Statistic


def main():
    statistic = Statistic()
    environment = Environment(True)
    agent = Agent(alpha=ALPHA, gamma=GAMMA, exploration=EXPLORATION)

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", help="Choose between : player | gui-agent | headless-agent", type=str, default="player", required=False)
    parser.add_argument("--watch", help="Disable saving", action="store_true")
    args = parser.parse_args()

    game = Game(environment)

    if args.mode == "gui-agent":
        engine = GUIAgentEngine(environment, agent, game, args.watch)
        while not environment.done:
            # Game screen
            if environment.start:
                engine.execute()
                # print(environment.dx)

            # Game over screen
            elif environment.game_over:
                engine.on_reset()
                # engine.on_game_over()

        engine.quit()
        statistic.apply(agent.load_history('history.dat'))

    elif args.mode == "headless-agent":
        engine = HeadlessAgentEngine(environment, agent, game)
        try:
            while True:
                engine.execute()
        except KeyboardInterrupt:
            agent.reward_count_history.append(agent.reward_count)
            agent.save_history("history.dat")
            agent.save_qtable("agent.dat")
            statistic.apply(agent.load_history('history.dat'))

    else:
        engine = GUIPlayerEngine(environment)
        while not environment.done:
            # Game screen
            if environment.start:
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

if __name__ == '__main__':
    main()
