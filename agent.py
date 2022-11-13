import os
import pickle
import random
import time

from config import ACTIONS, ACTION_ROTATE, ACTION_LEFT, ACTION_RIGHT
from tetri_mino import TetriMino


class Agent:
    def __init__(self, alpha=1, gamma=1, exploration=0, cooling_rate=1):
        self.last_action = 0
        self.state = [0] * 10
        self.qtables = {}
        self.init_state_in_qtable()
        self.init_radar()
        self.__alpha = alpha
        self.__gamma = gamma
        self.__exploration = exploration
        self.__cooling_rate = cooling_rate
        self.timer = time.time()
        self.previous_bp = "000000000"
        self.previous_state = [0] * 10
        self.actions = 0



    def init_radar(self):
        self.radar = {"zone": [[0] * 10 for _ in range(4)],
                      "y": 19}

    def init_state_in_qtable(self):
        if len(self.qtables) == 0:
            if os.path.exists("agent.dat"):
                self.load("agent.dat")
                return

            self.qtables = {}
            #print(self.qtables)

    def change_state(self, grid):
        tmp = []
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                if y < len(grid[x]) - 1 and y + 1 == 0:
                    tmp.append(y)
                    self.state = tmp


    def table_to_str(self, table):
        return ''.join(map(str, table))

    def insert_reward_in_state_qtable(self, mino, x, value, state_str, rotation):
        #print(state_str)
        maxQ = max(self.qtables[state_str][mino - 1][rotation])

        # (1 - self.__alpha) * qtable[action] + self.__alpha * (reward + self.__gamma * max_q)  <- version du projet noe pieerre

        tmp = self.__alpha * \
              (value + self.__gamma * maxQ -
               self.qtables[state_str][mino - 1][rotation][x])
        self.qtables[state_str][mino - 1][rotation][x] += tmp
        #print("INSERT QTABLE : key = ", state_str, ", mino = ", mino - 1, ", x = ", x, ", rotation = ", rotation,
        #      ", value = ", tmp)

        self.state = state_str

    def upsert_boundary_qtable(self, mino, state_str):
        self.previous_state = state_str
        state_str = self.table_to_str(state_str)
        self.previous_bp = state_str
        if state_str not in self.qtables:
            self.qtables[state_str] = {}
        if mino - 1 not in self.qtables[state_str]:
            self.qtables[state_str][mino - 1] = {}
        if len(self.qtables[state_str][mino - 1]) == 0:
            for i in range(len(TetriMino.mino_map[mino - 1])):
                x_range = TetriMino.mino_map[mino - 1][i]['X_RANGE']
                self.qtables[state_str][mino - 1][i] = {}
                for x in range(x_range):
                    self.qtables[state_str][mino - 1][i][x] = 0

    def best_actions(self, mino, dx, boundaries):

        table_action = []  # tout les actions que doit faire l'agent ici

        rotation, x = self.best_action(mino, boundaries)

        if dx > x:
            for i in range(x, dx):
                table_action.append(ACTION_LEFT)
            for i in range(rotation):
                table_action.append(ACTION_ROTATE)
        else:
            for i in range(rotation):
                table_action.append(ACTION_ROTATE)
            for i in range(dx, x):
                table_action.append(ACTION_RIGHT)

        #print(table_action)
        return table_action, rotation, x

    def best_action(self, mino, boundaries):
        if random.uniform(0, 1) < self.__exploration:
            self.__exploration *= self.__cooling_rate
            return random.randint(0, 3), random.randint(0, 9)
        else:
            hash = ''.join(map(str, boundaries))
            best_rotation = 0
            best_x = 0
            best_reward = None
            for rotation, xs in self.qtables[hash][mino - 1].items():
                for x, reward in xs.items():
                    if best_reward is None or reward > best_reward:
                        best_rotation = rotation
                        best_x = x
                        best_reward = reward
            return best_rotation, best_x

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.qtables, file)

    def load(self, filename):
        start = time.time()
        with open(filename, 'rb') as file:
            self.qtables = pickle.load(file)
        print("qtables load in", time.time() - start, "sec")

